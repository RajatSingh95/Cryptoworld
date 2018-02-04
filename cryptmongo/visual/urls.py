from django.conf.urls import url

from . import views

app_name= 'visual'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<clickdate>[\w \:]+)', views.index, name='index'),
]