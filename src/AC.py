# -*- coding: utf-8 -*-
"""
对AC系数 进行Z扫描，并进行游程编码（RLE）
Created on Wed May  6 15:21:10 2020

@author: super
"""
import numpy as np

def ZScan(block : np.ndarray):
    '''
    Z 字形扫描

    Parameters
    ----------
    block : 8 * 8
    待扫描的块

    Returns
    -------
    temp : list
    扫描后的结果

    '''
    temp = []
    #对于前 1-8 level
    for level in range(1, 8):
        if level % 2 == 0:
            #偶数level从左向右
            for j in range(level + 1):
                temp.append(block[level - j, j])
        else:
            #奇数level从右向左
            for j in range(level + 1):
                temp.append(block[j, level - j])
                
    
    #对于 8-15 level
    for level in range(8, 15):
        if level % 2 == 0:
            for j in range(level - 7, level - 7 + (15 - level)):
                temp.append(block[level - j, j])
        else:
            for j in range(level - 7, level - 7 + (15 - level)):
                temp.append(block[j, level - j])
                
       
    return temp

def reZScan(arr : list, block : np.ndarray):
    '''
    Z 字形扫描 的逆过程

    Parameters
    ----------
    arr : list
    63位AC系数
    
    block : np.ndarray
    经过DC变换的块 8 * 8
    
    Returns
    -------
    temp : 8 * 8
    结果

    '''
    #对于前 1-8 level
    num = 0
    for level in range(1, 8):
        if level % 2 == 0:
            #偶数level从左向右
            for j in range(level + 1):
                block[level - j, j] = arr[num]
                num = num + 1
        else:
            #奇数level从右向左
            for j in range(level + 1):
                block[j, level - j] = arr[num]
                num = num + 1            
    
    #对于 8-15 level
    for level in range(8, 15):
        if level % 2 == 0:
            for j in range(level - 7, level - 7 + (15 - level)):
                block[level - j, j] = arr[num]
                num = num + 1
        else:
            for j in range(level - 7, level - 7 + (15 - level)):
                block[j, level - j] = arr[num]
                num = num + 1 
                
    return block
    

def RLE(arr : list):
    '''
    RLE 游程编码

    Parameters
    ----------
    arr : list
    AC系数列表

    Returns
    -------
    temp : list
    行程编码结果

    '''
    temp = []
    num_0 = 0
    for i in arr:
        #累计不为0数 前面的0的个数
        if i == 0:
            num_0 += 1
        else:
            temp.append((num_0, i))
            num_0 = 0
    #后面全是0 EOB
    if num_0 != 0:
        temp.append((0, 0))
      
    return temp


def reRLE(temp : list):
    '''
    RLE 游程编码 逆过程

    Parameters
    ----------
    temp : list
    游程编码

    Returns
    -------
    arr : list
    AC系数列表

    '''
    arr = []
    for unit in temp:
        #0的个数；非零的数
        num_0 = unit[0]
        num = unit[1]
        
        #数字部分为0时 即EOB
        if num == 0:
            for i in range(63 - len(arr)):
                arr.append(0)
            return arr
        
        for i in range(num_0):
            arr.append(0)
        arr.append(num)
    
    return arr

