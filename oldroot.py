import requests

def vigenere_decrypt(ciphertext, key):
    plaintext = []
    key = key.upper()
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            plaintext.append(decrypted)
            key_index += 1
        else:
            plaintext.append(char)
    return ''.join(plaintext)

def recursive_vigenere_decrypt(ciphertext, key, times=3):
    result = ciphertext
    for _ in range(times):
        result = vigenere_decrypt(result, key)
    return result

def is_imgur_link_valid(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error checking URL: {e}")
        return False

if __name__ == '__main__':
    ciphertext = "GEETt7v"
    possible_keys = []

    results = []

    for key in possible_keys:
        cleaned_key = ''.join(filter(str.isalpha, key)).upper()
        decrypted = recursive_vigenere_decrypt(ciphertext, cleaned_key)
        isvalid = True
        if not is_imgur_link_valid(f"i.imgur.com/{decrypted}"):
            isvalid = False
        results.append({
            'key': key,
            'decrypted_text': decrypted,
            'valid_imgur': isvalid
        })

    for result in results:
        print(f"Key: {result['key']} -> Decrypted Text: {result['decrypted_text']} Is Valid Link: {result['valid_imgur']}")
