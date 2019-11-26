from utils import gamma_encoder, gamma_decoder, delta_encoder, delta_decoder

def gamma_test():
    print("=========================================")
    print("gamma test")
    print("=========================================")
    for num in [10, 20, 50, 100, 10000, 20000]: 
        encode_num = gamma_encoder(num)
        decode_num = gamma_decoder(encode_num)
        print("num : {}\nencode_num : {}\ndecode_num : {}".format(num, encode_num, decode_num))

def delta_test():
    print("=========================================")
    print("delta test")
    print("=========================================")
    for num in [10, 20, 50, 100, 10000, 20000]: 
        encode_num = delta_encoder(num)
        decode_num = delta_decoder(encode_num)
        print("num : {}\nencode_num : {}\ndecode_num : {}".format(num, encode_num, decode_num))

if __name__=='__main__': 
    gamma_test()
    delta_test()



