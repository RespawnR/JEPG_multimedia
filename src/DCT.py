# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:05:03 2020

@author: seigann
"""
import numpy as np
import math

def fill(img : np.ndarray):
    '''
    fill matrix 由于将图片按8*8的像素点进行划分，必须将图片补成16的整数倍
    
    Parameters
    ----------
    img : np.ndarray
        opened image.

    Returns
    -------
    filled img by unit 16 * 16
    '''
    height = img.shape[0]
    width = img.shape[1]
    if height % 16 != 0:
        for i in range(16 - height % 16):
            img = np.insert(img, -1, img[height - 1], axis = 0)
    if width % 16 != 0:
        for i in range(16 - width % 16):
            img = np.insert(img, -1, img[:,width - 1,:], axis = 1)
    
    return img
    
def split(part : np.ndarray):
    '''
    Split the image according to 8 * 8 pixels

    Parameters
    ----------
    part : np.ndarray
        y, cr, cb中的某个分量

    Returns
    -------
    blocks : ndarray.

    '''
    height = part.shape[0]
    width = part.shape[1]
    row = height // 8
    col = width // 8
    blocks = []
    for i in range(row):
        start_row = i * 8
        for j in range(col):
            start_col = j * 8
            end_row = start_row + 8
            end_col = start_col + 8
            blocks.append(part[start_row:end_row, start_col:end_col])
    
    return np.array(blocks)

def merge(y_b : np.ndarray, cr_b : np.ndarray, cb_b : np.ndarray, width, height):
    '''
    merge the image from 8 * 8 pixels

    Parameters
    ----------
    y_b:
        
    cr_b:
        
    cb_b:

    Returns
    -------
    y : ndarray.
    cr:
    cb
    
    '''
    # uv_height = (height - 1) // 16 + 1
    uv_width = (width - 1) // 16 + 1
    # y_height = 2 * uv_height
    y_width = 2 * uv_width
    
    count_y = y_b.shape[0]
    count_uv = cr_b.shape[0]
    
    line = y_b[0]
    for i in range(1, y_width):
        line = np.hstack((line, y_b[i]))
    
    y = line.copy()
    for i in range(y_width, count_y):
        if (i + 1) % y_width == 0:
            line = np.hstack((line, y_b[i]))
            y = np.vstack((y, line))
        elif i % y_width == 0:
            line = y_b[i]
        else:
            line = np.hstack((line, y_b[i]))            
    
    line1 = cr_b[0]
    line2 = cb_b[0]
    for i in range(1, uv_width):
        line1 = np.hstack((line1, cr_b[i]))
        line2 = np.hstack((line2, cb_b[i]))    
    cr = line1.copy()
    cb = line2.copy()
    for i in range(uv_width, count_uv):
        if (i + 1) % uv_width == 0:
            line1 = np.hstack((line1, cr_b[i]))
            line2 = np.hstack((line2, cb_b[i]))
            cr = np.vstack((cr, line1))
            cb = np.vstack((cb, line2))
        elif i % uv_width == 0:
            line1 = cr_b[i]
            line2 = cb_b[i]
        else:
            line1 = np.hstack((line1, cr_b[i]))   
            line2 = np.hstack((line2, cb_b[i]))   
    return y, cr, cb

def FDCT(blocks : np.ndarray):
    '''
    Forward DCT（离散余弦变换）正向DCT变换，对一个8 * 8的块

    Parameters
    ----------
    blocks : n * 8 * 8 ndarray

    Returns
    -------
    temp 处理后的块 n * 8 * 8

    '''
    #生成系数矩阵A，并完善
    A = np.zeros([8,8])
    for i in range(8):
        for j in range(8):
            if(i == 0):
                a = math.sqrt(1 / 8)
            else:
                a = math.sqrt(2 / 8)
            A[i][j] = a * math.cos(math.pi * (j + 0.5) * i / 8)
    
    A_T=A.transpose()#矩阵转置
    temp = np.matmul(A, blocks)#矩阵叉乘
    Y = np.matmul(temp, A_T)
    
    return Y

def  IDCT(block : np.ndarray):
    '''
     IDCT（离散余弦变换的逆变换）反向DCT变换，对一个8 * 8的块

    Parameters
    ----------
    block : n * 8 * 8 ndarray

    Returns
    -------
    temp 处理后的块 n * 8 * 8

    '''
    #生成系数矩阵A，并完善
    A = np.zeros([8,8])
    for i in range(8):
        for j in range(8):
            if(i == 0):
                a = math.sqrt(1 / 8)
            else:
                a = math.sqrt(2 / 8)
            A[i][j] = a * math.cos(math.pi * (j + 0.5) * i / 8)
    
    A_T=A.transpose()#矩阵转置
    temp = np.matmul(A_T, block)#矩阵叉乘
    Y = np.matmul(temp, A)
    Y = Y.astype(np.uint8)
    
    return Y
    


# a = np.ones([511,511,3])
# print(a.shape)
# print(fill(a).shape)
# print(split(fill(a)).shape)

