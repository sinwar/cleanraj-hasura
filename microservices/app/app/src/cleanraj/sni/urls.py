from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static


from .views import *


urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^$", homeView, name = "home"),
    url(r"^account/pro/(?P<pk>[a-zA-Z0-9_-]+)/$",ProView, name = "account_pro"),
    #url(r"^account/profile/(?P<pk>\d+)/$",ProfileView.as_view(), name = "account_profile"),
    url(r"^account/signup/", SignupView.as_view(), name = "account_signup"),
    url(r'^ajax/validate_username/$', validate_username, name='validate_username'),
    url(r'^savecords/$', save_cordinates, name='save_cordinates'),
    url(r'^showcords/$', show_garbage_points, name='show_garbage_points'),
    url(r'^localadmin/$', show_garbage_locations, name='show_garbage_locations'),
    url(r'^removelocation/$', remove_location, name='remove_location'),
    url(r'^suggestions/$', load_suggestions, name='load_suggestions'),
    url(r'^addsuggestion/$', add_suggestion, name='add_suggestion'),
    url(r"^account/", include("account.urls")),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

