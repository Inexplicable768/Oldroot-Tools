import string, requests
from itertools import product

cipher_text = "GEETt7v"
key1_candidates = ["LIGHT", "HOUSE", "POE", "LIGHTHOUSE", "EDGAR", "ALLEN", "ALLAN", "WESTER", "UNKNOWN", "UNTOLD", "UNREAD", "RAVEN", "UNFINISHED", "GEETt7v", "THELIGHTHOUSE", "EDGARALLANPOE", "EDGARALLENPOE"]
key2_candidates = ["LIGHT", "HOUSE", "POE", "LIGHTHOUSE", "EDGAR", "ALLEN", "ALLAN", "WESTER", "UNKNOWN", "UNTOLD", "UNREAD", "RAVEN", "UNFINISHED", "GEETt7v", "THELIGHTHOUSE", "EDGARALLANPOE", "EDGARALLENPOE"]

def create_vigenere_cube():
    alphabet = string.ascii_uppercase
    cube = {}
    for depth_index, depth_char in enumerate(alphabet):
        table = []
        for i in range(26):
            shifted = alphabet[i:] + alphabet[:i]
            shifted = shifted[depth_index:] + shifted[:depth_index]  # Apply depth shift
            table.append(shifted)
        cube[depth_char] = table
    return cube

def decrypt_char(cipher_char, layer_char, key_char, cube):
    alphabet = string.ascii_uppercase
    upper_char = cipher_char.upper()
    if upper_char not in alphabet:
        return cipher_char
    layer = cube[layer_char]
    row = alphabet.index(key_char)
    column = layer[row].index(upper_char)
    decrypted_char = alphabet[column]
    return decrypted_char.lower() if cipher_char.islower() else decrypted_char

def decrypt_message(ciphertext, key1, key2, cube):
    alphabet = string.ascii_uppercase
    key1 = key1.upper()
    key2 = key2.upper()
    plaintext = []
    for i, char in enumerate(ciphertext):
        if char.upper() not in alphabet:
            plaintext.append(char)
            continue
        layer_char = key1[i % len(key1)]
        key_char = key2[i % len(key2)]
        decrypted = decrypt_char(char, layer_char, key_char, cube)
        plaintext.append(decrypted)
    return ''.join(plaintext)

def try_all_key_combinations(ciphertext, key1_list, key2_list):
    cube = create_vigenere_cube()
    results = []
    for key1, key2 in product(key1_list, key2_list):
        decrypted = decrypt_message(ciphertext, key1, key2, cube)
        results.append((key1, key2, decrypted))
    return results

def isValidLink(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def print_all(onlyifvalid=False, output_file="output_results.txt"):
    print("Calculating Possibilities... Stand By")
    results = try_all_key_combinations(cipher_text, key1_candidates, key2_candidates)
    with open(output_file, "w", encoding="utf-8") as f:
        for key1, key2, decrypted in results:
            isval = isValidLink(f"https://imgur.com/{decrypted}")
            line = f"Key1: {key1} | Key2: {key2} => Decrypted: {decrypted} Is Valid Link: {isval}\n"
            if not onlyifvalid or (onlyifvalid and isval):
                f.write(line)
    print(f"Results written to {output_file}")

print_all()
