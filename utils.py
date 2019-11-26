import numpy as np
import time

from bitarray import bitarray

def byte_writer(path, content):
    with open(path, 'wb') as f:
        f.write(content)

def byte_reader(path):
    '''
    Args:
        path - string
    Return:
    '''
    with open(path, 'rb') as f: return f.read()

def txt_writer(path,content):
    with open(path, 'w') as f:
        f.write(content)

def txt_reader(path):
    '''
    Args:
        path - string
    Return:
    '''
    with open(path, 'r') as f: return f.read()

def binary_encoder(number, max_size=0):
    '''
    Args:
        number - int
            should be positive
        max_size - int
    Return:
        list
    '''
    binary = list()
    flag = 1 if number<2**max_size else 0

    count = 0
    while True:
        binary.append(number%2)
        number=number//2
        count+=1
        if flag==1 and count==max_size: break
        if flag==0 and number==0: break
    binary.reverse()
    
    return ''.join([str(v) for v in binary])

def gamma_encoder(number):
    '''
    Args:
        number - int
            should be positive
    Return:
        binary - list
    needs to be coded
    '''
    if number==0:return '0'
    idx = 0
    while 2**(idx+1)<=number+1: idx+=1
    return idx*'1'+'0'+binary_encoder(number-2**idx+1, idx)

def delta_encoder(number):
    if number==0:return '0'
    idx = 0
    while 2**(idx+1)<=number+1: idx+=1
    return gamma_encoder(idx)+binary_encoder(number-2**idx+1, idx)

def binary_decoder(codes):
    '''
    decoder for binary_encoder
    '''
    ncode = len(codes)
    var = 1
    number = 0 
    for i in range(ncode):
        number += int(codes[ncode-i-1])*var
        var*=2
    return number

def gamma_decoder(codes):
    ncode = len(codes)
    idx = 0 
    while codes[idx]!='0': idx+=1
    return 2**idx+ binary_decoder(codes[idx+1:])-1 

def delta_decoder(codes):
    ncode = len(codes)
    idx = 0 
    while codes[idx]!='0': idx+=1
    new_idx = 2**idx+ binary_decoder(codes[idx+1:2*idx+1])-1 
    return 2**new_idx+ binary_decoder(codes[2*idx+1:])-1 

def numlist2bitstring(numlist, encoder):
    return ''.join([encoder(num) for num in numlist])

def bitstring2byte(bitstring):
    num_trailing_bits = (8 - (len(bitstring) % 8)) % 8
    bitstring = '1' * num_trailing_bits + '0' * (8 - num_trailing_bits) + bitstring + '0' * num_trailing_bits
    return bitarray(bitstring).tobytes()

def byte2bitstring(byte):
    codes = bitarray(endian='big')
    codes.frombytes(byte)
    ntrail = 0
    for i in range(8):
        if codes[i]==True: ntrail+=1
        else: break
    if ntrail==0: codes = codes[8:]
    else: codes = codes[8:-ntrail] # trimmed code
    return codes 

def bitstring2numlist_delta(bitstring):
    numlist = list()
    L = len(bitstring)
    delta_idx = 0 
    while delta_idx<L:
        unary_value = 0
        while bitstring[delta_idx+unary_value]==True:
            unary_value+=1
        if unary_value==0: 
            numlist.append(0)
            delta_idx+=1

        gamma_string = ''              
        for i in range(delta_idx,delta_idx+2*unary_value+1):
            if bitstring[i]==True: gamma_string+='1'
            else: gamma_string+='0'
        gamma_value = gamma_decoder(gamma_string)

        delta_string = ''
        for i in range(delta_idx,delta_idx+2*unary_value+1+gamma_value):
            if bitstring[i]==True:  delta_string+='1'
            else:delta_string+='0'
        numlist.append(delta_decoder(delta_string))
        delta_idx+= 2*unary_value+1+gamma_value
    return numlist

class MeasureTime(object):
    def __init__(self, key):
        self._key = key

    def __enter__(self):
        self._time = time.time()
        return self

    def __exit__(self, type, value, traceback):
        print('Elapsed time {}: {}'.format(self._key, time.time() - self._time))

