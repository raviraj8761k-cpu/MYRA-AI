[app]
title = MYRA
package.name = myra
package.domain = com.boss
source.dir = .
source.include_exts = py,kv,png,jpg
source.exclude_dirs = .git,venv,.venv,__pycache__
version = 1.0.0
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 35
android.minapi = 23
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
