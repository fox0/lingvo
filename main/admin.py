from django.contrib import admin

from main.models import Word, NormalizedWord


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation')


class NormalizedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'normalized')


admin.site.register(Word, WordAdmin)
admin.site.register(NormalizedWord, NormalizedWordAdmin)
