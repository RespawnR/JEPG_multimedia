# -*- coding: utf-8 -*-
"""
对DC系数进行 DPCM差值编码
Created on Wed May  6 14:20:32 2020

@author: seigann
"""

import numpy as np

#由于在copress中存在循环 这里优点多余
def DPCM(blocks : np.ndarray):
    '''
     DPCM（差值编码），对所有8 * 8的块， 当然只对左上角的DC系数

    Parameters
    ----------
    blocks : num * 8 * 8

    Returns
    -------
    temp : list
    处理后DC系数列表

    '''
    num = blocks.shape[0]
    temp = []
    temp.append(blocks[0, 0, 0])
    for i in range(1, num):
        temp.append(blocks[i, 0, 0] - blocks[i-1, 0, 0])
            
    return temp

def reDPCM(arr : list):
    '''
     rDPCM（差值编码），反向，对DC系数列表，求原来的矩阵

    Parameters
    ----------
    arr : list

    Returns
    -------
    blocks : num * 8 * 8
    处理后DC系数列表

    '''
    size = len(arr)
    blocks = np.zeros([size, 8, 8])
    blocks[0, 0, 0] = arr[0]
    for i in range(1, size):
        blocks[i, 0, 0] = arr[i] + blocks[i-1, 0, 0]
    return blocks
