[app]
title = Tarot with Pictures
package.name = org.kivy.tarotapp
package.domain = org.kivy
version = 0.1
requirements = python3,kivy,pillow
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = images/*.jpg
orientation = portrait
fullscreen = 1
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET
# (list) Application requirements
# comma separated e.g. requirements = openssl,kivy

# (str) Presplash of the application
# android.presplash = images/presplash.png

# (list) The directory in which to store Android icon files.
# android.icons = %(source.dir)s/images/icons

# (str) Android screen orientation.
# options are 'landscape', 'portrait', 'all', 'sensor'
# but 'sensor' is not recommended and can cause issues

# (str) The logcat filters for your app
# The format is a comma-separated list of tags with a log level.
# Examples: '*:S' means suppress all tags by default
#           'python:D' means show python logs at Debug level.
android.logcat_filters = python:D,kivy:D,org.kivy.tarotapp:I,OpenGL:I,Input:I,System:I,Process:I,EGL_emulation:I,cutils:I,AudioTrack:I

[buildozer]
log_level = 2
build_dir = ./.buildozer
