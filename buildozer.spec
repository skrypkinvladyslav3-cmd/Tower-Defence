[app]
title = TowerDefense
package.name = towerdefense
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Зависимости для корректной работы Pygame на Android
requirements = python3,kivy,pygame_sdl2,pillow

orientation = landscape
fullscreen = 1

# Настройки Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
# Исправлено на 25b, как требовал лог ошибки!
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1