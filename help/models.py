from django.db import models

# Create your models here.
class Contact(models.Model):

    CONTACT_CHOICES = (
            (1, ("Contact")),
            (2, ("Reporting a Problem")),
            (3, ("Help Request"))
        )

    request = models.IntegerField(choices=CONTACT_CHOICES, default=1)
    email = models.EmailField()
    subject = models.TextField(max_length=128)
    content = models.TextField(max_length=2048)
    time = models.DateTimeField(auto_now_add=True)