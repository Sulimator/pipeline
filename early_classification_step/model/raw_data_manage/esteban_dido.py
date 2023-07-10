import numpy as np
import pandas as pd
import os
import sys
from datetime import date
import random

random.seed(0)
import pickle

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_PATH)

from raw_data_manage.alerce_api import AlerceStamps
from raw_data_manage.add_bogus_class import AddBogus
from raw_data_manage.stamps_from_catalog import StampsFromCatalog

if __name__ == "__main__":
    today = date.today()
    today_str = today.strftime("%b-%d-%Y")

    catalog_path = "../../datasets/dfcrossmatches_prioritized.csv"
    save_path = "../../datasets/dfcrossmatches_avros"
    output_frame = "../../pickles/esteban/pancho_septiembre.pkl"
    taxonomy_dict = {
        "SN": ["SLSN", "SNII", "SNIIb", "SNIIn", "SNIa", "SNIbc"],
        "AGN": ["AGN-I", "Blazar"],
        "VS": [
            "CV/Nova",
            "Ceph",
            "DSCT",
            "EBC",
            "EBSD/D",
            "LPV",
            "Periodic-Other",
            "RRL",
            "ZZ",
        ],
    }
    features_to_add = [
        "sgscore1",
        "distpsnr1",
        "sgscore2",
        "distpsnr2",
        "sgscore3",
        "distpsnr3",
        "isdiffpos",
    ]
    dataset = StampsFromCatalog(
        catalog_path=catalog_path, save_path=save_path, taxonomy_dict=taxonomy_dict
    )

    # dataset.download_avros()
    dataframe = dataset.create_frame(features=features_to_add)

    asteroids_dataframe = pd.read_pickle("../../pickles/training_set_extra_bogus.pkl")
    asteroids_dataframe = asteroids_dataframe[
        asteroids_dataframe["class"] == "asteroid"
    ]

    merged_dataframe = pd.concat(
        [dataframe, asteroids_dataframe], ignore_index=True, axis=0
    )
    pickle.dump(merged_dataframe, open(output_frame, "wb"), protocol=2)
    # print(asteroids_dataframe)

    # Adding bogus class to training set

    bogus_json_path = "/home/rcarrasco/Projects/ZTF_data/broker_bogus.json"
    training_set_path = output_frame
    save_path = os.path.join("../../pickles/esteban/", "bogus_and_features.pkl")

    add_bogus = AddBogus(
        training_set_path=training_set_path,
        bogus_path=bogus_json_path,
        save_path=save_path,
        extra_features=features_to_add,
    )

    add_bogus.json2dataframe()
    add_bogus.append_to_training()
    print(add_bogus.final_frame)
    add_bogus.save_dataframe(overwrite=True)

    data = pd.read_pickle(training_set_path)
    print("n_examples so far", len(data))

    # Adding manually classified bogus using alerce api

    bogus_list = pd.read_hdf("../../../data_analysis/bogus_list_alerce.hdf", key="h")
    bogus_list = bogus_list["ZTF_id"].values
    alerce = AlerceStamps(save_path="../../all_data/data_from_api")
    alerce.download_avros(
        object_ids=bogus_list, file_name="alert_frame_list_alerce_bogus.pkl"
    )
    alerce.create_frame_to_merge(
        frame_class="bogus",
        alerts_list="alert_frame_list_alerce_bogus.pkl",
        features=features_to_add,
    )
    pickle.dump(
        alerce.frame_to_merge,
        open(
            os.path.join("../../pickles/esteban/", "bogus_juliano_franz_pancho.pkl"),
            "wb",
        ),
        protocol=2,
    )
    # alerce.append_to_training(training_set_path)
    # alerce.save_dataframe(overwrite=True)

    bogus_list = pd.read_hdf("../../../data_analysis/bogus_list.hdf", key="h")
    bogus_list = bogus_list["ZTF_id"].values
    alerce = AlerceStamps(save_path="../../all_data/data_from_api")
    alerce.download_avros(
        object_ids=bogus_list, file_name="alert_frame_list_rorro_bogus.pkl"
    )
    alerce.create_frame_to_merge(
        frame_class="bogus",
        alerts_list="alert_frame_list_rorro_bogus.pkl",
        features=features_to_add,
    )
    pickle.dump(
        alerce.frame_to_merge,
        open(os.path.join("../../pickles/esteban/", "bogus_rorro.pkl"), "wb"),
        protocol=2,
    )

    data = pd.read_pickle(training_set_path)
    print("n_examples so far", len(data))
    print(np.unique(data["class"], return_counts=True))
