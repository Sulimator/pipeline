import numpy as np
import pandas as pd
from turbofats import FeatureFunctionLib
from numba import jit
import warnings


@jit(nopython=True)
def is_sorted(a):
    for i in range(a.size-1):
        if a[i+1] < a[i]:
            return False
    return True


class NewFeatureSpace(object):
    def __init__(self, feature_list, data_column_names=None):
        self.feature_objects = []
        self.feature_names = []
        if data_column_names is None:
            self.data_column_names = ['magpsf_corr', 'mjd', 'sigmapsf_corr']
        else:
            self.data_column_names = data_column_names

        for feature_name in feature_list:
            feature_class = getattr(FeatureFunctionLib, feature_name)
            feature_instance = feature_class()
            self.feature_objects.append(feature_instance)
            if feature_instance.is1d():
                self.feature_names.append(feature_name)
            else:
                self.feature_names += feature_instance.get_feature_names()

    def __lightcurve_to_array(self, lightcurve):
        return lightcurve[self.data_column_names].values.T

    def calculate_features(self, lightcurve):
        n_objects = len(lightcurve.index.unique())
        if n_objects > 1:
            raise Exception('TurboFATS cannot handle more than one lightcurve simultaneously')
        elif n_objects == 0 or len(lightcurve) <= 5:
            df = pd.DataFrame(columns=self.feature_names)
            df.index.name = 'oid'
            return df

        oid = lightcurve.index.values[0]
        lightcurve = lightcurve.copy()
        if not is_sorted(lightcurve['mjd'].values):
            lightcurve.sort_values('mjd', inplace=True)
            
        lightcurve_array = self.__lightcurve_to_array(lightcurve)
                    
        results = []
        for feature in self.feature_objects:
            try:
                result = feature.fit(lightcurve_array)
            except Exception as e:
                warnings.warn('Exeption when computing turbo-fats feature: '+str(e))
                if feature.is1d():
                    result = np.NaN
                else:
                    result = [np.NaN] * len(feature.get_feature_names())
            if feature.is1d():
                results.append(result)
            else:
                results += result
        results = np.array(results).reshape(1, -1).astype(np.float)
        df = pd.DataFrame(results, columns=self.feature_names, index=[oid])
        df.index.name = 'oid'
        return df
