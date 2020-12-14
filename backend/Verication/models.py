from django.db import models
import pandas as pd


class ExtractedFeatures(models.Model):
    user = models.CharField(max_length=100)
    features_file = models.FileField(upload_to='features')

    def __str__(self):
        return self.user


