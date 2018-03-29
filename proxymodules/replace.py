#!/usr/bin/env python2

import os
import re


class Module:
    def __init__(self, incoming=False, verbose=False, options=None):
        # extract the file name from __file__. __file__ is proxymodules/name.py
        self.name = __file__.rsplit('/', 1)[1].split('.')[0]
        self.description = 'Replace text on the fly by using regular expressions in a file or as module parameters'
        self.verbose = verbose
        self.search = None
        self.replace = None
        self.filename = None

        if options is not None:
            if 'search' in options.keys():
                self.search = options['search']
            if 'replace' in options.keys():
                self.replace = options['replace']
            if 'file' in options.keys():
                self.filename = options['file']
                try:
                    open(self.filename)
                except IOError as ioe:
                    print "Error opening %s: %s" % (self.filename, ioe.strerror)
                    self.filename = None

    def execute(self, data):
        pairs = []  # list of (search, replace) tuples
        if self.search is not None and self.replace is not None:
            pairs.append((self.search, self.replace))

        if self.filename is not None:
            for line in open(self.filename).readlines():
                # TODO: handle escaping of : character
                try:
                    search, replace = line.split(':', 1)
                    pairs.append((search.strip(), replace.strip()))
                except ValueError:
                    # line does not contain : and will be ignored
                    pass

        old_data = data
        for search, replace in pairs:
            # TODO: verbosity
            data = re.sub(search, replace, data)

        return data

    def help(self):
        h = '\tsearch: string or regular expression to search for\n'
        h += ('\treplace: string the search string should be replaced with\n')
        h += ('\tfile: file containing search:replace pairs, one per line\n')
        h += ('\n\tUse at least file or search and replace (or both).\n')
        return h


if __name__ == '__main__':
    print 'This module is not supposed to be executed alone!'
