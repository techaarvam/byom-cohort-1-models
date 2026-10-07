# Helpful Assistant — model02

**Short, friendly answers with an optional demo tool.**

| Field | Value |
|---|---|
| Model number | 2 |
| Tokenizer | neox (vocab 50,293 -> padded 50,304, EOS 0) |
| Presentation mode | `chat` |
| Presented stage | `sft` |
| Status | APPROVED |

Presented stage is **sft** (evaluation, 2026-10-08): DPO and toolcall both
collapse into canned "You're welcome!" replies or hallucinate malformed tool
names (create_game, get_fun) on the locked showcase set, while SFT keeps the
instruction-following assistant register (breakfast p1, hobby p3, TCS pricing
p5 framing). The utilities-v1 get_stock_price binding stays on p5, which SFT
answers in text at this size — matching the model08 sft precedent.

Artifact: `model02-final-fp32.onnx` (the `sft.onnx` checkpoint), 478,320,686 bytes.

Prompt set: `model02-v1`  ·  tool set: `utilities-v1`  ·  generation seed 7, temperature 0.7, top-p 0.9, cap 64 tokens.