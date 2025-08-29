[app]
title = Tarot with Pictures
package.name = org.kivy.tarotapp
package.domain = org.kivy
version = 0.1
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = images/*.jpg
requirements = python3,kivy,pillow
orientation = sensor
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET

[buildozer]
log_level = 2
build_dir = ./.buildozer
