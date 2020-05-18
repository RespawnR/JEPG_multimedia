# -*- coding: utf-8 -*-
"""
Created on Mon May  4 22:14:41 2020

@author: seigann
"""
import cv2
import numpy as np

def bgr2ycrcb(img):
    '''
    Convert RGB24 to YCrCb, 在这里我们用YUV420来表示。
    每个点保存一个Y值，每4个点保存一个Cr，Cb值
    
    Parameters
    ----------
    img : 
        opened image.
    width : 
        image width.
    height : 
        image height.

    Returns
    -------
    Y 2维.
    Cr 2维.
    Cb 2维.
    '''
    #这里的比重是按照BGR顺序
    y_prop = np.array([0.1140, 0.587, 0.299])
    cb_prop = np.array([0.5000, -0.3313, -0.1687])
    cr_prop = np.array([-0.0813, -0.4187, 0.5000])
    #每四个像素点 取一个cr,cb YUV420
    bgr = img[::2, ::2, :]
    #矩阵乘法
    y = np.dot(img, y_prop)
    cb = np.dot(bgr, cb_prop) + 128
    cr = np.dot(bgr, cr_prop) + 128
    #转换数值类型
    y = y.astype(np.uint8)
    cb = cb.astype(np.uint8)
    cr = cr.astype(np.uint8)
    return y, cr, cb

def ycrcb2bgr(y, cr, cb):
    '''
    Convert YCrCb to RGB24, 在这里我们用bgr来表示。
    YUV420 -> RGB24
    Parameters
    ----------
    y : 2维 
        .
    cr : 2维
        .
    cb : 2维
        .

    Returns
    -------
    img 2维 * 3.
    '''
    height = cr.shape[0]
    width = cr.shape[1]
    #将cr,cb进行扩充
    for i in range(height):
        index = height - i - 1
        cr = np.insert(cr, index, cr[index], axis = 0)
        cb = np.insert(cb, index, cb[index], axis = 0)
    for i in range(width):
        index = width - i - 1
        cr = np.insert(cr, index, cr[...,index], axis = 1)
        cb = np.insert(cb, index, cb[...,index], axis = 1)
    #将图像的长宽进行转置， 保证最后的转置不会将图像颠倒
    cr = cr.T
    cb = cb.T
    y = y.T
    # b = y + 1.772 * (cb - 128)
    # g = y - 0.34414 * (cb - 128) - 0.71414 * (cr - 128)
    # r = y + 1.402 * (cr - 128)
    #将bgr合并成 3 * w * h
    img = np.array((y, cr, cb))
    img = img.astype(np.uint8)
    #返回 h * w * 3
    return cv2.cvtColor(img.T, cv2.COLOR_YCrCb2BGR)
    
