import argparse
import asyncio
import logging
from timeit import Timer

import sys

from ngenix_test.processor import factory

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


def payload(_args):
    loop = asyncio.get_event_loop()

    processor = factory.get(_args.subparser, _args, loop)
    feature = asyncio.gather(*processor.run(), loop=loop)

    try:
        loop.run_until_complete(feature)
    except KeyboardInterrupt:
        logger.info('Performing cleanup...')
        if feature:
            feature.cancel()
            loop.run_until_complete(feature)
    finally:
        logger.info('Exit')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--async',
        default=False,
        action='store_true',
        help='use an async processing model'
    )
    subparsers = parser.add_subparsers(dest='subparser')
    parser_dump = subparsers.add_parser('dump')
    parser_dump.add_argument(
        '--output',
        help='an output directory where zip files are stored'
    )
    parser_dump.add_argument(
        '--format',
        default='xml',
        help='a report format (ex. xml, json, yaml and etc)'
    )
    parser_dump.add_argument(
        '--archives',
        type=int,
        default=50,
        help='a number of archives in the output directory'
    )
    parser_dump.add_argument(
        '--roots',
        type=int,
        default=100,
        help='a number of roots in the archive'
    )

    parser_report = subparsers.add_parser('report')
    parser_report.add_argument(
        '--input',
        help='an input directory where zip files are stored'
    )
    parser_report.add_argument(
        '--output',
        help='an output directory where report files are stored'
    )
    parser_report.add_argument(
        '--format',
        default='xml',
        help='a report format (ex. xml, json, yaml and etc)'
    )
    args = parser.parse_args()

    t = Timer(stmt=lambda: payload(args), setup='gc.enable()')
    logger.debug("{secs:.{prec}g} secs".format(secs=t.timeit(number=1), prec=2))

if __name__ == '__main__':
    main()
