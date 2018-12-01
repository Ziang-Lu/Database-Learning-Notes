#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of sqlite3 libray.
"""

__author__ = 'Ziang Lu'

import sqlite3

# Assume there is a table called 'Cookies'
with sqlite3.connect('Cookies') as conn:
    cursor = conn.cursor()
    cursor.execute(
        '''
        select host_key
        from cookies
        limit 10
        '''
    )
    results = cursor.fetchall()
    print(results)
