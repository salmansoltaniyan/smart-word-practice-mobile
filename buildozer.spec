[app]
# (str) Title of your application
title = Smart Word Practice

# (str) Package name
package.name = smartwordpractice

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.2.0,requests,pyjnius

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, sensorPortrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

[android]
# (int) Target Android API, should be as high as possible.
api = 33

# (int) Minimum API your APK / AAB will support.
minapi = 21

# (str) Android NDK version to use
ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
private_storage = True

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a