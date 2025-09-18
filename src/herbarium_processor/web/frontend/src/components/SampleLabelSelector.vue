<template>
  <div class="rounded-2xl border border-slate-200 bg-white shadow-sm p-6">
    <div class="grid md:grid-cols-[4fr_2fr] gap-6">
      <!-- Left: hardcoded JPG placeholder that swaps by selection -->
      <div>
        <!-- Label buttons -->
        <div class="mb-4 flex gap-2 overflow-x-auto pb-2">
          <button
            v-for="(opt, idx) in options"
            :key="opt.key"
            class="btn btn-sm rounded-full whitespace-nowrap"
            :class="selected === idx ? 'btn-neutral' : 'btn-outline'"
            @click="selected = idx"
          >
            {{ opt.title }}
          </button>
        </div>

        <img :src="options[selected].src" alt="Sample label" />
        <p class="mt-3 text-xs text-slate-500">
          {{ options[selected].desc }}
        </p>
      </div>

      <!-- Right: sample structured output (varies a bit by selection) -->
      <div class="">
        <h4 class="font-semibold mb-3">Sample output</h4>
        <dl class="grid gap-2 text-sm md:max-h-[32rem] md:overflow-auto">
          <template v-for="(val, key) in options[selected].fields" :key="key">
            <div v-if="val !== null && String(val).trim() !== ''">
              <dt class="text-slate-500 text-xs">{{ prettyKey(key) }}</dt>
              <dd class="font-medium">{{ val }}</dd>
            </div>
          </template>
        </dl>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import denseLabel from "@/assets/sample_labels/dense_info_label.jpg";
import underlinedLabel from "@/assets/sample_labels/underlined_label.jpg";
import handwrittenForeignLabel from "@/assets/sample_labels/handwritten_foreign_label.jpg";
import handwrittenRedeterminedLabel from "@/assets/sample_labels/handwritten_redetermined_label.jpg";

const options = [
  {
    key: "nonenglish",
    title: "Swedish + in cursive",
    desc: "In Swedish cursive and full of special characters like å and ö — yet Parsely can still recognize and extract the important fields.",
    src: handwrittenForeignLabel,
    fields: {
      label_header: "Herbarium bryologicum Hjalmar Möller",
      scientific_name: "Grimmia unicolor Hook.",
      field_collectors: "P. A. Larssén",
      field_collection_date: "24 August 1919",
      field_collection_location_verbatim: "Åmål på Södra Trollholma i Venern",
      state: "Dalsland",
      country: "Sweden",
    },
  },
  {
    key: "dense",
    title: "Verbose",
    desc: "Clear, but dense — the kind of label that would be tedious and time-consuming to transcribe by hand.",
    src: denseLabel,
    fields: {
      label_header:
        "BOTANICAL MUSEUM, UNIVERSITY OF HELSINKI (H) and BRYOPHYTE HERBARIUM OF HUMBOLDT STATE UNIVERSITY (HSC)",
      scientific_name:
        "Trachyloma indicum Mitt. var. teretirameum Miller & Manuel",
      identifier: "D. H. Norris",
      identification_date: "1982",
      field_collection_date: "24 July 1981",
      field_collection_location_verbatim:
        "5 km SE of Lake Wamba (5 km S of Tep-tep Airstrip). In elfin forest approaching moss forest on saddle of ridge leading to top of Mt. Finisterre,",
      field_collection_number: "64276",
      field_collectors: "Daniel H. Norris",
      comment:
        "(collection site no. 2u). Expedition sponsored by University of Helsinki, Academy of Finland and Humboldt State University (Arcata, California) under the auspices of National Herbarium at Lae, Wau Ecology Institute and University of Papua New Guinea",
      state: "Morobe Province",
      country: "Papua New Guinea",
      elevation: "3000 m",
      verbatim_latitude: "6°03'S",
      verbatim_longitude: "146°35'E",

      habitat_information: "Moist, diffusely lit bark of tree",
    },
  },
  {
    key: "redetermined",
    title: "122 years old",
    desc: "This 122-year-old handwritten label is messy — exsiccatae where the title should be, and a redetermination scrawled in the margin — but Parsely can still interpret it.",
    src: handwrittenRedeterminedLabel,
    fields: {
      scientific_name: "Acarospora strigata (Nyl.) Jatta",
      identifier: "Jatta",
      old_scientific_name: "Acarospora peltasticta, v. Zahlbr.",
      old_identifier: "Zahlbr.",
      field_collectors: "H. E. Hasse",
      field_collection_number: 1327.0,
      field_collection_location_verbatim: "Palm Springs",
      county: "Riverside",
      state: "California",
      country: "United States",
      exsiccatae: "EX HERB. H. E. HASSE.",
      comment: "(Type locality)",
    },
  },
  {
    key: "underlined",
    title: "Underlined",
    desc: "Tough labels like this are where humans still shine. Parsely gives you a strong draft — usually just a couple of fields to adjust.",
    src: underlinedLabel,
    fields: {
      label_header: "H.S. CONARD SC.D. BRYOPHYTA",
      scientific_name: "Homalothecium nuttallii (Wils.) Jaeg. & Sauerb.",
      identifier: "H.S. Conard",
      habitat_information: "Rocks",
      field_collectors: "Marion P. Harthill",
      field_collection_number: 301.0,
      field_collection_date: "18 January 1957",
      field_collection_location_verbatim: "Port Angeles, Elwha River",
      elevation: "400",
    },
  },
];

function prettyKey(str) {
  return str
    .split("_")                        // break on underscores
    .map(s => s.charAt(0).toUpperCase() + s.slice(1)) // capitalize each part
    .join(" ");                        // join with spaces
}

const selected = ref(0);
</script>
<style scoped></style>
