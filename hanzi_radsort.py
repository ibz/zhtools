#!/usr/bin/python

import re

import libzh

def main():
    with file("hanzi.txt") as f:
        chars = re.sub("[\n ]", "", f.read().decode('utf-8'))
    for c in chars[:100]:
        print c, libzh.kangxi_rs(c)

if __name__ == '__main__':
    main()
