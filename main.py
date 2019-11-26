from utils import txt_reader, txt_writer,\
                  delta_encoder, delta_decoder,\
                  numlist2bitstring, bitstring2byte, byte2bitstring,\
                  bitstring2numlist_delta, byte_writer, byte_reader
import sys

# =============================================================== #
def genalphabet():
    alpha_dict = list()
    for i in range(ord('a'), ord('z')+1):
        alpha_dict.append(chr(i))
    for i in range(ord('A'), ord('Z')+1):
        alpha_dict.append(chr(i))
    for i in range(ord('0'), ord('9')+1):
        alpha_dict.append(chr(i))
    alpha_dict.append(',')
    alpha_dict.append('.')
    alpha_dict.append(':')
    alpha_dict.append(';')
    alpha_dict.append('?')
    alpha_dict.append('!')
    alpha_dict.append('\n')
    alpha_dict.append(' ')
    alpha_dict.append('\r')
    alpha_dict.append('\t')
    return alpha_dict

class Trie(object):
    def __init__(self, alphabet):
        self.children = {}
        self.alphabet = alphabet
        self.val = None
    def trace(self, key):
        if key not in self.children.keys():
            self.generate()
        if self.children[key].val is None:
            return True, self.children[key], self.val
        else:
            return False, self.children[key], self.val
    def generate(self):
        for alpha in self.alphabet:
            self.children[alpha] = Trie(self.alphabet)

    def setval(self, val):
        self.val = val
# =============================================================== #
def encode_wrapper(inputpath, outputpath, alphabet):
    input_byte = byte_reader(inputpath)
    input_string = input_byte.decode('ascii')
    def encode(input_string):
        L = len(input_string)
        root = Trie(alphabet) # build structure
        root.generate()
        genval = 0

        for alpha in alphabet: # Add alphabet in dictionary in Trie Structure
            genval+=1
            root.children[alpha].setval(genval)

        endflag = False
        tmp = root

        encode_list = list()
        idx = 0
        while idx<L:
            curchar = input_string[idx]
            if curchar not in alphabet:
                print("Unvalid key")
                break
            endflag, tmp, curval = tmp.trace(curchar) # With the curchar, trace down the trie structure
            if endflag:
                genval+=1
                tmp.setval(genval) # If it reaches the leaf node, add with the last char in the trie
                tmp = root
                encode_list.append(curval) # Encode the leaf node  
            else:
                if idx==L-1:
                    encode_list.append(tmp.val) # Only consider the last case
                    break
                idx+=1
        return encode_list
    encode_list = encode(input_string)
    encode_bitstring = numlist2bitstring(numlist=encode_list, encoder=delta_encoder)
    encode_byte = bitstring2byte(encode_bitstring)
    byte_writer(path=outputpath, content=encode_byte)
# =============================================================== #
def decode_wrapper(inputpath, outputpath, alphabet):
    encode_byte = byte_reader(path=inputpath)
    def decode(encode_list):
        decode_dict = dict()
        genval = 0
        for alpha in alphabet: # Add alphabet in dictionary
            genval+=1
            decode_dict[genval] = alpha
        
        L = len(encode_list)

        string = ''
        for idx in range(L):
            val = encode_list[idx]
            tmp = decode_dict[val]
            string += tmp 
            if idx<L-1: # When decode a number into alphabet, add to the decoder dictionary
                genval+=1
                if encode_list[idx+1] == genval:
                    decode_dict[genval] = tmp + tmp[0]
                else:
                    decode_dict[genval] = tmp + decode_dict[encode_list[idx+1]][0]
        return string
    decode_bitstring = byte2bitstring(encode_byte)
    decode_numlist = bitstring2numlist_delta(decode_bitstring)
    decode_string = decode(decode_numlist).encode('ascii')
    byte_writer(path=outputpath, content=decode_string)
# =============================================================== #
