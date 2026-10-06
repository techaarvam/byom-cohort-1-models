# Science Explainer — model09

**Explains familiar science ideas in short, clear language.**

| Field | Value |
|---|---|
| Model number | 9 |
| Tokenizer | neox (vocab 50,293 -> padded 50,304, EOS 0) |
| Presentation mode | `next-word` |
| Presented stage | `pretrain` |
| Status | APPROVED |

Presented stage is **pretrain** in **next-word** mode (evaluation, 2026-10-06): both SFT
and DPO collapse into a katakana `が` repetition attractor on the locked showcase set
(the same failure mode as the Tamil models 5/6), while pretrain produces coherent,
on-topic English continuations. Mirrors the model05/model06 design.

Artifact: `model09-final-fp32.onnx` (the `pretrain.onnx` checkpoint), 478,320,686 bytes.

Prompt set: `model09-v1` (next-word completions)  ·  generation seed 7, temperature 0.7, top-p 0.9, cap 96 tokens.