# Android Build Notes

Two GitHub Actions workflows exist: `Build Android debug APK` runs
`buildozer android debug` and fails unless a real `*-debug.apk` is produced;
`Validate Android source` checks Python syntax, the Lanczos resize behaviour and
secret hygiene. A green build only proves the APK compiled, not that it works on
a device. Never label either result as a release build.

## Reproducible debug-build checklist

Use a supported 64-bit Linux environment and the current Buildozer /
python-for-android prerequisites. Follow the upstream documentation (CI uses JDK 17 and the
p4a commit pinned in `buildozer.spec`):

- https://buildozer.readthedocs.io/
- https://python-for-android.readthedocs.io/

Then run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install buildozer
buildozer android debug
```

A successful compile is not sufficient for release. Install the generated debug
APK on physical devices and verify startup, file permissions, photo selection,
resize output and error handling.

## Release builds

Do not build a release with the historical key. Rotate it first and configure the
replacement only through protected local or CI secrets as described in
[`SECURITY.md`](SECURITY.md). Before Play submission, verify the current target
API policy and produce an AAB from the reviewed commit.
