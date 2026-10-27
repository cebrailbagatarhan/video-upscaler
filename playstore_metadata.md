# Play Store Listing Draft — Not Release-Ready

This file is a truthful draft, not proof that the Android build has passed store
review or device validation.

## Current release blockers

- Rotate the exposed signing key and purge it from Git history.
- Produce a clean AAB with protected signing credentials.
- Test file access and photo output on physical Android devices.
- Add an Android-supported video backend before advertising video scaling.
- Provide a real privacy-policy URL, support address and store screenshots.
- Re-check the current Google Play target API requirement before submission.

## App title

Video Photo Resizer

## Short description

Resize photos locally with Lanczos filtering.

## Full description

Resize a single photo to a selected maximum resolution using Pillow's Lanczos
resampling. The app preserves the image's aspect ratio and processes the selected
file locally.

Scaling creates a larger pixel grid; it does not reconstruct missing detail and
is not AI super-resolution.

### Current Android feature set

- Select one JPG, JPEG, PNG, BMP or TIFF image.
- Choose a target size.
- Preserve aspect ratio while resizing.
- Save the result locally.

Video scaling is not currently supported in the Android package because an
FFmpeg executable is not bundled. Batch processing, AI enhancement, before/after
comparison, multiple languages and real-time progress are not implemented and
must not appear in the published listing.

## Category

Photography

## Content rating

To be completed in Play Console from the actual app questionnaire.

## Privacy and data safety

The current application code does not upload media or declare internet access.
This statement must be verified against the final AAB and all bundled
dependencies before publishing. Complete the Play Console Data safety form from
the shipped binary, not from this draft.

## Required publishing assets

- A reachable privacy-policy URL.
- A monitored support email.
- Screenshots captured from the tested release build.
- 512 × 512 app icon.
- 1024 × 500 feature graphic.
