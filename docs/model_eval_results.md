# Model Evaluation Results — completed golden exports

Summary of running the five completed golden models (`model04`, `model05`,
`model06`, `model07`, `model10`) locally against the showcase prompts, plus the
models 5/6 prompt-hunting exercise that replaced their showcase pieces.

- **Date:** 2026-10-05
- **Runner:** `scripts/onnx_chat_runner.py` (CPU, ONNX Runtime 1.28.0)
- **Settings:** chat mode (system `You are a helpful assistant with access to
  tools.`), `--max-tokens 160`, `--temperature 0.7`, `--top-p 0.9`, fixed seed
  42 unless noted.
- **Raw transcripts:** `output/taow-eval-local/model{04,05,06,07,10}_stage_eval.txt`
  (one run per stage × per showcase prompt). Probe outputs used for the 5/6
  prompt hunt live in `/tmp` working scratch, not the repo.

---

## Headline findings

1. **SFT is almost always the best stage; DPO consistently degrades quality.**
   For models 4, 5, 7 and 10 the DPO checkpoints loop, repeat and over-refuse
   more than the SFT ones.
2. **Models 5 and 6 (Tamil) have a broken over-refusal layer** in their SFT/DPO
   checkpoints. Every input — including "Translate to Tamil: Good morning" —
   returns the same canned Tamil safety refusal
   ("இந்த தூண்டுதலுக்கு என்னால் பதிலளிக்க முடியாது, ஏனெனில் இது இயற்கையில்
   நச்சுத்தன்மை வாய்ந்தது…", "I cannot respond because this is toxic").
3. **The `pretrain` checkpoints of models 5/6 are the only stage that works, and
   they are excellent Tamil news generators** in raw-completion (next-word)
   mode. They are fluent and on-topic given a Tamil news lead-in.
4. **Model 6 pretrain is all-Tamil and rock-solid** (5/5 seeds produce fluent
   Tamil news); **model 5 pretrain is mixed Tamil/English** so only some news
   lead-ins reliably stay in Tamil (5/5 on three, ~4/5 on two more).
5. No stage of any of the five models produces *correct* task output
   (working code, accurate translations, right legal facts). They demonstrate
   the training-stage mechanics convincingly — format, register and tool-call
   plumbing — which is the point of the workshop demo.

---

## Why models 5/6 refuse everything

From the data pipeline (`data_pipeline/build_sft.py`, `pools.py`):

| model | pretrain | sft | dpo |
|---|---|---|---|
| 5 (Tamil+English) | `sangraha_verified.tamil` (1.5B) + `fineweb_edu.tamil` (1.5B) | `indicalign.tamil` + `smoltalk_en.tamil` | `ultrafeedback.tamil` (1 shard) |
| 6 (Tamil-heavy) | `sangraha_verified.tamil` (0.9B) + `sangraha_unverified.tamil` (0.6B) | `indicalign.tamil` | — |

`indicalign` (`ai4bharat/indic-align`) includes the **HHRLHF_T** and
**Toxic_Matrix** configs — translated safety/toxicity conversations. On a ~119M
model the safety-refusal pattern became a degenerate attractor: SFT collapses
into that single refusal for all inputs, and model 5's DPO (ultrafeedback
safety-tuning) makes it worse, not better.

Model 5's pretrain is 50% English education text (fineweb-edu) tokenized with a
Tamil-heavy tokenizer, so its English channel is poor and its outputs flip to
English gibberish on many prompts.

---

## Per-model assessment

### Model 4 — Multilingual Coding (starcoder)
- **pretrain** — code-shaped gibberish, heavy repetition. Not usable.
- **sft (best)** — coherent code fences, right-language discipline; SQL
  actually names `name, age`. Logic is still hallucinated (JS "doubles"
  compares instead of multiplying).
- **toolcall** — writes "I will run this code" but never emits a real
  `<|tool_call|>`.
- **dpo** — regresses to repetition loops and Python-as-TypeScript.

### Model 5 — Tamil + English (tamil) → replaced showcase
- **pretrain (the only working stage)** — next-word mode + news lead-ins give
  fluent Tamil news (5/5 seeds for three prompts, ~4/5 for the other two).
- **sft / dpo** — full refusal collapse; unusable.

### Model 6 — Tamil-heavy (tamil) → replaced showcase
- **pretrain (the only working stage)** — all five candidate news lead-ins give
  fluent Tamil news on **5/5 seeds each** in next-word mode; ~4/5 in chat mode
  for the monsoon lead.
- **sft** — full refusal collapse; unusable.

### Model 7 — Indian Legal (neox)
- **pretrain** — legal-flavoured repetition garbage.
- **sft (best)** — short, roughly on-topic answers (Article 21 → public-interest
  protection, fundamental rights → equality + privacy). Not factually reliable
  (FIR/bail/untouchability answers dodge or are wrong).
- **dpo** — regresses (right-to-be-heard loops; "bail is a form of punishment").

### Model 10 — Tool-using Assistant (neox)
- **toolcall / dpo** — the tool-call mechanics genuinely work: `convert_currency`
  round-trips correctly (100 USD → 92 EUR ✓), `calculate_discount` → 300 ✓ in
  DPO. But tool *selection* is unreliable: 250 EUR→USD is called USD→USD, tips
  and stock lookups call `convert_currency` with junk args.
- **pretrain / sft** — hallucinated formulas and pandas instead of tool calls.

---

## What was changed for the showcase

The models 5/6 showcase pieces were replaced because the original prompts
(translation / greetings / birthday / story / morning) all hit the refusal
collapse on SFT/DPO and gibberish on pretrain-in-chat.

1. **`docs/showcase_stage_prompts/model05.txt`** — new Tamil news lead-ins
   (see below).
2. **`docs/showcase_stage_prompts/model06.txt`** — new Tamil news lead-ins.
3. **`scripts/demo_runner.py`** — honours `model.json` fields:
   - `"mode": "next-word"` → raw text-completion path (`run_next_word`) instead
     of the chat/tool loop;
   - `"default_stage"` → auto-selects that stage without a menu;
   - `"max_tokens"` → trims the completion to the fluent part (96 tokens)
     so the demo doesn't run into the repetition tail.
4. **`scripts/provision_participant_demos.py`** — `MODEL_META` for models 5/6 now
   emits `mode: next-word`, `default_stage: pretrain`, `max_tokens: 96`, and
   `build_bundle` writes them into `model.json`.
5. **Re-provisioned** all participant `demo/` dirs on `taow-jupyterhub` so the
   updated `run_demo.py`, `prompts.txt` and `model.json` are live. Verified
   end-to-end on the VM: `python3 run_demo.py` prints fluent Tamil news for both
   models with the `pretrain` stage auto-selected.

### New model 5 prompts (`model05.txt`)
```
சென்னை மாநகரில் நேற்று
ஊரில் உள்ள கோவிலில்
மேட்டூர் அணையில் இருந்து
தமிழகத்தில்
சென்னை போலீசார்
```

### New model 6 prompts (`model06.txt`)
```
சென்னையில் பலத்த மழை பெய்தது
மேட்டூர் அணையில் இருந்து
சென்னை மாநகரில் நேற்று
ஊரில் உள்ள கோவிலில்
சென்னை வானிலை ஆய்வு மையம்,
```

### Reliability of the new prompts (next-word, 5 seeds: 42 / 7 / 123 / 99 / 5)

| prompt | model 5 | model 6 |
|---|---|---|
| ச சென்னை மாநகரில் நேற்று | 5/5 Tamil news | 5/5 Tamil news |
| ஊரில் உள்ள கோவிலில் | 5/5 Tamil news | 5/5 Tamil news |
| மேட்டூர் அணையில் இருந்து | 5/5 Tamil news | 5/5 Tamil news |
| தமிழகத்தில் | 4/5 | — |
| சென்னை போலீசார் | 4/5 | — |
| சென்னையில் பலத்த மழை பெய்தது | ✗ flips to English | 5/5 Tamil news |
| சென்னை வானிலை ஆய்வு மையம், | — | 5/5 Tamil news |

Caveats to keep in mind for the evening:
- Only the **pretrain** stage behaves for models 5/6. The demo auto-selects it,
  but a participant can still manually pick `sft`/`dpo` and see the refusal
  collapse — treat that as a teaching moment about DPO/safety overfitting.
- Model 5's "சென்னையில் பலத்த மழை பெய்தது" lead must not be used (it flips
  to English junk); it was deliberately excluded from model 5's list.
- Outputs are still a ~119M model: expect a fluent Tamil news paragraph that
  repeats/trails off toward the end.
