from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from core.views import ChangeLanguageView

# admin.site.site_header = 'TechnoMark'
# admin.site.site_title = 'TechnoMark Admin Panel'
# admin.site.index_title = 'Welcome to TechnoMark Admin Panel'
urlpatterns = [
    path('change-language/', ChangeLanguageView.as_view(), name='change_language'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('product.urls', namespace='product')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

