<template>
  <div class="w-full bg-base-100 text-base-content">
    <!-- Hero -->
    <section class="mx-auto max-w-5xl px-4 pt-12 pb-10 text-center">
      <span
        class="inline-flex items-center gap-2 rounded-full border border-primary/40 bg-primary/10 px-4 py-1 text-sm font-medium text-primary"
      >
        Get started in minutes
      </span>
      <h1 class="mt-6 text-3xl sm:text-5xl font-bold tracking-tight">
        How to use Parsely
      </h1>
      <p class="mx-auto mt-4 max-w-3xl text-base sm:text-xl text-base-content/70">
        Parsely pairs research-grade AI with curator-friendly workflows. Follow these
        steps to move from raw specimen images to high-quality digitized records without
        losing the expertise that makes your collection special.
      </p>
      <div class="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
        <a class="btn btn-primary" href="/">Launch Parsely Studio</a>
        <a class="btn btn-ghost" href="/about">Learn about the team</a>
      </div>
    </section>

    <!-- Progress Steps -->
    <section class="mx-auto max-w-5xl px-4 pb-14">
      <div class="rounded-3xl border border-base-300 bg-base-200/60 p-6 sm:p-10 shadow-sm">
        <h2 class="text-2xl font-semibold text-base-content">A guided path from intake to export</h2>
        <p class="mt-3 text-base text-base-content/70">
          Parsely surfaces only the tools you need at each stage. The interface stays
          consistent so technicians and researchers feel confident every time they log in.
        </p>
        <ol class="mt-8 space-y-6">
          <li class="flex flex-col gap-4 rounded-2xl bg-base-100/80 p-6 sm:flex-row sm:items-start">
            <div class="badge badge-primary badge-lg text-base-100">1</div>
            <div>
              <h3 class="text-xl font-semibold">Create a batch & upload specimens</h3>
              <p class="mt-2 text-base-content/70">
                Drag-and-drop high-resolution scans or import from shared storage.
                Parsely automatically groups barcodes, labels, and sheets so that you can
                review dozens of specimens at once without losing track of provenance.
              </p>
            </div>
          </li>
          <li class="flex flex-col gap-4 rounded-2xl bg-base-100/80 p-6 sm:flex-row sm:items-start">
            <div class="badge badge-primary badge-lg text-base-100">2</div>
            <div>
              <h3 class="text-xl font-semibold">Fine-tune crops with visual feedback</h3>
              <p class="mt-2 text-base-content/70">
                Use the Crop Wizard to frame sheets, labels, and barcodes. Smart snapping
                keeps everything aligned while keyboard shortcuts speed up repetitive
                adjustments. Every action is undoable, so experimentation is safe.
              </p>
            </div>
          </li>
          <li class="flex flex-col gap-4 rounded-2xl bg-base-100/80 p-6 sm:flex-row sm:items-start">
            <div class="badge badge-primary badge-lg text-base-100">3</div>
            <div>
              <h3 class="text-xl font-semibold">Approve AI-suggested labels</h3>
              <p class="mt-2 text-base-content/70">
                Parsely reads printed and handwritten text, then surfaces structured
                suggestions for taxonomy, locality, collectors, and dates. You keep
                control—accept suggestions, edit inline, or mark items for specialist
                review with one click.
              </p>
            </div>
          </li>
          <li class="flex flex-col gap-4 rounded-2xl bg-base-100/80 p-6 sm:flex-row sm:items-start">
            <div class="badge badge-primary badge-lg text-base-100">4</div>
            <div>
              <h3 class="text-xl font-semibold">Export clean data to your CMS</h3>
              <p class="mt-2 text-base-content/70">
                When every specimen meets your quality bar, export standardized archives
                that drop directly into existing databases and publishing pipelines. Audit
                trails stay attached so that data stewards can trace every change.
              </p>
            </div>
          </li>
        </ol>
      </div>
    </section>

    <!-- Experience highlights -->
    <section class="mx-auto max-w-6xl px-4 pb-16">
      <h2 class="text-2xl sm:text-3xl font-semibold text-center">
        Thoughtful UX for busy digitization teams
      </h2>
      <p class="mx-auto mt-3 max-w-3xl text-center text-base-content/70">
        Parsely balances automation with human oversight. The interface is tuned for
        sustained digitization work, so your team can stay focused on the science.
      </p>
      <div class="mt-10 grid gap-6 md:grid-cols-3">
        <div class="rounded-2xl border border-base-300 bg-base-100/90 p-6 shadow-sm">
          <h3 class="font-semibold text-lg text-primary">Session-aware workspace</h3>
          <p class="mt-2 text-sm text-base-content/70">
            Resume exactly where you left off. Batches remember sort order, filters,
            and annotation progress, making handoffs between volunteers and staff
            effortless.
          </p>
        </div>
        <div class="rounded-2xl border border-base-300 bg-base-100/90 p-6 shadow-sm">
          <h3 class="font-semibold text-lg text-secondary">Delightful collaboration tools</h3>
          <p class="mt-2 text-sm text-base-content/70">
            Mention teammates, attach curator notes, and flag specimens that need an
            expert eye. Alerts show up instantly in the shared workspace so nothing gets
            lost in email threads.
          </p>
        </div>
        <div class="rounded-2xl border border-base-300 bg-base-100/90 p-6 shadow-sm">
          <h3 class="font-semibold text-lg text-accent">Accessibility from the start</h3>
          <p class="mt-2 text-sm text-base-content/70">
            High-contrast themes, keyboard navigation, and screen-reader friendly
            components ensure Parsely is usable by the full diversity of the herbarium
            community.
          </p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="mx-auto max-w-4xl px-4 pb-20">
      <div class="rounded-3xl bg-gradient-to-r from-primary to-secondary text-primary-content p-10 text-center">
        <h2 class="text-3xl font-semibold">Ready to see Parsely in your workflow?</h2>
        <p class="mt-3 text-base sm:text-lg opacity-90">
          We help you pilot with real specimens, train your team, and quantify the
          uplift so you can make the case for institution-wide adoption.
        </p>
        <a class="btn mt-6 bg-base-100 text-base-content hover:bg-base-200" href="mailto:hello@parsely.studio">
          Schedule a walkthrough
        </a>
      </div>
    </section>
  </div>
</template>

<script setup>
// This page uses static marketing content only.
</script>

<style scoped></style>
