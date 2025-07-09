INSTALLED_APPS = [
    'django.contrib.humanize',  # 可选
    'rest_framework',
    'channels',
    'chat'
    'users',
    'posts',
    'friends',
    'notifications',
]

ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        "CONFIG": {}
    }
}