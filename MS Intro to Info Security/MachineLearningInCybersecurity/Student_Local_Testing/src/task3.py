import numpy as np
import pandas as pd
from typing import Optional
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

class KmeansClustering:
    def __init__(self,random_state: int, init: str, n_init: int, max_iter: int, algorithm: str,tol: float):
        self.random_state = random_state
        self.init = init
        self.n_init = n_init
        self.max_iter = max_iter
        self.algorithm = algorithm
        self.tol = tol

    def kmeans_get_n_clusters(self, train_features:pd.DataFrame) -> int:
        model = KMeans(
            init=self.init,
            n_init=self.n_init,
            max_iter=self.max_iter,
            random_state=self.random_state,
            algorithm=self.algorithm,
            tol=self.tol
        )
        visualizer = KElbowVisualizer(model, k=(2, 10))
        visualizer.fit(train_features)

        k = int(visualizer.elbow_value_)
        return k

    def kmeans_train(self, train_features: pd.DataFrame, k:Optional[int]=None) -> list:
        if k is None:
            k = self.kmeans_get_n_clusters(train_features)

        self.kmeans_model = KMeans(
            n_clusters=k,
            init=self.init,
            n_init=self.n_init,
            max_iter=self.max_iter,
            random_state=self.random_state,
            algorithm=self.algorithm, 
            tol=self.tol
        )

        cluster_ids = self.kmeans_model.fit_predict(train_features)
        return list(cluster_ids)

    def kmeans_test(self, test_features: pd.DataFrame) -> list:
        cluster_ids = self.kmeans_model.predict(test_features)
        return list(cluster_ids)

