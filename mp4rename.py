import datetime
import logging

import pytz as pytz
import os
import re
import sys
from pymediainfo import MediaInfo

logger = logging.getLogger("mp4rename")


def do_rename(filename):
    tagged_date = get_tagged_date(filename=filename)
    if tagged_date:
        extension = re.search('\.([a-zA-Z0-9]+)$', filename).groups()[0].lower()
        tagged_date_local = tagged_date.astimezone(tz=pytz.timezone('Europe/Brussels'))
        new_filename = format_filename(timestamp=tagged_date_local, extension=extension)
        new_abs_filename = os.path.abspath(os.path.join(filename, os.pardir, new_filename))
        if filename != new_filename:
            logger.info(filename, '->', new_filename)
            os.rename(filename, new_abs_filename)
        else:
            logger.info(filename, ' (not changed)')
    else:
        raise RuntimeError('Could not determine tagged date for {}'.format(filename))


def get_tagged_date(filename):
    media_info = MediaInfo.parse(filename=filename)
    for track in media_info.tracks:
        if hasattr(track, 'tagged_date'):
            return parse_date_string(track.tagged_date)
    return None


def parse_date_string(value):
    return datetime.datetime.strptime(value, "UTC %Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone('UTC'))


def format_filename(timestamp, fmt='%Y%m%d_%H%M%S', extension='mp4'):
    return '{name}.{extension}'.format(
        name=datetime.datetime.strftime(timestamp, fmt),
        extension=extension,
    )


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        do_rename(filename)
