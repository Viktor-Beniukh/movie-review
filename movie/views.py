from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Avg
from django.db.models.functions import Cast, Round
from django.db import models
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.views.generic.edit import FormMixin

from movie.forms import ReviewForm, MovieForm, RatingForm
from movie.models import (
    Genre,
    Movie,
    Director,
    Actor,
    Category,
    MovieFrames,
    Rating,
)


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
    queryset = (
        Movie.objects.select_related("category")
        .prefetch_related("directors", "actors", "genres")
        .annotate(
            avg_rating=Cast(
                Round(Avg("film_rating__rating")), models.IntegerField()
            )
        )
    )
    template_name = "movie/movie_list.html"
    paginate_by = 6


class MovieDetailView(GenreYear, DetailView, FormMixin):
    model = Movie
    slug_field = "slug"
    form_class = RatingForm
    template_name = "movie/movie_detail.html"

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(queryset, slug=slug)

    def get_success_url(self):
        movie = self.get_object()
        return reverse_lazy("movie:movie-detail", kwargs={"slug": movie.slug})

    def form_valid(self, form):
        movie = self.get_object()
        rating_value = form.cleaned_data["rating"]
        user = self.request.user

        try:
            rating = Rating.objects.get(user=user, movie=movie)
            rating.rating = rating_value
            rating.save()
        except Rating.DoesNotExist:
            Rating.objects.create(user=user, movie=movie, rating=rating_value)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        average_rating = (
            Rating.objects.filter(movie=self.object)
            .aggregate(avg_rating=Avg("rating"))["avg_rating"]
        )
        context["average_rating"] = (
            int(average_rating) if average_rating is not None else 0
        )
        return context


class MoviesFilterView(GenreYear, ListView):
    """Filtering of movies by year of release and genre ids"""
    paginate_by = 3

    def get_queryset(self):
        queryset = (
            Movie.objects.filter(
                Q(year_of_release__in=self.request.GET.getlist(
                    "year_of_release"
                )
                ) | Q(genres__in=self.request.GET.getlist("genres"))
            )
            .annotate(avg_rating=Avg("film_rating__rating"))
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


class MovieCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    CreateView
):
    model = Movie
    form_class = MovieForm
    template_name = "movie/add_movie.html"
    success_url = reverse_lazy("movie:movie-list")
    success_message = "The movie has been successfully created."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class MovieFramesCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    CreateView
):
    model = MovieFrames
    template_name = "movie/add_movie_frame.html"
    fields = "__all__"
    success_url = reverse_lazy("movie:movie-list")
    success_message = "The frame to the movie has been successfully created."


class ReviewCreateView(LoginRequiredMixin, View):

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


class AddCategoryView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    CreateView
):
    model = Category
    template_name = "movie/add_category.html"
    fields = ("name", "slug")
    success_message = "The category has been successfully created."


class ActorCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    CreateView
):
    model = Actor
    template_name = "movie/add_or_edit_actor.html"
    fields = "__all__"
    success_url = reverse_lazy("movie:movie-list")
    success_message = "The actor has been successfully created."


class ActorUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    UpdateView
):
    model = Actor
    template_name = "movie/add_or_edit_actor.html"
    slug_field = "name"
    fields = "__all__"
    success_url = reverse_lazy("movie:movie-list")
    success_message = "The actor has been successfully updated."


class DirectorCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    CreateView
):
    model = Director
    template_name = "movie/add_or_edit_director.html"
    fields = "__all__"
    success_url = reverse_lazy("movie:movie-list")
    success_message = "The director has been successfully created."


class DirectorUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    UpdateView
):
    model = Director
    template_name = "movie/add_or_edit_director.html"
    slug_field = "name"
    fields = "__all__"
    success_url = reverse_lazy("movie:movie-list")
    success_message = "The director has been successfully updated."


class GenreCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    GenreYear,
    CreateView
):
    model = Genre
    template_name = "movie/add_genre.html"
    fields = "__all__"
    success_url = reverse_lazy("movie:movie-list")
    success_message = "The genre has been successfully created."
