import abc
import os
from typing import NamedTuple
from pprint import pprint
from pymongo.collection import Collection
from db_plugins.db.mongo import MongoConnection
from db_plugins.db.mongo.models import Object, Detection, NonDetection
from db_plugins.db.mongo.helpers.update_probs import (
    create_or_update_probabilities_bulk,
)
from mongo_scribe.command.exceptions import NonExistentCollectionException
from mongo_scribe.db.factories.update_probability import UpdateProbabilitiesOperation

models_dictionary = {
    "object": Object,
    "detection": Detection,
    "non_detection": NonDetection,
}


class Classifier(NamedTuple):
    classifier_name: str
    classifier_version: str


class ScribeCollection(abc.ABC):
    @abc.abstractmethod
    def insert_many(self, inserts, ordered=False):
        ...

    @abc.abstractmethod
    def bulk_write(self, updates):
        ...

    @abc.abstractmethod
    def update_probabilities(self, operation: UpdateProbabilitiesOperation):
        ...


class ScribeCollectionMock(ScribeCollection):
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def insert_many(self, inserts, ordered=False):
        print(f"Inserting into {self.collection_name}:")
        pprint(inserts)

    def bulk_write(self, updates):
        print(f"Bulk writing into {self.collection_name}:")
        pprint(updates)

    def update_probabilities(self, operation: UpdateProbabilitiesOperation):
        print("Updating probabilities")
        pprint({
            "updates": operation.updates,
            "classifier": operation.classifier
        })


class ScribeCollectionMongo(ScribeCollection):
    def __init__(self, connection: MongoConnection, collection_name):
        try:
            db_model = models_dictionary[collection_name]
            self.connection = connection
            self.collection: Collection = connection.query(db_model).collection
        except KeyError as exc:
            raise NonExistentCollectionException from exc

    def insert_many(self, inserts, ordered=False):
        if len(inserts) > 0:
            self.collection.insert_many(inserts, ordered=ordered)

    def bulk_write(self, updates):
        if len(updates) > 0:
            self.collection.bulk_write(updates)

    def update_probabilities(self, operation: UpdateProbabilitiesOperation):
        classifier = operation.classifier
        update_data = operation.updates
        if len(update_data) > 0:
            aids, probabilities = map(list, zip(*update_data))

            create_or_update_probabilities_bulk(
                self.collection,
                classifier=classifier.classifier_name,
                version=classifier.classifier_version,
                aids=aids,
                probabilities=probabilities
            )


def get_model_collection(
    connection: MongoConnection, model_name: str
) -> ScribeCollection:
    """
    Returns the collection based on a model name string.
    Raises NonExistantCollection if the model name doesn't exist.
    """
    if os.getenv("MOCK_DB_COLLECTION", "False") == "True":
        return ScribeCollectionMock(model_name)

    return ScribeCollectionMongo(connection, model_name)
