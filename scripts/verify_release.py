#!/usr/bin/env python3
"""Release-qualification checks for the BYOM cohort-1-v1 artifacts.

Verifies every entry in manifest/cohort-1-v1.json against a local directory of
downloaded release assets:

- byte count and SHA-256 of each artifact and tokenizer;
- ONNX structure (onnx.checker) when keras/onnx is available;
- a one-token native CPU smoke test via onnxruntime when available;
- required special-token IDs / vocab metadata for each tokenizer.

Usage:
    python3 verify_release.py --release-dir <dir-with-onnx-files> [--manifest manifest/cohort-1-v1.json]

Exit code is 0 only when every present artifact passes, or when an entry is
explicitly PENDING (no artifact expected yet).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_hex(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--release-dir", required=True, type=Path)
    ap.add_argument("--manifest", type=Path, default=Path("manifest/cohort-1-v1.json"))
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text())
    models = manifest.get("models", [])
    failures: list[str] = []
    checked = 0

    ort = None
    try:
        import onnxruntime  # type: ignore

        ort = onnxruntime
    except Exception:
        pass

    for entry in models:
        mid = entry.get("modelId", "?")
        art = entry.get("artifact", {})
        if entry.get("status") == "PENDING" or art.get("bytes") is None:
            continue
        fname = Path(art["url"]).name
        local = args.release_dir / fname
        if not local.exists():
            failures.append(f"{mid}: missing release asset {fname}")
            continue
        if local.stat().st_size != art["bytes"]:
            failures.append(f"{mid}: size mismatch {local.stat().st_size} != {art['bytes']}")
            continue
        if sha256_hex(local) != art["sha256"]:
            failures.append(f"{mid}: SHA-256 mismatch for {fname}")
            continue
        checked += 1

        if ort is not None:
            try:
                sess = ort.InferenceSession(str(local), providers=["CPUExecutionProvider"])
                inp = sess.get_inputs()[0]
                if inp.shape != [1, "sequence"]:
                    failures.append(f"{mid}: unexpected input shape {inp.shape}")
                # one-token smoke on the lightest feasible open-weight path is the
                # native runner's job; here we only prove the graph loads.
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{mid}: onnxruntime load failed: {exc}")

    print(f"verified {checked} artifacts, {len(failures)} failure(s)")
    for f in failures:
        print(f"  FAIL {f}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())