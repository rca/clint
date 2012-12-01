"""
Command Object.

Provides a superclass for easily creating command line tools.  This includes a
logging object with a console handler that intelligently sends output to stdout
or stderr depending on the log level and argument parsing using the optparse
module.
"""
from __future__ import absolute_import

import logging
import re

from argparse import ArgumentParser

from clint.logging.handlers import ConsoleHandler

USAGE_REGEX = r'^\n*([\w\W\s\n]+?)\n+$'


class Command(object):
    def __init__(self, doc=None):
        self.parser = ArgumentParser(description=re.sub(USAGE_REGEX, r'\1', doc or self.__class__.__doc__))
        self._fill_parser()

        self.args = self.parser.parse_args()

        self.logger = None

        self._setup_logger()

    def _fill_parser(self):
        p = self.parser

        p.add_argument('-l', '--loglevel', default='info',
                       help='Set log level, default info')

    def _setup_logger(self):
        # setup the root logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = ConsoleHandler()
        ch.setLevel(getattr(logging, self.args.loglevel.upper()))
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.logger.addHandler(ch)

    def quit(self):
        pass

    def run(self):
        print 'define the run method in your subclass'
