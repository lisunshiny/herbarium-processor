# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

## Formatting

ESLint enforces a single attribute per line for Vue templates through the pre-commit hook. To apply the same rules while you work:

1. Open the repository in VS Code and install the recommended extensions when prompted. The ESLint extension (`dbaeumer.vscode-eslint`) is required so VS Code can run ESLint fixes on save.
2. With the extension installed, save any `.vue` or JavaScript file. The workspace settings enable `source.fixAll.eslint`, so ESLint rewrites the file using the exact rules enforced by the hook—including splitting template attributes onto separate lines.
3. If you use another editor, run ESLint manually from the frontend directory instead: `npm exec eslint -- --fix "src/**/*.{js,vue}"`.

That way, ESLint—not Prettier—controls the formatting everywhere the codebase expects it.
