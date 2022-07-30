#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyautogui as guilib
from matplotlib import pyplot as plt
import numpy as np
import mss, os

from pyrsistent import b
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import read, solve

MONITOR = 2

sct = mss.mss()

def get_screenshot(region=None):
    arr = np.array(sct.grab(sct.monitors[MONITOR]))[:,:,:3]
    if region:
        return arr[region[1]:region[3], region[0]:region[2]]
    return arr

def click(x, y):
    m = sct.monitors[MONITOR]
    guilib.click(m['left'] + x, m['top'] + y)

def inputSln(sln, topleft):
    if sln.fromAction is None:
        return

    inputSln(sln.parent, topleft)
    for loc in (sln.fromAction, sln.toAction):
        if loc[0] == 'stack':
            click(topleft[0] + read.cardloffset * loc[1] + read.cardroffset//2,
                topleft[1] + read.cardboffset * loc[2] + read.cardboffset//2)
        
        else:
            click(topleft[0] + read.spotroffset * loc[1] + read.spotloffset, topleft[1] + read.spotyoffset)
    assert(False)

def main():
    guilib.PAUSE = 5
    board, topleft = read.getBoard()
    print(board)
    sln = solve.solveGame(board)
    inputSln(sln, topleft)

if __name__ == '__main__':
    main()
