[app]
title = Tarot with Pictures
package.name = tarotapp
package.domain = org.example
version = 1.0

# Simplified requirements - remove pillow to avoid libffi issues
requirements = python3,kivy==2.2.2

# Source configuration
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv
source.include_patterns = images/*,*.png,*.jpg

# Screen orientation
orientation = portrait
fullscreen = 1

# Android specific - using more stable API/NDK versions
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET,READ_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 23c
android.accept_sdk_license = True

# Use only one architecture to avoid build complexity
android.archs = armeabi-v7a

# Disable problematic features
android.gradle_dependencies = 
android.add_src = 

[buildozer]
log_level = 2
warn_on_root = 1
