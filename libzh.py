#!/usr/bin/python

import re
import sqlite3

strip_tone_re = re.compile(r"^([a-z]+)[1-4]?$")

def pinyinize(s, tone_mark=True):
    connection = sqlite3.connect("cedict.db")
    cursor = connection.cursor()

    pinyins = []

    for c in s:
        cursor.execute("SELECT pinyin FROM dict WHERE traditional = ? OR simplified = ?", (c, c))
        row = cursor.fetchone()
        if row is None:
            pinyins.append(c)
        else:
            pinyin = row[0]
            if not tone_mark:
                pinyin = strip_tone_re.match(pinyin).group(1)
            pinyins.append(pinyin)

    connection.close()

    return " ".join(pinyins)
