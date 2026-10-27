# Security and Android build notes

## Exposed release signing material

Earlier public commits included a release signing keystore and its passwords in `buildozer.spec`. The key and passwords must be considered **compromised**. Their removal from the current code is not a rotation or Git history erasure.

1. Check whether this key was used to sign any distributed Android package / Google Play upload.
2. If used, follow Google Play's applicable upload-key reset or signing-key migration process; coordinate any direct-APK upgrade implications.
3. Generate a new keystore **outside this repository**, using a unique password, and store it in a secure credential manager.
4. Supply signing configuration through the `P4A_RELEASE_KEYSTORE`, `P4A_RELEASE_KEYSTORE_PASSWD`, `P4A_RELEASE_KEYALIAS` and `P4A_RELEASE_KEYALIAS_PASSWD` environment variables (local shell or approved CI secret storage). Do not add passwords to `buildozer.spec`, shell scripts, ZIP files, logs, or public build artifacts.
5. Review Git history, forks and downloadable artifacts. History rewriting alone does not revoke compromised keys.

## Actual Android debug build

GitHub Actions workflow `.github/workflows/build-android.yml` now calls `buildozer -v android debug` and uploads `bin/*-debug.apk` only if a real APK is produced. The workflow fails when compilation fails; a text metadata artifact is **not** an APK.

```sh
python -m pip install 'buildozer==1.5.0' 'Cython<3'
buildozer -v android debug
```

Debug builds need no release keystore. Their existence is not proof that FFmpeg works on Android: `main.py` invokes an external `ffmpeg` executable, which must be explicitly packaged/configured for production use and verified on a real device.

## Release builds

`build_playstore.sh` must only be used after setting up a **new private signing configuration** (the `P4A_RELEASE_*` variables above) and validating the build pipeline. The repository no longer provides release signing keys or passwords; the script refuses to run without them.

## Regression check

`python scripts/check_release_secrets.py` (run by the `Validate Android source` workflow) rejects tracked `.keystore`, `.jks`, `.p12`, `.apk`, `.aab` and `.zip` artifacts plus non-empty signing values in Buildozer configuration.

## Reporting

Do not open a public issue containing credentials, private keys, personal data, or exploitable details. Contact the repository owner privately through the contact method listed on their GitHub profile.
