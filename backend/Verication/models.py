from django.db import models
import pandas as pd
import uuid
import os


class ExtractedFeatures(models.Model):
    user = models.CharField(max_length=100)
    features_file = models.FileField(upload_to='features')

    def __str__(self):
        return self.user


def get_file_path(filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (ext, uuid.uuid4())
    return os.path.join('media\\features', filename)
