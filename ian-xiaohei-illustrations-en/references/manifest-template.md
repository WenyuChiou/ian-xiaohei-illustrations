# Render manifest (template)

After generating, write this as `manifest.md` inside `assets/<article-slug>-illustrations/`. It makes every image reproducible, individually re-rollable, and accessible.

**Article-level** (fill in after the step-2 shot list): slug `<article-slug>` · motif `<the shared visual motif>` · base seed `<int>` (per-image seeds may diverge after a re-roll) · annotation_lang `<en / … >` · aspect `<16:9 / … >`

| # | file | placement (after which paragraph / section) | theme | structure type | seed | tool | alt-text |
|---|------|---------------------------------------------|-------|----------------|------|------|----------|
| 01 | 01-trust.png | after the "building trust" paragraph | trust is laid one piece of evidence at a time | concept metaphor | 4217 | codex image_gen | "A small creature lays evidence bricks to build a path toward a door labelled trust." |

Keep each image's **full prompt** in the Prompts section below — prompts are long, so don't cram them into a table cell. (Use a 4+ digit seed; single-digit seeds give some backends systematic outputs.)

## Prompts

### 01-trust.png — seed 4217

```text
<the full prompt text that was sent to the image tool for this image>
```

## Why this manifest exists

- **Reproducibility** — regenerate any single image verbatim from its prompt + seed.
- **Consistency** — one shared seed across the whole article keeps the recurring character looking the same in every image.
- **Iteration** — re-roll one image (vary only its seed) without touching the rest.
- **Accessibility** — the alt-text column drops straight into a blog, Notion, or a screen reader.
