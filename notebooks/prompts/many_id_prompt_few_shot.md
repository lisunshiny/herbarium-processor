You are an AI assistant trained to extract structured data from herbarium specimen label images.

You will be shown two label images embedded directly in this prompt:
- The first image is an example with a known correct output.
- The second image is a new specimen label that you must process.

Your task is to extract and return **only** the following 24 fields from the **second image** in a valid JSON object using `snake_case` keys:

- `verbatim_scientific_name`
- `verbatim_scientific_name_qualifier`
- `verbatim_identified_by`
- `verbatim_identified_date`
- `verbatim_collected_by`
- `additional_collected_by`
- `record_number`
- `verbatim_event_date`
- `verbatim_coordinates`
- `verbatim_elevation`
- `verbatim_habitat`
- `verbatim_substrate`
- `verbatim_associated_taxa`
- `verbatim_country`
- `verbatim_state`
- `verbatim_county`
- `verbatim_municipality`
- `verbatim_locality`
- `verbatim_datum`
- `decimal_latitude`
- `decimal_longitude`

Return `null` for any field that is not clearly present or legible. Do **not** infer or fabricate any information. Do **not** return extra fields.

---

**Example Image:**  
<|image_0|>

**Correct JSON Output:**
```json
{
  "id": null,
  "verbatim_scientific_name": "Acarospora strigata",
  "verbatim_scientific_name_qualifier": "(Nyl.) Jatta",
  "verbatim_identified_by": null,
  "verbatim_identified_date": null,
  "verbatim_collected_by": "Ronald & Judith Robertson",
  "additional_collected_by": null,
  "record_number": "9318",
  "verbatim_event_date": "2 July 2005",
  "verbatim_habitat": "Dolomite outcrop in Bristlecone-limber pine forest",
  "verbatim_substrate": "On rock",
  "verbatim_associated_taxa": null,
  "decimal_latitude": "N37°30'18",
  "decimal_longitude": "W118°09'11",
  "verbatim_country": "USA",
  "verbatim_state": "California",
  "verbatim_county": "Mono",
  "verbatim_municipality": null,
  "verbatim_locality": "UC White Mtns. Research Station Crooked Creek road, East of Research Station.",
  "verbatim_coordinates": "N37°30' 18\" W118°09′ 11″",
  "verbatim_datum": null,
  "verbatim_elevation": "9995'"
}
```

---

**Image to Process:**  
<|image_1|>

Return your answer as a single valid JSON object using only the 24 fields listed above.
