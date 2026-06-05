# QA Checklist

## Must pass

- 16:9 horizontal.
- Clean white background.
- The active IP character is present (Xiaohei by default; your custom character if one is active).
- The active IP character carries the core action, not just decoration.
- No copied old composition — a fresh metaphor for this text.
- Absurd, creative, interesting.
- Clean and sparse; subject under ~60% of the frame.
- One image, one core structure.
- Labels few, short, readable.
- Orange only for the main path or arrows.
- Red only for key points, problems, reminders, or results.
- Blue only for secondary notes, feedback, or system state.

## Machine-checkable QA (objective)

The checks above are subjective. Two of them can be verified mechanically — use the repo's helper as a hard gate on each saved PNG:

```bash
python tools/check_image.py assets/<slug>-illustrations/01-topic.png --aspect 16:9
```

It asserts (1) the image really is the target aspect ratio, and (2) at least ~35% of pixels are near-white (the "lots of whitespace" rule). If you are not inside the repo, do the same two checks inline: read the PNG dimensions for the ratio, and estimate the near-white pixel fraction. (The helper's whitespace check needs Pillow; without it, only the aspect check is enforced.)

For the **labels**, the objective check is a read-back: look at the generated image, read each handwritten label, and compare it to the label you intended. A mismatch (typo / garbled / wrong word) is a fail — regenerate with fewer / shorter labels, or fall back to a text-free image + caption (SKILL.md step 4). This stays a vision read-back because only you know the intended text.

## Failure signals (regenerate or locally edit)

- A top-left title like "Common Pitfalls / Workflow / System Architecture / Roadmap".
- Xiaohei looks like a mascot, emoji, or cute cartoon.
- Looks like a PPT, course slide, or formal flowchart.
- Too many elements, arrows, or nodes.
- Text becomes a long explanation.
- Background has paper texture, shadow, gradient, beige, or noise.
- A real UI screenshot or techy interface.
- Many typos or unreadable labels.
- Too rigid, with no absurd metaphor.
- Too similar to an old case in `assets/examples/`.

## Iteration moves

- **Too plain**: make Xiaohei the subject of the action; add one strange-but-coherent metaphor.
- **Too complex**: cut nodes; keep one action and 3–5 short labels.
- **Too cute**: emphasize deadpan, blank serious expression, not cute, not a mascot.
- **Too PPT**: drop titles, frames, tidy grids, and excess arrows; switch to a hand-drawn scene.
- **Too like an old case**: keep the core meaning; swap the main object and Xiaohei's action.
- **Text errors**: prefer a local edit; if there are many errors, regenerate with fewer labels.

## Delivery judgment

A good image should first feel "a bit strange", then become clear within one second.

If it looks like a tutorial page rather than an absurd product sketch on blank paper, it fails.
