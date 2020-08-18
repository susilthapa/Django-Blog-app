from django.contrib import admin
from .models import Post,Comment
admin.site.register(Post)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('short_description', 'post', 'author', 'edited')
	search_fields = ('author__username', 'post__title')
	# list_filter = ('edited',)


admin.site.register(Comment, CommentAdmin)