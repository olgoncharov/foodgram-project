from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin, flatpages
from django.urls import path, include

urlpatterns = [
    path('', include('modules.users.urls')),
    path('', include('modules.recipes.urls')),
    path('', include('modules.purchases.urls')),
    path('api/v1/', include('modules.api.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path(
        'about-author/',
        flatpages.views.flatpage,
        {'url': '/about-author/'},
        name='about-author'
    ),
    path(
        'about-spec/',
        flatpages.views.flatpage,
        {'url': '/about-spec/'},
        name='about-spec'
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


handler404 = "modules.recipes.views.page_not_found"
handler500 = "modules.recipes.views.server_error"
