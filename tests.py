"""
Some functions used for testing functionality.
"""

__author__ = 'Alex Alkire'
__version__ = '0.1'
__license__ = 'MIT'
import os


def getMissingList():
    filelist = list()
    for filename in os.listdir('images'):
        print("A:", filename[:-4])
        try:
            a = int(filename[:-4])
            filelist.append(a)
        except:
            pass
    out = []
    print(filelist)
    for i in range(0,1024):
        if i not in filelist:
            out.append(i)
    print("missing:",  out)
    return out