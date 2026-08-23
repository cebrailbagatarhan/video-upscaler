# Security

## Android release signing

The repository previously tracked an Android release keystore and plaintext signing configuration. Treat that key material as compromised even after it disappears from the current tree, because Git history and existing clones may retain it.

Required response if the key was used:

1. Stop signing new releases with it.
2. Rotate the Google Play upload key through the Play Console process, or create a new signing key before any first release.
3. Store the replacement keystore in a secret manager or an encrypted, access-controlled backup outside this repository.
4. Supply signing configuration through the `P4A_RELEASE_*` environment variables documented in `README.md`.
5. Consider a coordinated history rewrite only after rotation. History rewriting does not invalidate a leaked private key and disrupts existing clones.

The repository regression check rejects tracked `.keystore`, `.jks`, `.p12`, `.apk`, `.aab`, and `.zip` artifacts plus non-empty signing values in Buildozer configuration.

## Reporting

Do not open a public issue containing credentials, private keys, personal data, or exploitable details. Contact the repository owner privately through the contact method listed on their GitHub profile.
