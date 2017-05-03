#!/usr/bin/env python2
# -*- coding: utf-8

import os
import locale
locale.setlocale(locale.LC_ALL,'')
code = locale.getpreferredencoding()

names = ['background','foreground']
for i in range(0,16):
    names.append('color'+str(i).encode(code))

with open(os.path.expanduser('~/.Xresources'),'r') as f:
    xr = f.read()

colors = []

xr = xr.split('\n')
for line in xr:
    for name in names:
        if line.find(name) > -1:
            bi = line.find(name)
            bi = line[bi:].find('#')+bi
            colors.append(line[bi:bi+7]+'ff')

