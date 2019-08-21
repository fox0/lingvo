from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=255, db_index=True, unique=True)
    translation = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ('word',)


class NormalizedWord(models.Model):
    word = models.CharField(max_length=255, db_index=True, unique=True)
    normalized = models.CharField(max_length=255)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ('word',)
