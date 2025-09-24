[app]

# (str) Title of your application
title = Video Photo Upscaler

# (str) Package name
package.name = videoupscaler

# (str) Package domain (needed for android packaging)
package.domain = com.videoupscaler

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
version.regex = __version__ = ['\"](.*?)['\"]
version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Application author
author = Video Upscaler Team

# (str) Application description
description = Professional video and photo upscaling app with multiple resolution options

# (str) Short description (max 80 characters)
short_description = Upscale videos and photos to higher resolutions

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
#service.entrypoint = org.kivy.android.PythonService

# (str) Android app theme, default is ok for Kivy-based app
#android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) Android API level to target
android.api = 33

# (str) Minimum API level
android.minapi = 21

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (list) Android application meta-data to set (key=value format)
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references = @aar/some-library

# (bool) Indicate whether the screen should stay on
# Don't forget you'll need the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO

# (str) Android signing mode: debug or release
android.release_artifact = aab

# (str) Path to a custom keystore for the release build
#android.release_keystore =

# (str) Password for the keystore
#android.release_keystore_passwd =

# (str) Key alias for the keystore
#android.release_key_alias =

# (str) Password for the key
#android.release_key_passwd =

[gradle]
android.gradle_dependencies = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
android.enable_androidx = True

# (str) Gradle repositories
android.gradle_repositories = google(), mavenCentral()

# (str) Gradle dependencies
android.gradle_dependencies = androidx.appcompat:appcompat:1.4.2, androidx.core:core:1.8.0
