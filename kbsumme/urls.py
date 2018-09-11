from django.urls import path
from kbsumme import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upPosd', views.upPosd, name='upPosd'),
    path('upload', views.upload, name='upload'),
    path('plist', views.projectlist, name='plist'),
    path('iocount', views.iocount, name='iocount'),
    path('projectStat', views.projectStat, name='projectStat'), #TODO check the purpose of name again.
    path('<slug:pid>', views.projectStat, name='projectStats'),
    path('upPBB', views.upPBB, name='upPBB'),
    path('price', views.price, name='price')
]
