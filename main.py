# Criptologia - G301
# Cifrado de Feistel
# ___________________________________
# Presentado por: 
# Cristian Leandro Romero
# Cod.20222678026
# Danny Alexander Morales Olaya
# Cod.20222678001
#_____________________________________
def key_expasion(bin_key: str) -> dict:
    list_taps = [11, 13, 14, 16]
    dict_keys = {}
    
    # Number of key
    for i in range(8):
        list_key = []
        
        # Number of rounds
        for j in range(16):
            msb = ""
            lsb = ""
            
            if i == 0 and j == 0:
                msb = "1"
            else:
                # Get position from right to left
                tap1 = bin_key[-list_taps[0]]
                tap2 = bin_key[-list_taps[1]]
                tap3 = bin_key[-list_taps[2]]
                tap4 = bin_key[-list_taps[3]]
                
                # XOR
                xor_result1 = "0" if tap1 == tap2 else "1" 
                xor_result2 = "0" if xor_result1 == tap3 else "1" 
                msb = "0" if xor_result2 == tap4 else "1"
                
            lsb = bin_key[31]
            list_key.append(lsb)
            
            # Move string to the right
            bin_key = msb + bin_key[:-1]
            
        dict_keys[i] = list_key
        
    return dict_keys

def feistel_cipher(bin_msg: str, dict_keys: dict) -> str:
    le_msg = bin_msg[:16] # MSB
    re_msg = bin_msg[-16:] # LSB
    
    # Number of rounds
    for i in range(8):
        key_n = "".join(dict_keys.get(i))
        xor_result1 = "".join(["1" if bit1 != bit2 else "0" for bit1, bit2 in zip(re_msg, key_n)])
        xor_result2 = "".join(["1" if bit1 != bit2 else "0" for bit1, bit2 in zip(le_msg, xor_result1)])
        
        le_msg = re_msg
        re_msg = xor_result2
        
        print(i, le_msg + re_msg)
    
    # Swap positions
    cipher_text = re_msg + le_msg
    
    return cipher_text
        
def feistel_decipher(bin_msg: str, dict_keys: dict) -> str:
    re_msg = bin_msg[:16] # MSB
    le_msg = bin_msg[-16:] # LSB
    
    # Number of rounds
    for cont, i in enumerate(reversed(range(8))):
        key_n = "".join(dict_keys.get(i))
        xor_result1 = "".join(["1" if bit1 != bit2 else "0" for bit1, bit2 in zip(le_msg, key_n)])
        xor_result2 = "".join(["1" if bit1 != bit2 else "0" for bit1, bit2 in zip(re_msg, xor_result1)])
        
        re_msg = le_msg
        le_msg = xor_result2
        
        print(cont, re_msg + le_msg)
    
    # Swap positions
    decipher_text = le_msg + re_msg
    
    return decipher_text
        
if __name__ == "__main__":
    is_running = True
    
    while is_running:
        print("//** CIFRADO FEISTEL **//")
        msg = input("Ingrese el mensaje de 4 caracteres: ")
        key = input("Ingrese la clave de 4 caracteres: ")
        
        if len(msg) == 4 and len(key) == 4:
            bin_msg = ["{0:08b}".format(ord(char)) for char in msg]
            bin_key = ["{0:08b}".format(ord(char)) for char in key]
            
            text_bin_msg = "".join(bin_msg)
            text_bin_key = "".join(bin_key)
            
            print("\n--Valores de entrada--")
            print("Mensaje:", text_bin_msg)
            print("Clave:", text_bin_key)
            
            # Generate key dictionary from the input key
            dict_keys = key_expasion(text_bin_key)
            
            print("\n--Expansión de claves--")
            for key, value in dict_keys.items():
                print(key, "".join(value))
            
            print("\n--Cifrado--")
            cipher_text = feistel_cipher(text_bin_msg, dict_keys)
            print("Binario: " + cipher_text)
            print("Texto:", "".join([chr(int(cipher_text[i:i+8], 2)) for i in range(0, 32, 8)]))
            
            print("\n--Descifrado--")
            decipher_text = feistel_decipher(cipher_text, dict_keys)
            print("Binario: " + decipher_text)
            print("Texto:", "".join([chr(int(decipher_text[i:i+8], 2)) for i in range(0, 32, 8)]))

            is_running = False
            
            