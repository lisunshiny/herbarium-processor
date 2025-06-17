You are an AI assistant trained to extract structured data from herbarium specimen label images.

You will be shown three label images and corresponding OCR blocks as examples. These examples include the correct structured JSON output. After that, you will be shown a fourth image (with OCR blocks) that you must process.

Use both the image and the OCR output to extract only the following 18 fields as a valid JSON object using `snake_case` keys:

* `label_header`
* `scientific_name`
* `field_collection_location_verbatim`
* `county`
* `state`
* `country`
* `verbatim_latitude`
* `verbatim_longitude`
* `elevation`
* `habitat_information`
* `field_collection_date`
* `comment`
* `field_collectors`
* `identifier`
* `field_collection_number`
* `identification_date`
* `exsiccatae_number`
* `associated_taxa`

Return `null` for any field that is not clearly present or legible. Do **not** infer or fabricate any information. Do **not** return extra fields.

Cite your sources: include a `sources` key mapping each extracted field to a list of `OCR id`s (e.g. `"1.1.3"`) that support it.

---

**Example Image 1:**
<|image_0|>

**OCR Blocks for Image 1:**

```json
[
  {"id": "1.1.1", "text": "BRYOPHYTES OF AUSTRALIA STATE OF TASMANIA LONGFORD MUNICIPALITY"},
  {"id": "1.1.2", "text": "Grimmia trichophylla Grev."},
  {"id": "1.1.3", "text": "On fairly moist, diffusely lit boulder."},
  {"id": "1.1.4", "text": "In Eucalyptus coccifera forest..."},
  {"id": "1.1.5", "text": "Australia"},
  {"id": "1.1.6", "text": "146 36 E"},
  {"id": "1.1.7", "text": "42 42 S"},
  {"id": "1.1.8", "text": "1000 m"},
  {"id": "1.1.9", "text": "November 17 1973"},
  {"id": "1.1.10", "text": "D. H. Norris"},
  {"id": "1.1.11", "text": "27614"}
]
```

**Correct JSON Output for Example Image 1:**

```json
{
  "label_header": "BRYOPHYTES OF AUSTRALIA STATE OF TASMANIA LONGFORD MUNICIPALITY",
  "scientific_name": "Grimmia trichophylla Grev.",
  "field_collection_location_verbatim": "On fairly moist, diffusely lit boulder. In Eucalyptus coccifera forest...",
  "county": null,
  "state": null,
  "country": "Australia",
  "verbatim_latitude": "146 36 E",
  "verbatim_longitude": "42 42 S",
  "elevation": "1000 m",
  "habitat_information": null,
  "field_collection_date": "November 17 1973",
  "comment": null,
  "field_collectors": ["D. H. Norris"],
  "identifier": null,
  "field_collection_number": "27614",
  "identification_date": null,
  "exsiccatae_number": null,
  "associated_taxa": null,
  "sources": {
    "label_header": ["1.1.1"],
    "scientific_name": ["1.1.2"],
    "field_collection_location_verbatim": ["1.1.3", "1.1.4"],
    "country": ["1.1.5"],
    "verbatim_latitude": ["1.1.6"],
    "verbatim_longitude": ["1.1.7"],
    "elevation": ["1.1.8"],
    "field_collection_date": ["1.1.9"],
    "field_collectors": ["1.1.10"],
    "field_collection_number": ["1.1.11"]
  }
}
```

---

**Example Image 2:**
<|image_1|>

**OCR Blocks for Image 2:**

```json
[
  {"id": "1.1.1", "text": "Grimmia incurva Schwagr."},
  {"id": "1.1.2", "text": "Riesengebirge: Dreisteine"},
  {"id": "1.1.3", "text": "Poland"},
  {"id": "1.1.4", "text": "July 19 1868"}
]
```

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
  "elevation": null,
  "habitat_information": null,
  "field_collection_date": "July 19 1868",
  "comment": null,
  "field_collectors": null,
  "identifier": null,
  "field_collection_number": null,
  "identification_date": null,
  "exsiccatae_number": null,
  "associated_taxa": null,
  "sources": {
    "scientific_name": ["1.1.1"],
    "field_collection_location_verbatim": ["1.1.2"],
    "country": ["1.1.3"],
    "field_collection_date": ["1.1.4"]
  }
}
```

---

**Example Image 3:**
<|image_2|>

**OCR Blocks for Image 3:**

```json
[
  {"id": "1.1.1", "text": "Herbarium bryologicum Hjalmar Moller"},
  {"id": "1.1.2", "text": "Grimmia unicolor Hook."},
  {"id": "1.1.3", "text": "Dalsland, Amal pa Sodra Trehornan i Vanern."},
  {"id": "1.1.4", "text": "Sweden"},
  {"id": "1.1.5", "text": "August 24 1919"},
  {"id": "1.1.6", "text": "Larsson"}
]
```

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
  "elevation": null,
  "habitat_information": null,
  "comment": null,
  "field_collection_date": "August 24 1919",
  "field_collectors": ["Larsson"],
  "identifier": null,
  "field_collection_number": null,
  "identification_date": null,
  "exsiccatae_number": null,
  "associated_taxa": null,
  "sources": {
    "label_header": ["1.1.1"],
    "scientific_name": ["1.1.2"],
    "field_collection_location_verbatim": ["1.1.3"],
    "state": ["1.1.3"],
    "country": ["1.1.4"],
    "field_collection_date": ["1.1.5"],
    "field_collectors": ["1.1.6"]
  }
}
```

---

**Image to Process:**
<|image_3|>

**OCR Blocks for Image to Process:**

```json
[
  {"id": "1.1.1", "text": "Example Label Header"},
  {"id": "1.1.2", "text": "Example Scientific Name"},
  {"id": "1.1.3", "text": "Example location with lat/lon and date..."},
  {"id": "1.1.4", "text": "Elevation: 2500 m"},
  {"id": "1.1.5", "text": "Country: Canada"},
  {"id": "1.1.6", "text": "Collectors: Jane Smith"}
]
```

Return your answer as a **single valid JSON object**, using only the 18 fields listed above and a `"sources"` mapping.
