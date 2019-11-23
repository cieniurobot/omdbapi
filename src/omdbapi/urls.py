from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from api_rest.views import Index

urlpatterns = [
    url(r'^$', Index.as_view()),
    url(r'^docs/', include_docs_urls(title='OMDb API docs.', public=True)),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', views.obtain_auth_token),
    path('api/v1/', include('api_rest.urls')),
]
