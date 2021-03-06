# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:21:23 2020

@author: seigann
"""
class Coding:
    
    def __init__(self):
        self.DC_Y2 = {value: key for key, value in self.DC_Y.items()}
        self.DC_UV2 = {value: key for key, value in self.DC_UV.items()}
        self.AC_Y2 = {value: key for key, value in self.AC_Y.items()}
        self.AC_UV2 = {value: key for key, value in self.AC_UV.items()}
    
    
    def VLI(self, num):
        '''
        变长整数编码
    
        Parameters
        ----------
        num : int
        待转换的整数
    
        Returns
        -------
        [len, str] : list
        转换后的结果
    
        '''
        num = int(num)
        #如果是0不做处理, 返回len 0, str ''
        if num == 0:
            return [0, '']
        
        #bin() 将返回int或long的二进制表示
        s = bin(abs(num)).replace('0b', '') #去掉前缀 0b
        #对于负数 用正数编码的反码表示
        if num < 0:
            s2 = ''
            for c in s:
                #if表达式为真，放前面的，假后面的
                s2 += '0' if c == '1' else '1'
            return [len(s2), s2]
        #对于正数
        else:
            return [len(s), s]
    
    
    def reVLI(self, b):
        '''
        变长整数编码的逆过程
    
        Parameters
        ----------
        b : str
        二进制字符串
    
        Returns
        -------
        num : int
        转换后的结果
    
        '''
        s = ''
        #负数情况
        if b[0] == '0':
            #先反码 表示回来 再加-号即可
            for c in b:
                s += '0' if c == '1' else '1'
            #int(x, base = 10)
            #x -- 字符串或数字。
            #base -- 进制数，默认十进制。
            return -int(s, 2)
        else:
            s += b
            return int(s, 2)
    
    
    def Huffman_Y(self, dc, ac_rle):
        '''
        (将 runlength 和 size 合并 + VLI变长编码)并根据相应的huffmanTable 转换成 01比特流
        （对一个 8 * 8的块处理 一个dc,一个ac_rle列表）
        
        Parameters
        ----------
        dc : int
        该处理块的DC系数
        
        ac_rle : list
        该处理块的AC系数 的 行程编码
    
        Returns
        -------
        bits : str
        二进制比特流
    
        '''
        bits = ''
        #处理dc 即+ 前面部分的huffman编码 + 后面的VLI
        dc = self.VLI(dc)
        bits += self.DC_Y[dc[0]] + dc[1]
        #处理ac
        for e in ac_rle:
            runlength = e[0]
            value = e[1]
            temp = self.VLI(value)   #转换成VLI
            
            while runlength > 15:
                runlength -= 15
                bits += self.AC_Y[(15, 0)]
                
            bits += self.AC_Y[(runlength, temp[0])] #前两部分
            bits += temp[1] #VLI编码
        return bits
        
        
        
    
    
    def Huffman_C(self, dc, ac_rle):
        '''
        (将 runlength 和 size 合并 + VLI变长编码)并根据相应的huffmanTable 转换成 01比特流
        （对一个 8 * 8的块处理 一个DC,一个rle）
        
        Parameters
        ----------
        dc : int
        该处理块的DC系数
        
        ac_rle : list
        该处理块的AC系数 的 行程编码
    
        Returns
        -------
        bits : str
        二进制比特流
    
        '''
        bits = ''
        #处理dc 即+ 前面部分的huffman编码 + 后面的VLI
        dc = self.VLI(dc)
        bits += self.DC_UV[dc[0]] + dc[1]
        #处理ac
        for e in ac_rle:
            runlength = e[0]
            value = e[1]
            temp = self.VLI(value)   #转换成VLI
            
            while runlength > 15:
                runlength -= 15
                bits += self.AC_UV[(15, 0)]
                
            bits += self.AC_UV[(runlength, temp[0])] #前两部分
            bits += temp[1] #VLI编码
        return bits
    
    
    def decodeing(self, bits, width, height):
        '''
        根据比特流数据，和原图像的宽高，进行解码，得到 dc 和 rle数据
        
        Parameters
        ----------
        bits : str
        二进制比特流
        
        width : int
        图像的宽
    
        height : int
        图像的高
        
        Returns
        -------
        dcs_y : list
        dcs_cr: list
        dcs_cb: list
        acs_rle_y: list
        acs_rle_cr: list
        acs_rle_cb: list
        
        '''
        uv_height = (height - 1) // 16 + 1
        uv_width = (width - 1) // 16 + 1
        y_height = 2 * uv_height
        y_width = 2 * uv_width
        #dc list
        dcs_y = []
        dcs_cr = []
        dcs_cb = []
        acs_rle_y = []
        acs_rle_cr = []
        acs_rle_cb = []
        #扫描指针
        p_head = 0
        p_tail = 1
        
        #解析Y分量
        while(len(acs_rle_y) < y_height * y_width):
            #找到dc并加入dcs_y
            while(bits[p_head : p_tail] not in self.DC_Y2.keys()):
                p_tail += 1
            #解析dc size
            size = self.DC_Y2[bits[p_head : p_tail]]
            p_head = p_tail
            p_tail += size
            #解析dc
            if size == 0:
                amplitude = 0
            else:
                amplitude = self.reVLI(bits[p_head : p_tail])
            dcs_y.append(amplitude)
            p_head = p_tail
            p_tail += 1
            
            #解析63个ac
            length = 0
            ac_rle_y = []
            while True:
                while(bits[p_head : p_tail] not in self.AC_Y2.keys()):
                    p_tail += 1
                #解析ac runlength, size
                temp = self.AC_Y2[bits[p_head : p_tail]]
                
                if temp == (15, 0):
                    ac_rle_y.append((15,0))
                    length += 15
                elif temp == (0, 0):
                    ac_rle_y.append((0,0))
                    p_head = p_tail
                    p_tail += 1
                    break
                else:
                    runlength = temp[0]
                    size = temp[1]
                    p_head = p_tail
                    p_tail += size
                    amplitude = self.reVLI(bits[p_head : p_tail])
                    ac_rle_y.append((runlength, amplitude))
                    length += runlength
                    length += 1
                p_head = p_tail
                p_tail += 1
                # print(ac_rle_y)
                if(length >= 63):
                    break        
            acs_rle_y.append(ac_rle_y)
        
        # #解析Cr分量
        while(len(acs_rle_cr) < uv_height * uv_width):
            #找到dc并加入dcs_y
            while(bits[p_head : p_tail] not in self.DC_UV2.keys()):
                p_tail += 1
            #解析dc size
            size = self.DC_UV2[bits[p_head : p_tail]]
            p_head = p_tail
            p_tail += size
            #解析dc
            if size == 0:
                amplitude = 0
            else:
                amplitude = self.reVLI(bits[p_head : p_tail])
            dcs_cr.append(amplitude)
            p_head = p_tail
            p_tail += 1
            
            #解析63个ac
            length = 0
            ac_rle_cr = []
            while True:
                while(bits[p_head : p_tail] not in self.AC_UV2.keys()):
                    p_tail += 1
                #解析ac runlength, size
                temp = self.AC_UV2[bits[p_head : p_tail]]
                
                if temp == (15, 0):
                    ac_rle_cr.append((15,0))
                    length += 15
                elif temp == (0, 0):
                    ac_rle_cr.append((0,0))
                    p_head = p_tail
                    p_tail += 1
                    break
                else:
                    runlength = temp[0]
                    size = temp[1]
                    p_head = p_tail
                    p_tail += size
                    amplitude = self.reVLI(bits[p_head : p_tail])
                    ac_rle_cr.append((runlength, amplitude))
                    length += runlength
                    length += 1
                p_head = p_tail
                p_tail += 1
                # print(ac_rle_cr)
                if(length >= 63):
                    break        
            acs_rle_cr.append(ac_rle_cr)
        
        #解析cb
        while(len(acs_rle_cb) < uv_height * uv_width):
            #找到dc并加入dcs_y
            while(bits[p_head : p_tail] not in self.DC_UV2.keys()):
                p_tail += 1
            #解析dc size
            size = self.DC_UV2[bits[p_head : p_tail]]
            p_head = p_tail
            p_tail += size
            #解析dc
            if size == 0:
                amplitude = 0
            else:
                amplitude = self.reVLI(bits[p_head : p_tail])
            dcs_cb.append(amplitude)
            p_head = p_tail
            p_tail += 1
            
            #解析63个ac
            length = 0
            ac_rle_cb = []
            while True:
                while(bits[p_head : p_tail] not in self.AC_UV2.keys()):
                    p_tail += 1
                #解析ac runlength, size
                temp = self.AC_UV2[bits[p_head : p_tail]]
                
                if temp == (15, 0):
                    ac_rle_cb.append((15,0))
                    length += 15
                elif temp == (0, 0):
                    ac_rle_cb.append((0,0))
                    p_head = p_tail
                    p_tail += 1
                    break
                else:
                    runlength = temp[0]
                    size = temp[1]
                    p_head = p_tail
                    p_tail += size
                    amplitude = self.reVLI(bits[p_head : p_tail])
                    ac_rle_cb.append((runlength, amplitude))
                    length += runlength
                    length += 1
                p_head = p_tail
                p_tail += 1
                # print(ac_rle_cb)
                if(length >= 63):
                    break        
            acs_rle_cb.append(ac_rle_cb)
        
    
        return dcs_y, dcs_cr, dcs_cb, acs_rle_y, acs_rle_cr, acs_rle_cb
    
    '''
    以下分别是  JPEG 标准推荐的亮度、色度DC、AC Huffman 编码表 
    '''
    DC_Y = {
        0: '00',
        1: '010',
        2: '011',
        3: '100',
        4: '101',
        5: '110',
        6: '1110',
        7: '11110',
        8: '111110',
        9: '1111110',
        10: '11111110',
        11: '111111110'
    }
    
    DC_UV = {
        0: '00',
        1: '01',
        2: '10',
        3: '110',
        4: '1110',
        5: '11110',
        6: '111110',
        7: '1111110',
        8: '11111110',
        9: '111111110',
        10: '1111111110',
        11: '11111111110'
    }
    
    AC_Y = {
        (0, 0): '1010',
        (0, 1): '00',
        (0, 2): '01',
        (0, 3): '100',
        (0, 4): '1011',
        (0, 5): '11010',
        (0, 6): '1111000',
        (0, 7): '11111000',
        (0, 8): '1111110110',
        (0, 9): '1111111110000010',
        (0, 10): '1111111110000011',
        (1, 1): '1100',
        (1, 2): '11011',
        (1, 3): '1111001',
        (1, 4): '111110110',
        (1, 5): '11111110110',
        (1, 6): '1111111110000100',
        (1, 7): '1111111110000101',
        (1, 8): '1111111110000110',
        (1, 9): '1111111110000111',
        (1, 10): '1111111110001000',
        (2, 1): '11100',
        (2, 2): '11111001',
        (2, 3): '1111110111',
        (2, 4): '111111110100',
        (2, 5): '1111111110001001',
        (2, 6): '1111111110001010',
        (2, 7): '1111111110001011',
        (2, 8): '1111111110001100',
        (2, 9): '1111111110001101',
        (2, 10): '1111111110001110',
        (3, 1): '111010',
        (3, 2): '111110111',
        (3, 3): '111111110101',
        (3, 4): '1111111110001111',
        (3, 5): '1111111110010000',
        (3, 6): '1111111110010001',
        (3, 7): '1111111110010010',
        (3, 8): '1111111110010011',
        (3, 9): '1111111110010100',
        (3, 10): '1111111110010101',
        (4, 1): '111011',
        (4, 2): '1111111000',
        (4, 3): '1111111110010110',
        (4, 4): '1111111110010111',
        (4, 5): '1111111110011000',
        (4, 6): '1111111110011001',
        (4, 7): '1111111110011010',
        (4, 8): '1111111110011011',
        (4, 9): '1111111110011100',
        (4, 10): '1111111110011101',
        (5, 1): '1111010',
        (5, 2): '11111110111',
        (5, 3): '1111111110011110',
        (5, 4): '1111111110011111',
        (5, 5): '1111111110100000',
        (5, 6): '1111111110100001',
        (5, 7): '1111111110100010',
        (5, 8): '1111111110100011',
        (5, 9): '1111111110100100',
        (5, 10): '1111111110100101',
        (6, 1): '1111011',
        (6, 2): '111111110110',
        (6, 3): '1111111110100110',
        (6, 4): '1111111110100111',
        (6, 5): '1111111110101000',
        (6, 6): '1111111110101001',
        (6, 7): '1111111110101010',
        (6, 8): '1111111110101011',
        (6, 9): '1111111110101100',
        (6, 10): '1111111110101101',
        (7, 1): '11111010',
        (7, 2): '111111110111',
        (7, 3): '1111111110101110',
        (7, 4): '1111111110101111',
        (7, 5): '1111111110110000',
        (7, 6): '1111111110110001',
        (7, 7): '1111111110110010',
        (7, 8): '1111111110110011',
        (7, 9): '1111111110110100',
        (7, 10): '1111111110110101',
        (8, 1): '111111000',
        (8, 2): '111111111000000',
        (8, 3): '1111111110110110',
        (8, 4): '1111111110110111',
        (8, 5): '1111111110111000',
        (8, 6): '1111111110111001',
        (8, 7): '1111111110111010',
        (8, 8): '1111111110111011',
        (8, 9): '1111111110111100',
        (8, 10): '1111111110111101',
        (9, 1): '111111001',
        (9, 2): '1111111110111110',
        (9, 3): '1111111110111111',
        (9, 4): '1111111111000000',
        (9, 5): '1111111111000001',
        (9, 6): '1111111111000010',
        (9, 7): '1111111111000011',
        (9, 8): '1111111111000100',
        (9, 9): '1111111111000101',
        (9, 10): '1111111111000110',
        (10, 1): '111111010',
        (10, 2): '1111111111000111',
        (10, 3): '1111111111001000',
        (10, 4): '1111111111001001',
        (10, 5): '1111111111001010',
        (10, 6): '1111111111001011',
        (10, 7): '1111111111001100',
        (10, 8): '1111111111001101',
        (10, 9): '1111111111001110',
        (10, 10): '1111111111001111',
        (11, 1): '1111111001',
        (11, 2): '1111111111010000',
        (11, 3): '1111111111010001',
        (11, 4): '1111111111010010',
        (11, 5): '1111111111010011',
        (11, 6): '1111111111010100',
        (11, 7): '1111111111010101',
        (11, 8): '1111111111010110',
        (11, 9): '1111111111010111',
        (11, 10): '1111111111011000',
        (12, 1): '1111111010',
        (12, 2): '1111111111011001',
        (12, 3): '1111111111011010',
        (12, 4): '1111111111011011',
        (12, 5): '1111111111011100',
        (12, 6): '1111111111011101',
        (12, 7): '1111111111011110',
        (12, 8): '1111111111011111',
        (12, 9): '1111111111100000',
        (12, 10): '1111111111100001',
        (13, 1): '11111111000',
        (13, 2): '1111111111100010',
        (13, 3): '1111111111100011',
        (13, 4): '1111111111100100',
        (13, 5): '1111111111100101',
        (13, 6): '1111111111100110',
        (13, 7): '1111111111100111',
        (13, 8): '1111111111101000',
        (13, 9): '1111111111101001',
        (13, 10): '1111111111101010',
        (14, 1): '1111111111101011',
        (14, 2): '1111111111101100',
        (14, 3): '1111111111101101',
        (14, 4): '1111111111101110',
        (14, 5): '1111111111101111',
        (14, 6): '1111111111110000',
        (14, 7): '1111111111110001',
        (14, 8): '1111111111110010',
        (14, 9): '1111111111110011',
        (14, 10): '1111111111110100',
        (15, 0): '11111111001',
        (15, 1): '1111111111110101',
        (15, 2): '1111111111110110',
        (15, 3): '1111111111110111',
        (15, 4): '1111111111111000',
        (15, 5): '1111111111111001',
        (15, 6): '1111111111111010',
        (15, 7): '1111111111111011',
        (15, 8): '1111111111111100',
        (15, 9): '1111111111111101',
        (15, 10): '1111111111111110',
    }
    
    AC_UV = {
        (0, 0): '00',
        (0, 1): '01',
        (0, 2): '100',
        (0, 3): '1010',
        (0, 4): '11000',
        (0, 5): '11001',
        (0, 6): '111000',
        (0, 7): '1111000',
        (0, 8): '111110100',
        (0, 9): '1111110110',
        (0, 10): '111111110100',
        (1, 1): '1011',
        (1, 2): '111001',
        (1, 3): '11110110',
        (1, 4): '111110101',
        (1, 5): '11111110110',
        (1, 6): '111111110101',
        (1, 7): '1111111110001000',
        (1, 8): '1111111110001001',
        (1, 9): '1111111110001010',
        (1, 10): '1111111110001011',
        (2, 1): '11010',
        (2, 2): '11110111',
        (2, 3): '1111110111',
        (2, 4): '111111110110',
        (2, 5): '111111111000010',
        (2, 6): '1111111110001100',
        (2, 7): '1111111110001101',
        (2, 8): '1111111110001110',
        (2, 9): '1111111110001111',
        (2, 10): '1111111110010000',
        (3, 1): '11011',
        (3, 2): '11111000',
        (3, 3): '1111111000',
        (3, 4): '111111110111',
        (3, 5): '1111111110010001',
        (3, 6): '1111111110010010',
        (3, 7): '1111111110010011',
        (3, 8): '1111111110010100',
        (3, 9): '1111111110010101',
        (3, 10): '1111111110010110',
        (4, 1): '111010',
        (4, 2): '111110110',
        (4, 3): '1111111110010111',
        (4, 4): '1111111110011000',
        (4, 5): '1111111110011001',
        (4, 6): '1111111110011010',
        (4, 7): '1111111110011011',
        (4, 8): '1111111110011100',
        (4, 9): '1111111110011101',
        (4, 10): '1111111110011110',
        (5, 1): '111011',
        (5, 2): '1111111001',
        (5, 3): '1111111110011111',
        (5, 4): '1111111110100000',
        (5, 5): '1111111110100001',
        (5, 6): '1111111110100010',
        (5, 7): '1111111110100011',
        (5, 8): '1111111110100100',
        (5, 9): '1111111110100101',
        (5, 10): '1111111110100110',
        (6, 1): '1111001',
        (6, 2): '11111110111',
        (6, 3): '1111111110100111',
        (6, 4): '1111111110101000',
        (6, 5): '1111111110101001',
        (6, 6): '1111111110101010',
        (6, 7): '1111111110101011',
        (6, 8): '1111111110101100',
        (6, 9): '1111111110101101',
        (6, 10): '1111111110101110',
        (7, 1): '1111010',
        (7, 2): '11111111000',
        (7, 3): '1111111110101111',
        (7, 4): '1111111110110000',
        (7, 5): '1111111110110001',
        (7, 6): '1111111110110010',
        (7, 7): '1111111110110011',
        (7, 8): '1111111110110100',
        (7, 9): '1111111110110101',
        (7, 10): '1111111110110110',
        (8, 1): '11111001',
        (8, 2): '1111111110110111',
        (8, 3): '1111111110111000',
        (8, 4): '1111111110111001',
        (8, 5): '1111111110111010',
        (8, 6): '1111111110111011',
        (8, 7): '1111111110111100',
        (8, 8): '1111111110111101',
        (8, 9): '1111111110111110',
        (8, 10): '1111111110111111',
        (9, 1): '111110111',
        (9, 2): '1111111111000000',
        (9, 3): '1111111111000001',
        (9, 4): '1111111111000010',
        (9, 5): '1111111111000011',
        (9, 6): '1111111111000100',
        (9, 7): '1111111111000101',
        (9, 8): '1111111111000110',
        (9, 9): '1111111111000111',
        (9, 10): '1111111111001000',
        (10, 1): '111111000',
        (10, 2): '1111111111001001',
        (10, 3): '1111111111001010',
        (10, 4): '1111111111001011',
        (10, 5): '1111111111001100',
        (10, 6): '1111111111001101',
        (10, 7): '1111111111001110',
        (10, 8): '1111111111001111',
        (10, 9): '1111111111010000',
        (10, 10): '1111111111010001',
        (11, 1): '111111001',
        (11, 2): '1111111111010010',
        (11, 3): '1111111111010011',
        (11, 4): '1111111111010100',
        (11, 5): '1111111111010101',
        (11, 6): '1111111111010110',
        (11, 7): '1111111111010111',
        (11, 8): '1111111111011000',
        (11, 9): '1111111111011001',
        (11, 10): '1111111111011010',
        (12, 1): '111111010',
        (12, 2): '1111111111011011',
        (12, 3): '1111111111011100',
        (12, 4): '1111111111011101',
        (12, 5): '1111111111011110',
        (12, 6): '1111111111011111',
        (12, 7): '1111111111100000',
        (12, 8): '1111111111100001',
        (12, 9): '1111111111100010',
        (12, 10): '1111111111100011',
        (13, 1): '11111111001',
        (13, 2): '1111111111100100',
        (13, 3): '1111111111100101',
        (13, 4): '1111111111100110',
        (13, 5): '1111111111100111',
        (13, 6): '1111111111101000',
        (13, 7): '1111111111101001',
        (13, 8): '1111111111101010',
        (13, 9): '1111111111101011',
        (13, 10): '1111111111101100',
        (14, 1): '11111111100000',
        (14, 2): '1111111111101101',
        (14, 3): '1111111111101110',
        (14, 4): '1111111111101111',
        (14, 5): '1111111111110000',
        (14, 6): '1111111111110001',
        (14, 7): '1111111111110010',
        (14, 8): '1111111111110011',
        (14, 9): '1111111111110100',
        (14, 10): '1111111111110101',
        (15, 0): '1111111010',
        (15, 1): '111111111000011',
        (15, 2): '1111111111110110',
        (15, 3): '1111111111110111',
        (15, 4): '1111111111111000',
        (15, 5): '1111111111111001',
        (15, 6): '1111111111111010',
        (15, 7): '1111111111111011',
        (15, 8): '1111111111111100',
        (15, 9): '1111111111111101',
        (15, 10): '1111111111111110',
    }
