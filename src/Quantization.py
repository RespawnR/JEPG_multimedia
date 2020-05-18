# -*- coding: utf-8 -*-
"""
量化模块
Created on Tue May  5 21:54:24 2020

@author: seigann
"""
import numpy as np

# 亮度量化表
Y_table = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]])

# C量化表
C_table = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]])

def Quan_Y(block : np.ndarray):
    '''
    量化Y
    
    Parameters
    ----------
    block : 
        n * 8 * 8 的像素块

    Returns
    -------
    量化后的数据 : n * 8 * 8
    '''
    #四舍五入，由于np.around 当类似-0.1时会变成-0
    Y = np.around(block / Y_table)
    #所以最后还要在进行判断-0，转换成0
    return np.where(Y != -0, Y, 0).astype(np.int16)

def Quan_C(block : np.ndarray):
    '''
    量化C
    
    Parameters
    ----------
    block : 
        n * 8 * 8 的像素块

    Returns
    -------
    量化后的数据 : n * 8 * 8
    '''
    #四舍五入，由于np.around 当类似-0.1时会变成-0
    Y = np.around(block / C_table)
    #所以最后还要在进行判断-0，转换成0
    return np.where(Y != -0, Y, 0).astype(np.int16)

def reQuan_Y(block : np.ndarray):
    '''
    反量化Y
    
    Parameters
    ----------
    block : 
       n * 8 * 8 的像素块

    Returns
    -------
    反量化后的数据 : n * 8 * 8
    '''
    return block * Y_table

def reQuan_C(block : np.ndarray):
    '''
    反量化Y
    
    Parameters
    ----------
    block : 
        n * 8 * 8 的像素块

    Returns
    -------
    反量化后的数据 : n * 8 * 8
    '''
    return block * C_table
