from django.contrib import admin
from .models import  Post, Comment, User


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)


#@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'date')
    list_filter = ('date')
    search_fields = ('author', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)