import numpy as np
import pandas as pd
import sklearn.model_selection
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.decomposition import PCA

def tts(  dataset: pd.DataFrame,
                       label_col: str, 
                       test_size: float,
                       should_stratify: bool,
                       random_state: int) -> tuple[pd.DataFrame,pd.DataFrame,pd.Series,pd.Series]:

    features = dataset.drop(columns=[label_col])
    labels = dataset[label_col]

    stratify_col = labels if should_stratify else None

    train_features, test_features, train_labels, test_labels = sklearn.model_selection.train_test_split(
        features, labels,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_col
    )
    return train_features,test_features,train_labels,test_labels

class PreprocessDataset:
    def __init__(self, 
                 one_hot_encode_cols:list[str],
                 min_max_scale_cols:list[str],
                 n_components:int,
                 feature_engineering_functions:dict
                 ):
        self.one_hot_encode_cols = one_hot_encode_cols
        self.min_max_scale_cols = min_max_scale_cols
        self.n_components = n_components
        self.feature_engineering_functions = feature_engineering_functions

        self.one_hot_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.min_max_scaler = MinMaxScaler()
        self.pca = PCA(n_components=n_components, random_state=0)
        return

    def one_hot_encode_columns_train(self,train_features:pd.DataFrame) -> pd.DataFrame:
        cols_to_encode = train_features[self.one_hot_encode_cols]
        other_cols = train_features.drop(columns=self.one_hot_encode_cols)

        self.one_hot_encoder.fit(cols_to_encode)
        encoded_array = self.one_hot_encoder.transform(cols_to_encode)

        encoded_df = pd.DataFrame(
            encoded_array,
            columns=self.one_hot_encoder.get_feature_names_out(self.one_hot_encode_cols),
            index=train_features.index
        )

        one_hot_encoded_dataset = pd.concat([encoded_df, other_cols], axis=1)
        return one_hot_encoded_dataset

    def one_hot_encode_columns_test(self,test_features:pd.DataFrame) -> pd.DataFrame:
        cols_to_encode = test_features[self.one_hot_encode_cols]
        other_cols = test_features.drop(columns=self.one_hot_encode_cols)

        encoded_array = self.one_hot_encoder.transform(cols_to_encode)

        encoded_df = pd.DataFrame(
            encoded_array,
            columns=self.one_hot_encoder.get_feature_names_out(self.one_hot_encode_cols),
            index=test_features.index
        )

        one_hot_encoded_dataset = pd.concat([encoded_df, other_cols], axis=1)
        return one_hot_encoded_dataset

    def min_max_scaled_columns_train(self,train_features:pd.DataFrame) -> pd.DataFrame:
        cols_to_scale = train_features[self.min_max_scale_cols]
        other_cols = train_features.drop(columns=self.min_max_scale_cols)

        self.min_max_scaler.fit(cols_to_scale)
        scaled_array = self.min_max_scaler.transform(cols_to_scale)

        scaled_df = pd.DataFrame(
            scaled_array,
            columns=self.min_max_scale_cols,
            index=train_features.index
        )

        min_max_scaled_dataset = pd.concat([scaled_df, other_cols], axis=1)
        return min_max_scaled_dataset

    def min_max_scaled_columns_test(self,test_features:pd.DataFrame) -> pd.DataFrame:
        cols_to_scale = test_features[self.min_max_scale_cols]
        other_cols = test_features.drop(columns=self.min_max_scale_cols)

        scaled_array = self.min_max_scaler.transform(cols_to_scale)
        scaled_df = pd.DataFrame(
            scaled_array,
            columns=self.min_max_scale_cols,
            index=test_features.index
        )

        min_max_scaled_dataset = pd.concat([scaled_df, other_cols], axis=1)
        return min_max_scaled_dataset

    def pca_train(self,train_features:pd.DataFrame) -> pd.DataFrame:
        cleaned_features = train_features.dropna(axis=1)
        self.pca_cols = cleaned_features.columns

        self.pca.fit(cleaned_features)
        pca_array = self.pca.transform(cleaned_features)
        column_names = [f"component_{i+1}" for i in range(self.n_components)]

        pca_dataset = pd.DataFrame(
            pca_array,
            columns=column_names,
            index=train_features.index
        )

        return pca_dataset

    def pca_test(self,test_features:pd.DataFrame) -> pd.DataFrame:
        cleaned_features = test_features[self.pca_cols]
        pca_array = self.pca.transform(cleaned_features)
        column_names = [f"component_{i+1}" for i in range(self.n_components)]

        pca_dataset = pd.DataFrame(
            pca_array, 
            columns=column_names,
            index=test_features.index
        )
        return pca_dataset

    def feature_engineering_train(self,train_features:pd.DataFrame) -> pd.DataFrame:
        feature_engineered_dataset = train_features.copy()

        for new_column_name, engineering_function in self.feature_engineering_functions.items():
            feature_engineered_dataset[new_column_name] = engineering_function(train_features)
        
        return feature_engineered_dataset
    
    def feature_engineering_test(self,test_features:pd.DataFrame) -> pd.DataFrame:
        feature_engineered_dataset = test_features.copy()

        for new_column_name, engineering_function in self.feature_engineering_functions.items():
            feature_engineered_dataset[new_column_name] = engineering_function(test_features)

        return feature_engineered_dataset

    def preprocess_train(self,train_features:pd.DataFrame) -> pd.DataFrame:
        preprocessed_dataset = self.one_hot_encode_columns_train(train_features)
        preprocessed_dataset = self.min_max_scaled_columns_train(preprocessed_dataset)
        preprocessed_dataset = self.feature_engineering_train(preprocessed_dataset)

        return preprocessed_dataset
    
    def preprocess_test(self,test_features:pd.DataFrame) -> pd.DataFrame:
        preprocessed_dataset = self.one_hot_encode_columns_test(test_features)
        preprocessed_dataset = self.min_max_scaled_columns_test(preprocessed_dataset)
        preprocessed_dataset = self.feature_engineering_test(preprocessed_dataset)
        
        return preprocessed_dataset

