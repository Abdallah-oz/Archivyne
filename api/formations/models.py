from django.db import models

# Create your models here.
class Formations(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prix=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.title