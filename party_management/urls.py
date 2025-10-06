"""
URL configuration for party_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# party_management/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from members import views as member_views # <- ይህንን import አድርግ
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # የፕሮጀክቱ ዋና ገጽ (http://127.0.0.1:8000/)
    path('', member_views.landing_page, name='landing_page'),

    # የ 'members' መተግበሪያ ዩአርኤሎች
    path('members/', include('members.urls')),
    
    # የ Django ውስጠ-ግቡ የማረጋገጫ ዩአርኤሎች
    # ይህ 'login/', 'logout/', 'password_change/', 'password_reset/'... የመሳሰሉትን ይጨምራል
    # path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)