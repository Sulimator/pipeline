import abc


class SurveyParser(abc.ABC):
    _source = None

    @abc.abstractmethod
    def parse_message(self, message: dict, extra_fields: bool = False):
        """
        :param message: A single message from an astronomical survey. Typically this corresponds a dict.
        :param extra_fields: Boolean than indicates if the parser get all remained data on a field called 'extra_fields'

        Note that the Creator may also provide some default implementation of the factory method.
        """
        pass

    @abc.abstractmethod
    def get_source(self):
        """
        Note that the Creator may also provide some default implementation of the factory method.
        """
        pass

    @abc.abstractmethod
    def can_parse(self, message: dict) -> bool:
        """
        Note that the Creator may also provide some default implementation of the factory method.
        """
        pass
