from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    BIOLOGICAL_GENDER = (
        (True, 'Male'),
        (False, 'Female')
    )
    male = models.BooleanField(choices=BIOLOGICAL_GENDER, null=True)
    age = models.IntegerField(null=True)
    weight_kg = models.FloatField(null=True)
    height_cm = models.FloatField(null=True)
    ACTIVENESS = (
        (1.2, 'Sedentary (little or no exercise)'),
        (1.375, 'Lightly active (exercise 1–3 days/week)'),
        (1.55, 'Moderately active (exercise 3–5 days/week)'),
        (1.725, 'Active (exercise 6–7 days/week)'),
        (1.9, 'Very active (hard exercise 6–7 days/week)'),
    )
    activity_coefficient = models.FloatField(choices=ACTIVENESS, null=True)
    meals_p_day = models.IntegerField(
        default=3,
        choices=((2, 2), (3, 3), (4, 4), (5, 5),),
        null=True,
        )
    GOAL_CHOICES = (
        (-1, 'Weight loss'),
        (0, 'Weight maintenance'),
        (1, 'Gain weight'),
    )
    goal = models.IntegerField(choices=GOAL_CHOICES, null=True, default=0)
    bmr = models.IntegerField(null=True, editable=False)
    amr = models.IntegerField(null=True, editable=False)
    bmi = models.FloatField(null=True, editable=False)

    @property
    def calculate_bmr(self):
        try:
            bmr_base = (10 * int(self.weight_kg)) + (6.25 * int(self.height_cm)) - (5 * int(self.age))
            return int(bmr_base + 5) if self.male else int(bmr_base - 161)
        except TypeError:
            return 0

    @property
    def calculate_amr(self):
        try:
            return int(self.bmr * float(self.activity_coefficient))
        except TypeError:
            return 0

    @property
    def calculate_bmi(self):
        try:
            return round(self.weight_kg / float(self.height_cm)**2 * 10000, 2)
        except TypeError:
            return 0

    def save(self, *args, **kwargs):
        self.bmr = self.calculate_bmr
        self.amr = self.calculate_amr
        self.bmi = self.calculate_bmi
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Weight(models.Model):
    weight = models.FloatField(null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.profile} | {self.weight} kg.'
