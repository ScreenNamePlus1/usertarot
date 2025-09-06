[app]
title = Tarot with Pictures
package.name = org.kivy.tarotapp
package.domain = org.kivy
version = 0.1
requirements = python3,kivy==2.3.0,pillow==10.4.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = images/*.jpg, images/rider-waite-tarot/*.png, images/rider-waite-tarot/*.jpg
orientation = portrait
fullscreen = 1
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 23.1.7779620
android.sdk_path = /home/runner/android-sdk
# Presplash image
android.presplash = images/presplash.png
# Icon directory
android.icons = %(source.dir)s/images/icons

# (str) Android screen orientation.
# options are 'landscape', 'portrait', 'all', 'sensor'
# but 'sensor' is not recommended and can cause issues

# (str) The logcat filters for your app
android.logcat_filters = python:D,kivy:D,org.kivy.tarotapp:I,OpenGL:I,Input:I,System:I,Process:I,EGL_emulation:I,cutils:I,AudioTrack:I

[buildozer]
log_level = 2
build_dir = ./.buildozer
