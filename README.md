
# Herbarium processor
fka the Lichen Digital Analysis & Data Delivery sYstem

### How it works
This project is meant to make it easier to digitize herbarium specimens in bulk. 

Given a bunch of specimen label images, it will:

* Crop, auto-rotate and process those images to prepare for AI extraction
* Call OCR for each image, returning text to assist in AI extraction
* Send specimen labels, and their OCR output, to a model (currently Gemini 2.5 Pro) for extraction.

## Using the tool

### Step 1: Setup
1) `git clone` the repo
2) Obtain a Google API key and credentials
4) In the cloned repo, add a .env file in the root directory with the following content:

   ```
   GOOGLE_API_KEY=your_key_here
   GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
   ```
5) Run `poetry install` in the terminal to install the project dependencies (`pip3 install poetry` if you don't have it).
6) If you plan on contributing to the repo, we use precommit to strip notebook metadata. Also run 

```
poetry run pre-commit install
```


### Step 1: Using the tool

From here you have two options to use the processor, either the **web interface** or the **Python notebook**.

#### Web app
1. Start the server:
   - For development with hot reload, use `poetry run dev`.
   - For a faster demo without hot reload and with eight worker processes so GET requests don't hang, run `poetry run demo`.
2. Visit `http://localhost:8000/` to upload images. After processing, predicted fields can be edited in the browser alongside the OCR annotated image.
3. Click **Finalize CSV** to save your edits and then download the CSV.
4. Note that the info is all stored in the /tmp folder.

#### Notebook
1. Open the notebook located at notebooks/herbarium_processor.ipynb
2. Specify a dir to process -- note that you can delete all of the items in the img/bucket directory and use that.

### Deploying on Google Cloud Run

You can run the web app on GCP using Cloud Run.

1. **Build the container image** (replace `PROJECT_ID` with your GCP project):

   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/herbarium-processor
   ```

2. **Deploy to Cloud Run**:

   ```bash
   gcloud run deploy herbarium-processor \
       --image gcr.io/PROJECT_ID/herbarium-processor \
       --platform managed \
       --region REGION \
       --allow-unauthenticated \
       --set-env-vars GOOGLE_API_KEY=your_key
   ```

3. **Provide Vision API credentials**. Cloud Run can use a service account with
   the Vision API enabled, or you can mount a key file stored in Secret
   Manager at `~/.secrets/vision-key.json`:

   ```bash
   gcloud secrets create vision-key --data-file=path/to/vision-key.json
   gcloud run services update herbarium-processor \
       --update-secrets GOOGLE_APPLICATION_CREDENTIALS=vision-key:latest
   ```

After deployment, Cloud Run will output the service URL where the app is available.


Some other commands for debugging the Dockerfile locally

```
docker build -t herbarium-processor .
```

```
docker run --rm -p 8000:8080 \
  --env-file .env \
  -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/vision-key.json \
  -v $HOME/.secrets/vision-key.json:/secrets/vision-key.json:ro \
  herbarium-processor

```