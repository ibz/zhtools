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
