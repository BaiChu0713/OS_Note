import random
import struct
from typing import List, Tuple, Dict


class DES:
    """纯Python实现的DES加密算法"""

    # 初始置换表 (IP)
    IP = [
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]

    # 逆初始置换表 (IP^-1)
    IP_INV = [
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
        32, 0, 40, 8, 48, 16, 56, 24
    ]

    # 扩展置换表 (E)
    E = [
        31, 0, 1, 2, 3, 4,
        3, 4, 5, 6, 7, 8,
        7, 8, 9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31, 0
    ]

    # P盒置换
    P = [
        15, 6, 19, 20, 28, 11, 27, 16,
        0, 14, 22, 25, 4, 17, 30, 9,
        1, 7, 23, 13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10, 3, 24
    ]

    # PC-1 (密钥初始置换)
    PC1 = [
        56, 48, 40, 32, 24, 16, 8, 0,
        57, 49, 41, 33, 25, 17, 9, 1,
        58, 50, 42, 34, 26, 18, 10, 2,
        59, 51, 43, 35, 62, 54, 46, 38,
        30, 22, 14, 6, 61, 53, 45, 37,
        29, 21, 13, 5, 60, 52, 44, 36,
        28, 20, 12, 4, 27, 19, 11, 3
    ]

    # PC-2 (密钥压缩置换)
    PC2 = [
        13, 16, 10, 23, 0, 4, 2, 27,
        14, 5, 20, 9, 22, 18, 11, 3,
        25, 7, 15, 6, 26, 19, 12, 1,
        40, 51, 30, 36, 46, 54, 29, 39,
        50, 44, 32, 47, 43, 48, 38, 55,
        33, 52, 45, 41, 49, 35, 28, 31
    ]

    # 左移位数表
    SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # S盒
    S_BOX = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    @staticmethod
    def permute(block: int, table: List[int], input_size: int) -> int:
        """根据置换表进行位置换"""
        result = 0
        for pos, src_pos in enumerate(table):
            if block & (1 << (input_size - 1 - src_pos)):
                result |= (1 << (len(table) - 1 - pos))
        return result

    @staticmethod
    def left_rotate(n: int, d: int, bits: int = 28) -> int:
        """循环左移"""
        return ((n << d) | (n >> (bits - d))) & ((1 << bits) - 1)

    @staticmethod
    def generate_subkeys(key: int) -> List[int]:
        """生成16轮子密钥"""
        # PC-1置换
        key_permuted = DES.permute(key, DES.PC1, 64)

        # 分割成左右两部分
        left = (key_permuted >> 28) & 0x0FFFFFFF
        right = key_permuted & 0x0FFFFFFF

        subkeys = []
        for round_num in range(16):
            # 左移
            left = DES.left_rotate(left, DES.SHIFT_SCHEDULE[round_num])
            right = DES.left_rotate(right, DES.SHIFT_SCHEDULE[round_num])

            # 合并并PC-2置换
            combined = (left << 28) | right
            subkey = DES.permute(combined, DES.PC2, 56)
            subkeys.append(subkey)

        return subkeys

    @staticmethod
    def f_function(right: int, subkey: int) -> int:
        """F函数"""
        # 扩展置换
        expanded = DES.permute(right, DES.E, 32)

        # 与子密钥异或
        xored = expanded ^ subkey

        # S盒替换
        sbox_output = 0
        for i in range(8):
            # 取出6位
            chunk = (xored >> (42 - 6 * i)) & 0x3F
            row = ((chunk & 0x20) >> 4) | (chunk & 0x01)
            col = (chunk >> 1) & 0x0F
            sbox_val = DES.S_BOX[i][row][col]
            sbox_output |= (sbox_val << (28 - 4 * i))

        # P盒置换
        return DES.permute(sbox_output, DES.P, 32)

    @staticmethod
    def encrypt_block(block: int, key: int, rounds: int = 16) -> Tuple[int, Dict[int, int]]:
        """加密一个64位数据块，返回每轮加密结果"""
        # 生成子密钥
        subkeys = DES.generate_subkeys(key)

        # 初始置换
        block_permuted = DES.permute(block, DES.IP, 64)

        # 分割成左右两部分
        left = (block_permuted >> 32) & 0xFFFFFFFF
        right = block_permuted & 0xFFFFFFFF

        round_results = {}

        # 16轮Feistel网络
        for round_num in range(rounds):
            # 保存当前轮次结果
            current_block = (left << 32) | right
            current_final = DES.permute(current_block, DES.IP_INV, 64)
            round_results[round_num + 1] = current_final

            # F函数和异或
            f_result = DES.f_function(right, subkeys[round_num])
            new_right = left ^ f_result

            # 更新左右部分
            left = right
            right = new_right

        # 最终置换
        final_block = (right << 32) | left  # 注意最后不需要交换
        ciphertext = DES.permute(final_block, DES.IP_INV, 64)
        round_results[16] = ciphertext

        return ciphertext, round_results

    @staticmethod
    def bytes_to_int(data: bytes) -> int:
        """将字节转换为整数"""
        return int.from_bytes(data, 'big')

    @staticmethod
    def int_to_bytes(value: int, length: int = 8) -> bytes:
        """将整数转换为字节"""
        return value.to_bytes(length, 'big')


class DESAnalysis:
    """DES差分海明重量分析"""

    @staticmethod
    def hamming_weight(data: int) -> int:
        """计算整数的海明重量"""
        return bin(data).count('1')

    @staticmethod
    def generate_bitstring_with_hamming_weight(weight: int, length: int) -> int:
        """生成指定海明重量的位串"""
        if weight > length:
            weight = length

        # 创建初始位串
        positions = list(range(length))
        random.shuffle(positions)

        result = 0
        for i in range(weight):
            result |= (1 << positions[i])

        return result

    @staticmethod
    def experiment_A_fixed_key(num_samples: int = 5) -> Dict:
        """情况A：固定密钥，变化明文差分"""
        print("开始实验A：固定密钥，变化明文差分")
        results = {}

        for hw_diff in range(1, 65):
            # 进度显示
            if hw_diff % 8 == 0:
                progress = hw_diff / 64 * 100
                print(f"实验A进度: {progress:.1f}%")

            round_weights = {i: [] for i in range(1, 17)}

            for sample in range(num_samples):
                # 固定密钥
                key = random.getrandbits(64)

                # 生成具有特定差分海明重量的明文对
                m1 = random.getrandbits(64)
                diff = DESAnalysis.generate_bitstring_with_hamming_weight(hw_diff, 64)
                m2 = m1 ^ diff

                # 验证差分海明重量
                actual_hw = DESAnalysis.hamming_weight(m1 ^ m2)

                if actual_hw == hw_diff:
                    # 加密并记录每轮结果
                    c1, rounds1 = DES.encrypt_block(m1, key, 16)
                    c2, rounds2 = DES.encrypt_block(m2, key, 16)

                    for round_num in range(1, 17):
                        round_c1 = rounds1[round_num]
                        round_c2 = rounds2[round_num]
                        cipher_diff = round_c1 ^ round_c2
                        cipher_hw = DESAnalysis.hamming_weight(cipher_diff)
                        round_weights[round_num].append(cipher_hw)

            # 计算平均值
            results[hw_diff] = {}
            for round_num in range(1, 17):
                weights = round_weights[round_num]
                if weights:
                    results[hw_diff][round_num] = sum(weights) / len(weights)
                else:
                    results[hw_diff][round_num] = 0

        print("实验A完成")
        return results

    @staticmethod
    def experiment_B_fixed_plaintext(num_samples: int = 5) -> Dict:
        """情况B：固定明文，变化密钥差分"""
        print("开始实验B：固定明文，变化密钥差分")
        results = {}

        for hw_diff in range(1, 65):
            # 进度显示
            if hw_diff % 8 == 0:
                progress = hw_diff / 64 * 100
                print(f"实验B进度: {progress:.1f}%")

            round_weights = {i: [] for i in range(1, 17)}

            for sample in range(num_samples):
                # 固定明文
                plaintext = random.getrandbits(64)

                # 生成具有特定差分海明重量的密钥对
                k1 = random.getrandbits(64)
                diff = DESAnalysis.generate_bitstring_with_hamming_weight(hw_diff, 64)
                k2 = k1 ^ diff

                # 验证差分海明重量
                actual_hw = DESAnalysis.hamming_weight(k1 ^ k2)

                if actual_hw == hw_diff:
                    # 加密并记录每轮结果
                    c1, rounds1 = DES.encrypt_block(plaintext, k1, 16)
                    c2, rounds2 = DES.encrypt_block(plaintext, k2, 16)

                    for round_num in range(1, 17):
                        round_c1 = rounds1[round_num]
                        round_c2 = rounds2[round_num]
                        cipher_diff = round_c1 ^ round_c2
                        cipher_hw = DESAnalysis.hamming_weight(cipher_diff)
                        round_weights[round_num].append(cipher_hw)

            # 计算平均值
            results[hw_diff] = {}
            for round_num in range(1, 17):
                weights = round_weights[round_num]
                if weights:
                    results[hw_diff][round_num] = sum(weights) / len(weights)
                else:
                    results[hw_diff][round_num] = 0

        print("实验B完成")
        return results

    @staticmethod
    def print_results(results: Dict, title: str):
        """打印结果表格"""
        print(f"\n{title}:")
        print("差分HW\t第1轮\t第2轮\t第4轮\t第8轮\t第16轮")
        print("------\t----\t----\t----\t----\t-----")

        display_hw = [1, 8, 16, 32, 48, 64]
        display_rounds = [1, 2, 4, 8, 16]

        for hw in display_hw:
            if hw in results:
                print(f"{hw}", end="\t")
                for round_num in display_rounds:
                    if round_num in results[hw]:
                        print(f"{results[hw][round_num]:.1f}", end="\t")
                    else:
                        print("0.0", end="\t")
                print()

    @staticmethod
    def save_results_to_csv(results: Dict, filename: str):
        """保存结果到CSV文件"""
        with open(filename, 'w') as f:
            # 写入表头
            f.write("HW_Diff")
            for round_num in range(1, 17):
                f.write(f",Round{round_num}")
            f.write("\n")

            # 写入数据
            for hw_diff in range(1, 65):
                if hw_diff in results:
                    f.write(str(hw_diff))
                    for round_num in range(1, 17):
                        if round_num in results[hw_diff]:
                            f.write(f",{results[hw_diff][round_num]:.2f}")
                        else:
                            f.write(",0.00")
                    f.write("\n")


def main():
    """主函数"""
    print("DES差分海明重量统计分析")
    print("=" * 50)

    # 执行实验A
    results_A = DESAnalysis.experiment_A_fixed_key(num_samples=3)
    DESAnalysis.print_results(results_A, "情况A：固定密钥，变化明文差分")
    DESAnalysis.save_results_to_csv(results_A, "experiment_A_results.csv")

    print("\n" + "=" * 50 + "\n")

    # 执行实验B
    results_B = DESAnalysis.experiment_B_fixed_plaintext(num_samples=3)
    DESAnalysis.print_results(results_B, "情况B：固定明文，变化密钥差分")
    DESAnalysis.save_results_to_csv(results_B, "experiment_B_results.csv")

    print("\n实验结果分析完成！")
    print("详细结果已保存到CSV文件")


if __name__ == "__main__":
    main()