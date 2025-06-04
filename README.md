
# Herbarium processor
fka the Lichen Digital Analysis & Data Delivery sYstem

### Summary
Given an image of a specimen label, this library will use computer vision and AI to return the formatted data of that label, e.g.

<table>
  <tr>
    <td>Input</td>
    <td>Output</td></tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/lisunshiny/herbarium-processor/refs/heads/main/img/IMG_2709.jpg" /></td>
    <td>
      <pre>
        {
          "Catalog #": "245081",
          "Occurrence ID": null,
          "Taxon": "Acarospora strigata (Nyl.) Jatta",
          "Family": null,
          "Determiner": null,
          "Date Determined": null,
          "Collector": "H. E. HASSE",
          "Number": "1327",
          "Date": null,
          "Verbatim Date": null,
          "Locality": "Palm Springs (Type locality) Riverside Co. Cal",
          "Latitude/Longitude": null,
          "Elevation": null,
          "Verbatim Elevation": null,
          "Habitat": null
        }
    </pre>
  </tr>
</table>

### Quick setup
1) `git clone` the repo
2) Obtain a Google API key (note that https://aistudio.google.com/ is an easy way to obtain one)
4) In the cloned repo, add a .env file with the following content:

   ```
   GOOGLE_API_KEY=your_key_here
   ```
5) Run the Jupyter notebook. The first cell contains the image that is being processed, if you want to test a different image update the value of that variable.
6) Check out the json response at the end of the notebook, or in the tmp/ directory.

## Installation
To install the necessary dependencies, run the following command in your terminal:
```bash
pip install -r requirements.txt
```

### How it works
This is currently being developed. Given an image of a specimen label, it:

1) Uses an image-to-text i.e. OCR service to extract the text from the label
** note**: Calling the OCR is not yet implemeneted, I just hardcoded the json responses from [Google Cloud Vision API](https://cloud.google.com/vision/docs/drag-and-drop) into /json/ to shim this step.
2) Cleans up the OCR response to be much smaller in order to prep it for passing it to the model (in this case, Gemini 2.5 Pro)
3) Drafts up system instructions
 TODO: Fine-tune this prompt if needed
4) Asks the AI agent to fill out the herbarium fields.
