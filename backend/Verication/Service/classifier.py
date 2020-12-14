from pyodds.utils.importAlgorithm import algorithm_selection
from .features_extraction import Extractor
import numpy as np
import pandas as pd
import glob
import os


class Classifier:
	def __init__(self, features):
		self.clf = algorithm_selection('lof', 1, 0.3)
		self.clf.fit(features)
		self.test_features = []

	def classify(self, session):
		test_features = Extractor.extract_features(session)
		prediction_result = self.clf.predict(test_features)
		outlierness_score = self.clf.decision_function(test_features)

		return prediction_result, outlierness_score

	def decide(self, prediction_result):
		coef = sum(prediction_result)
		if coef > 0:
			decision = True
		else:
			decision = False

		return decision
