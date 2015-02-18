from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'makeystreet.views.home', name='home'),
    url(r'^profile/$', 'makeystreet.views.profile', name='profile'),
    url(r'^link/github/$', 'makeystreet.views.linkgithub', name="linkgithub"),
    url(r'^callback/$', 'makeystreet.views.callback', name='callback'),
    url(r'^listrepo/$', 'makeystreet.views.listrepo', name='listrepo'),
    url(r'^create_hook/(?P<repo_id>[\w\-_]+)/$', 'makeystreet.views.create_hook', name='create_hook'),
    url(r'^webhook/(?P<login>[\w\-_]+)/$', 'makeystreet.views.webhook', name='webhook'),
    url(r'^activity/$', 'makeystreet.views.activity', name='activity'),
    # url(r'^makeystreet/', include('makeystreet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
