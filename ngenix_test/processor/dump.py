import os
import re

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from zipfile import ZipFile

from ngenix_test.models import Root
from ngenix_test.processor.base import BaseProcessor
from ngenix_test.serializer import factory

__all__ = ['DumpProcessor']


class DumpProcessor(BaseProcessor):
    name = 'dump'

    def run(self):
        os.makedirs(self.args.output, exist_ok=True)

        executor = ProcessPoolExecutor(max_workers=cpu_count())

        for i in range(self.args.archives):
            filename = os.path.join(self.args.output, "{}.zip".format(i))

            if self.args.async:
                yield self.loop.run_in_executor(
                    executor,
                    self.generate_archive,
                    filename,
                    self.args.roots,
                    self.args.format
                )
            else:
                self.generate_archive(
                    filename,
                    self.args.roots,
                    self.args.format
                )

    @staticmethod
    def generate_archive(filename, roots, format):
        serializer = factory.get(format)

        with ZipFile(filename, 'w') as f:
            for _ in range(roots):
                root = Root.create()

                root_filename = "{}.{}".format(
                    re.sub(r'[/\\:*?"<>|]', '_', str(root)),
                    serializer.name
                )

                f.writestr(root_filename, serializer.serialize(root))
