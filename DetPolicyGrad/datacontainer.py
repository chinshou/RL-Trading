import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

from sklearn import metrics, preprocessing
from talib.abstract import *

class ContainerException(Exception):
    pass

class Container():
    def __init__(self):
        pass

    @property
    def num_assets(self):
        return self.train_data.shape[0]

    @property
    def train_length(self):
        return self.train_data.shape[1]

    @property
    def test_length(self):
        return self.test_data.shape[1]

    @property
    def num_features(self):
        return self.train_data.shape[2]

    def get_data(self, train=True):
        if train:
            return self.train_data
        else:
            return self.test_data

    def initial_time(self, train=True, episode_length=None):
        if train:
            init_time = np.random.randint(low=0,
                                          high=self.train_length - episode_length)
        else:
            init_time = np.random.randint(low=0,
                                          high=self.test_length - episode_length)
        end_time = init_time + episode_length
        return init_time, end_time 

    def get_features(self, train, time):
        data = self.get_data(train=train)
        return data[:, time, :]

class TestContainer(Container):
    def __init__(self, shape='sine', num_assets=3, num_samples=200, train_split=0.7):
        super().__init__()

        if shape is 'sine':
            closes = [np.sin(2*np.pi*np.linspace(start=0, # [num_assets, num_samples]
                                                 stop=8,
                                                 num=num_samples))+(np.pi/8)*asset for asset in range(num_assets)]
        data = self.featurize(closes)

        split_level = int(num_samples * train_split)
        self.train_data = data[:, 0:split_level, :]                                                                                                                        
        self.test_data = data[:, split_level:, :]

    def featurize(self, closes):
        all_features = []
        for close in closes:
            diff = np.diff(close)
            diff = np.insert(diff, 0, 0)
            features = np.column_stack((close, diff)) # [num_samples, 2]
            all_features.append(features)
        return np.array(all_features) # [num_assets, num_samples, 2]
