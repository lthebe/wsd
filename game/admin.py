from django.contrib import admin
from .models import Game, GamePlayed
# Register your models here.
class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Game, GameAdmin)
admin.site.register(GamePlayed)
