from django.shortcuts import render, reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages

from recipe.utils import proper_username

from PIL import Image, UnidentifiedImageError
from password_strength import PasswordPolicy
import random
import datetime

from recipe.models import User, Recipe, Profile, Comment, List
from recipe.forms import NewRecipeForm, NewCommentForm


# Create your views here.
@require_http_methods(["GET"])
def index(request):

    # User is signed in
    if request.user.is_authenticated:
        
        return HttpResponseRedirect(reverse("homepage"))  

    # User is not signed in
    else:
        return render(request, "recipe/welcome.html")


# User registration
@require_http_methods(["POST"])
def register_user(request):

    # On form submission
    if request.method == "POST":  
          
        # Get the submitted user info
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # Perform password check
        if password != confirm:
            return render(request, "recipe/welcome.html", {
                "email": email,
                "username": username,
                "register_error": "Passwords did not match."
        })

        # Test password strength https://pypi.org/project/password-strength/
        policy = PasswordPolicy.from_names(
            length=8,  # min length: 8
            uppercase=1,  # need min. 1 uppercase letters
            numbers=1,  # need min. 1 digits
        ) 

        if policy.test(password):
            return render(request, "recipe/welcome.html", {
                "email": email,
                "username": username,
                "register_error": "The password must be atleast 8 characters long, and must include atleast one uppercase letter and a digit."
            })

        # Validate username
        if not proper_username(username):
            return render(request, "recipe/welcome.html", {
                    "email": email,
                    "username": username,
                    "register_error": "Your username must be 4 to 16 characters long with no spaces; and can only use letters, numbers and may include underscores '_'"
        })

        # Create user
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError as e:
            if "username" in str(e):
                 return render(request, "recipe/welcome.html", {
                    "email": email,
                    "username": username,
                    "register_error": "Username is taken."
        })
            if "email" in str(e):
                 return render(request, "recipe/welcome.html", {
                    "email": email,
                    "username": username,
                    "register_error": "Email address is in use."
        })

        login(request, user)

        # Create user profile
        profile = Profile(user=user)
        profile.save()

        messages.add_message(request, messages.INFO, 'Welcome to BlackPepper!')
        return HttpResponseRedirect(reverse("index"))


# User login
@require_http_methods(["POST"])
def login_user(request):
    
    # Get the submitted user info and try to authenticate
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        messages.add_message(request, messages.INFO, 'Welcome Back!')
        return HttpResponseRedirect(reverse("index")) 
    else:
        return render(request, "recipe/welcome.html", {
            "username": username,
            "login_error": "Incorrect username or password."
        })


# Logout
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Successfully Logged Out.')
    return HttpResponseRedirect(reverse("index"))  


# Homepage
@login_required
@require_http_methods(["GET"])
def homepage(request, page="1"):

    # User following list
    users = Profile.objects.get(user__username=request.user).following.all()

    user_list = []
    for user in users:
        profile = Profile.objects.get(user=user)
        recipes = profile.recipe.filter().order_by("-time")[:5]
        for recipe in recipes:
            user_list.append(recipe)

    user_list = sorted(user_list, key=lambda x: x.time, reverse=True)

    # Pagination
    p = Paginator(user_list, 4)
    page_obj = p.get_page(page)
        
    # Without the following three lines, the homepage does not load if there is no recipe in the database 
    random_recipe = None
    latest_list = None
    if Recipe.objects.filter(title__icontains=""):
        max_id = Recipe.objects.all().aggregate(max_id=Max("id"))['max_id']

        # Random recipe 
        while not random_recipe:
            try:
                pk = random.randint(1, max_id)
                random_recipe = Recipe.objects.get(pk=pk)
            except TypeError:
                pass
            # Raised when random primary key hits a deleted object
            except ObjectDoesNotExist:
                pass

        # Latest recipe list
        latest_list = []
        while len(latest_list) < 5 and max_id > 0:
            try:
                latest_list.append(Recipe.objects.get(pk=max_id))
            except ObjectDoesNotExist:
                pass
            max_id -= 1

    return render(request, "recipe/home.html", {
        "user_list": page_obj,
        "random_recipe": random_recipe,
        "latest_list": latest_list,
    })


# Create route
@login_required
@require_http_methods(["GET", "POST"])
def new(request):

    # On form submission
    if request.method == "POST":
        
        # Get submitted data
        title = request.POST.get("title")
        description = request.POST.get("description")
        ingredients = request.POST.get("ingredients")
        directions = request.POST.get("directions")
        notes = request.POST.get("notes")
        author = request.user
        image = request.FILES.get("image")

        # Verify image
        try:
            image.verify()
        # Failed
        except UnidentifiedImageError:
            pass
            # messages.add_message(request, messages.ERROR, 'Your image could not be uploaded.')
        # Empty field
        except AttributeError:
            pass

        recipe = Recipe(title=title, 
            description=description, 
            ingredients=ingredients, 
            directions=directions, 
            notes=notes, 
            author=author,
            image=image
        )

        recipe.save()

        # Add to user profile object
        profile = Profile.objects.get(user__username=request.user)
        profile.recipe.add(recipe)

        messages.add_message(request, messages.INFO, 'Recipe has successfully been created.')
        return HttpResponseRedirect(reverse("recipe", args=[recipe.pk]))
        
    # Create form for new recipe
    form = NewRecipeForm()

    return render(request, "recipe/new.html", {
        "form": form
    })


# Profile route
@require_http_methods(["GET"])
def profile(request, username, page="1", error_message=None):

    # Load user profile info and recipes
    user = User.objects.get(username=username)
    recipes = Recipe.objects.all().filter(author__username=username).order_by("-time")
    profile = Profile.objects.get(user__username=username)

    # Pagination
    p = Paginator(recipes, 5)
    page_obj = p.get_page(page)
    
    return render(request, "recipe/profile.html", {
        "user": user,
        "profile": profile,
        "page_obj": page_obj,
        "error_message": error_message
    })


# Change password
@login_required
@require_http_methods(["POST"])
def change_password(request):

    if request.method == "POST":

        # Check if the passwords match
        if request.POST.get("new-password") != request.POST.get("confirm-password"):    
            return HttpResponseRedirect(reverse("profile_error", kwargs={"username":request.user.username, "error_message":"Passwords do not match."}))

        # Check if the current password is entered correctly
        elif not check_password(request.POST.get("current-password"), request.user.password):
            return HttpResponseRedirect(reverse("profile_error", kwargs={"username":request.user.username, "error_message":"Incorrect password."}))

        # Check if the new password is different than the old
        elif request.POST.get("current-password") == request.POST.get("new-password"):
            return HttpResponseRedirect(reverse("profile_error", kwargs={"username":request.user.username, "error_message":"New password must be different."}))
            
        # Lastly, test password strength https://pypi.org/project/password-strength/
        policy = PasswordPolicy.from_names(
            length=8,  # min length: 8
            uppercase=1,  # need min. 1 uppercase letters
            numbers=1,  # need min. 1 digits
        ) 

        if policy.test(request.POST.get("new-password")):
            return HttpResponseRedirect(reverse("profile_error", kwargs={"username":request.user.username, "error_message":"The password must be atleast 8 characters long, and must include atleast one uppercase letter and a digit."}))
        
        # Change password, log user in then redirect
        else:
            user = User.objects.get(username=request.user)
            user.set_password(request.POST.get("new-password"))
            user.save()
            login(request, user)

            messages.add_message(request, messages.INFO, 'Your password has successfully been changed.')
            return HttpResponseRedirect(reverse("profile", args=[user]))

            
# Recipe page
@require_http_methods(["GET"])
def recipe(request, id, page="1"):

    # Get recipe 
    recipe = Recipe.objects.get(pk=id)

    # Check if the user liked the recipe
    liked = False
    if request.user in recipe.yummy.all():
        liked = True

    # Get comments and paginate
    comments = Comment.objects.all().filter(recipe__pk=id).order_by("-pk")

    p = Paginator(comments, 5)
    page_obj = p.get_page(page)

    # Comment form
    comment_form = NewCommentForm()

    # Form to edit recipe
    edit_form = NewRecipeForm({
        "title": recipe.title,
        "description": recipe.description,
        "image": recipe.image,
        "ingredients": recipe.ingredients,
        "directions": recipe.directions,
        "notes": recipe.notes
    })

    # Get user lists
    try:
        lists = List.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        lists = []

    return render(request, "recipe/recipe.html", {
        "recipe": recipe,
        "comments": page_obj,
        "form": comment_form,
        "liked": liked,
        "edit_form": edit_form,
        "lists": lists,
    })


# Search
@login_required
@require_http_methods(["POST"])
def search(request, page="1"):

    # A search performed by sumbitting a query into searchbar
    if request.method == "POST":

        query = request.POST.get("search")

        # Page is selected via dropdown form 
        if request.POST.get("page"):
            page = request.POST.get("page")

        exact_results = Recipe.objects.filter(title__iexact=query)
        similar_results = Recipe.objects.filter(title__icontains=query)

        # for result in similar_results:
        #     if result in exact_results:
        #         similar_results.remove(result)

        results = similar_results | exact_results

        # Pagination
        p = Paginator(results, 5)
        page_obj = p.get_page(page)
        
        return render(request, "recipe/search.html", {
            "query": query,
            "results": page_obj
        })


# Search user
@login_required
@require_http_methods(["POST"])
def search_user(request, page="1"):
    
    # Similar to recipe search
    if request.method == "POST":

        query = request.POST.get("search")

        # Page is selected via dropdown form 
        if request.POST.get("page"):
            page = request.POST.get("page")

        exact_results = Profile.objects.filter(user__username__iexact=query)
        similar_results = Profile.objects.filter(user__username__icontains=query)

        results = similar_results | exact_results

        p = Paginator(results, 10)
        page_obj = p.get_page(page)

        return render(request, "recipe/search-user.html", {
            "query": query,
            "results": page_obj
        })


# Follow
@login_required
@require_http_methods(["POST"])
def follow(request, username):

    if request.method == "POST":

        # Get profile objects of user that is making the request and the target user
        user = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user__username=request.user)
        target = User.objects.get(username=username)
        target_profile = Profile.objects.get(user__username=username)

        # Target and user are the same, redirect immediately
        if user.username == target.username:
            return HttpResponseRedirect(reverse("profile", args=[username]))

        # Check if following already
        if user in target_profile.followed_by.all():
            user_profile.following.remove(target)
            target_profile.followed_by.remove(user)
        else:
            user_profile.following.add(target)
            target_profile.followed_by.add(user)
        
        return HttpResponseRedirect(reverse("profile", args=[username]))


# Like recipes
@login_required
@require_http_methods(["POST"])
def like(request, id):
    
    # Select recipe and user from database
    recipe = Recipe.objects.get(pk=id)
    user = User.objects.get(username=request.user)

    # Like or unlike and redirect
    if user in recipe.yummy.all():
        recipe.yummy.remove(user)
    else: 
        recipe.yummy.add(user)

    return HttpResponseRedirect(reverse("recipe", args=[recipe.id]))
    

# Comment on recipes
@login_required
@require_http_methods(["POST"])
def comment(request, id):

    # Select recipe and user
    recipe = Recipe.objects.get(pk=id)
    user = User.objects.get(username=request.user)

    # Create new comment
    comment = Comment(user=user, content=request.POST.get("content"), recipe=recipe)
    if request.FILES.get("image"):
        try:
            image = Image.open(request.FILES.get("image"))
            image.verify()
            comment.image = request.FILES.get("image")
        except UnidentifiedImageError:
            pass
    comment.save()

    messages.add_message(request, messages.INFO, f'Commented on "{recipe.title}"')
    return HttpResponseRedirect(reverse("recipe", args=[recipe.id]))

# Delete comment
@login_required
@require_http_methods(["POST"])
def delete_comment(request):

    if request.method == "POST":

        # Get comment
        comment = Comment.objects.get(pk=request.POST.get("comment"))
        
        if comment.user == request.user:
            comment.delete()

        messages.add_message(request, messages.INFO, f'Your comment on "{comment.recipe.title}" has been deleted.')
        return HttpResponseRedirect(reverse("recipe", args=[comment.recipe.id]))


# Edit bio
@login_required
@require_http_methods(["POST"])
def edit_bio(request):

    if request.method == "POST":

        # Get profile by request
        profile = Profile.objects.get(user=request.user)
        new_bio = request.POST.get("new_bio")
        
        profile.bio = request.POST.get("new_bio")
        profile.save()

        messages.add_message(request, messages.INFO, 'Your bio has been updated.')
        return HttpResponseRedirect(reverse("profile", args=[profile.user]))


# Set profile picture
@login_required
@require_http_methods(["POST"])
def profile_picture(request):

    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        
        # Verify image
        try:
            image = Image.open(request.FILES.get("picURL"))
            image.verify()
            profile.picture = request.FILES.get("picURL")
            profile.save()
            messages.add_message(request, messages.INFO, 'Your profile picture has been updated.')
        # Failed
        except UnidentifiedImageError:
            messages.add_message(request, messages.INFO, 'Image could not be uploaded.')
        # Request to remove image
        except AttributeError:
            profile.picture = request.FILES.get("picURL")
            profile.save()
            messages.add_message(request, messages.INFO, 'Your profile picture has been removed.')

        return HttpResponseRedirect(reverse("profile", args=[profile.user]))


# Access following users
@login_required
@require_http_methods(["GET"])
def following(request):
    
    # Get the following field for the user
    profile = Profile.objects.get(user=request.user)
    following = profile.following.all()

    # Get user profiles
    users = []
    for i in following:
        i = Profile.objects.get(user=i)
        users.append(i)

    return render(request, "recipe/following.html", {
        "users": users
    })


# Edit a recipe
@login_required
@require_http_methods(["POST"])
def edit_recipe(request, id):
    
    if request.method == "POST":

        # Confirm request user and requested recipe author
        recipe = Recipe.objects.get(pk=id)
        
        if recipe.author == request.user:
            
            # Get form data and update recipe
            recipe.title = request.POST.get("title")
            recipe.description = request.POST.get("description")
            recipe.ingredients = request.POST.get("ingredients")
            recipe.directions = request.POST.get("directions")
            recipe.notes = request.POST.get("notes")

            # Verify image
            try:
                image = Image.open(request.FILES.get("image"))
                image.verify()
                recipe.image = request.FILES.get("image")
            # Failed
            except UnidentifiedImageError:
                pass
                # messages.add_message(request, messages.ERROR, 'Image could not be uploaded.')
            # No input
            except AttributeError:
                pass

            recipe.save()

            messages.add_message(request, messages.INFO, f'Recipe "{recipe.title}" has been updated.')
            return HttpResponseRedirect(reverse("recipe", args=[id]))


# Delete a recipe
@login_required
@require_http_methods(["POST"])
def delete_recipe(request, id):

    if request.method == "POST":

        # Confirm user
        recipe = Recipe.objects.get(pk=id)

        if recipe.author == request.user:

            # Delete recipe and redirect
            recipe.delete()

        messages.add_message(request, messages.INFO, f'Recipe "{recipe.title}" has been deleted.')
        return HttpResponseRedirect(reverse("index"))


# Preview recipe prior to publishing
@login_required
@require_http_methods(["POST"])
def preview(request):

# Get submitted data
    title = request.POST.get("title")
    description = request.POST.get("description")
    ingredients = request.POST.get("ingredients")
    directions = request.POST.get("directions")
    notes = request.POST.get("notes")
    author = request.user
    image = "https://i.ibb.co/nCpzBM5/DALL-E-2023-01-30-11-48-47-cooking-egg-with-cast-iron-skillet-3-D-pixel-art.png"

    recipe = Recipe(title=title, 
        description=description, 
        ingredients=ingredients, 
        directions=directions, 
        notes=notes, 
        author=author,
        image=image,
        time=datetime.datetime.now()
    )
    
    messages.add_message(request, messages.INFO, 'Press "Go back" button to continue with recipe creation.')
    return render(request, "recipe/preview.html", {
        "recipe": recipe,
    })


# View user lists
@login_required
@require_http_methods(["GET"])
def user_lists(request):

    # Get user lists
    try:
        lists = List.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        lists = []
    
    return render(request, "recipe/user-lists.html", {
        "lists": lists
    })


# Create a list
@login_required
@require_http_methods(["POST"])
def create_list(request):
    
    if request.method == "POST":
        # Create new list and refresh listings page
        list = List(
            name = request.POST.get("name"),
            user = request.user
        )
        list.save()

    messages.add_message(request, messages.INFO, f'List "{list.name}" has been created.')
    return HttpResponseRedirect(reverse("user_lists"))


# Add recipe to a list
@login_required
@require_http_methods(["POST"])
def add_to_list(request, id):

    if request.method == "POST":
    
        recipe = Recipe.objects.get(pk=id)

        list_id = request.POST.get("list")

        # If the user wanted to create a new list
        try:
            list = List.objects.get(pk=list_id)
        except ValueError:
            list = List(
                name = request.POST.get("new-list-name"),
                user = request.user
            )
            list.save()

        if recipe in list.recipe.all():
            messages.add_message(request, messages.INFO, f'Recipe "{recipe.title}" is already in your List "{list.name}".')
        else:
            list.recipe.add(recipe)
            messages.add_message(request, messages.INFO, f'Recipe "{recipe.title}" has been added to your List "{list.name}".')

        return HttpResponseRedirect(reverse("recipe", args=[id]))


# Edit list
@login_required
@require_http_methods(["GET", "POST"])
def edit_list(request, id):

    # To render page
    if request.method == "GET":
        list = List.objects.get(pk=id)
    
        return render(request, "recipe/edit-list.html", {
            "list": list
        })
    
    if request.method == "POST":

        # Get list
        list = List.objects.get(pk=id)
            
        # Determine what the request is for
        if request.POST.get("event") == "rename-list":

            # Handle name change request
            list.name = request.POST.get("rename-list")
            list.save()

        elif request.POST.get("event") == "remove-recipe":
            
            # Handle recipe remove request
            recipe = Recipe.objects.get(pk=request.POST.get("recipe"))
            list.recipe.remove(recipe)

        elif request.POST.get("event") == "delete-list":

            # Handle delete list request   
            list.delete()
            messages.add_message(request, messages.INFO, f'List "{list.name}" has been deleted.')
            return HttpResponseRedirect(reverse("user_lists"))   

        messages.add_message(request, messages.INFO, f'List "{list.name}" has been updated.')
        return HttpResponseRedirect(reverse("edit_list", args=[id]))
        