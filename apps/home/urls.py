from django.conf.urls.defaults import patterns,url


urlpatterns = patterns('apps.home.views',
		url(r'^tweets/*','tweet_view', name='tweets'),
		url(r'^logout','logout_view', name='vista_de_logout'),
		url(r'^index','index_view', name='vista_principal'),
		url(r'^login','login_view', name='vista_de_logeo'),
		url(r'^vistaPrincipal','busquedaWord', name='vistaPrincipal'),
)
