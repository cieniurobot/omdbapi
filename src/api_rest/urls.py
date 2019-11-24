from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^movie/$', views.MovieSearchView.as_view()),
    url(r'^my-user-favourite-movie/$', views.MyUserFavouriteMovieCreateListView.as_view()),
    url(r'^my-user-favourite-movie/(?P<pk>[0-9]+)$', views.MyUserFavouriteMovieDeleteView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
