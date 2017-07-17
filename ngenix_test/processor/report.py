import glob
import os
import asyncio

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count

from zipfile import ZipFile

from ngenix_test.processor.base import BaseProcessor
from ngenix_test.serializer import factory

__all__ = ['ReportProcessor']


class ReportProcessor(BaseProcessor):
    name = 'report'

    def run(self):
        os.makedirs(self.args.output, exist_ok=True)

        executor = ThreadPoolExecutor()
        queue = asyncio.Queue(loop=self.loop)

        yield self.loop.run_in_executor(
            executor,
            self.read_archive,
            self.args.input,
            self.args.format,
            queue,
            self.loop
        )

        yield asyncio.ensure_future(
            self.report_worker(
                self.args.output, 'csv', queue),
            loop=self.loop
        )

    def read_archive(self, _input, _format, queue, loop=None):
        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            for filename in glob.glob(os.path.join(_input, '*.zip')):
                future = executor.submit(self.read_archive_roots, filename, _format)
                for root in future.result():
                    loop.call_soon_threadsafe(queue.put_nowait, root)
        # Done with queue loop
        loop.call_soon_threadsafe(queue.put_nowait, None)

    @staticmethod
    def read_archive_roots(filename, _format):
        result = []

        serializer = factory.get(_format)

        with ZipFile(filename, 'r') as f:
            for filename_root in f.infolist():
                with f.open(filename_root) as f_root:
                    result.append(serializer.deserialize(f_root.read()))
        return result

    @staticmethod
    async def report_worker(output, _format, queue):
        serializer = factory.get(_format)

        filename_roots = os.path.join(output, "roots.{}".format(_format))
        filename_objects = os.path.join(output, "objects.{}".format(_format))

        with open(filename_roots, 'w') as f_roots:
            with open(filename_objects, 'w') as f_objects:
                while True:
                    root = await queue.get()

                    # If None break the infinite loop
                    if not root:
                        break

                    f_roots.write(serializer.serialize(root) + '\n')

                    for obj in root.objects:
                        f_objects.write(serializer.serialize(obj) + '\n')
