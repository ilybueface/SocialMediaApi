from django.contrib import admin
from .models import (
    Post,
    CustomUser,
    Follow,
    Comment,
    Like,
)


admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
