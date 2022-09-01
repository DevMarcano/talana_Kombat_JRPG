from django.urls import re_path as url
from Kombat import views as kom_view

urlpatterns = [
    url(r'^narrar/$', kom_view.narrarkombat),
]
