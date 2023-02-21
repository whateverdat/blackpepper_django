from django.shortcuts import render
from help.forms import NewContactForm, NewSupportForm
from help.models import Contact
from django.core.exceptions import ObjectDoesNotExist
import datetime

# Create your views here.
def index(request):

    # Form submission
    if request.method == "POST":
        
        if request.POST.get("request"):
            form = NewSupportForm(request.POST)
        else:
            form = NewContactForm(request.POST)
        
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            latest = Contact.objects.latest("time")
            td = (now-latest.time)
            seconds = td.seconds
        except ObjectDoesNotExist:
            seconds = 61

        if form.is_valid() and 60 < seconds:
            form.save()
            message = "Your form has successfully been submitted."

        else:
            message = "Please try again in a few minutes."

    try:
        print(message)
    except UnboundLocalError:
        message = None

    support_form = NewSupportForm()
    contact_form = NewContactForm()
    return render(request, "help/help.html", {
        "contact_form": contact_form,
        "support_form": support_form,
        "message": message
    })

