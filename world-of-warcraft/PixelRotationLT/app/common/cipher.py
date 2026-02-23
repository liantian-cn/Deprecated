# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import json
import random
import string
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

__all__ = ['bytes_decrypt', 'bytes_encrypt', 'string_decrypt', 'string_encrypt', 'obj2file', 'file2obj',
           'encrypt2file_s', 'decrypt2file_s', 'encrypt2file_b', 'decrypt2file_b']

SALT_LENGTH = 8
SALT_CHARS = string.ascii_letters + string.digits

# key_file = Path(sys.argv[0])
# key_file_hash = sha3_512(key_file.read_bytes()).digest()
# AES_KEY = key_file_hash[:32]
AES_KEY = b'&\tw\x8a\xdd\xe1@\x80\x8af\xd7\x07\xd3\x98\x93\x93W\xc8N\xf7\x10\xe3\x89=\xeb\xb2\xbcg\xf4\x7f(\xb6'


def get_random_string(length: int = 32, chars: str = SALT_CHARS) -> str:
    return ''.join(random.choice(chars) for i in range(length))


def prepare_the_str(key: str) -> str:
    # 如果key不是block_size的整数倍，则补齐
    while len(key) % AES.block_size != 0:
        key += '\0'
    return key


def prepare_the_bytes(key: bytes) -> bytes:
    # 如果key不是block_size的整数倍，则补齐
    while len(key) % AES.block_size != 0:
        key += b'\0'
    return key


def prepare_b64_decode(encrypted_str: str) -> str:
    # 为base64解密的字符串补齐=
    missing_padding = 4 - len(encrypted_str) % 4
    if missing_padding:
        encrypted_str += '=' * missing_padding
    return encrypted_str


def bytes_encrypt(plain_bytes: bytes) -> bytes:
    nonce = get_random_bytes(12)
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.encrypt(plain_bytes) + nonce


def bytes_decrypt(encrypted_bytes: bytes) -> bytes:
    nonce = encrypted_bytes[-12:]
    encrypted_bytes = encrypted_bytes[:-12]
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt(encrypted_bytes)


def string_encrypt(plain_str: str) -> str:
    # 先将文字补足长度，转换为bytes
    plain_str = prepare_the_str(plain_str)
    plain_bytes = plain_str.encode()
    encrypted_bytes = bytes_encrypt(plain_bytes)
    encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes)
    encrypted_str = str(encrypted_b64, encoding='utf-8').strip().replace('=', '')
    return encrypted_str


def string_decrypt(encrypted_str: str) -> str:
    encrypted_str = prepare_b64_decode(encrypted_str)
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_str.encode(encoding='utf-8'))
    plain_bytes = bytes_decrypt(encrypted_bytes)
    plain_str = str(plain_bytes, encoding='utf-8').replace('\0', '')
    return plain_str


def encrypt2file_s(plain: str, file_path: Path) -> int:
    header = b'u:'
    plain_b = plain.encode('utf-8')
    return file_path.write_bytes(header + bytes_encrypt(plain_b))


def decrypt2file_s(file_path: Path) -> str:
    file_bytes = file_path.read_bytes()
    encrypted_bytes = file_bytes[len(b'u:'):]
    plain_bytes = bytes_decrypt(encrypted_bytes)
    return plain_bytes.decode('utf-8')


def encrypt2file_b(plain: bytes, file_path: Path) -> int:
    header = b'b:'
    return file_path.write_bytes(header + bytes_encrypt(plain))


def decrypt2file_b(file_path: Path) -> bytes:
    file_bytes = file_path.read_bytes()
    encrypted_bytes = file_bytes[len(b'b:'):]
    plain_bytes = bytes_decrypt(encrypted_bytes)
    return plain_bytes


def obj2file(obj, file_path: Path) -> int:
    return encrypt2file_s(json.dumps(obj), file_path)


def file2obj(file_path: Path):
    return json.loads(decrypt2file_s(file_path))
