from django.conf.urls import *
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

from app import views as app_views
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    #Statics
    url(r'^static/(?P<path>.*)$' , serve, 
                                  {'document_root': settings.MEDIA_ROOT}),
    url(r'^(.*)/static/(?P<path>.*)$', serve, 
                                {'document_root' : settings.MEDIA_ROOT}),

    #Statistics
    url(r'^statistics$', app_views.statistics, name='statistics'),

    #Collaborators
    url(r'^collaborators$', app_views.collaborators, name='collaborators'),

    #Contest: Temporary url
    url(r'^contest$', app_views.contest, name='contest'),

    #Blog
    url(r'^blog$', 
        RedirectView.as_view(url='https://drscratchblog.wordpress.com')),

    #Dashboards
    url(r'^show_dashboard', app_views.show_dashboard, name='show_dashboard'),
    url(r'^download_certificate', app_views.download_certificate, name='certificate'),

    #Translation
    url(r'^i18n/', include('django.conf.urls.i18n'), name="translation"),
    url(r'^blocks$', app_views.blocks, name='blocks'),

    #Organizations
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        app_views.reset_password_confirm, name='reset_password_confirm'),
    url(r'^change_pwd$', app_views.change_pwd, name='change_pwd'),
    #url(r'^organization_hash', 'app.views.organization_hash',),
    url(r'^sign_up_organization$', app_views.sign_up_organization, name='sign_up_organizations'),
    url(r'^organization/stats/(\w+)', app_views.stats, name='organization_stats'),
    url(r'^organization/downloads/(.*)', app_views.downloads, name='organization_downloads'),
    url(r'^organization/settings/(\w+)', app_views.settings, name='organization_settings'),
    url(r'^organization/(.*)', app_views.organization, name='organization'),
    url(r'^login_organization$', app_views.login_organization, name='organization_login'),
    url(r'^logout_organization$', app_views.logout_organization, name='organization_logout'),


    #Coders
    url(r'^coder_hash', app_views.coder_hash, name='coder_hash'),
    url(r'^sign_up_coder$', app_views.sign_up_coder, name='sign_up_coder'),
    url(r'^coder/stats/(\w+)', app_views.stats, name='coder_stats'),
    url(r'^coder/downloads/(.*)', app_views.downloads, name='coder_downloads'),
    url(r'^coder/settings/(\w+)', app_views.settings, name='coder_settings'),
    url(r'^coder/(.*)', app_views.coder, name='coder'),
    url(r'^login_coder$', app_views.login_coder, name='coder_login'),
    url(r'^logout_coder$', app_views.logout_coder, name='coder_logout'),

    #Upload a .CSV
    url(r'^analyze_CSV$', app_views.analyze_CSV, name='csv'),

    #Plugins
    url(r'^plugin/(.*)', app_views.plugin, name='plugin'),

    #Discuss
    url(r'^discuss$', app_views.discuss, name='discuss'),

    #Ajax
    url(r'search_email/$', app_views.search_email, name='search_email'),
    url(r'search_username/$', app_views.search_username, name='search_username'),
    url(r'search_hashkey/$', app_views.search_hashkey, name='search_hashkey'),


    #Error pages
    #url(r'^500', 'app.views.error500',),
    #url(r'^404', 'app.views.error404',),

    #Learn
    url(r'^learn/(\w+)', app_views.learn, name='learn'),
    url(r'^$', app_views.main, name='main'),
    url(r'^.*', app_views.redirect_main, name='redirect_main'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
