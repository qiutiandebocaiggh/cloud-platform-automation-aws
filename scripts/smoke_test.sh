#!/usr/bin/env bash
# smoke_test.sh — Quick curl-based smoke test for cloud-platform-service
# Usage: ./scripts/smoke_test.sh [BASE_URL]
# Default: http://localhost:8000

set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
PASS=0
FAIL=0

check() {
  local label="$1"
  local url="$2"
  local expected_code="$3"

  actual_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url")

  if [ "$actual_code" == "$expected_code" ]; then
    echo "  [PASS] $label (HTTP $actual_code)"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] $label — expected HTTP $expected_code, got $actual_code"
    FAIL=$((FAIL + 1))
  fi
}

echo ""
echo "Smoke test: $BASE_URL"
echo "================================================"

check "GET /health"         "$BASE_URL/health"         "200"
check "GET /ready"          "$BASE_URL/ready"           "200"
check "GET /metrics"        "$BASE_URL/metrics"         "200"
check "GET /simulate-error" "$BASE_URL/simulate-error"  "500"

echo "================================================"
echo "Result: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  echo "Status: FAILED"
  exit 1
else
  echo "Status: ALL CHECKS PASSED"
  exit 0
fi
