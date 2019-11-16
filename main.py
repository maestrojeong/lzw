from utils import txt_reader 
import sys

# =============================================================== #

def genalphabet2():
    alpha_dict = list()
    for i in range(ord('a'), ord('d')+1):
        alpha_dict.append(chr(i))
    return alpha_dict

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
    return alpha_dict

alpha_dict = genalphabet()
#alpha_dict = genalphabet2()
print(alpha_dict)

class Trie(object):
    def __init__(self):
        self.children = {}
        self.val = None
    def trace(self, key):
        if key not in self.children.keys():
            self.generate()
        if self.children[key].val is None:
            return True, self.children[key], self.val
        else:
            return False, self.children[key], self.val
    def generate(self):
        for alpha in alpha_dict:
            self.children[alpha] = Trie()

    def setval(self, val):
        self.val = val

# =============================================================== #
path = 'ex2.txt'
input_string = txt_reader(path)[:-1]
print(input_string)

def encode(input_string):
    L = len(input_string)
    root = Trie()
    root.generate()
    genval = 0
    for alpha in alpha_dict:
        genval+=1
        root.children[alpha].setval(genval)

    endflag = False
    tmp = root

    encode_list = list()
    idx = 0
    while idx<L:
        curchar = input_string[idx]
        #print("idx : {}, curchar : {}".format(idx, curchar))
        if curchar not in alpha_dict:
            print("Unvalid key")
            break
        endflag, tmp, curval = tmp.trace(curchar)
        #print("endflag : {}, curval : {}, tmpval : {}".format(endflag, curval, tmp.val))
        if endflag:
            genval+=1
            tmp.setval(genval)
            tmp = root
            encode_list.append(curval)
        else:
            if idx==L-1:
                encode_list.append(tmp.val)
                break
            idx+=1
    return encode_list
encode_list = encode(input_string)
print(encode_list)

def decode(encode_list):
    decode_dict = dict()
    genval = 0
    for alpha in alpha_dict:
        genval+=1
        decode_dict[genval] = alpha
    
    L = len(encode_list)

    string = ''
    for idx in range(L):
        val = encode_list[idx]
        tmp = decode_dict[val]
        #print("idx : {}, val : {}, tmp : {}".format(idx, val, tmp))
        string += tmp 
        if idx<L-1:
            genval+=1
            decode_dict[genval] = tmp + decode_dict[encode_list[idx+1]][0]
    return string

string = decode(encode_list)
print(string)






