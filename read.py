#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from main import *
import cv2 as cv

DEBUG = 0

tloffsety = 305
tloffsetx = 29
cardroffset = 98
cardboffset = 30
cardloffset = 128

spotloffset = 315
spotroffset = 130
spotyoffset = -130

def findimage(template, image=None):
    if image is None:
        image = get_screenshot()
    res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    _, _, _, maxloc = cv.minMaxLoc(res)
    if DEBUG:
        image[maxloc[1], :, :] = 255
        image[:, maxloc[0], :] = 255
        plt.imshow(image[:,:,::-1])
        plt.show()
    return maxloc

def getBoard():
    screenshot = get_screenshot()
    topleft = findimage(cv.imread('images/window.png'), screenshot)
    topleft = [topleft[0] + tloffsetx, topleft[1] + tloffsety]

    cards = {}
    for f in os.listdir('images/cards'):
        cards[f[0]] = cv.imread('images/cards/'+f)

    board = []
    for cardx in range(8):
        col = ''
        for cardy in range(5):
            section = screenshot[topleft[1] + cardboffset * cardy : topleft[1] + cardboffset * (cardy + 1),
                topleft[0] + cardloffset * cardx : topleft[0] + cardloffset * cardx + cardroffset]
            
            best = ''
            bestDiff = 0
            for cname in cards:
                res = cv.matchTemplate(section, cards[cname], cv.TM_CCOEFF_NORMED)
                _, maxval, _, _ = cv.minMaxLoc(res)
                if best == '' or maxval > bestDiff:
                    best = cname
                    bestDiff = maxval
            
            col += best

            if DEBUG:
                plt.subplot(5, 8, cardy*8+cardx+1)
                plt.imshow(section[:,:,::-1])
        board.append(col)

    if DEBUG:
        plt.show()
    
    return board, topleft

def main():
    board, _ = getBoard()
    import solve
    solve.solveGame(board)

if __name__ == '__main__':
    main()
