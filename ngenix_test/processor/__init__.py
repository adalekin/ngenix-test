from ngenix_test.processor.dump import DumpProcessor
from ngenix_test.processor.report import ReportProcessor

__all__ = ['Factory']


class Factory:
    _processors = {}
    _supported_processors = (DumpProcessor, ReportProcessor)

    def get(self, processor_name, args, loop=None):
        processor = self._processors.get(processor_name, None)

        if processor is None:
            processor = next(filter(lambda p: p.name == processor_name, self._supported_processors))(args, loop)
            self._processors[processor_name] = processor

        return processor

factory = Factory()
