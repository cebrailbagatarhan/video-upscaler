#!/usr/bin/env bash
set -euo pipefail

required_variables=(
  P4A_RELEASE_KEYSTORE
  P4A_RELEASE_KEYSTORE_PASSWD
  P4A_RELEASE_KEYALIAS
  P4A_RELEASE_KEYALIAS_PASSWD
)

for variable_name in "${required_variables[@]}"; do
  if [[ -z "${!variable_name:-}" ]]; then
    echo "Missing required release signing environment variable: ${variable_name}" >&2
    exit 1
  fi
done

if [[ ! -f "${P4A_RELEASE_KEYSTORE}" ]]; then
  echo "Release keystore does not exist: ${P4A_RELEASE_KEYSTORE}" >&2
  exit 1
fi

if git ls-files --error-unmatch -- "${P4A_RELEASE_KEYSTORE}" >/dev/null 2>&1; then
  echo "Refusing to use a release keystore tracked by Git." >&2
  exit 1
fi

python scripts/check_release_secrets.py

echo "Cleaning previous Buildozer output..."
buildozer android clean

echo "Building a release artifact with signing values supplied by the environment..."
buildozer android release

echo "Release build completed. Inspect bin/ and verify the signature before upload."
