[app]
title = Tarot with Pictures
package.name = tarotapp
package.domain = org.kivy
version = 1.0

# Application requirements
requirements = python3,kivy==2.3.0,pillow==10.4.0

# Source configuration
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt
source.include_patterns = images/*,images/rider-waite-tarot/*
source.exclude_exts = spec

# Application metadata
author = Your Name
description = A beautiful tarot card reading application with multiple spreads

# Screen orientation
orientation = portrait
fullscreen = 1

# Android specific
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Application icons and graphics
android.presplash = images/presplash.png
android.presplash_color = #000000
android.icons = %(source.dir)s/images/icons
android.icon = %(source.dir)s/images/icon.png

# Gradle and build configuration
android.gradle_dependencies = 

# Screen orientation options
# options are 'landscape', 'portrait', 'all', 'sensor'
android.orientation = portrait

# Logcat filters
android.logcat_filters = python:D,kivy:D,%(package.name)s:I

# Architecture
android.archs = arm64-v8a, armeabi-v7a

# Release configuration
android.release_artifact = apk
android.debug = 0

# Services
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

[buildozer]
log_level = 2
build_dir = ./.buildozer
warn_on_root = 1
