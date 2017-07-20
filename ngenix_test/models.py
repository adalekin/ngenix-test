import random
import string


class Root:
    __slots__ = ['id', 'level', 'objects']

    def __str__(self):
        return "{}:{}".format(self.id, self.level)

    @classmethod
    def create(cls):
        obj = cls()
        obj.id = ''.join(
            list(map(lambda _: random.choice(string.ascii_uppercase + string.digits), range(10)))
        )

        obj.level = random.randint(1, 100)

        obj.objects = [
            Object.create() for _ in range(random.randint(1, 10))
        ]

        return obj


class Object:
    __slots__ = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def create(cls):
        name = ''.join(
            list(map(lambda _: random.choice(string.ascii_uppercase + string.digits), range(10)))
        )

        obj = cls()
        obj.name = name

        return obj
