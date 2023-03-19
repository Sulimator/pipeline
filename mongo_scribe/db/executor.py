import os
from typing import List, Dict
from db_plugins.db.mongo import MongoConnection
from db_plugins.db.mongo.models import Object, Detection, NonDetection
from ..command.commands import Command
from ..command.exceptions import NonExistentCollectionException


class ScribeCommandExecutor:
    """
    Class which contains all availible Scribe DB Operations
    """

    allowed = (
        Object.__tablename__,
        Detection.__tablename__,
        NonDetection.__tablename__,
    )

    def __init__(self, config):
        connection = MongoConnection()
        connection.connect(config["MONGO"])
        self.connection = connection

    def _bulk_execute(self, collection_name: str, commands: List[Command]):
        """
        Executes a list of commands obtained from a Kafka topic
        Does nothing when the command list is empty
        """
        if collection_name not in self.allowed:
            raise NonExistentCollectionException()

        operations = []
        for command in commands:
            operations.extend(command.get_operations())

        if os.getenv("MOCK_DB_COLLECTION"):
            print(operations)
        elif operations:
            self.connection.database[collection_name].bulk_write(operations)
        else:
            return
        
    def bulk_execute(self, commands: List[Command]):
        """
        Receives all commands and separates them according to their collection
        """
        commands_per_collection: Dict[str, list] = {}
        for command in commands:
            collection = command.collection
            if collection not in commands_per_collection:
                commands_per_collection[collection] = []
            commands_per_collection[collection].append(command)

        for collection_name, command_list in commands_per_collection.items():
            self._bulk_execute(collection_name, command_list)
            
