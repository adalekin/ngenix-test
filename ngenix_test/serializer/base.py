class BaseSerializer:
    name = ''

    def serialize(self, obj):
        raise NotImplementedError

    def deserialize(self, s):
        raise NotImplementedError
