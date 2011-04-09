#!/usr/bin/python

import os
import sys
import sqlite3

def load_rs(f, cursor):
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        c, rad_type, rs = line.split("\t")
        if rad_type != "kRSKangXi":
            continue
        c = unichr(int(c.split("+")[1], 16))
        radical, additional_strokes = rs.split(".")
        cursor.execute("INSERT INTO kangxi_rs (c, radical, additional_strokes) VALUES (?, ?, ?)", (c, radical, additional_strokes))

if __name__ == '__main__':
    dirname, dbname = sys.argv[1:3]
    with open(os.path.join(dirname, "Unihan_RadicalStrokeCounts.txt")) as f:
        connection = sqlite3.connect(dbname)
#        connection.text_factory = str
        try:
            cursor = connection.cursor()
            load_rs(f, cursor)
            connection.commit()
        finally:
            connection.close()
