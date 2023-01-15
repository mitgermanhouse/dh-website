from adminsortable.models import SortableMixin
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DietaryRestriction(models.Model):
    long_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=127)

    def __str__(self):
        return self.long_name


class Member(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    class_year = models.IntegerField(
        null=True, validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    major = models.CharField(max_length=127, null=True)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to="images/", null=True)

    auto_lateplates = models.ManyToManyField(
        "menu.MealDayTime", related_name="auto_lateplate_members", blank=True
    )
    dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def lateplate_str(self):
        drs = self.dietary_restrictions.all()
        dr_str = "".join([dr.short_name for dr in drs])

        return self.user.get_full_name() + " " + dr_str


class Plushie(models.Model):
    name = models.CharField(max_length=127, blank=False)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GalleryContent(SortableMixin):
    class Meta:
        ordering = ["gallery_order"]

    title = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="gallery/")

    gallery_order = models.PositiveIntegerField(
        default=0, editable=False, db_index=True
    )

    def __str__(self):
        return self.title or self.caption
