from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Connections)
admin.site.register(models.SpellingBee)
admin.site.register(models.Wordle)
admin.site.register(models.LoggedRequest)
admin.site.register(models.Sudoku)
admin.site.register(models.Strands)
