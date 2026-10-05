# License and redistribution status — READ THIS

This directory documents the licensing status of what this repository
redistributes. It is **not yet a legal review**; it is an honest status report
with open items.

## Status summary

| Item | Status |
|---|---|
| Repository content (docs, model cards, scripts, manifests) | Original TechAarvam material; covered by the repo license. `LICENSE` file pending selection. |
| Model weights (`modelNN-final-fp32.onnx`) | Trained on the cohort pipeline from public corpora (see `docs/model_eval_results.md` and `qualification/`). **Redistribution rights for the derived training inputs have not been fully verified.** |
| `tokenizers/neox.json` | Derivative of a GPT-NeoX-family tokenizer. Likely permissive, but **not confirmed** for rehosting here. |
| `tokenizers/starcoder.json` | StarCoder/BigCode tokenizer. BigCode licenses restrict some uses. **Needs confirmation before public redistribution is relied on.** |
| `tokenizers/tamil.json` | Tamil tokenizer. Origin and license **unverified**. |

## Open action before a wider public release

1. Confirm each tokenizer's redistribution license and, if needed, replace
   with an equivalently-trained tokenizer whose rights are clear.
2. Confirm the training corpora licenses permit downstream redistribution of
   the derived checkpoints.
3. Add explicit per-artifact license entries here once confirmed.

Until those are resolved, treat the public availability of the three tokenizer
files and the derived weights as a **release risk** to be closed before the
demo is broadly promoted.