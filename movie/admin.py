from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from movie.models import (
    Category,
    Actor,
    Director,
    Genre,
    Movie,
    MovieFrames,
    Rating,
    Review,
)


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug",)
    list_display_links = ("name", )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    search_fields = ("name",)
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='50' height='60'"
        )

    get_image.short_description = "Image"


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "age",)
    search_fields = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='50' height='60'"
        )

    get_image.short_description = "Image"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("user", )


class MovieFramesInline(admin.TabularInline):
    model = MovieFrames
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='100' height='130'"
        )

    get_image.short_description = "Movie episodes"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "category",
        "year_of_release",
        "country",
        "world_premiere",
    )
    list_filter = ("category", "year_of_release", "country",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "category__name")
    inlines = [MovieFramesInline, ReviewInline]
    save_on_top = True
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "slug", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"),),
        }),
        (None, {
            "fields": (("directors", "actors", "genres", "category"),)
        }),
        (None, {
            "fields": (("year_of_release", "world_premiere", "country"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_the_usa", "fees_in_the_world"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.poster.url} width='100' height='130'"
        )

    get_image.short_description = "Poster"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "parent", "movie")
    readonly_fields = ("user",)


@admin.register(MovieFrames)
class MovieFramesAdmin(admin.ModelAdmin):
    list_display = ("title", "movies", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='50' height='60'"
        )

    get_image.short_description = "Image"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "rating")


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
