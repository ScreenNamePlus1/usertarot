[app]
title = Tarot with Pictures
package.name = tarotapp
package.domain = org.example
version = 1.0
requirements = python3,kivy
source.dir = .
source.include_exts = py,png,jpg,jpeg
fullscreen = 0
icon.filename = images/CardBacks.jpg

[buildozer]
log_level = 2
# Don't download SDK - use the one we've set up
android.skip_update = True
# Use system locations that we've already set up
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b
android.ndk = 25b
android.api = 33
android.minapi = 21
android.build_tools = 33.0.2
android.archs = arm64-v8a,armeabi-v7a
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
# Use stable p4a version
p4a.branch = develop