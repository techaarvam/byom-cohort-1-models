# Math Solver — model08

**Handles arithmetic and simple algebra, with a demo calculator tool.**

| Field | Value |
|---|---|
| Model number | 8 |
| Tokenizer | neox (vocab 50,293 -> padded 50,304, EOS 0) |
| Presentation mode | `chat` |
| Presented stage | `sft` |
| Status | APPROVED |

Presented stage is **sft** (evaluation, 2026-10-06): DPO and toolcall collapse into a
canned "Let's solve this problem using Python code." attractor on the locked showcase
set, while SFT stays on-topic across all five prompts. Verbose but correct math framing
matching the model04/model07 precedent.

Artifact: `model08-final-fp32.onnx` (the `sft.onnx` checkpoint), 478,320,686 bytes.

Prompt set: `model08-v1`  ·  tool set: `utilities-v1`  ·  generation seed 7, temperature 0.7, top-p 0.9, cap 64 tokens.