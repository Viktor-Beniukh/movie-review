from django.urls import path

from movie.views import (
    MovieListView,
    MovieDetailView,
    DirectorView,
    ActorView,
    CategoryDetailView,
)

app_name = "movie"


urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("<slug:slug>/", MovieDetailView.as_view(), name="movie-detail"),
    path(
        "director/<str:slug>/",
        DirectorView.as_view(),
        name="director-detail"
    ),
    path("actor/<str:slug>/", ActorView.as_view(), name="actor-detail"),
    path(
        "category/<slug:slug>/",
        CategoryDetailView.as_view(),
        name="category-movies"
    ),

]
