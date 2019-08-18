from django.contrib import admin

from main.models import Word


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation')


admin.site.register(Word, WordAdmin)
