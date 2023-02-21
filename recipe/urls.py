from django.urls import path

from . import views

urlpatterns = [
    # Homepage and welcome page routes
    path("", views.index, name="index"),
    path("home", views.homepage, name="homepage"),
    path("home/<int:page>", views.homepage, name="homepage_page"),
    # Register, Login, Logout routes
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    # Recipe routes
    path("new", views.new, name="new"),
    path("preview", views.preview, name="preview"),
    path("recipe/<int:id>/edit", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:id>/delete", views.delete_recipe, name="delete_recipe"),
    path("recipe/<int:id>", views.recipe, name="recipe"),
    path("recipe/<int:id>/<int:page>", views.recipe, name="recipe_page"),
    # Profile routes
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/<int:page>", views.profile, name="profile_page"),
    path("profile/<str:username>/<str:error_message>", views.profile, name="profile_error"),
    # Search Routes
    path("search/recipe", views.search, name="search"),
    path("search/user", views.search_user, name="search_user"),
    path("search/recipe/<int:page>", views.search, name="search_page"),
    path("search/user/<int:page>", views.search_user, name="search_user_page"),
    # Following page
    path("following", views.following, name="following"),
    # Lists
    path("lists", views.user_lists, name="user_lists"),
    path("list/create", views.create_list, name="create_list"),
    path("list/add/<int:id>", views.add_to_list, name="add_to_list"),
    path("list/<int:id>/edit", views.edit_list, name="edit_list"), 
    # Database routes, no templates
    path("comment/<int:id>", views.comment, name="comment"),
    path("comment/delete", views.delete_comment, name="delete_comment"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("like/<int:id>", views.like, name="like"),
    path("bio", views.edit_bio, name="edit_bio"),
    path("password", views.change_password, name="change_password"),
    path("pp", views.profile_picture, name="profile_picture")
]