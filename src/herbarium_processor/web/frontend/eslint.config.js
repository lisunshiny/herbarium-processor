import js from "@eslint/js";
import vue from "eslint-plugin-vue";
import jsonc from "eslint-plugin-jsonc";
import globals from "globals";

export default [
  { ignores: ["dist/**", "node_modules/**"] },
  {
    languageOptions: {
      globals: {
        ...globals.browser, // adds window, document, fetch, etc.
        ...globals.node, // adds console, process, module, etc.
      },
    },
  },

  js.configs.recommended,
  ...vue.configs["flat/recommended"],
  ...jsonc.configs["flat/recommended-with-json"],
  {
    files: ["**/*.vue"],
    languageOptions: {
      parser: (await import("vue-eslint-parser")).default,
      parserOptions: { ecmaVersion: 2024, sourceType: "module" },
    },
  },
];
