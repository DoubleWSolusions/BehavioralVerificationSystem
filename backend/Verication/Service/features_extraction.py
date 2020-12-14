import numpy as np
import pandas as pd
import glob
import os


class Extractor:

    @staticmethod
    def extract_features(file_list):
        feature_vector = [None] * 8

        for fileName in file_list:
            data = np.genfromtxt(fileName, dtype=None, delimiter=',')
            data = data[1:]

            time_col = data[:, 1]
            num_minutes = int(float(time_col[-1]) / 300)
            split_at = time_col.astype(float).searchsorted(np.asarray([(i + 1) * 60 for i in range(num_minutes)]))
            data_list = np.split(data, split_at)

            for data in data_list:
                rows = data.shape[0]
                avgSpeed = 0
                meanx = 0
                meany = 0
                numberOfClicks = 0
                drags = 0
                TimeSpent = avgMoves = avgTime = 0
                if rows > 1:
                    TimeSpent = data[rows - 1, 1].astype(np.float) - data[0, 1].astype(np.float)
                    for i in range(1, rows):
                        timeT = data[i, 1].astype(np.float) - data[i - 1, 1].astype(np.float)

                        avgSpeed = avgSpeed + ((np.linalg.norm(
                            [data[i, 4].astype(np.float) - data[i - 1, 4].astype(np.float),
                             data[i, 5].astype(np.float) - data[i - 1, 5].astype(np.float)])) / (timeT * rows + 1))

                        meanx = meanx + ((data[i, 1].astype(np.float) - data[i - 1, 1].astype(np.float)) * (
                            data[i - 1, 4].astype(np.float))) / TimeSpent

                        meany = meany + ((data[i, 1].astype(np.float) - data[i - 1, 1].astype(np.float)) * (
                            data[i - 1, 5].astype(np.float))) / TimeSpent

                        if ((data[i - 1, 3].astype(np.str) != "Drag")
                                and (data[i, 3].astype(np.str) == "Drag")):
                            drags = drags + 1

                        if data[i - 1, 2] != data[i, 2]:
                            numberOfClicks = numberOfClicks + 1

                    avgMoves = (rows / TimeSpent)
                    avgTime = (TimeSpent / rows)

                features = np.array([avgTime, avgSpeed, TimeSpent, avgMoves, meanx, meany, numberOfClicks, drags])
                feature_vector = np.row_stack((feature_vector, features))

        feature_vector = feature_vector[1:, :]

        df = pd.DataFrame(data=feature_vector,
                          columns=["avgTime", 'avgSpeed', 'TimeSpent',
                                   'avgMoves', 'meanx', 'meany',
                                   'numberOfClicks', 'drags'])

        return df
