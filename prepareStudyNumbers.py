#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance
import pytesseract


threshold = 100
table = []
for i in range(256):
    if i < threshold: table.append(0)
    else: table.append(1)

def initSudokupic(sudokuregion):
    xsize, ysize = sudokuregion.size
    xdelta = xsize / 9
    ydelta = ysize / 9
    sudokupic = []
    for i in range(81):
        x = i % 9
        y = i / 9
        numberregion = (xdelta * x + 20, ydelta * y + 20, xdelta * (x + 1) - 20, ydelta * (y + 1) - 20)
        numberpic = sudokuregion.convert('L').crop((numberregion))
        sudokupic.append(numberpic)
    return sudokupic


if __name__ == '__main__':
    image = Image.open('testmap/all3.png')
    sudokubox = (50, 430, 1190, 1570)
    sudokuregion = image.convert('L').crop(sudokubox).point(table, '1')
    #sudokuregion.show()
    sudokupic = initSudokupic(sudokuregion)
    for i, p in enumerate(sudokupic):
        p.save('numbers/3' + str(i) + '_' + str(i % 9) + '_' + str(i / 9) + '.png')
