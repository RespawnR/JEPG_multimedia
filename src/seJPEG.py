# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:05:06 2020

@author: seigann
"""
import numpy as np
# from PIL import Image
import RGB2YCrCb
import DCT
import Quantization
import DC
import AC
from coding import Coding


def compress(img : np.ndarray, flag = True):
    '''
    输入压缩图像 n * m * 3 (bgr)格式
    返回压缩后的数据流
    
    Parameters
    ----------
    img : np.ndarray
        图像数据
    
    Returns
    -------
    bits : string
        压缩后的比特流
    
    '''
    
    bits = ''
    '''
    1.色彩空间的转换
    色彩空间转换，由BGR -> YCRCB
    这里为了方便 把图像填补为16的倍数
    '''
    #1.1 fill 图像
    img = DCT.fill(img)
    #-------------------------------------------------------------------------
    if flag:
        tips = 'compress:\nfill img.shape : \t' + repr(img.shape)
        print(tips)
    #1.2 色彩空间转换
    y, cr, cb = RGB2YCrCb.bgr2ycrcb(img)
    #-------------------------------------------------------------------------
    if flag:
        tips = 'RGB2YCrCb y|cr|cb.shape : \t' \
            + repr(y.shape) + repr(cr.shape) + repr(cb.shape)
        print(tips)
    
    '''
    2.FDCT变换
    DCT变换
    这里利用了 numpy的特性，利用矩阵的广播叉乘，点除 进行DCT变换及量化
    '''
    #2.1 分割像素块
    y_blocks = DCT.split(y)
    cr_blocks = DCT.split(cr)
    cb_blocks = DCT.split(cb)
    #-------------------------------------------------------------------------
    if flag:
        tips = 'split y|cr|cb.shape : \t' \
            + repr(y_blocks.shape) + repr(cr_blocks.shape) + repr(cb_blocks.shape)
        print(tips)
    #2.2 对每个像素块进行DCT变换
    y_dct = DCT.FDCT(y_blocks)
    cr_dct = DCT.FDCT(cr_blocks)
    cb_dct = DCT.FDCT(cb_blocks)
    #-------------------------------------------------------------------------
    if flag:
        tips = 'FDCT y|cr|cb.shape : \t' \
            + repr(y_dct.shape) + repr(cr_dct.shape) + repr(cb_dct.shape)
        print(tips)
        
    
    '''
    3.量化
    由于以下的操作不再 利用矩阵的运算 故使用循环
    '''
    y_quan = Quantization.Quan_Y(y_dct)
    cr_quan = Quantization.Quan_C(cr_dct)
    cb_quan = Quantization.Quan_C(cb_dct)
    #-------------------------------------------------------------------------
    if flag:
        tips = 'Quan y|cr|cb.shape : \t' \
            + repr(y_quan.shape) + repr(cr_quan.shape) + repr(cb_quan.shape)
        print(tips)
    
    
    '''
    4.ZSCAN RLE DPCM
    '''
    y_acs_rle = []
    cr_acs_rle = []
    cb_acs_rle = []
    y_dcs = []
    cr_dcs = []
    cb_dcs = []
    count_y = y_quan.shape[0]
    count_uv = cr_quan.shape[0]
    #对每个像素块进行DPCM; ZSCAN, RLE
    for i in range(count_y):
        temp = AC.ZScan(y_quan[i])
        y_ac_rle = AC.RLE(temp)
        y_acs_rle.append(y_ac_rle)
        if i == 0:
            y_dcs.append(y_quan[i][0][0])
        else:
            y_dcs.append(y_quan[i][0][0] - y_quan[i-1, 0, 0])
    for i in range(count_uv):
        tempcr = AC.ZScan(cr_quan[i])
        tempcb = AC.ZScan(cb_quan[i])
        cr_ac_rle = AC.RLE(tempcr)
        cb_ac_rle = AC.RLE(tempcb)
        cr_acs_rle.append(cr_ac_rle)
        cb_acs_rle.append(cb_ac_rle)
        if i == 0:
            cr_dcs.append(cr_quan[i][0][0])
            cb_dcs.append(cb_quan[i][0][0])
        else:
            cr_dcs.append(cr_quan[i][0][0] - cr_quan[i-1, 0, 0])
            cb_dcs.append(cb_quan[i][0][0] - cb_quan[i-1, 0, 0])

    '''
    5.Huffman编码
    按照y,cr,cb的顺序进行
    '''
    code = Coding()
    for i in range(count_y):
        y_bits = code.Huffman_Y(y_dcs[i], y_acs_rle[i])
        bits += y_bits
    for i in range(count_uv):
        cr_bits = code.Huffman_C(cr_dcs[i], cr_acs_rle[i])
        bits += cr_bits
    for i in range(count_uv):
        cb_bits = code.Huffman_C(cb_dcs[i], cb_acs_rle[i])
        bits += cb_bits 
    
    return bits

def decompress(bits, witdh, height):
    '''
    根据比特流数据，和原图像的宽高，进行解码，得到原图像 n * m * 3 （bgr）形式
    
    Parameters
    ----------
    bits : string
        压缩后的比特流
    
    Returns
    -------
    img : np.ndarray
        图像数据
    
    '''
    
    '''
    1.Huffman编码的逆过程
    '''
    code = Coding()
    y_dcs, cr_dcs, cb_dcs, y_acs_rle, cr_acs_rle, cb_acs_rle \
        = code.decodeing(bits, height, witdh)
    '''
    2.反向ZSCAN,RLE,DPCM
        2.1 反向DPCM
        2.2 反向RLE, ZScan
    '''
    count_y = len(y_dcs)
    count_uv = len(cr_dcs)
    #2.1 反向DPCM
    y_quan = DC.reDPCM(y_dcs)
    cr_quan = DC.reDPCM(cr_dcs)
    cb_quan = DC.reDPCM(cb_dcs)
    #2.2 反向RLE, ZScan
    for i in range(count_y):
        AC.reZScan(AC.reRLE(y_acs_rle[i]), y_quan[i])
    for i in range(count_uv):
        AC.reZScan(AC.reRLE(cr_acs_rle[i]), cr_quan[i])
        AC.reZScan(AC.reRLE(cb_acs_rle[i]), cb_quan[i])
    '''
    3.去量化
    '''
    y_dct = Quantization.reQuan_Y(y_quan)
    cr_dct = Quantization.reQuan_C(cr_quan)
    cb_dct = Quantization.reQuan_C(cb_quan)
    '''
    4.IDCT
    '''
    y_b = DCT.IDCT(y_dct)
    cr_b = DCT.IDCT(cr_dct)
    cb_b = DCT.IDCT(cb_dct)
    '''
    5.结合像素块，返回原大小
    '''
    y, cr, cb = DCT.merge(y_b, cr_b, cb_b, witdh, height)
    '''
    6.色彩空间转换
    '''
    img_ = RGB2YCrCb.ycrcb2bgr(y, cr, cb)
    
    return img_

