from django.urls import path

from movie.views import (
    MovieListView,
    MoviesFilterView,
    MovieSearchView,
    MovieDetailView,
    MovieCreateView,
    MovieFramesCreateView,
    ReviewCreateView,
    DirectorView,
    DirectorCreateView,
    DirectorUpdateView,
    ActorView,
    ActorCreateView,
    ActorUpdateView,
    CategoryDetailView,
    AddCategoryView,
    GenreCreateView,
)

app_name = "movie"


urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("movie/create/", MovieCreateView.as_view(), name="movie-create"),
    path(
        "movie-frame/create/",
        MovieFramesCreateView.as_view(),
        name="movie-frame-create"
    ),
    path("movie-filter/", MoviesFilterView.as_view(), name="movie-filter"),
    path("movie-search/", MovieSearchView.as_view(), name="movie-search"),
    path("<slug:slug>/", MovieDetailView.as_view(), name="movie-detail"),
    path("<slug:slug>/rating/", MovieDetailView.as_view(), name="add-rating"),
    path("review/<int:pk>/", ReviewCreateView.as_view(), name="review-create"),
    path(
        "director/create/",
        DirectorCreateView.as_view(),
        name="director-create"
    ),
    path(
        "director/<str:slug>/",
        DirectorView.as_view(),
        name="director-detail"
    ),
    path(
        "director/<str:slug>/update/",
        DirectorUpdateView.as_view(),
        name="director-update"
    ),
    path("actor/create/", ActorCreateView.as_view(), name="actor-create"),
    path("actor/<str:slug>/", ActorView.as_view(), name="actor-detail"),
    path(
        "actor/<str:slug>/update/",
        ActorUpdateView.as_view(),
        name="actor-update"
    ),
    path(
        "category/create/",
        AddCategoryView.as_view(),
        name="category-create"
    ),
    path(
        "category/<slug:slug>/",
        CategoryDetailView.as_view(),
        name="category-movies"
    ),
    path("genre/create/", GenreCreateView.as_view(), name="genre-create"),
]
