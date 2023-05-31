from django.urls import path

from movie.views import (
    MovieListView,
    MoviesFilterView,
    MovieSearchView,
    MovieDetailView,
    ReviewCreateView,
    DirectorView,
    ActorView,
    CategoryDetailView,
)

app_name = "movie"


urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("movie-filter/", MoviesFilterView.as_view(), name="movie-filter"),
    path("movie-search/", MovieSearchView.as_view(), name="movie-search"),
    path("<slug:slug>/", MovieDetailView.as_view(), name="movie-detail"),
    path("review/<int:pk>/", ReviewCreateView.as_view(), name="review-create"),
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
