#!/usr/bin/env python

# Copyright (c) 2009 Ionut Bizau <ionut@bizau.ro>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import sqlite3

strip_tone_re = re.compile(r"^([a-z]+)[1-5]?$")

def pinyinize(s, tone_mark=True):
    if s is None:
        return None
    if s == "":
        return []

    connection = sqlite3.connect("cedict.db")
    cursor = connection.cursor()

    pinyin = []

    for c in s:
        cursor.execute("SELECT pinyin FROM dict WHERE traditional = ? OR simplified = ?", (c, c))
        rows = cursor.fetchall()
        if len(rows) == 0:
            pinyin.append(tuple())
        else:
            pinyin.append(tuple(set(p.lower() if tone_mark else strip_tone_re.match(p.lower()).group(1) for p, in rows)))

    connection.close()

    return pinyin

def kangxi_rs(c):
    connection = sqlite3.connect("unihan.db")
#    connection.text_factory = str
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT radical, additional_strokes FROM kangxi_rs WHERE c = ?", (c,))
        return list(cursor)
    finally:
        connection.close()
