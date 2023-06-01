from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from movie.models import Review, Movie


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ("user", "text",)


class MovieForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = (
            "title",
            "slug",
            "tagline",
            "description",
            "poster",
            "year_of_release",
            "country",
            "directors",
            "actors",
            "genres",
            "world_premiere",
            "budget",
            "fees_in_the_usa",
            "fees_in_the_world",
            "category",
        )
