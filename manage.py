#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lingvo.settings')
    from django.core.management import execute_from_command_line
    if len(sys.argv) == 1:
        sys.argv.append('runserver')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
