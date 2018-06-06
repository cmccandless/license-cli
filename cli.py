#!/usr/bin/env python
import argutil
# import argparse
import requests
import requests_cache
import json
import logging
import sys
from itertools import chain

# from rule import (Permissions, Conditions, Limitations)

logger = logging.getLogger()

API_BASE_URL = 'https://licenseapi.herokuapp.com/'
API_LICENSE_URL = API_BASE_URL + 'licenses/'
API_RULES_URL = API_BASE_URL + 'rules'
API_STATUS_URL = API_BASE_URL + 'status/'

requests_cache.install_cache('cli-cache', expire_after=3600)
parser = None


class License(object):
    def __init__(self, json_license):
        self.nickname = None
        for k, v in json_license.items():
            setattr(self, k, v)

    def __str__(self):
        if self.nickname:
            return '{} ({})'.format(self.title, self.nickname)
        return self.title


def get_rules():
    page = requests.get(API_RULES_URL)
    data = json.loads(page.text)
    return data['rules']


@argutil.callable('list')
def list_licenses(opts):
    rules = get_rules()
    if opts.rules:
        for category, subset in rules.items():
            print(category.title())
            for rule in subset:
                if logger.isEnabledFor(logging.DEBUG):
                    print('  {label} ({tag}): {description}'.format(**rule))
                else:
                    print('  {label}: {description}'.format(**rule))
    else:
        page = requests.get(API_LICENSE_URL)
        data = json.loads(page.text)
        licenses = [License(l) for l in data['licenses']]
        for license in licenses:
            print(str(license))


@argutil.callable('status')
def api_status(opts):
    with requests_cache.disabled():
        page = requests.get(API_STATUS_URL)
        print(page.text)


parser = argutil.get_parser()


def get_parser_info(parser):
    opts = {}
    commands = {}
    if parser._positionals and parser._positionals._actions:
        for a in parser._positionals._actions:
            if isinstance(a, argparse._StoreAction) and not a.option_strings:
                if a.choices:
                    def apply_at_leaf(_commands, choices):
                        if _commands:
                            for k in _commands.keys():
                                apply_at_leaf(_commands[k][1], choices)
                        else:
                            for c in choices:
                                _commands[c] = (opts, {})
                    apply_at_leaf(commands, a.choices)
    if parser._optionals and parser._optionals._group_actions:
        for a in parser._optionals._group_actions:
            if a.help == argparse.SUPPRESS:
                continue
            if isinstance(a, argparse._HelpAction):
                continue
            if isinstance(a, argparse._StoreTrueAction):
                for o in a.option_strings:
                    if len(a.option_strings) < 2 or o.startswith('--'):
                        opts[o] = None
            elif isinstance(
                a,
                (argparse._StoreAction, argparse._AppendAction)
            ):
                for o in a.option_strings:
                    if len(a.option_strings) < 2 or o.startswith('--'):
                        opts[o] = a.choices or []
    if not commands and parser._subparsers:
        for a in parser._subparsers._actions:
            if isinstance(a, argparse._SubParsersAction):
                for k, v in a.choices.items():
                    commands[k] = get_parser_info(v)
    return opts, commands


def get_subcommand_parser_info(parser, argv):
    opts, commands = get_parser_info(parser)
    while argv:
        while argv and argv[0] not in commands:
            argv.pop(0)
        if argv:
            opts, commands = commands[argv.pop(0)]
    return opts, commands


def get_valid(parser, argv):
    opts, commands = get_subcommand_parser_info(parser, list(argv))
    if argv and argv[-1].startswith('-'):
        o = argv[-1]
        if opts.get(o, None):
            return opts[o]
    return chain(opts.keys(), commands.keys())


if __name__ == '__main__':
    argv = list(sys.argv[1:])
    if '--debug' in argv:
        logging.basicConfig(level=logging.DEBUG)
        argv = [v for v in argv if v != '--debug']
    if (
        argv and
        '-h' not in argv and
        '--help' not in argv and
        argv[-1].endswith('commands')
    ):
        import argparse
        argv = argv[:-1]
        for v in get_valid(parser, argv):
            print(v)
        sys.exit(0)
    opts = parser.parse_args(argv)
    opts.func(opts)
