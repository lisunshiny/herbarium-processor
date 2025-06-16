You are an AI assistant trained to extract structured data from herbarium specimen label images.

You will be shown two label images embedded directly in this prompt:
- The first image is an example with a known correct output.
- The second image is a new specimen label that you must process.

Your task is to extract and return **only** the following 24 fields from the **second image** in a valid JSON object using `snake_case` keys:

- `label header`
- `scientific name`
- `field collection location verbatim`
- `county`
- `state`
- `country`
- `verbatim latitude`
- `verbatim longitude`
- `elevation`
- `habitat information`
- `field collection date`
- `field collector`
- `field collection number`
- `exsiccatae number`
- `associated taxa`

Return `null` for any field that is not clearly present or legible. Do **not** infer or fabricate any information. Do **not** return extra fields.

---

**Example Image:**  
<|image_0|>

**Correct JSON Output:**
```json
{
  "id": null,
  "label header": "BRYOPHYTES OF AUSTRALIA STATE OF TASMANIA LONGFORD MUNICIPALITY",
  "scientific_name": "Grimmia trichophylla Grev.",
  "field_collection_location_verbatim": "On fairly moist, diffusely lit boulder. In Eucalyptus coccifera forest of shores of Lake Dobson, Mt. Field Natl. Park.",
  "county": null,
  "state": null,
  "country": "Australia",
  "verbatim_latitude": "146 36 E",
  "verbatim_longitude": "42 42 S",
  "elevation":  "1000 m",
  "habitat_information": null,
  "field_collection_date": "November 17 1973",
  "field_collector": "D. H. Norris",
  "field_collection_number": "27614",
  "exsiccatae_number": null,
  "associated_taxa": null
}
```

---

**Image to Process:**  
<|image_1|>

Return your answer as a single valid JSON object using only the 15 fields listed above.
