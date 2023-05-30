from django.views.generic import ListView, DetailView

from movie.models import Genre, Movie, Director, Actor, Category


class GenreYear:
    """Genres and years of release movies"""
    @staticmethod
    def get_genres():
        return Genre.objects.all()

    @staticmethod
    def get_years_release():
        return (
            Movie.objects.values("year_of_release").distinct()
            .order_by("-year_of_release")
        )


class MovieListView(GenreYear, ListView):
    model = Movie
    movies = (
        Movie.objects.select_related("category")
        .prefetch_related("directors", "actors", "genres")
    )
    template_name = "movie/movie_list.html"


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "slug"


class DirectorView(GenreYear, DetailView):
    model = Director
    template_name = "movie/director.html"
    slug_field = "name"


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = "movie/actor.html"
    slug_field = "name"


class CategoryDetailView(GenreYear, DetailView):
    model = Category
    template_name = "movie/category.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["movies"] = Movie.objects.filter(category=self.object.id)
        return context
