#!/usr/bin/env python
import os
import sys

import hacks
hacks.setup_hack_for_ora_12704_errors_on_bulk_create()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dueling_decimals.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
