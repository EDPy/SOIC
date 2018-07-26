from django.contrib import admin

from .models import Posd, KbMeta, T3000db, Stueckliste

admin.site.register(Posd)
admin.site.register(KbMeta)
admin.site.register(T3000db)
admin.site.register(Stueckliste)
