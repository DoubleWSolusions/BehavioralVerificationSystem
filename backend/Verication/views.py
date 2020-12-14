from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, renderers
from django.core.files import File
import pandas as pd
import numpy as np


class CollectingData(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            res = request.data
            #print(request.data)
            user = res['user']
            data = np.array(res.getlist('myArray[coords][]'))
            data = data.reshape(-1, 5)
            cols = res.getlist('form[]')
            df = pd.DataFrame(data=data, columns=cols)
            path = get_file_path(user)
            print(path)
            df.to_csv(path)
            features = ExtractedFeatures(user=user, features_file=path)
            serializer = ExtractedFeatureSerializer(features)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)