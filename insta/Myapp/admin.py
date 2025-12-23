from django.contrib import admin
from .models import Post14,ContactMessage,Report


@admin.register(Post14)
class Post14Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'caption', 'created_at', 'total_likes')
    search_fields = ('user__username', 'caption')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

admin.site.register(ContactMessage, ContactMessageAdmin)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'post', 'is_replied', 'created_at')
    list_filter = ('is_replied',)
    search_fields = ('reporter__username', 'reason')
