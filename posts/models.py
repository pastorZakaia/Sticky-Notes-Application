from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """
    Model representing the author of a bulletin board post.
    Fields:
    - name: CharField for the author's name.
    Methods:
    - No specific methods are defined in this model.
    :param models.Model: Django's base model class.
     """


# Class to display sticky note
class Post(models.Model):
    title = models.CharField(max_length=220)  # Max len for error handling
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Define a ForeignKey for the author's relationship
    author = models.ForeignKey(User, on_delete=models.CASCADE,
    null=True, blank=True)

    def __str__(self):
        return self.title
    

    class Meta:  # Using Djangos inbuilt function for timestamp
        ordering = ["-created_at"]


name = models.CharField(max_length=255)

