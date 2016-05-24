from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.show_dashboard, name='show-dashboard'),
    url(r'^render-template/$', views.render_template, name='render-template'),
)

