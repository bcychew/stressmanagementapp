from threading import Thread
from django.contrib import admin
from .models import Post, UserProfile, Thread, Comment

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Thread)
admin.site.register(Comment)