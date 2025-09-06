[app]
title = Tarot with Pictures
package.name = tarotapp
package.domain = org.example
version = 1.0

# Simplified requirements - remove pillow to avoid libffi issues
requirements = python3,kivy==2.3.0  # Updated to latest stable Kivy

# Source configuration
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv
source.include_patterns = images/*,*.png,*.jpg

# Screen orientation
orientation = portrait
fullscreen = 1

# Android specific - using more stable API/NDK versions
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET  # Removed READ_EXTERNAL_STORAGE as images are bundled in APK
android.api = 34  # Updated to Android 14 for better compatibility
android.minapi = 21
android.ndk = r27d  # Latest LTS NDK for 64-bit support
android.accept_sdk_license = True

# Support both 32-bit and 64-bit architectures
android.archs = armeabi-v7a,arm64-v8a

# Disable problematic features
android.gradle_dependencies = 
android.add_src = 

[buildozer]
log_level = 2
warn_on_root = 1
