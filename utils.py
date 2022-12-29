# -*- coding: utf-8 -*-
"""
    File: utils.py
    Author: Pablo Alfaro Saracho
    Description: Utilities
"""

def header(txt: str, width=100, filler='-', align='c'):
    assert align in 'lcr'
    return {'l': txt.ljust, 'c': txt.center, 'r': txt.rjust}[align](width, filler)

if __name__ == '__main__':
    print('Header function example')
    print(header("INPUT"))
    print(header("PROCESSING"))
    print(header("OUTPUT"))
    print(header("PROCESSING",align='l'))
    print(header("OUTPUT",align='r'))
