from django.urls import path
from kbsumme import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upPosd', views.upPosd, name='upPosd'),
    path('upT3000', views.upT3000_Meta, name='upT3000'),
    path('plist', views.projectlist, name='plist'),
    path('iocount', views.iocount, name='iocount'),
    path('projectStat', views.projectStat, name='projectStat'), #TODO check the purpose of name again.
    path('<int:pid>', views.projectStat, name='projectStats'),
    path('upPBB', views.upPBB, name='upPBB'),
]
