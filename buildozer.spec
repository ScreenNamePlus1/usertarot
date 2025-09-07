[app]
title = Tarot with Pictures
package.name = tarotapp
package.domain = org.example
version = 1.0
requirements = python3,kivy==2.1.0,pillow,cython
source.dir = .
source.include_exts = py,png,jpg,jpeg
fullscreen = 0

[buildozer]
log_level = 2
android.archs = arm64-v8a,armeabi-v7a
android.ndk = 25b
android.sdk = 29
