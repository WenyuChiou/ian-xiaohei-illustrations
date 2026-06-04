---
name: ian-xiaohei-illustrations-en
description: Generate hand-drawn, deadpan "Xiaohei" explainer illustrations for articles, blog posts, Notion docs, workflows, and methodology content. Use when the user asks to illustrate an article, draw a concept / workflow / metaphor, make a "shot list" of body images, or wants a clean, absurd, white-background hand-drawn explainer image (NOT a PPT infographic, NOT a cute cartoon). English-first, but the visual style is language-agnostic. Triggers include "hand-drawn article illustration", "deadpan mascot explainer", "illustrate this post", "draw this workflow", "body images / shot list for a blog".
---

# Xiaohei Deadpan Explainer Illustrations (English)

## Core positioning

Design and generate 16:9 horizontal explainer illustrations for written content. The goal is NOT commercial illustration, a PPT infographic, or a cute cartoon — it is to turn one key judgment, workflow, structure, state, or metaphor from the text into a clean, absurd, hand-drawn explainer image that is readable but never a user manual.

The default visual IP is **Xiaohei**: a small solid-black creature with white dot eyes, thin legs, and a blank deadpan expression, earnestly doing one absurd-but-coherent job. Xiaohei must perform the core action of the image — never stand beside it as decoration.

This is a fully English-authored skill. The visual style is language-agnostic, so it works for an article in any language; annotations default to short English.

## Read these references (load as needed, don't dump all into context)

- `references/style-dna.md` — visual style DNA, color rules, text rules, hard nos.
- `references/xiaohei-ip.md` — Xiaohei's form, personality, action library, and forbiddens.
- `references/composition-patterns.md` — structure types, the original-metaphor method, and the anti-copy rule.
- `references/prompt-template.md` — the single-image generation prompt template.
- `references/qa-checklist.md` — post-generation checks and iteration rules.
- `references/custom-ip-template.md` — scaffold for `references/custom-ip.md` when a user brings their own character (copy and fill in).
- `assets/examples/` — low-frequency visual calibration only (line density, whitespace, color restraint, how Xiaohei participates). Do NOT copy their compositions.

## Bring your own character (custom IP)

Xiaohei is the **default** character, not a hard requirement. A user can swap in their own mascot or icon; everything else (white background, hand-drawn line art, color discipline, composition rules) stays identical.

Two ways to seed a custom IP:

- **From a description** — the user describes the character (shape, eyes, limbs, vibe). Capture it in `references/custom-ip.md`, using `references/custom-ip-template.md` as the scaffold.
- **From a sample image** — the user gives a reference image (their logo / mascot / icon). Read the image, describe its silhouette, eyes, limbs, and feel **in words**, draft `references/custom-ip.md`, and confirm with the user before generating. Text-to-image tools here render from that text description, not the image itself; pin a fixed `seed` to keep the character consistent across images.

**The one rule every custom IP must inherit:** the character must *perform the core conceptual action* of each image — never sit in a corner as a logo. If it can't do the article's core action, this skill is the wrong tool. Keep that line non-negotiable for any character.

When a custom IP profile is active, use it everywhere the prompt template says "the IP character"; otherwise default to Xiaohei (`references/xiaohei-ip.md`).

## Workflow

### 1. Digest the text

Read the article, link, Notion page, Markdown, or screenshot. Extract: the core claim; which paragraphs carry a cognitive turn; what is worth illustrating; what is better left as text. Don't illustrate evenly — pick "cognitive anchors" (a key judgment, a break point, an input→output loop, a fork, a before/after, a common pit, a role-state change).

### 2. Shot list first

If the user only asks "what should I illustrate / where do images help", return a shot list before generating anything. For each shot, write: where it goes, theme, core idea, structure type, what Xiaohei is doing, suggested elements, and suggested short English labels. Default 4–8 shots; 1–3 for short pieces; rarely exceed 9. Enough is enough — don't turn the article into a picture book.

### 3. Single generation (tool-agnostic)

If the user clearly asks to "generate / output / make the image", don't stop to confirm. Generate each image separately — never tile multiple images into one.

First resolve the **active IP character**: if the user supplied a custom IP (a description or a sample image), use `references/custom-ip.md`; otherwise default to Xiaohei.

Pick the image tool by availability (do NOT hardcode one vendor):

1. Built-in `image_gen` (Codex) → use it directly. Strongest at in-image text; supports edit / inpaint.
2. An image-generation MCP (e.g. `mcp__image-gen__generate_image`, set `aspect_ratio="16:9"`, `output_format="png"`, `num_outputs=1`) → use it. Text-to-image models (Flux family) render English text reasonably; keep labels to ≤4 total, each ≤4 words, to reduce rendering errors.
3. No image tool available → don't pretend to generate. For each shot, output a ready-to-paste English prompt from `references/prompt-template.md`. That is a valid deliverable, not a failure.

Each image explains exactly one core structure. The prompt must include: 16:9 horizontal; pure white background; black hand-drawn line art; sparse red/orange/blue handwritten English labels; lots of whitespace; Xiaohei as the subject of the core action; and forbid PPT / commercial / cute / complex-architecture / top-left type-title.

Do not copy past cases. Examples only calibrate style density and how Xiaohei participates. Reinvent a fresh, strange-but-coherent metaphor for THIS text every time.

### 4. QA and iterate

Check against `references/qa-checklist.md`. Regenerate or locally edit if: Xiaohei is mere decoration; the frame is too full; it looks like a flowchart / PPT; too much text or many typos; a top-left title appears; it's too cute / childish / rigid; or the background isn't clean white.

### 5. Save and deliver

If the user is working inside a workspace, copy finals to:

```text
assets/<article-slug>-illustrations/
```

Name them in order: `01-topic.png`, `02-topic.png`, ... Keep the original generations; don't overwrite existing assets unless the user explicitly asks to replace.

## Output discipline

Strategy output (before generating) is short and precise. Delivery output (after generating) includes: how many were generated, each image's purpose, the save paths, and which images are most reliable vs optional. Don't lecture about style theory — let the images speak.

---

*Derived from "Ian Xiaohei Illustrations" by Ian ([helloianneo](https://github.com/helloianneo/ian-xiaohei-illustrations)), MIT-licensed. English adaptation; the "Xiaohei" visual IP is credited to the original author.*
