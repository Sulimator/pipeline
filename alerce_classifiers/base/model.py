import os.path
from abc import ABC, abstractmethod

import pandas as pd
import wget
import validators

from .mapper import Mapper

class AlerceModel(ABC):
    mapper: Mapper

    def __init__(self, model_path: str, mapper: Mapper = None):
        self.model = None
        self.mapper = mapper
        self._load_model(model_path)

    @abstractmethod
    def _load_model(self, model_path: str) -> None:
        """
        Private method to load your model in memory. For example in torch models, you can use torch.load() for load
        the model.

        :param model_path: string of the path
        :return: None
        """

    # TODO: change input and output type to their DTOs
    @abstractmethod
    def predict(self, data_input: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate the prediction!
        """

    @classmethod
    def download(cls, url: str, download_path: str = "/tmp") -> str:
        """
        Generic method to download a file from url. This method can be used for download model from S3, and after tha
        load the model to memory
        :param url: URL of downloadable file
        :param download_path: Path to store the file
        :return: Local destination path of the file
        """
        if not validators.url(url):
            raise Exception(f"{url} is not a valid url")
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        filename = url.split("/")[-1]
        destination = os.path.join(download_path, filename)
        if not os.path.exists(destination):
            wget.download(url, destination)
        return destination