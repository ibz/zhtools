#!/usr/bin/python

from __future__ import with_statement

import re
import sqlite3
import sys

line_re = re.compile(r"^(.+?) (.+?) \[(.+?)\] /(.+)/$")

def txt2sqlite(f, cursor):
    for i, line in enumerate(f):
        line = line.decode("utf-8").strip()
        if line.startswith("#"):
            continue
        m = line_re.match(line)
        if not m:
            print (u"Invalid line: %s" % line).encode("utf-8")
            continue
        traditional, simplified, pinyin, english = m.groups()
        cursor.execute("INSERT INTO dict (traditional, simplified, pinyin, english) VALUES (?, ?, ?, ?)", (traditional, simplified, pinyin, english))
    print "Lines processed: %s" % (i + 1)

def main():
    filename, dbname = sys.argv[1:3]
    with open(filename, "r") as f:
        connection = sqlite3.connect(dbname)
        try:
            cursor = connection.cursor()
            txt2sqlite(f, cursor)
            connection.commit()
        finally:
            connection.close()

if __name__ == '__main__':
    main()
