from django import forms

from movie.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ("user", "text",)
