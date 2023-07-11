import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_PATH)
from models.classifiers.deepHits_real_bog_nans_norm_crop_stamp_model import (
    DeepHiTSRealBogNanNormCropStampModel,
)
from trainers.base_trainer import Trainer
from parameters import param_keys, general_keys
from modules.data_set_generic import Dataset
from modules.data_loaders.frame_to_input import FrameToInput
import numpy as np
import pandas as pd


def get_dataset_from_name(
    model: DeepHiTSRealBogNanNormCropStampModel, path: str
) -> Dataset:
    params_copy = model.params.copy()
    params_copy.update({param_keys.DATA_PATH_TRAIN: path})
    frame_to_input = FrameToInput(params_copy)
    frame_to_input.dataset_preprocessor.set_pipeline(
        model.dataset_preprocessor.preprocessing_pipeline[:-1]
    )
    return frame_to_input.get_preprocessed_dataset_unsplitted()


def recall_over_specific_class(positive_class_value, predictions, labels):
    Positives = np.sum([labels == positive_class_value])
    TP = np.sum((predictions == labels)[labels == positive_class_value])
    print(Positives)
    print(TP)
    print(TP / Positives)
    return TP / Positives


if __name__ == "__main__":
    data_name = "converted_pancho_septiembre.pkl"
    data_folder = "/home/ereyes/Projects/Thesis/datasets/ALeRCE_data"
    data_path = os.path.join(data_folder, data_name)

    n_classes = 2
    params = {
        param_keys.RESULTS_FOLDER_NAME: "real_bogus",
        param_keys.DATA_PATH_TRAIN: data_path,
        param_keys.WAIT_FIRST_EPOCH: False,
        param_keys.N_INPUT_CHANNELS: 3,
        param_keys.CHANNELS_TO_USE: [0, 1, 2],
        param_keys.TRAIN_ITERATIONS_HORIZON: 10000,
        param_keys.TRAIN_HORIZON_INCREMENT: 10000,
        param_keys.TEST_SIZE: n_classes * 300,
        param_keys.VAL_SIZE: n_classes * 200,
        param_keys.NANS_TO: 0,
        param_keys.NUMBER_OF_CLASSES: n_classes,
        param_keys.CROP_SIZE: 21,
        param_keys.INPUT_IMAGE_SIZE: 21,
        param_keys.VALIDATION_MONITOR: general_keys.LOSS,
        param_keys.VALIDATION_MODE: general_keys.MIN,
        param_keys.ENTROPY_REG_BETA: None,
    }
    trainer = Trainer(params)

    model = DeepHiTSRealBogNanNormCropStampModel(
        params, model_name="Real_Bog_Retrieved"
    )
    train_set, val_set, test_set = model._data_init()
    retrieve_folder = "/home/ereyes/Projects/Thesis/datasets/ALeRCE_data/OD_retieved"
    normal_train = pd.read_pickle(
        os.path.join(retrieve_folder, "train_real_normal_data.pkl")
    )
    outliers = pd.read_pickle(os.path.join(retrieve_folder, "new_od_boguses.pkl"))

    x_train = np.concatenate([normal_train, outliers])
    y_train = np.concatenate([np.ones(len(normal_train)), np.zeros(len(outliers))])

    model.fit(x_train, y_train, test_data=(test_set.data_array, test_set.data_label))
    bogus_data_name = "bogus_juliano_franz_pancho.pkl"
    bogus_path = os.path.join(data_folder, "converted_" + bogus_data_name)
    bogus_dataset = get_dataset_from_name(model, bogus_path)
    print("bogus.shape: ", bogus_dataset.data_array.shape)
    bogus_predictions = model.predict(bogus_dataset.data_array)
    bogus_recall = recall_over_specific_class(
        0, bogus_predictions, np.zeros(len(bogus_predictions))
    )

    real_data_name = "tns_confirmed_sn.pkl"
    real_path = os.path.join(data_folder, "converted_" + real_data_name)
    real_dataset = get_dataset_from_name(model, real_path)
    print("real.shape: ", real_dataset.data_array.shape)
    real_predictions = model.predict(real_dataset.data_array)
    real_recall = recall_over_specific_class(
        1, real_predictions, np.ones(len(real_predictions))
    )

    # trainer.train_model_n_times(DeepHiTSRealBogNanNormCropStampModel, params,
    #                             train_times=1,
    #                             model_name='Real-Bogus')
    #
    # trainer.print_all_accuracies()

"""
Test Metrics: loss 0.120748, accuracy 0.966667
Normalized confusion matrix Acc 0.9667
[[0.97666667 0.02333333]
 [0.04333333 0.95666667]]
Confusion matrix, without normalization Acc 0.9667
[[293   7]
 [ 13 287]]

bogus.shape:  (3370, 21, 21, 3)
3370
3117
0.9249258160237389

real.shape:  (247, 21, 21, 3)
247
213
0.8623481781376519

Process finished with exit code 0

"""
