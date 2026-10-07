# BYOM Cohort 1 Models

Ten ~120M-parameter language models trained by the first **Build Your Own
Model** cohort at TechAarvam, published as FP32 ONNX checkpoints and served to
the public in-browser demo at `https://techaarvam.com/workshops/byom_demos`.

## What is published

Each model publishes exactly **one presentation artifact**,
`modelNN-final-fp32.onnx`, uploaded as a GitHub Release asset under the pinned,
immutable tag **`cohort-1-v1`**. All ten models present the stage that
**evaluated best** (SFT, tool-call, or pretrain) — never a "last stage"
assumption, because DPO can degrade output for some models.

| Model | Presented stage | Mode | Artifact |
|---|---|---|---|
| model01 Everyday English | `sft` | chat | `model01-final-fp32.onnx` |
| model02 Helpful Assistant | `sft` | chat | `model02-final-fp32.onnx` |
| model03 Python Builder | `toolcall` | chat | `model03-final-fp32.onnx` |
| model04 Polyglot Coder | `sft` | chat | `model04-final-fp32.onnx` |
| model05 Tamil + English | `pretrain` | next-word | `model05-final-fp32.onnx` |
| model06 Tamil Voice | `pretrain` | next-word | `model06-final-fp32.onnx` |
| model07 Indian Law Guide | `sft` | chat | `model07-final-fp32.onnx` |
| model08 Math Solver | `sft` | chat | `model08-final-fp32.onnx` |
| model09 Science Explainer | `pretrain` | next-word | `model09-final-fp32.onnx` |
| model10 Tool Assistant | `toolcall` | chat | `model10-final-fp32.onnx` |

The two Tamil-Tamil models present their `pretrain` checkpoint in raw
next-word mode because their SFT/DPO stages collapsed into a single canned
safety refusal during evaluation.

## Pinned contract

`manifest/cohort-1-v1.json` is the contract between the artifact release and
the website. It contains, per model: the pinned release asset URL, byte size,
SHA-256 digest, tokenizer name and digest, vocabulary metadata, generation
settings (temperature 0.7, top-p 0.9, seed 7, per-model token cap), prompt-set
ID, tool-set ID, and presentation mode/stage. The website loads this manifest
and validates every digest before running a model.

Release URLs are pinned to the immutable tag `cohort-1-v1`; the GitHub
repository is the canonical immutable archive. **Browser downloads** are
served from a CORS-enabled Google Cloud Storage mirror (the GitHub Release
CDN does not send `Access-Control-Allow-Origin`, so browsers cannot read the
bytes directly from github.com):
`https://storage.googleapis.com/techaarvam-byom-cohort-1-models/cohort-1-v1/{modelNN}-final-fp32.onnx`.
The application never uses a mutable `latest` URL. Any change to a model, tokenizer, prompt
setting, schema, or tool requires `cohort-1-v2` or later.

## Layout

```
README.md
LICENSES/                 # redistribution status (READ THIS)
docs/                     # evaluation write-up + showcase prompt sets
models/model01..10.md     # model cards
tokenizers/neox.json      # byte-for-byte copies used during training
tokenizers/starcoder.json
tokenizers/tamil.json
manifest/cohort-1-v1.json
checksums/cohort-1-v1.sha256
qualification/            # stage-selection + per-model qualification records (v1)
scripts/verify_release.py # release-qualification checks (symlink-free, no binary blobs in git)
```

## Verify a release

Run from a checkout after downloading `dist/` assets to the same directory as
`scripts/`:

```bash
python3 scripts/verify_release.py --release-dir dist 2>/dev/null \
    || python3 -m pip install onnxruntime --quiet
```

The script checks each manifest entry's byte count and SHA-256, validates the
tokenizer digest and vocabulary, runs `onnx.checker`, and performs a one-token
native CPU smoke test.

## Notes

- ONNX binaries are **not** stored in git or Git LFS; they are GitHub Release
  assets only. Each is below GitHub's 2 GiB per-asset limit.
- The repository content (manifests, cards, docs, scripts) is original
  TechAarvam material. The model weights and the three tokenizer files carry
  the redistribution caveat below.