# Android Build Notes

The GitHub Actions workflow validates source and secret hygiene; it does not
currently produce an APK or AAB. Do not label its artifact or status as an Android
build.

## Reproducible debug-build checklist

Use a supported 64-bit Linux environment and the current Buildozer /
python-for-android prerequisites. Follow the upstream documentation rather than
pinning an old JDK or SDK from this repository:

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
