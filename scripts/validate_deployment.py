#!/usr/bin/env python3
"""
validate_deployment.py
Validates that the cloud-platform-service is running correctly by calling
/health, /ready, and /metrics and checking expected fields.

Usage:
    python scripts/validate_deployment.py --base-url http://<EC2-IP>:8000
"""

import argparse
import sys

import requests

CHECKS = [
    {
        "name": "Health Check (/health)",
        "path": "/health",
        "expected_status": 200,
        "required_fields": ["status", "service", "version", "timestamp"],
        "field_assertions": {"status": "healthy"},
    },
    {
        "name": "Readiness Check (/ready)",
        "path": "/ready",
        "expected_status": 200,
        "required_fields": ["ready", "timestamp"],
        "field_assertions": {"ready": True},
    },
    {
        "name": "Metrics (/metrics)",
        "path": "/metrics",
        "expected_status": 200,
        "required_fields": ["counters", "uptime_seconds"],
        "field_assertions": {},
    },
]


def run_check(base_url: str, check: dict) -> bool:
    url = f"{base_url}{check['path']}"
    passed = True

    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as exc:
        print(f"  [FAIL] {check['name']} — connection error: {exc}")
        return False

    # Status code
    if resp.status_code != check["expected_status"]:
        print(
            f"  [FAIL] {check['name']} — "
            f"expected HTTP {check['expected_status']}, got {resp.status_code}"
        )
        passed = False

    # Parse body
    try:
        body = resp.json()
    except ValueError:
        print(f"  [FAIL] {check['name']} — response is not JSON")
        return False

    # Required fields
    for field in check["required_fields"]:
        if field not in body:
            print(f"  [FAIL] {check['name']} — missing field: '{field}'")
            passed = False

    # Value assertions
    for field, expected in check["field_assertions"].items():
        actual = body.get(field)
        if actual != expected:
            print(
                f"  [FAIL] {check['name']} — "
                f"field '{field}' expected {expected!r}, got {actual!r}"
            )
            passed = False

    if passed:
        print(f"  [PASS] {check['name']}")

    return passed


def main():
    parser = argparse.ArgumentParser(description="Validate cloud-platform-service deployment")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the deployed service (default: http://localhost:8000)",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    print(f"\nValidating deployment at: {base_url}")
    print("=" * 50)

    results = [run_check(base_url, check) for check in CHECKS]

    passed = sum(results)
    total = len(results)

    print("=" * 50)
    print(f"Result: {passed}/{total} checks passed")

    if passed < total:
        print("Status: FAILED\n")
        sys.exit(1)
    else:
        print("Status: ALL CHECKS PASSED\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
