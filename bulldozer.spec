[app]

# (str) Title of your application
title = Tarot with Pictures

# (str) Package name
package.name = org.kivy.tarotapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kivy

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,pillow

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Supported orientation (one of landscape, portrait or all)
orientation = all

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) Permissions for Android
android.permissions = INTERNET

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build artifact storage, absolute or relative to spec file.
build_dir = ./.buildozer
