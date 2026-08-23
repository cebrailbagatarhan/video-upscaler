# Security

## Release signing

Release keystores, aliases and passwords must never be committed. Keep them in a
password manager or protected CI secret store and expose them only to the release
job. Debug builds must use a disposable debug key.

This repository previously contained a release keystore and its credentials.
Removing those files from the current branch does **not** remove them from Git
history or third-party clones. Treat that key as compromised:

1. Stop signing releases with the exposed key.
2. Create a new release/upload key with a unique password.
3. Follow the store's official key-upgrade or upload-key-reset process.
4. Replace protected CI secrets with the rotated values.
5. Purge the old material from Git history using a coordinated history rewrite,
   then invalidate caches and notify every collaborator to re-clone.

For local python-for-android signing, use environment variables rather than
tracked configuration:

```bash
export P4A_RELEASE_KEYSTORE=/secure/path/release.keystore
export P4A_RELEASE_KEYSTORE_PASSWD='from-a-secret-manager'
export P4A_RELEASE_KEYALIAS='release_alias'
export P4A_RELEASE_KEYALIAS_PASSWD='from-a-secret-manager'
buildozer android release
```

Do not paste real secret values into shell history. Prefer your CI provider's
masked-secret mechanism or a temporary environment file outside the repository.

## Reporting

Report suspected vulnerabilities privately to the repository owner. Do not open
a public issue containing credentials, private files or exploit details.
