#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of sqlite3 libray (driver).
"""

import psycopg2

# Fake table: 'bears'
with psycopg2.connect('dbname=bears') as conn:
    pass
