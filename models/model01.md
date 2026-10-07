# Everyday English — model01

**Friendly writing, short explanations, and clear answers.**

| Field | Value |
|---|---|
| Model number | 1 |
| Tokenizer | neox (vocab 50,293 -> padded 50,304, EOS 0) |
| Presentation mode | `chat` |
| Presented stage | `sft` |
| Status | APPROVED |

Presented stage is **sft** (evaluation, 2026-10-08): DPO loops on p1 ("Dear, dear,
dear friend") and drifts off-topic on p3 ("Dear King... enjoying your music"),
while SFT stays in an English-writing frame — email form (p1), a clean one-line
greeting (p3, reason=end) and the correct capital (p4: Tokyo). pretrain next-word
loops badly on p4/p5. Follows the model04/07/08 precedent of presenting SFT.

Artifact: `model01-final-fp32.onnx` (the `sft.onnx` checkpoint), 478,320,686 bytes.

Prompt set: `model01-v1`  ·  tool set: `—`  ·  generation seed 7, temperature 0.7, top-p 0.9, cap 64 tokens.