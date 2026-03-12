#!/usr/bin/env python3
"""Compare baseline vs agentic critic results side-by-side."""

import json
import sys
import os
from pathlib import Path


def load_results(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def compare(baseline_path, agentic_path):
    baseline = load_results(baseline_path)
    agentic = load_results(agentic_path)

    print(f"Baseline: {len(baseline)} samples from {baseline_path}")
    print(f"Agentic:  {len(agentic)} samples from {agentic_path}")
    print("=" * 80)

    for i, (b, a) in enumerate(zip(baseline, agentic)):
        sample_id = b.get("id", f"sample_{i}")
        print(f"\n{'='*80}")
        print(f"Sample: {sample_id}")
        print(f"{'='*80}")

        # Compare critic suggestions across rounds
        for round_idx in range(5):
            b_key = f"target_diagram_critic_suggestions{round_idx}"
            a_key = f"target_diagram_critic_suggestions{round_idx}"

            b_sugg = b.get(b_key)
            a_sugg = a.get(a_key)

            if b_sugg is None and a_sugg is None:
                break

            print(f"\n--- Round {round_idx} ---")
            if b_sugg:
                print(f"[BASELINE] {str(b_sugg)[:200]}...")
            if a_sugg:
                print(f"[AGENTIC]  {str(a_sugg)[:200]}...")

            # Check for code execution log (agentic only)
            code_key = f"target_diagram_critic_code_exec{round_idx}"
            if code_key in a:
                code_log = a[code_key]
                if code_log:
                    print(f"[CODE_EXEC] {str(code_log)[:300]}...")

            # Timing comparison
            elapsed_key = f"target_diagram_critic_elapsed{round_idx}"
            if elapsed_key in a:
                print(f"[TIMING] Agentic: {a[elapsed_key]}s")

        # Check final image field
        b_img_field = b.get("eval_image_field", "N/A")
        a_img_field = a.get("eval_image_field", "N/A")
        print(f"\nFinal image field — Baseline: {b_img_field} | Agentic: {a_img_field}")

        # Check if images were actually generated
        b_has_img = bool(b.get(b_img_field, "")) if b_img_field != "N/A" else False
        a_has_img = bool(a.get(a_img_field, "")) if a_img_field != "N/A" else False
        print(f"Image generated — Baseline: {b_has_img} | Agentic: {a_has_img}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_results.py <baseline.json> <agentic.json>")
        sys.exit(1)
    compare(sys.argv[1], sys.argv[2])
