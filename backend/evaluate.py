"""
ScamCheck KZ - Clean Architecture Evaluation Runner
"""

import json
import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

from use_cases.analyze_fraud import AnalyzeFraudUseCase
from domain.value_objects import Language


def run_evaluation():
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", "cases.json")
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found at {dataset_path}")
        sys.exit(1)

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    use_case = AnalyzeFraudUseCase()

    total = len(cases)
    correct_level = 0
    correct_scheme = 0

    print("=== ScamCheck KZ Model Evaluation (Clean Architecture) ===")
    print(f"Total test cases: {total}\n")

    for case in cases:
        res = use_case.execute(case["text"], lang_code=case.get("lang", "ru"))
        predicted_level = res.level.value
        expected_level = case["expected_level"]

        level_match = predicted_level == expected_level
        if level_match:
            correct_level += 1

        predicted_scheme = res.scheme.id if res.scheme else None
        expected_scheme = case.get("expected_scheme")

        scheme_match = predicted_scheme == expected_scheme
        if scheme_match:
            correct_scheme += 1

        status = "✅ PASS" if level_match and scheme_match else "❌ FAIL"
        print(f"Case #{case['id']} [{case['lang'].upper()}]: {status}")
        print(f"  Text: {case['text'][:60]}...")
        print(f"  Expected: level={expected_level}, scheme={expected_scheme}")
        print(f"  Got:      level={predicted_level}, scheme={predicted_scheme}, score={res.score}%\n")

    acc_level = round((correct_level / total) * 100, 2)
    acc_scheme = round((correct_scheme / total) * 100, 2)

    print("=== SUMMARY METRICS ===")
    print(f"Level Classification Accuracy: {acc_level}% ({correct_level}/{total})")
    print(f"Scheme Identification Accuracy: {acc_scheme}% ({correct_scheme}/{total})")


if __name__ == "__main__":
    run_evaluation()
