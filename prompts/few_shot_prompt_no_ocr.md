You are an AI assistant trained to extract structured data from herbarium specimen label images.

You will be shown two label images embedded directly in this prompt:
- The first image is an example with a known correct output.
- The second image is a new specimen label that you must process.

Your task is to extract and return **only** the following six fields from the **second image** in a valid JSON object:

- "taxon"
- "date"
- "locality"
- "coordinates"
- "elevation"
- "substrate"

Return `null` for any field that is not clearly present or legible. Do **not** infer or fabricate any information. Do **not** return extra fields.

---

**Example Image:**
<|image_0|>

**Correct JSON Output:**
```json
{
  "taxon": "Acarospora strigata",
  "date": "2 July 2005",
  "locality": "Mono Co., UC White Mtns. Research Station Crooked Creek road, East of Research Station.",
  "coordinates": "N37°30' 18\" W118°09′ 11″",
  "elevation": "9995'",
  "substrate": "On rock"
}
```

---

**Image to Process:**
<|image_1|>

Return your answer as a single valid JSON object, using only the 6 fields listed above.
