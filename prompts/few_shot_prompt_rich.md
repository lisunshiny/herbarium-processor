You are an AI assistant trained to extract structured data from herbarium specimen label images.

You will be shown three label images embedded directly in this prompt:
- The first, second, and third images are examples with a known correct output.
- The fourth image is a new specimen label that you must process.

Your task is to extract and return **only** the following 18 fields from the **final image** in a valid JSON object using `snake_case` keys:

- `label_header`
- `scientific_name`
- `field_collection_location_verbatim`
- `county`
- `state`
- `country`
- `verbatim_latitude`
- `verbatim_longitude`
- `elevation`
- `habitat_information`
- `field_collection_date`
- `comment`
- `field_collectors`
- `identifier`
- `identification_date`
- `field_collection_number`
- `exsiccatae_number`
- `associated_taxa`


Return `null` for any field that is not clearly present or legible. Do **not** infer or fabricate any information. Do **not** return extra fields.

---

**Example Image 1:**  
<|image_0|>

**Correct JSON Output for Example Image 1:**
```json
{
  "label_header": "BRYOPHYTES OF AUSTRALIA STATE OF TASMANIA LONGFORD MUNICIPALITY",
  "scientific_name": "Grimmia trichophylla Grev.",
  "field_collection_location_verbatim": "In Eucalyptus coccifera forest of shores of Lake Dobson, Mt. Field Natl. Park",
  "county": null,
  "state": null,
  "country": "Australia",
  "verbatim_latitude": "146 36 E",
  "verbatim_longitude": "42 42 S",
  "elevation":  "1000 m",
  "habitat_information": "On fairly moist, diffusely lit boulder.",
  "field_collection_date": "November 17 1973",
  "comment": null,
  "field_collectors": ["D. H. Norris"],
  "field_collection_number": "27614",
  "identifier": null,
  "identification_date": null,
  "exsiccatae_number": null,
  "associated_taxa": null
}
```

**Example Image 2:**  
<|image_1|>

**Correct JSON Output for Example Image 2:**
```json
{
  "label_header": "Fay A. MacFadden",
  "scientific_name": "Aerobryopsis scariosa Bratram",
  "field_collection_location_verbatim": "Hawaiian Islands, Oahu, Tho Pali. On ground under brush by roadway, near crest.",
  "county": null,
  "state": null,
  "country": null,
  "verbatim_latitude": null,
  "verbatim_longitude": null,
  "elevation":  null,
  "habitat_information": null,
  "comment": "(Previously known only from Luzon, P. I.)",
  "field_collection_date": "December 27, 1958",
  "field_collectors": ["Gail Savage"],
  "field_collection_number": "22915",
  "identifier": "E. B. Bartram",
  "identification_date": null,
  "exsiccatae_number": "P. M. Patterson #2869",
  "associated_taxa": null
}
```

**Example Image 3:**  
<|image_2|>


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
  "field_collectors": ["Larsson"],
  "field_collection_number": null,
  "identifier": null,
  "identification_date": null,
  "exsiccatae_number": null,
  "associated_taxa": null
}
```
---

**Image to Process:**  
<|image_3|>


Return your answer as a single valid JSON object using only the 18 fields listed above.
