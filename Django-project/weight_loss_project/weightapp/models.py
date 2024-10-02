from django.db import models
from django.contrib.auth.models import User

class WeightModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField(max_length=15)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date_added')