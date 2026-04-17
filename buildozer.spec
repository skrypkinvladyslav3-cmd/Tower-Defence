[app]

# (str) Название вашей игры
title = TowerDefense

# (str) Имя пакета (без пробелов)
package.name = towerdefense

# (str) Домен (можно оставить так)
package.domain = org.test

# (str) Папка с исходным кодом (точка означает текущую папку)
source.dir = .

# (list) Расширения файлов, которые нужно включить в APK
source.include_exts = py,png,jpg,kv,atlas

# (str) Версия приложения
version = 0.1

# (list) ЗАВИСИМОСТИ. Это самое важное для работы на Android!
requirements = python3,kivy,pygame_sdl2,pillow

# (str) Ориентация экрана
orientation = landscape

# (bool) Флаг полноэкранного режима
fullscreen = 1

# (list) Разрешения для Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) API уровень (31 сейчас стандарт для Google Play)
android.api = 31

# (int) Минимальный API (21 — поддержка старых телефонов)
android.minapi = 21

# (str) Версия NDK (23b самая стабильная для Kivy)
android.ndk = 23b

# (bool) Автоматически принимать лицензии SDK
android.accept_sdk_license = True

# (list) Архитектуры. Оставил только одну (arm64-v8a), чтобы сборка шла в 2 раза быстрее!
android.archs = arm64-v8a

[buildozer]
# Уровень логов (2 — максимально подробно, чтобы видеть ошибки)
log_level = 2
warn_on_root = 1