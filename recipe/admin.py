from django.contrib import admin

from recipe.models import User, Recipe, Profile
from help.models import Contact

# Register your models here.
admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Profile)
admin.site.register(Contact)
