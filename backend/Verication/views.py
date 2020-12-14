import glob
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, renderers
import pandas as pd
import numpy as np
from .Service.classifier import Classifier
from .Service.features_extraction import Extractor


class CollectingData(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            res = request.data
            user = res['user']
            data = np.array(res.getlist('myArray[]'))
            data = data.reshape(-1, 5)
            cols = res.getlist('form[]')
            df = pd.DataFrame(data=data, columns=cols)
            print(df)
            path = get_file_path(user)
            df.to_csv(path)
            features = ExtractedFeatures(user=user, features_file=path)
            serializer = ExtractedFeatureSerializer(features)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class VerificationData(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            res = request.data
            user = res['user']
            data = np.array(res.getlist('myArray[coords][]'))
            data = data.reshape(-1, 5)
            cols = res.getlist('form[]')
            test_df = pd.DataFrame(data=data, columns=cols)
            training_Files = glob.glob("media/features/" + user + "/*")
            training_features = Extractor.extract_features(training_Files)
            cls = Classifier(training_features)
            pred, score = cls.classify(test_df)
            answer = cls.decide(pred)
            if answer:
                return Response('Correct user', status=status.HTTP_201_CREATED)
            else:
                return Response('Incorrect user', status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)