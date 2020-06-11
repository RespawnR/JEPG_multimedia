# JEPG_multimedia
Design and Implementation of JEPG Image Compression Encoding and Decoding

JPEG图像压缩的编码与解码的设计与实现
---
2017级软件工程 2508程序作业
---

## 1. JPEG图像的压缩与解压缩流程

## 2. 文件结构及说明
共有4大模块，1个主程序:
- RGB2YCrCb.py
- DCT.py
- Quantitation.py
- DC.py, AC.py, coding.py
- seJPEG.py（主）

### RGB2YCrCb.py
功能：色彩空间的转换
- bgr2ycrcb()
- ycrcb2bgr()
### DCT.py
功能：正向离散余弦变换和逆向离散余弦变换
- fill()：补齐图像（本例采用YUV420，故补齐16的整数倍）
- split()：将某一分量（Y或Cr或Cb分量）分割成8 * 8像素块
- merge()：将多个8 * 8像素块合并成Y或Cr或Cb分量
- FDCT()：将某一分量的分割后所有的8 * 8像素块进行FDCT变换
- IDCT()：将去量化后的某一分量的所有像素块进行IDCT变换
### Quantitation.py
功能：量化和去量化
- Quan_Y()：将某一分量的进行FDCT变换后所有像素块根据亮度（Y）量化表进行量化
- Quan_C()：将某一分量的进行FDCT变换后所有像素块根据亮度（UV）量化表进行量化
- reQuan_Y()：去量化
- reQuan_C()：去量化
### DC.py, AC.py, coding.py
功能：熵编码模块
### seJPEG.py
功能：整体模块接口

