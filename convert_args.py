#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Input spc file')
parser.add_argument('-d', '--dir', help='Input directory')
parser.add_argument('-o', '--output_format', help='Output format')
args = parser.parse_args()
print args
