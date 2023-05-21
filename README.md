
# BlackPepper, for CS50W Final: 'Capstone' 
# whateverdat2.pythonanywhere.com
## Introduction:
For the CS50W's final assignment, I intended to create a compact app where users can store and organize their recipes, and have access to them from anywhere. **BlackPepper** is essentially an online cookbook; aside from personal use, it aims to create a network for people who share the same passion. During the COVID-19 quarantine, I grew passionate for trying different recipes in my now-so-abundant spare time. To my surprise, many of my friends had too. We have spent a significent portion of the quarantine sharing recipes with each other, and only if we had a more organized way to share!  
## Disctinctiveness and Complexity:
BlackPepper was different than anything I have built before. Aside from `Django` being a new framework for me, I wanted to use something other than `Bootstrap` to style my frontend. *With **BlackPepper**, I wanted to explore different frameworks.* After some research, I decided to use `Pico.css` which is easy to use yet customizable and for my future projects, I want to explore `React` and `Tailwind CSS`.

During the development, I had the opportunity to get a taste for the frontend power of `JavaScript`. I activated-deactivated buttons; changed the attributes of forms, hid and displayed various `HTML` elements according to the user input. *I aspired to create a more polished and responsive user experience.* I tried to think not as a developer--but as a user, and constantly adjusted the functionalities of **BlackPepper** towards ease of use and practicality. 

As my next short-term goal, I aim to learn how to effectively deploy my app and share with my friends thus *turning my project into an actual network that would fit its purpose.*

I had also created a second `Django` app under the project's root that is fully dedicated to teaching the basic functionality of **BlackPepper** and create a line of communication between me and my app's possible users--when the audience grows out of my social-zone!

Having the ability to develop web applications gave me the opportunity to combine multiple things that interest me--one being programming. I will continue to work towards creating more and different applications that interest me! 
## Contents:
Under the root of my project directory, there are two `django` apps: `recipe` contains the main app files and `help` contains the files for the help application. 

In the `requirements.txt` file, aside from standard django dependencies, I have used `django-cleanup` to automate the process of removing an image file once its corresponding model or model-field is deleted. Also to verify any image file that is uploaded to the app--and since it is the default requirement for django image uploading process--I used `Pillow`. Lastly, I used `django-password-strength` to automate the process of checking whether a password meets the security criterias.

The `blackpepper` folder hosts `settings.py` and `urls.py`. Both of which are pretty standard aside from being modified to create a folder to hold the uploaded files during development.
***

In the `help` folder there is a small application with one view and one template. It is a one-page application that consists of three parts: a part where the main functionality of **BlackPepper** is explained with the help of visualizations; and two other parts used for leaving different entries to the database under the contact model. `help.js` inside the folder `static` controls the navigation within the help app. Aside from handling the page-view and button animations, I also implemented a search-bar that searches within the titles of `Learn/How To` section of the help page. The app is mobile-responsive due to the media queries that are set up in the `theme.css` file.
***

Now to the `recipe` folder, which is the main app:

`models.py` hosts 5 models. 

The first one *User* is a modified version of django's standard user model. I have enforced the email field to be unique, thus allowing the same email address to only be assigned to one user.

*Recipe* model hold the data for recipes that are created within the app. Recipe author, title, description, additional notes, directions, ingredients, like count, timestamp and finally the recipe image.

A *Profile* instance is created for every user once they are registered. Which holds every recipe for that user, along with the follow information and profile details such as user bio and user profile picture.

*Lists* are way of organizing recipes. A user can create many lists, and add to them not only their own recipes, but other users' recipes as well.

A *Comment* instance is unique to a user and a post. Aside from holding text, it can also contain an image.   
***
There are only two django forms in the `forms.py`. *NewRecipeForm* and *NewCommentForm* that are stylized with custom labels and widgets.

Under the `static` folder:

*There are not many and content-heavy JavaScript files within the static folder since I have opted to write the code within the script tags in each HTML file. It amplifies the readability and keeps the corresponding code for each page more organized. I will talk about each page's code later.*

`flashMessage.js` makes any django message disappear after 5 seconds, and when connected using a desktop, it controls the button located in the flash message. Once clicked the message disappears immediately.

`theme.js` controls the toggle between light and dark themes. Once either of them are selected, the user preference is stored within `localStorage`. The dark and light themes themselves are set by utilizing `pico.css`.

`styles.css` contains required media queries to make the app mobile-responsive, aside from `CSS` customization.
***
A lot is going on in the app `templates`:
`layout.html` creates the nav-bar. It consists of nav-links and a searchbar if signed in; and *Login* and *Create an Account* buttons when not signed in. It also holds the *django message*, as well as a *JavaScript* tag on top that checks the input in the searchbar. If the query is longer than three characters, it activates the form.

`welcome.html` is the default page of the application when the user is not signed in. It has a brief introduction to the application, and two forms: one of which is for signing in and the other is for signing up. User can switch between them with the buttons located in the navbar. Also each form has an error-message field attached to them. When the backend fails to verify user input or something is not correctly entered, the message is populated and the user is informed. This is handled by the *JavaScript* code attached to the *HTML.*

`home.html` displays a feed for the signed in user. Unauthenticated users cannot view this page. Left of the page shows one recipe selected randomly from the database, and five of the latest recipes published. Right side is reserved for the recipes shared recently by the users followed by the user currently viewing the page. This section is paginated and only four recipe is shown at the same time.

`new.html` is the recipe creation page. It is initially populated by a form and two buttons at the end of the page. Some of the form fields are tagged as *required*. Upon filling these fields, the two buttons at the end of the page become active. *Preview* button creates a recipe object instance and displays it on a new page without saving--which is `preview.html`. *Share* button activates the model which prompts the user for one last time before actually publishing the recipe. All fields have counters on top of them, which displays the count of characters entered to the field, as well as the maximum amount.

`recipe.html` is where all the information about a recipe is displayed. Visiting user can interact with the recipe at the top of the page. They can like the recipe, or they can add the recipe to a list of theirs. Under all the recipe information, if the user is signed in, they can create comments, and if the recipe already has comments that belong to the user, they can choose to delete them. Comments that include images grow in size on mouse hover, this is just *CSS*. Comments are also paginated. Lastly on the bottom of the page, provided the user visiting the recipe page is the author of the recipe, user can choose to edit, or delete the recipe. When clicked on edit, with *JavaScript* everything on the page is hidden, and a form prefilled with the existing recipe information is shown. Every field of the recipe can be changed from here.

`profile.html` the profile information of a user along with their recipes--that are paginated. A user visiting someone else's profile can follow them from here. If the user is viewing their own profile, they can perform various actions from this page, related their profile. They can edit their bio, change their profile picture or password under the options menu. Also, the help page is accessible from this same menu. 

`search.html` is where the search results for recipes are listed. Once a search is performed, if the user wants to perform a search for user, they can simply click *users* button just over the results, which redirects user to `search-user.html` with the same query. The results page is nicely paginated and a page selector is added to the top of the results. Lastly, when a user-search is performed, with *JacaScript*, the search-field located in the navbar is altered to perform a user search, so the next query entered to this field, immediately performs a user-search.

`following.html` lists all the users followed by the user visiting this page. A search-field is located on top of the page that dynamically hides and displays matching users entered in thi field as query.

`user-lists.html` shows every list of the user. In a similar fashion to the last page, a searchfield is located on top of the page that performs dynamic search among lists. In addition to this, there are search-fields on top of every list that performs dynamic recipe searches inside their respective lists. Located next to this for each list, there is a *Edit* button which redirects to `edit-list.htm`, where user can rename or delete their list, as well as removing recipes from it.
***
Now to the views in `views.py`:

`index` view is rather straight-forward. Here, it is checked if the user is signed in. If so, they are redirected to *homepage.* If not, *welcome.html* is rendered.

`register_user` has no dedicated view. It just performs user registration request, sent from *welcome* page. If successful, the user is redirected to *homepage*, if not, the *welcome* page is rendered with the necessary information about the error.

`login_user` is similarly structured. On success, user is redirected to *homepage* and on error, *welcome* page is rendered with the necessary information about the error.

`logout_user` logs out the user.

`homepage` fetches the data required by *home.html*. First, it returns up to five recipes from each user followed by the user viewing the page--ordered and displayed by time. Then gets a random recipe by creating a random number between 1 and the highest primary key available. It is done inside a while loop in case the randomly selected number hits a deleted recipe. And lastly, it fetches five latest recipes from database and renders the homepage with the collected data.

`new` route handles recipe creations and rendering recipe creation page. On a post request, it collects the posted information, and if there is an image upload, verifies the image. If this verification fails, the recipe is created without any image. After creating the recipe, it is linked to the user profile object. On a get request, it creates an empty recipe form and renders the creation page.

`profile` is only accessible by get. After retrieving the user data--information and recipes--*profile.html* is rendered.

`change_password`, after verifications updates user password. In case of a failure, profile page--where the form is submitted from--is rendered with the necesary error message.

`recipe` returns the data for a recipe and checks if the viewing user has liked the recipe or not. Also, it handles the comment section for a recipe. Which consists of rendering a recipe form, and paginating retrieved comments.

`search` and `search-user` return the results matching the query. First, they check for an exact match and then, they check if the query is contained by any result title. This way, exact match is displayed above other results.

`follow` updates the database according to requests. If the user making the request targets a user they already follow, they effectively unfollow their target. Otherwise, they follow their target. 

`like` works in a similar fashion to follow. First the relation between the user and the recipe is checked--whether it is liked or not--then, the database is updated accordingly.

`comment` takes the user input then creates a comment object related to the target recipe and user. If there is an image attached, it is also verified here.

`delete_comment` handles the delete requests on comments. Provided that the comment belongs to the user making the request, it is deleted from the database.  

`edit_bio`, after confirming the user, this route updates the bio. If no data is attached to the post request, the field for bio is cleaned--removed.

`profile_picture` verifies the uploaded file. If it indeed is an image, the profile picture is updated. If there are no file attached, the picture is removed. In case of an error, an error message is thrown--this is ideally when a user tries to upload anything other than an image file.

`following` retrieves every user followed by the user making the request. If no results, the data returns as None, which is handled in the template.

`edit_recipe` takes care of edit requests on recipes. The image, if changed, is again verified here. `delete_recipe` removes the recipe object from the database after confirming the relation between the user and the recipe.

`preview` creates a recipe object instance without saving, and renders a preview page, where functionalities such as liking the recipe, adding it to a list or commenting on it are disabled. 

`user_lists` retrieves the data of every list created by the user and `create_list` creates a list object that belongs to the user making the request. `add_to_list` targets a recipe, and adds it to a list specified by the user.

`edit_list` on get request loads the list information, to be edited by the user. On post requests to this route, first it is determined what the request is for. It handles three separate requests: one to rename list, one to remove recipe from the list and last one to delete the recipe.

***
`utils.py` only contains one function to check the username. If the username is acceptable it returns True, else False. 

## How to run BlackPepper:
After cloning the repo, you should check the requirements.txt for the dependencies used. It is a good practise that a virtual environment is also set and enabled prior to downloading dependencies. After all the dependencies are installed head over to the project root--it contains `manage.py`. Next, you can simply run the command `python3 manage.py runserver` then visit the port the server is running on.


















