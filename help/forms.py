from django import forms
from help.models import Contact

# Create your forms here
class NewSupportForm(forms.ModelForm):
    class Meta:
        model = Contact

        fields = ("request", "email", "subject", "content", )

        labels = {
            "request": "",
            "email": "Contact information",
            "subject": "Subject for request",
            "content": "Request",
        }

        widgets = {
            "email": forms.Textarea(attrs={"rows": 1, "cols": 2, "style": "resize:none;", "autofocus": "true", "placeholder": "Contact information" }),
            "subject": forms.Textarea(attrs={"rows": 1, "style": "resize:none;", "placeholder": "Subject of request"}),
            "content": forms.Textarea(attrs={"rows": 10, "style": "resize:none;", "placeholder": "Request"}),
        }

        required = ("request", "email", "subject", "content",)

class NewContactForm(forms.ModelForm):
    class Meta:
        model = Contact

        fields = ("email", "subject", "content", )

        labels = {
            "email": "Contact information",
            "subject": "Subject for request",
            "content": "Request",
        }

        widgets = {
            "email": forms.Textarea(attrs={"rows": 1, "cols": 2, "style": "resize:none;", "autofocus": "true", "placeholder": "Contact information" }),
            "subject": forms.Textarea(attrs={"rows": 1, "style": "resize:none;", "placeholder": "Subject of request"}),
            "content": forms.Textarea(attrs={"rows": 10, "style": "resize:none;", "placeholder": "Request"}),
        }

        required = ("email", "subject", "content",)