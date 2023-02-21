from django import forms
from recipe.models import Recipe, Comment

# Create your forms here.
class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe

        fields = ("title", "description", "ingredients", "directions", "notes", "image",)

        labels = {
            "title": "Title of your recipe:",
            "description": "A short description for the dish:",
            "ingredients": "List of ingredients:",
            "directions": "Directions, step by step:",
            "notes": "Additional notes:",
            "image": "Image to display:"
        }

        widgets = {
            "title": forms.Textarea(attrs={"rows": 2, "cols": 2, "style": "resize:none; font-size: 16px", "autofocus": "true" }),
            "description": forms.Textarea(attrs={"rows": "2", "style": "resize:none; font-size: 16px"}),
            "ingredients": forms.Textarea(attrs={"rows": "20", "style": "resize:none; font-size: 16px"}),
            "directions": forms.Textarea(attrs={"rows": "20", "style": "resize:none; font-size: 16px"}),
            "notes": forms.Textarea(attrs={"rows": 10, "style": "resize:none; font-size: 16px"}),
        }

        required = ("title", "description", "ingredients", "directions",)

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ("content", "image")

        labels = {"content": "New comment:"}

        widgets = {"content": forms.Textarea(attrs={"rows": 5, "style": "resize:none; font-size:1rem"})}