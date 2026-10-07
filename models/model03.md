# Python Builder — model03

**Short, correct Python code with a coding-coach register.**

| Field | Value |
|---|---|
| Model number | 3 |
| Tokenizer | starcoder (vocab 49,168 -> padded 49,280, EOS 0) |
| Presentation mode | `chat` |
| Presented stage | `toolcall` |
| Status | APPROVED |

Presented stage is **toolcall** (evaluation, 2026-10-08): SFT collapsed into a
broken attractor (Korean dump on p5, `def Square(x,y): return x + y` on p1,
unrelated imports on p2/p3), so it is not presentable. The toolcall checkpoint
stays on Python intent across all five locked prompts and writes real code
(e.g. p3 opens a ```python def print_numbers(numbers)``` block). No
`dpo.onnx` export exists on the node (same slot-end yield skip as model09), so
toolcall also avoids that gap. Follows the model10 precedent of presenting
toolcall when it is the best stage.

Artifact: `model03-final-fp32.onnx` (the `toolcall.onnx` checkpoint), 473,208,878 bytes.

Prompt set: `model03-v1`  ·  tool set: `coder-v1`  ·  generation seed 7, temperature 0.7, top-p 0.9, cap 64 tokens.