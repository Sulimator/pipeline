import numpy as np
import pandas as pd
from alerce_classifiers.base.dto import InputDTO
from alerce_classifiers.base.mapper import Mapper
from alerce_classifiers.transformer_lc_features.utils import FEATURES_ORDER
from alerce_classifiers.utils.dataframe import DataframeUtils

from .dict_transform import FEAT_DICT

class LCHeaderMapper(Mapper):
    _fid_mapper = {
        0: "u",
        1: "g",
        2: "r",
        3: "i",
        4: "z",
        5: "Y",
    }
    _rename_cols = {
        "mag": "FLUXCAL",
        "e_mag": "FLUXCALERR",
        "fid": "BAND",
        "mjd": "MJD",
    }
    _feat_dict = FEAT_DICT

    def _get_detections(self, input: InputDTO):
        needed_cols = list(self._rename_cols.keys()).append("forced")
        return input.detections[needed_cols]

    def _get_headers(self, input: InputDTO):
        headers = pd.DataFrame.from_records(
            input.detections["extra_fields"].values,
            index=input.detections.index
        )
        headers = headers[headers["diaObject"].notnull()]
        headers = headers[~headers.index.duplicated(keep="first")]
        headers = pd.DataFrame.from_records(
            headers["diaObject"].values, index=headers.index
        )
        headers = headers[list(self._feat_dict.keys())]
        headers = headers.rename(columns=self._feat_dict)
        headers = headers.sort_index()
        headers.replace({np.nan: -9999}, inplace=True)
        return headers


    def _preprocess_detections(self, detections: pd.DataFrame):
        # Compute max epochs, maximum length per index and band
        max_epochs = DataframeUtils.get_max_epochs(detections)
        # Group by aid and creating lightcurve
        detections = detections.groupby(["aid"]).agg(lambda x: list(x))
        # Declare features that are time series
        list_time_feat = ["MJD", "FLUXCAL", "FLUXCALERR"]
        band_key = "BAND"
        # Transform features that are time series to matrices
        for key_used in list_time_feat:
            detections[key_used] = detections.apply(
                lambda x: DataframeUtils.separate_by_filter(
                    x[key_used], x[band_key], max_epochs
                ),
                axis=1,
            )
        # Normalizing time (subtract the first detection)
        detections["MJD"] = detections.apply(
            lambda x: DataframeUtils.normalizing_time(x["MJD"]), axis=1
        )

        detections["mask"] = detections.apply(
            lambda x: DataframeUtils.create_mask(x["FLUXCAL"]), axis=1
        )
        return detections

    def _preprocess_headers(self, headers: pd.DataFrame, quantiles: dict):
        all_feat = []
        for col in headers.columns:
            all_feat += [
                quantiles[col].transform(headers[col].to_numpy().reshape(-1, 1))
            ]

        response = np.concatenate(all_feat, 1)
        batch, num_features = response.shape
        response = response.reshape([batch, num_features, 1])
        return response

    def preprocess(self, input: InputDTO, **kwargs):
        # TODO: obtain the forced photometry field name
        detections = self._get_detections(input)
        headers = self._get_headers(input, kwargs["quantiles"])

        preprocessed_light_curve = self._preprocess_detections(detections)
        preprocessed_headers = self._preprocess_headers(headers)
        return preprocessed_light_curve, preprocessed_headers
    
    def postprocess(self):
        pass


class LCFeatureMapper(LCHeaderMapper):
    def _get_features(self, input: InputDTO):
        features = input.features
        return features.replace({ None: np.nan })
    
    def _preprocess_features(self, features: pd.DataFrame, feature_quantiles: dict):
        features.replace({np.nan: -9999, np.inf: -9999, -np.inf: -9999}, inplace=True)
        all_feat = []
        for col in FEATURES_ORDER:
            all_feat += [
                feature_quantiles[col].transform(
                    features[col].to_numpy().reshape(-1, 1)
                )
            ]
        response = np.concatenate(all_feat, 1)
        batch, num_features = response.shape
        response = response.reshape([batch, num_features, 1])
        return response        

    def preprocess(self, input: InputDTO, **kwargs):
        features = self._get_features(input)
        preprocessed_features = self._preprocess_features(features, kwargs["feature_quantiles"])
        lc, headers = super().preprocess(input, quantiles=kwargs["header_quantiles"])
        return lc, headers, preprocessed_features