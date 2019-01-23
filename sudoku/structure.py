from sudoku.cell import idx2xy

def xy2block(x, y):
    '''convert an index to a the x-y-coordinate of the 3x3 block (the third neighborhood) of the cell. Possible values are x from 1..3 and y from 1..3'''
    return [((x - 1) // 3) * 3 + 1,((y - 1) // 3) * 3 + 1]

def inc(ia, incr):
    '''create a copy of an int[]. The values of the copy are the original values incremented by a fixed number'''
    iaC = [None] * 9
    for i in range(9):
        iaC[i] = ia[i] + incr
    return iaC

# the horizontal neighbarhoods made of the cells from the 9 rows
H1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
H2 = inc(H1, 9)
H3 = inc(H2, 9)
H4 = inc(H3, 9)
H5 = inc(H4, 9)
H6 = inc(H5, 9)
H7 = inc(H6, 9)
H8 = inc(H7, 9)
H9 = inc(H8, 9)
# the vertical neighbarhoods made of cells from the 9 columns
V1 = [0, 9, 18, 27, 36, 45, 54, 63, 72]
V2 = inc(V1, 1)
V3 = inc(V2, 1)
V4 = inc(V3, 1)
V5 = inc(V4, 1)
V6 = inc(V5, 1)
V7 = inc(V6, 1)
V8 = inc(V7, 1)
V9 = inc(V8, 1)
# the block neighbarhoods made of the cells from the 3x3 "blocks" from left to right, top down
B1 = [0, 1, 2, 9, 10, 11, 18, 19, 20]
B2 = inc(B1, 3)
B3 = inc(B2, 3)
B4 = inc(B1, 27)
B5 = inc(B4, 3)
B6 = inc(B5, 3)
B7 = inc(B1, 54)
B8 = inc(B7, 3)
B9 = inc(B8, 3)
# all horizontal, vertical or block neighbarhoods
ALL_H = [H1, H2, H3, H4, H5, H6, H7, H8, H9]
ALL_V = [V1, V2, V3, V4, V5, V6, V7, V8, V9]
ALL_B = [B1, B2, B3, B4, B5, B6, B7, B8, B9]

# all neighbarhoods
ALL_NEIGHBARHOODS = [H1, H2, H3, H4, H5, H6, H7, H8, H9, V1, V2, V3, V4, V5, V6, V7, V8, V9, B1, B2, B3, B4, B5, B6, B7, B8, B9]

NEIGHBARHOOD_MAPPING = {}
for i in range(81):
    xy = idx2xy(i)
    x = xy[0]
    y = xy[1]
    blockXy = xy2block(x, y)
    g = (blockXy[0] - 1) // 3 + blockXy[1] - 1
    NEIGHBARHOOD_MAPPING[i] = [ALL_H[y - 1], ALL_V[x - 1], ALL_B[g]]

def getNeighborHood(idx):
    '''return the neighbarhoods of a cell as an int[]'''
    return NEIGHBARHOOD_MAPPING.get(idx)

def getAllNeighborhoods():
    '''return all neighbarhoods. Used to validate that all cells from each neighbarhood have different values, for instance'''
    return ALL_NEIGHBARHOODS