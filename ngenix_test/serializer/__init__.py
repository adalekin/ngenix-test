from ngenix_test.serializer._csv import CSVSerializer
from ngenix_test.serializer._xml import XMLSerializer

__all__ = ['Factory']


class Factory:
    _serializers = {}
    _supported_serializers = (XMLSerializer, CSVSerializer)

    def get(self, serializer_name):
        serializer = self._serializers.get(serializer_name, None)

        if serializer is None:
            serializer = next(filter(lambda s: s.name == serializer_name, self._supported_serializers))()
            self._serializers[serializer_name] = serializer

        return serializer

factory = Factory()
