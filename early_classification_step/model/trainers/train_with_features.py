import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_PATH)
from models.classifiers.deepHits_with_features_entropy_reg import (
    DeepHiTSWithFeaturesEntropyReg,
)
from models.classifiers.deepHits_entopy_reg_model import DeepHiTSEntropyRegModel
from trainers.base_trainer import Trainer
from parameters import param_keys, general_keys

if __name__ == "__main__":
    N_TRAINS = 10
    data_path = os.path.join(PROJECT_PATH, "../pickles", "training_set_May-06-2020.pkl")
    # data_path = "../../pickles/converted_data.pkl"

    n_classes = 5
    params = {
        param_keys.RESULTS_FOLDER_NAME: "chinr_sharpnr_ecliptic_galactic",
        param_keys.DATA_PATH_TRAIN: data_path,
        param_keys.WAIT_FIRST_EPOCH: False,
        param_keys.N_INPUT_CHANNELS: 3,
        param_keys.CHANNELS_TO_USE: [0, 1, 2],
        param_keys.TRAIN_ITERATIONS_HORIZON: 30000,
        param_keys.TRAIN_HORIZON_INCREMENT: 10000,
        param_keys.TEST_SIZE: n_classes * 100,
        param_keys.VAL_SIZE: n_classes * 100,
        param_keys.NANS_TO: 0,
        param_keys.NUMBER_OF_CLASSES: n_classes,
        param_keys.CROP_SIZE: 21,
        param_keys.INPUT_IMAGE_SIZE: 21,
        param_keys.VALIDATION_MONITOR: general_keys.LOSS,
        param_keys.VALIDATION_MODE: general_keys.MIN,
        param_keys.ENTROPY_REG_BETA: 0.5,
        param_keys.LEARNING_RATE: 1e-4,
        param_keys.DROP_RATE: 0.5,
        param_keys.BATCH_SIZE: 32,
        param_keys.KERNEL_SIZE: 3,
        param_keys.FEATURES_NAMES_LIST: [
            "sgscore1",
            "distpsnr1",
            "sgscore2",
            "distpsnr2",
            "sgscore3",
            "distpsnr3",
            "isdiffpos",
            "fwhm",
            "magpsf",
            "sigmapsf",
            "ra",
            "dec",
            "diffmaglim",
            "rb",
            "distnr",
            "magnr",
            "classtar",
            "ranr",
            "decnr",
            "ndethist",
            "ncovhist",
            "ecl_lat",
            "ecl_long",
            "gal_lat",
            "gal_long",
        ],
    }
    trainer = Trainer(params)

    trainer.train_model_n_times(
        DeepHiTSWithFeaturesEntropyReg,
        params,
        train_times=N_TRAINS,
        model_name="DeepHitsFeatures",
    )

    params.update({param_keys.FEATURES_NAMES_LIST: None})

    trainer.train_model_n_times(
        DeepHiTSEntropyRegModel,
        params,
        train_times=N_TRAINS,
        model_name="DeepHitsEntropyRegBeta%.4f" % params[param_keys.ENTROPY_REG_BETA],
    )

    trainer.print_all_accuracies()
