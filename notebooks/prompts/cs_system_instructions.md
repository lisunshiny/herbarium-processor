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
- `comment`
- `field collection date`
- `field collector`
- `field collection number`
- `exsiccatae number`
- `associated taxa`

Return `null` for any field that is not clearly present or legible. Do **not** infer or fabricate any information. Do **not** return extra fields.

---

**Example Image 1:**  
<|cs_16625_23|>

**Correct JSON Output for Example Image 1:**
```json
{
  "label_header": "BRYOPHYTES OF AUSTRALIA STATE OF TASMANIA LONGFORD MUNICIPALITY",
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
  "comment": null,
  "field_collector": "D. H. Norris",
  "field_collection_number": "27614",
  "exsiccatae_number": null,
  "associated_taxa": null
}
```

**Example Image 2:**  
<|cs_16625_24|>

**Correct JSON Output for Example Image 2:**
```json
{
  "label_header": null,
  "scientific_name": "Grimmia incurva Schwagr.",
  "field_collection_location_verbatim": "Riesengebirge: Dreisteine",
  "county": null,
  "state": null,
  "country": "Poland",
  "verbatim_latitude": null,
  "verbatim_longitude": null,
  "elevation":  null,
  "habitat_information": null,
  "comment": null,
  "field_collection_date": "July 19 1868",
  "field_collector": null,
  "field_collection_number": null,
  "exsiccatae_number": null,
  "associated_taxa": null
}
```

**Example Image 3:**  
<|cs_16625_25|>


**Correct JSON Output for Example Image 3:**
```json
{
  "label_header": "Herbarium bryologicum Hjalmar Moller",
  "scientific_name": "Grimmia unicolor Hook.",
  "field_collection_location_verbatim": "Dalsland, Amal pa Sodra Trehornan i Vanern.",
  "county": null,
  "state": "Dalsland",
  "country": "Sweden",
  "verbatim_latitude": null,
  "verbatim_longitude": null,
  "elevation":  null,
  "habitat_information": null,
  "comment": null,
  "field_collection_date": "August 24 1919",
  "field_collector": "Larsson",
  "field_collection_number": null,
  "exsiccatae_number": null,
  "associated_taxa": null
}
```
---

**Image to Process:**  
<|add image|>


Return your answer as a single valid JSON object using only the 15 fields listed above.
