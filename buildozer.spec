[app]
title = Underwood's Tarot
package.name = org.kivy.tarotapp
package.domain = org.kivy
version = 0.1
requirements = python3,kivy,pillow
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = images/images/*.jpg
orientation = all
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET

[buildozer]
log_level = 2
build_dir = ./.buildozer
