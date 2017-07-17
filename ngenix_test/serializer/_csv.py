from collections import Iterable

from ngenix_test.serializer.base import BaseSerializer


class CSVSerializer(BaseSerializer):
    name = 'csv'

    def serialize(self, obj):
        values = []

        for name in obj.__slots__:
            value = getattr(obj, name)
            if isinstance(value, str) or not isinstance(value, Iterable):
                values.append(str(value))

        return ','.join(values)
