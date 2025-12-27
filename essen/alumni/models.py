from django.db import models

class Alumnus(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    kerb = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField()
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Alumni"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
