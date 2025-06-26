
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
5) Run `poetry install` in the terminal to install the project dependencies.


### Step 1: Using the tool

From here you have two options to use the processor, either the **web interface** or the **Python notebook**.

#### Web app
1. Start the server with `poetry run uvicorn herbarium_processor.web.main:app --reload`.
2. Visit `http://localhost:8000/` to upload images. After processing, predicted fields can be edited in the browser alongside the OCR annotated image.
3. Click **Finalize CSV** to save your edits and then download the CSV.
6. Note that the info is all stored in the /tmp folder.

#### Notebook
1. Open the notebook located at notebooks/herbarium_processor.ipynb
2. Specify a dir to process -- note that you can delete all of the items in the img/bucket directory and use that. 
