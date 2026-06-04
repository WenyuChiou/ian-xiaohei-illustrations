# Custom IP profile (template)

Copy this file to `references/custom-ip.md` and fill it in to replace Xiaohei with your own character. Keep it short — this is a description the image tool reads, not a formal spec.

- **Name:** {your character's name}
- **Silhouette / body:** {one solid, simple shape — a blob, a bean, a box, a rounded icon. Simple reads best at small sizes.}
- **Eyes:** {e.g. two white dots / one eye / a thin visor}
- **Limbs:** {thin legs? thin arms? none?}
- **Face / expression:** {deadpan? blank? one fixed look — avoid complex emotion}
- **Feel:** {earnest worker / clumsy operator / calm machine — NOT a cute mascot, NOT a polished brand logo}
- **Action verbs it does well:** {pull, haul, stack, guard, pour, stitch, ... — the jobs it performs inside scenes}
- **Forbiddens:** {what to never draw — complex clothing, shiny eyes, text on the body, a glossy 3D logo look, etc.}
- **Seed (optional):** {a fixed integer to keep the character consistent across multiple images}

## The non-negotiable invariant

`performs_core_action: true`

Your character MUST be the one performing each image's core action. If you remove it and the metaphor still fully holds, it was decoration — rewrite so the character does the work. A character that only stands in a corner turns this skill into a generic illustration prompt and defeats its entire purpose.

## Seeding from a sample image (bring your own icon)

If you have a picture of your mascot or icon, give it to the assistant. It will:

1. Look at the image and describe the silhouette / eyes / limbs / feel **in words**, here in this file (text-to-image tools render from this text, not from the image itself).
2. Confirm the description with you before generating.
3. Pin a fixed `seed` so the character stays consistent across a whole article's worth of images.

Keep the character simple and high-contrast — a single solid silhouette survives the hand-drawn, sparse style far better than a detailed, multi-color logo.
