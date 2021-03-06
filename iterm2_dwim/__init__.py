#!/usr/bin/env python
from contextlib import contextmanager
import os
import subprocess
import sys
import traceback

from iterm2_dwim.editors import emacs
from iterm2_dwim.logger import log
from iterm2_dwim.parsers import get_path_and_line


Editor = emacs.Editor


def notify(exception):
    subprocess.check_call([
        '/usr/local/bin/terminal-notifier',
        '-title', 'iterm2-dwim',
        '-subtitle', exception.__class__.__name__,
        '-message', str(exception),
    ])


@contextmanager
def notification_on_error():
    try:
        yield
    except Exception as ex:
        notify(ex)
        log(traceback.format_exc())
        exit(1)


def main():
    with notification_on_error():
        log('\nsys.argv: %s' % ' '.join(sys.argv))

        path, line = get_path_and_line(*sys.argv[1:])

        log('Got path and line: %s %d' % (path, line))

        Editor(path, line).visit_file()
