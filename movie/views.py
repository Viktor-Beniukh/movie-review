from django.db.models import Q
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView

from movie.forms import ReviewForm
from movie.models import Genre, Movie, Director, Actor, Category


class GenreYear:
    """Genres and years of release movies"""
    @staticmethod
    def get_genres():
        return Genre.objects.all()

    @staticmethod
    def get_years_release():
        return (
            Movie.objects.all().all()
            .values("year_of_release").distinct()
            .order_by("-year_of_release")
        )


class MovieListView(GenreYear, ListView):
    model = Movie
    movies = (
        Movie.objects.select_related("category")
        .prefetch_related("directors", "actors", "genres")
    )
    template_name = "movie/movie_list.html"
    paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "slug"


class MoviesFilterView(GenreYear, ListView):
    """Filtering of movies by year of release and genre ids"""
    paginate_by = 1

    def get_queryset(self):
        queryset = (
            Movie.objects.filter(
                Q(year_of_release__in=self.request.GET.getlist(
                    "year_of_release"
                )
                ) | Q(genres__in=self.request.GET.getlist("genres"))
            )
        )
        return queryset.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year_of_release"] = (
            "".join(
                [
                    f"year_of_release={char}&"
                    for char in self.request.GET.getlist("year_of_release")
                ]
            )
        )
        context["genres"] = (
            "".join(
                [
                    f"genres={char}&"
                    for char in self.request.GET.getlist("genres")
                ]
            )
        )
        return context


class MovieSearchView(GenreYear, ListView):
    """Search movies by title"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(
            title__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f"q={self.request.GET.get('q')}&"
        return context


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


class ReviewCreateView(View):

    @staticmethod
    def post(request, pk):
        data = request.POST.copy()
        data.update({"user": request.user.id})
        form = ReviewForm(data)
        movie = Movie.objects.get(id=pk)

        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.user = request.user
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())
