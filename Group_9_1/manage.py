#!/usr/bin/env python
import os
import sys
from cuckoo import analyse

if __name__ == '__main__':
    analyse.open_movie_file()
    analyse.data_processing()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Group_9.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

