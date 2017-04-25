from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	# url(r'^secrets$', views.secrets),
	url(r'^secrets/(?P<sort>\w+)$', views.secrets),
	url(r'^logout$', views.logout),
	url(r'^share$', views.share),
	url(r'^like/(?P<secret_id>\d+)', views.like),
	url(r'^unlike/(?P<secret_id>\d+)', views.unlike),
	url(r'^delete/(?P<secret_id>\d+)', views.delete),
]