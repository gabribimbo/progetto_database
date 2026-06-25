#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Gabriele
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pulizie_service.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
