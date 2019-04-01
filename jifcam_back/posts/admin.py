from django.contrib import admin

# Register your models here.
from .models import Post, Video, PostLike, PostComment, CommentComment

# admin.site.register(Post)
admin.site.register(Video)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(CommentComment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "video", "created_at", "updated_at", "is_active")
    list_filter = ("id", "author", "is_active")

    def is_very_benevolent(self, obj):
        return obj.benevolence_factor > 75