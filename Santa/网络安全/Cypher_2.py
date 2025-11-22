import random
import math
from typing import Tuple, List


class PublicKeyCrypto:
    """公钥密码算法实现类"""

    @staticmethod
    def mod_exp(b: int, n: int, m: int) -> int:
        """
        模指运算: 计算 b^n mod m
        使用快速幂算法
        """
        result = 1
        base = b % m

        while n > 0:
            if n & 1:  # 如果n是奇数
                result = (result * base) % m
            base = (base * base) % m
            n = n >> 1  # n = n // 2

        return result

    @staticmethod
    def miller_rabin_test(n: int, k: int = 5) -> bool:
        """
        Miller-Rabin素性测试
        n: 待测试数
        k: 测试次数，默认5次
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        # 将n-1写成d*2^r的形式
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        def check_composite(a: int) -> bool:
            """检查是否为合数"""
            x = PublicKeyCrypto.mod_exp(a, d, n)
            if x == 1 or x == n - 1:
                return False
            for _ in range(r - 1):
                x = (x * x) % n
                if x == n - 1:
                    return False
            return True

        # 进行k次测试
        for _ in range(k):
            a = random.randint(2, n - 2)
            if check_composite(a):
                return False
        return True

    @staticmethod
    def generate_large_prime(bits: int = 64) -> int:
        """生成大素数"""
        while True:
            # 生成奇数
            n = random.getrandbits(bits) | 1
            if PublicKeyCrypto.miller_rabin_test(n):
                return n

    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """扩展欧几里得算法"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = PublicKeyCrypto.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """求模逆元"""
        gcd, x, _ = PublicKeyCrypto.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("模逆元不存在")
        return x % m


class LFSR:
    """线性反馈移位寄存器"""

    def __init__(self, seed: int, polynomial: int, length: int = 8):
        """
        seed: 初始种子值
        polynomial: 反馈多项式，用位掩码表示
        length: 寄存器长度
        """
        self.state = seed
        self.polynomial = polynomial
        self.length = length
        self.mask = (1 << length) - 1

    def next_bit(self) -> int:
        """生成下一个随机比特"""
        feedback = 0
        # 计算反馈位
        for i in range(self.length):
            if (self.polynomial >> i) & 1:
                feedback ^= (self.state >> i) & 1

        # 移位并更新状态
        self.state = ((self.state << 1) | feedback) & self.mask
        return feedback

    def next_byte(self) -> int:
        """生成下一个随机字节"""
        result = 0
        for i in range(8):
            result = (result << 1) | self.next_bit()
        return result

    def generate_keystream(self, length: int) -> bytes:
        """生成指定长度的密钥流"""
        keystream = bytearray()
        for _ in range(length):
            keystream.append(self.next_byte())
        return bytes(keystream)


class DHKeyExchange:
    """DH密钥协商算法"""

    def __init__(self, prime_bits: int = 64):
        self.p = PublicKeyCrypto.generate_large_prime(prime_bits)

        # 选择原根g（简化处理，选择较小的数）
        self.g = 2
        while PublicKeyCrypto.mod_exp(self.g, (self.p - 1) // 2, self.p) == 1:
            self.g += 1

    def generate_key_pair(self) -> Tuple[int, int]:
        """生成密钥对"""
        private_key = random.randint(2, self.p - 2)
        public_key = PublicKeyCrypto.mod_exp(self.g, private_key, self.p)
        return private_key, public_key

    def compute_shared_secret(self, private_key: int, other_public_key: int) -> int:
        """计算共享密钥"""
        return PublicKeyCrypto.mod_exp(other_public_key, private_key, self.p)


class ElGamal:
    """ElGamal加密算法"""

    def __init__(self, prime_bits: int = 64):
        self.p = PublicKeyCrypto.generate_large_prime(prime_bits)
        self.g = 2
        while PublicKeyCrypto.mod_exp(self.g, (self.p - 1) // 2, self.p) == 1:
            self.g += 1

    def generate_key_pair(self) -> Tuple[int, Tuple[int, int, int]]:
        """生成密钥对"""
        private_key = random.randint(2, self.p - 2)
        public_key = PublicKeyCrypto.mod_exp(self.g, private_key, self.p)
        return private_key, (self.p, self.g, public_key)

    def encrypt(self, public_key: Tuple[int, int, int], message: int) -> Tuple[int, int]:
        """加密"""
        p, g, h = public_key
        k = random.randint(2, p - 2)
        c1 = PublicKeyCrypto.mod_exp(g, k, p)
        c2 = (message * PublicKeyCrypto.mod_exp(h, k, p)) % p
        return c1, c2

    def decrypt(self, private_key: int, ciphertext: Tuple[int, int], p: int) -> int:
        """解密"""
        c1, c2 = ciphertext
        s = PublicKeyCrypto.mod_exp(c1, private_key, p)
        s_inv = PublicKeyCrypto.mod_inverse(s, p)
        return (c2 * s_inv) % p


class RSA:
    """RSA加密算法"""

    def __init__(self, prime_bits: int = 32):
        self.prime_bits = prime_bits

    def generate_key_pair(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """生成RSA密钥对"""
        # 生成两个大素数
        p = PublicKeyCrypto.generate_large_prime(self.prime_bits)
        q = PublicKeyCrypto.generate_large_prime(self.prime_bits)

        n = p * q
        phi = (p - 1) * (q - 1)

        # 选择公钥指数e
        e = 65537
        while math.gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)

        # 计算私钥指数d
        d = PublicKeyCrypto.mod_inverse(e, phi)

        public_key = (e, n)
        private_key = (d, n)

        return public_key, private_key

    def encrypt(self, public_key: Tuple[int, int], message: int) -> int:
        """RSA加密"""
        e, n = public_key
        return PublicKeyCrypto.mod_exp(message, e, n)

    def decrypt(self, private_key: Tuple[int, int], ciphertext: int) -> int:
        """RSA解密"""
        d, n = private_key
        return PublicKeyCrypto.mod_exp(ciphertext, d, n)


class FileCrypto:
    """文件加密工具类"""

    @staticmethod
    def encrypt_file_lfsr(input_file: str, output_file: str, seed: int, polynomial: int):
        """使用LFSR加密文件"""
        lfsr = LFSR(seed, polynomial)

        with open(input_file, 'rb') as f_in:
            plaintext = f_in.read()

        keystream = lfsr.generate_keystream(len(plaintext))
        ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))

        with open(output_file, 'wb') as f_out:
            f_out.write(ciphertext)

    @staticmethod
    def decrypt_file_lfsr(input_file: str, output_file: str, seed: int, polynomial: int):
        """使用LFSR解密文件（加密解密的对称性）"""
        FileCrypto.encrypt_file_lfsr(input_file, output_file, seed, polynomial)

    @staticmethod
    def encrypt_file_rsa(input_file: str, output_file: str, public_key: Tuple[int, int], block_size: int = 8):
        """使用RSA加密文件"""
        e, n = public_key

        with open(input_file, 'rb') as f_in:
            plaintext = f_in.read()

        # 分块加密
        encrypted_blocks = []
        for i in range(0, len(plaintext), block_size):
            block = plaintext[i:i + block_size]
            # 将字节块转换为整数
            message_int = int.from_bytes(block, 'big')
            # 确保消息小于n
            if message_int >= n:
                raise ValueError("消息块太大，请减小block_size")
            # 加密
            encrypted_int = PublicKeyCrypto.mod_exp(message_int, e, n)
            encrypted_blocks.append(encrypted_int.to_bytes((n.bit_length() + 7) // 8, 'big'))

        with open(output_file, 'wb') as f_out:
            for block in encrypted_blocks:
                f_out.write(block)

    @staticmethod
    def decrypt_file_rsa(input_file: str, output_file: str, private_key: Tuple[int, int]):
        """使用RSA解密文件"""
        d, n = private_key
        block_size = (n.bit_length() + 7) // 8

        with open(input_file, 'rb') as f_in:
            ciphertext = f_in.read()

        # 分块解密
        decrypted_blocks = []
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i + block_size]
            # 将字节块转换为整数
            cipher_int = int.from_bytes(block, 'big')
            # 解密
            decrypted_int = PublicKeyCrypto.mod_exp(cipher_int, d, n)
            # 转换回字节
            decrypted_block = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
            decrypted_blocks.append(decrypted_block)

        with open(output_file, 'wb') as f_out:
            for block in decrypted_blocks:
                f_out.write(block)


def main():
    """主测试函数"""
    print("=" * 50)
    print("公钥密码算法编程模拟实验")
    print("=" * 50)

    # 测试模指运算
    print("\n1. 模指运算测试:")
    result = PublicKeyCrypto.mod_exp(2, 10, 1000)
    print(f"2^10 mod 1000 = {result}")

    # 测试素数判定
    print("\n2. 素数判定测试:")
    test_numbers = [17, 25, 97, 100]
    for num in test_numbers:
        is_prime = PublicKeyCrypto.miller_rabin_test(num)
        print(f"{num} 是素数: {is_prime}")

    # 测试DH密钥协商
    print("\n3. DH密钥协商测试:")
    dh = DHKeyExchange(prime_bits=32)

    # Alice生成密钥对
    alice_private, alice_public = dh.generate_key_pair()
    # Bob生成密钥对
    bob_private, bob_public = dh.generate_key_pair()

    # 计算共享密钥
    alice_shared = dh.compute_shared_secret(alice_private, bob_public)
    bob_shared = dh.compute_shared_secret(bob_private, alice_public)

    print(f"Alice共享密钥: {alice_shared}")
    print(f"Bob共享密钥: {bob_shared}")
    print(f"密钥协商成功: {alice_shared == bob_shared}")

    # 测试ElGamal算法
    print("\n4. ElGamal算法测试:")
    elgamal = ElGamal(prime_bits=32)
    private_key, public_key = elgamal.generate_key_pair()

    message = 123456
    ciphertext = elgamal.encrypt(public_key, message)
    decrypted = elgamal.decrypt(private_key, ciphertext, public_key[0])

    print(f"原始消息: {message}")
    print(f"加密结果: {ciphertext}")
    print(f"解密结果: {decrypted}")
    print(f"加解密成功: {message == decrypted}")

    # 测试RSA算法
    print("\n5. RSA算法测试:")
    rsa = RSA(prime_bits=16)
    public_key, private_key = rsa.generate_key_pair()

    message = 12345
    ciphertext = rsa.encrypt(public_key, message)
    decrypted = rsa.decrypt(private_key, ciphertext)

    print(f"原始消息: {message}")
    print(f"加密结果: {ciphertext}")
    print(f"解密结果: {decrypted}")
    print(f"加解密成功: {message == decrypted}")

    # 测试LFSR
    print("\n6. LFSR测试:")
    lfsr = LFSR(seed=0b1101, polynomial=0b1011, length=4)
    print("LFSR生成的10个比特:", [lfsr.next_bit() for _ in range(10)])

    # 重新初始化LFSR
    lfsr = LFSR(seed=0b1101, polynomial=0b1011, length=4)
    keystream = lfsr.generate_keystream(5)
    print("LFSR生成的5个字节:", list(keystream))

    print("\n7. 文件加密测试:")
    # 创建测试文件
    test_content = b"Hello, this is a test file for public key cryptography algorithms!"
    with open("test_input.txt", "wb") as f:
        f.write(test_content)

    # LFSR文件加密
    FileCrypto.encrypt_file_lfsr("test_input.txt", "test_encrypted_lfsr.bin",
                                 seed=0b11011010, polynomial=0b10001101)
    FileCrypto.decrypt_file_lfsr("test_encrypted_lfsr.bin", "test_decrypted_lfsr.txt",
                                 seed=0b11011010, polynomial=0b10001101)

    # 验证LFSR加解密
    with open("test_decrypted_lfsr.txt", "rb") as f:
        decrypted_content = f.read()
    print(f"LFSR文件加解密成功: {test_content == decrypted_content}")

    # RSA文件加密（使用较小的密钥）
    rsa_small = RSA(prime_bits=16)
    pub_key, priv_key = rsa_small.generate_key_pair()

    FileCrypto.encrypt_file_rsa("test_input.txt", "test_encrypted_rsa.bin", pub_key, block_size=2)
    FileCrypto.decrypt_file_rsa("test_encrypted_rsa.bin", "test_decrypted_rsa.txt", priv_key)

    # 验证RSA加解密
    with open("test_decrypted_rsa.txt", "rb") as f:
        rsa_decrypted = f.read()
    print(f"RSA文件加解密成功: {test_content == rsa_decrypted}")


if __name__ == "__main__":
    main()