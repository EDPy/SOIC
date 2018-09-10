from django.contrib import admin

from .models import Posd, KbMeta, T3000db, Stueckliste, Customer, PbbMeta, Pbb

admin.site.register(Posd)
admin.site.register(KbMeta)
admin.site.register(T3000db)
admin.site.register(Stueckliste)
admin.site.register(Customer)
admin.site.register(PbbMeta)
admin.site.register(Pbb)
