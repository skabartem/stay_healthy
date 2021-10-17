from django.db import models
from users.models import User


class AbstractRecipe(models.Model):
    id = models.AutoField(editable=False, primary_key=True)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, null=True)
    kcal = models.IntegerField(null=True)
    source_link = models.TextField(max_length=500, null=True)
    difficulty = models.CharField(
        null=True,
        choices=(
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('A challenge', 'A challenge'),
            ('Unknown', 'Unknown')),
        max_length=20,
    )
    time = models.CharField(null=True, max_length=200)
    image_url = models.TextField(max_length=500, null=True)

    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        abstract = True


class Recipe(AbstractRecipe):
    pass


class RecipeToApprove(AbstractRecipe):
    pass


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
