from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="main.html")),
    path("members/", include("members.urls")),
    path("leaves/", include("leaves.urls")),
    path("orders/", include("orders.urls")),
    path("grants/", include("grants.urls")),
    path("signs/", include("signs.urls")),
    path('paul-sentry-debug/', trigger_error),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
    # 미디어 서빙(디버깅)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
