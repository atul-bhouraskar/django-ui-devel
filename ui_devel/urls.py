from django.conf.urls import *

from . import views

urlpatterns = patterns('',
    url(r'^$', views.show_dashboard, name='show-dashboard'),
    url(r'^render-template/$', views.render_template, name='render-template'),
)

