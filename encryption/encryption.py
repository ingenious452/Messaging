"""
Description: Encryption algorithm used to 
shift each character of message by 3.

Author: {^^}
"""



import itertools
from typing import List, Tuple


# Symmetric Encryption
#------------------------------------ROTN-----------------------------
def shift_character(message: str, n: int) -> str:
    """
    Take a message string and return a string
    shifted by 'n' place.
    
    :args message: message string to be encrypted.
    :args n: number of character to shift.
    :return cipher_text: encrypted text.
    """

    encrypted_text = ''
    for char in message.lower():
        encrypted_text += chr((ord(char) - 97 + n) % 26 + 97)   # keep the number in range of 0 to 26 and module of 26 add the extra remainder to 97
    return encrypted_text                                           


def shift_character_back(message: str, n: int) -> str:
    """
    Take a message string and return a string
    shifted by 'n' place.
    
    :args message: message string to be encrypted.
    :args n: number of character to shift.
    :return cipher_text: encrypted text.
    """

    encrypted_text = ''
    for char in message.lower():
        encrypted_text += chr((ord(char) - 97 - n) % 26 + 97)   # keep the number in range of 0 to 26 and module of 26 add the extra remainder to 97
    return encrypted_text   


def shift_brute_force(cipher: str) -> str:
    """
    Take a cipher text which has been encrypted and try
    to brute force to get the plain text.
    
    :args message: cipher text to brute force.
    :return plain_text: plain text string."""

    POSSIBLE_CHARS = 26   # The encrypted message can have only on of 26 possible value.

    for possible_char in range(POSSIBLE_CHARS):
        print(f'Places: {possible_char}, message: {shift_character_back(cipher, possible_char)}')



# Asymmetric encryption
# it uses two keys(public, private)
#---------------------------------------RSA-------------------------------
def is_prime(num: int) -> bool:
    """
    Take a number and return True if the number is
    prime else return Flase.
    
    :args num: number to check for prime.
    :return: boolean True or False.
    """
    for n in range(2, int(num**1/2)+1):
        if num % n == 0:
            return False
    return True


def factors_of(num: int) -> List[int]:
    """
    Take a number an return a list of all it's factors
    
    :args num: integer whose factors to calculate.
    :retun factors: List of factors of the given number.
    """

    factors = []
    for n in range(2, num+1):
        if num % n == 0:
            factors.append(n)
    return factors


def coprime_with(num: int) -> List[int]:
    """
    Take a number calculate all the number coprime with it 
    and return the list.
    
    :args num: Number to check coprime with.
    
    :return coprimes: all the coprime number list.
    """
    coprimes = []
    factors_num = factors_of(num)

    for i in range(1, num+1):
        if not set(factors_of(i)).intersection(factors_num):
            coprimes.append(i)
    return coprimes
    

def encryption_key(prime_product: int, phi: int) -> int:
    """
    Take the prime_product and phi value and calculate e
    by checking the value which is coprime with both prime_product
    and phi.
    
    :args prime_product: The product of two secret prime number.
    :return i or None: The value.
    """

    modulo_factors = set(factors_of(prime_product))
    phi_factor = set(factors_of(phi))

    for i in range(2, phi):
        if not (set(factors_of(i)).intersection(modulo_factors)
        or set(factors_of(i)).intersection(phi_factor)):
            return i
    return None


def decryption_key(e: int, phi: int) -> int:
    """
    Take the encryption key and phi value and calculate d
    by checking the value such that (e * d) % phi == 1
    
    :args prime_product: The product of two secret prime number.
    :return i or None: The decryption-key value.
    """
    
    for i in itertools.count(start=int(phi / e)):
        v = (e * i) % phi
        if v==1: break
    return i


def rsa(message: str, asymmetric_key: Tuple):
    """
    Given a message/cipher respectively encrypt/decrypt the message usign RSA method.
    c = m^e mod prime_product
    m = c^d mod prime_product

    :args message: message to encrypt/decrypt.
    :return cipher: cipher or message encrypted or decrypted using rsa asymmetric keys.
    """
    # c = m^e mod prime_product
    key, prime_product = asymmetric_key 
    char_codes = [ord(char) for char in message]
    # print(cipher_code)
    message = [chr(pow(code, key, prime_product)) for code in char_codes]
    return ''.join(message)


if __name__ == '__main__':
    # always select the number larger. for it to work
    prime_number1, prime_number2 = (5, 89)
    prime_product = prime_number1 * prime_number2  # N modulus
    # phi function is coprime of all the number with prime_product

    phi = (prime_number1 - 1)*(prime_number2 - 1)  # easy way to calculate all the coprime

    # encryption key 
    # choose e where 1 < e < phi
    # coprime with prime_product and phi.
    e_key = encryption_key(prime_product, phi)

    # find decryption key 
    # d = d*emod phi == 1
    d_key = decryption_key(e_key, phi)
    
    print('Key Generation'.center(50, '-'))
    print(f'Prime1: {prime_number1} \nPrime2: {prime_number2}')
    print('Product:', prime_product)
    print(f'Phi: {phi}')
    print('encryption-key:', e_key)
    print('decryption-key:', d_key)

    print()

    print('Encryption'.center(50, '-'))
    c = rsa_encryption('Money is very important', (e_key, prime_product))
    print('Cipher:', c)
    m = rsa_decryption(c, (d_key, prime_product))
    print('Message:', m)
