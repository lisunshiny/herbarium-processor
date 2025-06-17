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
  {
    "id": "1.1.1",
    "text": "BRYOPHYTES OF AUSTRALIA",
    "bounding_box": [
      {
        "x": 217,
        "y": 308
      },
      {
        "x": 332,
        "y": 308
      },
      {
        "x": 332,
        "y": 315
      },
      {
        "x": 217,
        "y": 315
      }
    ],
    "average_confidence": 0.9393793666666665,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.2",
    "text": "Grinnia trichophylla HAMILTON STATE OF Grev MUNICIPALITY TASMANIA .",
    "bounding_box": [
      {
        "x": 173,
        "y": 316
      },
      {
        "x": 332,
        "y": 316
      },
      {
        "x": 332,
        "y": 349
      },
      {
        "x": 173,
        "y": 349
      }
    ],
    "average_confidence": 0.8553493722222223,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.3",
    "text": "On In shores fairly Eucalyptus of moist Lake , coccifers diffusely Dobson , Mt. lit forest Field boulder of Natl .",
    "bounding_box": [
      {
        "x": 190,
        "y": 354
      },
      {
        "x": 386,
        "y": 354
      },
      {
        "x": 386,
        "y": 380
      },
      {
        "x": 190,
        "y": 380
      }
    ],
    "average_confidence": 0.9025044852380952,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.4",
    "text": "Park 42 \u00b0 42'8 . El . . ca. 1000 M. 146 \u00b0 36 ' x",
    "bounding_box": [
      {
        "x": 195,
        "y": 380
      },
      {
        "x": 367,
        "y": 380
      },
      {
        "x": 367,
        "y": 396
      },
      {
        "x": 195,
        "y": 396
      }
    ],
    "average_confidence": 0.8112164681249999,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.5",
    "text": "Coll . D. H. Norris # 17 27614 November 1973",
    "bounding_box": [
      {
        "x": 178,
        "y": 415
      },
      {
        "x": 361,
        "y": 415
      },
      {
        "x": 361,
        "y": 436
      },
      {
        "x": 178,
        "y": 436
      }
    ],
    "average_confidence": 0.8855009879999999,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.6",
    "text": "UC",
    "bounding_box": [
      {
        "x": 337,
        "y": 496
      },
      {
        "x": 357,
        "y": 496
      },
      {
        "x": 357,
        "y": 507
      },
      {
        "x": 337,
        "y": 507
      }
    ],
    "average_confidence": 0.9159893,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.7",
    "text": "01 2 3 4 5 6 7 8 9 10",
    "bounding_box": [
      {
        "x": 378,
        "y": 965
      },
      {
        "x": 600,
        "y": 965
      },
      {
        "x": 600,
        "y": 973
      },
      {
        "x": 378,
        "y": 973
      }
    ],
    "average_confidence": 0.9640660349999999,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.8",
    "text": "cm copyright reserved",
    "bounding_box": [
      {
        "x": 378,
        "y": 978
      },
      {
        "x": 597,
        "y": 978
      },
      {
        "x": 597,
        "y": 987
      },
      {
        "x": 378,
        "y": 987
      }
    ],
    "average_confidence": 0.9101358833333334,
    "block_type": "TEXT"
  }
]

```

**Correct JSON Output for Example Image 1:**

```json
{
  "label_header": "BRYOPHYTES OF AUSTRALIA STATE OF TASMANIA LONGFORD MUNICIPALITY",
  "scientific_name": "Grimmia trichophylla Grev.",
  "field_collection_location_verbatim": "In Eucalyptus coccifera forest of shores of Lake Dobson, Mt. Field Natl. Park.",
  "county": null,
  "state": null,
  "country": "Australia",
  "verbatim_latitude": "146 36 E",
  "verbatim_longitude": "42 42 S",
  "elevation": "1000 m",
  "habitat_information": "On fairly moist, diffusely lit boulder.",
  "field_collection_date": "November 17 1973",
  "comment": null,
  "field_collectors": ["D. H. Norris"],
  "identifier": null,
  "field_collection_number": "27614",
  "identification_date": null,
  "exsiccatae_number": null,
  "associated_taxa": null,
  "sources": {
    "label_header": ["1.1.1", "1.1.2"],
    "scientific_name": ["1.1.2"],
    "field_collection_location_verbatim": ["1.1.3", "1.1.4"],
    "country": ["1.1.1"],
    "verbatim_latitude": ["1.1.4"],
    "verbatim_longitude": ["1.1.4"],
    "elevation": ["1.1.4"],
    "habitat_information": ["1.1.3"],
    "field_collection_date": ["1.1.5"],
    "field_collectors": ["1.1.5"],
    "field_collection_number": ["1.1.5"]
  }
}
```

---

**Example Image 2:**
<|image_1|>

**OCR Blocks for Image 2:**

```json
[
  {
    "id": "1.1.1",
    "text": "IMAGED",
    "bounding_box": [
      {
        "x": 557,
        "y": 56
      },
      {
        "x": 608,
        "y": 56
      },
      {
        "x": 608,
        "y": 67
      },
      {
        "x": 557,
        "y": 67
      }
    ],
    "average_confidence": 0.9891382,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.2",
    "text": "Jaza . Mac Inddene",
    "bounding_box": [
      {
        "x": 392,
        "y": 269
      },
      {
        "x": 495,
        "y": 269
      },
      {
        "x": 495,
        "y": 294
      },
      {
        "x": 392,
        "y": 294
      }
    ],
    "average_confidence": 0.5416027075,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.3",
    "text": "Aerobryopsis Hawaiian scariosa Islands , Bartram Oahu , The Pali . , near crest The . no- 22915",
    "bounding_box": [
      {
        "x": 179,
        "y": 288
      },
      {
        "x": 491,
        "y": 288
      },
      {
        "x": 491,
        "y": 324
      },
      {
        "x": 179,
        "y": 324
      }
    ],
    "average_confidence": 0.7896102883333332,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.4",
    "text": "On Coll ground . Gail under Savage Bartran brush , December by roadway 27 , 1958",
    "bounding_box": [
      {
        "x": 198,
        "y": 315
      },
      {
        "x": 362,
        "y": 315
      },
      {
        "x": 362,
        "y": 352
      },
      {
        "x": 198,
        "y": 352
      }
    ],
    "average_confidence": 0.9360346375,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.5",
    "text": "( Det Ex Previously . . Herb E. B. . P. known M. Patterson only from # Luzon 2869 , P. I. )",
    "bounding_box": [
      {
        "x": 195,
        "y": 345
      },
      {
        "x": 381,
        "y": 345
      },
      {
        "x": 381,
        "y": 373
      },
      {
        "x": 195,
        "y": 373
      }
    ],
    "average_confidence": 0.8827427626086957,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.6",
    "text": "U",
    "bounding_box": [
      {
        "x": 608,
        "y": 943
      },
      {
        "x": 627,
        "y": 943
      },
      {
        "x": 627,
        "y": 959
      },
      {
        "x": 608,
        "y": 959
      }
    ],
    "average_confidence": 0.71506804,
    "block_type": "TEXT"
  },
  {
    "id": "1.1.7",
    "text": "0 cm 1 2 3 4 5 6 copyright 7 8 reserved 9 10",
    "bounding_box": [
      {
        "x": 374,
        "y": 954
      },
      {
        "x": 598,
        "y": 954
      },
      {
        "x": 598,
        "y": 976
      },
      {
        "x": 374,
        "y": 976
      }
    ],
    "average_confidence": 0.9444656371428571,
    "block_type": "TEXT"
  }
]
```

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
  "sources": {
    "label_header": ["1.1.2"],
    "scientific_name": ["1.1.3"],
    "field_collection_location_verbatim": ["1.1.2"],
    "comment": ["1.1.5"],
    "field_collection_date": ["1.1.4"],
    "field_collectors": ["1.1.4"],
    "field_collection_number": ["1.1.3"],
    "identifier": ["1.1.3"],
    "exsiccatae_number": ["1.1.5"],
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
