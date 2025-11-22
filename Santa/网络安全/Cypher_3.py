import random
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
from collections import defaultdict
import csv


class RandomnessTest:
    """随机性检测类"""

    @staticmethod
    def runs_test(sequence: List[int]) -> Dict:
        """
        游程分布检测
        返回各种长度游程的统计结果
        """
        if isinstance(sequence, str):
            sequence = [int(bit) for bit in sequence]

        runs = []
        current_run = 1
        current_bit = sequence[0]

        for i in range(1, len(sequence)):
            if sequence[i] == current_bit:
                current_run += 1
            else:
                runs.append((current_bit, current_run))
                current_bit = sequence[i]
                current_run = 1
        runs.append((current_bit, current_run))

        # 统计各种长度的游程
        run_stats = defaultdict(lambda: {'0': 0, '1': 0})
        for bit, length in runs:
            run_stats[length][str(bit)] += 1

        return {
            'total_runs': len(runs),
            'run_distribution': dict(run_stats),
            'runs_sequence': runs
        }

    @staticmethod
    def autocorrelation_test(sequence: List[int], lag: int = 1) -> float:
        """
        自相关检测
        计算指定延迟的自相关系数
        """
        n = len(sequence)
        if n <= lag:
            return 0.0

        # 将序列转换为±1
        seq_plus_minus = [1 if bit == 1 else -1 for bit in sequence]

        # 计算自相关
        correlation = 0
        for i in range(n - lag):
            correlation += seq_plus_minus[i] * seq_plus_minus[i + lag]

        return correlation / (n - lag)


class LFSR:
    """线性反馈移位寄存器"""

    def __init__(self, polynomial_str: str, initial_state: int = None):
        """
        polynomial_str: 连接多项式字符串，如 "1011" 表示 x^4 + x + 1
        initial_state: 初始状态，如果为None则随机生成
        """
        self.polynomial = int(polynomial_str, 2)
        self.length = len(polynomial_str)

        if initial_state is None:
            # 随机生成初始状态，确保不全为0
            self.state = random.getrandbits(self.length)
            while self.state == 0:
                self.state = random.getrandbits(self.length)
        else:
            self.state = initial_state

        self.mask = (1 << self.length) - 1
        self.sequence = []

    def next_bit(self) -> int:
        """生成下一个随机比特"""
        feedback = 0
        # 计算反馈位
        for i in range(self.length):
            if (self.polynomial >> i) & 1:
                feedback ^= (self.state >> i) & 1

        # 输出最低位
        output = self.state & 1

        # 移位并更新状态
        self.state = ((self.state >> 1) | (feedback << (self.length - 1))) & self.mask
        self.sequence.append(output)

        return output

    def generate_sequence(self, length: int) -> List[int]:
        """生成指定长度的随机序列"""
        self.sequence = []
        for _ in range(length):
            self.next_bit()
        return self.sequence.copy()

    def generate_bytes(self, num_bytes: int) -> bytes:
        """生成指定字节数的随机序列"""
        result = bytearray()
        for _ in range(num_bytes):
            byte_val = 0
            for i in range(8):
                byte_val = (byte_val << 1) | self.next_bit()
            result.append(byte_val)
        return bytes(result)

    def get_period(self, max_test: int = 10000) -> int:
        """估算序列周期"""
        initial_state = self.state
        sequence = []

        for i in range(max_test):
            bit = self.next_bit()
            sequence.append(bit)

            # 检查是否回到初始状态
            if i > self.length and self.state == initial_state:
                return i + 1

        return -1  # 在max_test内未检测到周期


class RC4:
    """RC4流密码算法"""

    def __init__(self, key: bytes):
        """
        key: 加密密钥
        """
        self.key = key
        self.S = list(range(256))
        self.i = 0
        self.j = 0
        self.state_log = []  # 记录I,J,K变化

        # 密钥调度算法(KSA)
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def next_byte(self) -> int:
        """生成下一个随机字节"""
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256

        # 交换S[i]和S[j]
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]

        # 生成输出字节
        k = self.S[(self.S[self.i] + self.S[self.j]) % 256]

        # 记录状态
        self.state_log.append({
            'i': self.i,
            'j': self.j,
            'k': k,
            'S_i': self.S[self.i],
            'S_j': self.S[self.j]
        })

        return k

    def generate_keystream(self, length: int) -> bytes:
        """生成指定长度的密钥流"""
        result = bytearray()
        for _ in range(length):
            result.append(self.next_byte())
        return bytes(result)

    def save_state_log(self, filename: str):
        """保存状态日志到CSV文件"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Step', 'I', 'J', 'K', 'S[I]', 'S[J]'])
            for step, state in enumerate(self.state_log):
                writer.writerow([
                    step + 1,
                    state['i'],
                    state['j'],
                    state['k'],
                    state['S_i'],
                    state['S_j']
                ])

    def save_ijk_to_text(self, filename: str, num_bytes: int = 100):
        """将I,J,K数据输出到文本文件中"""
        # 重新初始化以确保有足够的数据
        self.__init__(self.key)
        # 生成指定长度的密钥流来记录数据
        self.generate_keystream(num_bytes)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RC4算法 I, J, K 状态变化数据\n")
            f.write("=" * 50 + "\n")
            f.write(f"密钥: {self.key}\n")
            f.write(f"生成字节数: {num_bytes}\n")
            f.write("=" * 50 + "\n")
            f.write(f"{'步骤':<6} {'I':<4} {'J':<4} {'K':<4} {'S[I]':<6} {'S[J]':<6}\n")
            f.write("-" * 50 + "\n")

            for step, state in enumerate(self.state_log[:num_bytes]):
                f.write(f"{step + 1:<6} {state['i']:<4} {state['j']:<4} {state['k']:<4} "
                        f"{state['S_i']:<6} {state['S_j']:<6}\n")

            # 添加统计信息
            f.write("\n" + "=" * 50 + "\n")
            f.write("统计信息:\n")
            f.write(f"总步数: {len(self.state_log)}\n")

            # I值的统计
            i_values = [state['i'] for state in self.state_log]
            f.write(f"I值范围: {min(i_values)} - {max(i_values)}\n")
            f.write(f"I值平均值: {np.mean(i_values):.2f}\n")

            # J值的统计
            j_values = [state['j'] for state in self.state_log]
            f.write(f"J值范围: {min(j_values)} - {max(j_values)}\n")
            f.write(f"J值平均值: {np.mean(j_values):.2f}\n")

            # K值的统计
            k_values = [state['k'] for state in self.state_log]
            f.write(f"K值范围: {min(k_values)} - {max(k_values)}\n")
            f.write(f"K值平均值: {np.mean(k_values):.2f}\n")

            # 输出前10个字节的密钥流
            f.write("\n前10个输出字节(十六进制): ")
            keystream_bytes = [state['k'] for state in self.state_log[:10]]
            f.write(' '.join(f"{b:02X}" for b in keystream_bytes))
            f.write("\n")

            f.write("前10个输出字节(十进制): ")
            f.write(' '.join(str(b) for b in keystream_bytes))


class StreamCipherFile:
    """流密码文件加密类"""

    @staticmethod
    def encrypt_file(input_file: str, output_file: str, keystream: bytes):
        """使用流密码加密文件"""
        with open(input_file, 'rb') as f:
            plaintext = f.read()

        # 流加密：逐字节异或
        ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))

        with open(output_file, 'wb') as f:
            f.write(ciphertext)

    @staticmethod
    def decrypt_file(input_file: str, output_file: str, keystream: bytes):
        """使用流密码解密文件（与加密相同）"""
        StreamCipherFile.encrypt_file(input_file, output_file, keystream)


class Visualization:
    """可视化类"""

    @staticmethod
    def plot_rc4_states(rc4: RC4, num_steps: int = 100):
        """绘制RC4内部状态变化图"""
        if len(rc4.state_log) < num_steps:
            num_steps = len(rc4.state_log)

        steps = list(range(1, num_steps + 1))
        i_vals = [state['i'] for state in rc4.state_log[:num_steps]]
        j_vals = [state['j'] for state in rc4.state_log[:num_steps]]
        k_vals = [state['k'] for state in rc4.state_log[:num_steps]]

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

        # 绘制I值变化
        ax1.plot(steps, i_vals, 'b-', linewidth=1, label='I')
        ax1.set_ylabel('I Value')
        ax1.set_title('RC4 Internal State Changes - I Value')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # 绘制J值变化
        ax2.plot(steps, j_vals, 'r-', linewidth=1, label='J')
        ax2.set_ylabel('J Value')
        ax2.set_title('RC4 Internal State Changes - J Value')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # 绘制K值变化
        ax3.plot(steps, k_vals, 'g-', linewidth=1, label='K')
        ax3.set_xlabel('Step')
        ax3.set_ylabel('K Value')
        ax3.set_title('RC4 Internal State Changes - K Value (Output)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        plt.tight_layout()
        plt.savefig('rc4_state_changes.png', dpi=300, bbox_inches='tight')
        plt.show()

    @staticmethod
    def plot_lfsr_sequence(sequence: List[int], title: str = "LFSR Sequence"):
        """绘制LFSR序列图"""
        plt.figure(figsize=(12, 4))
        plt.step(range(len(sequence)), sequence, where='post')
        plt.xlabel('Bit Position')
        plt.ylabel('Bit Value')
        plt.title(title)
        plt.ylim(-0.1, 1.1)
        plt.grid(True, alpha=0.3)
        plt.savefig('lfsr_sequence.png', dpi=300, bbox_inches='tight')
        plt.show()


def test_lfsr_randomness():
    """测试LFSR的随机性"""
    print("=" * 60)
    print("LFSR随机性测试")
    print("=" * 60)

    # 测试不同的连接多项式
    polynomials = {
        "x^4 + x + 1": "1011",
        "x^4 + x^3 + 1": "1101",
        "x^5 + x^2 + 1": "100101",
        "x^8 + x^4 + x^3 + x^2 + 1": "100011101"
    }

    for poly_name, poly_str in polynomials.items():
        print(f"\n测试多项式: {poly_name} ({poly_str})")

        lfsr = LFSR(poly_str, initial_state=0b1101)

        # 生成测试序列
        sequence = lfsr.generate_sequence(1000)

        # 随机性检测
        runs_result = RandomnessTest.runs_test(sequence)
        autocorr_1 = RandomnessTest.autocorrelation_test(sequence, 1)
        autocorr_5 = RandomnessTest.autocorrelation_test(sequence, 5)

        # 估算周期
        period = lfsr.get_period(5000)

        print(f"  序列长度: {len(sequence)} bits")
        print(f"  总游程数: {runs_result['total_runs']}")
        print(f"  延迟1自相关: {autocorr_1:.4f}")
        print(f"  延迟5自相关: {autocorr_5:.4f}")
        print(f"  估算周期: {period if period > 0 else '>5000'}")

        # 显示游程分布
        run_dist = runs_result['run_distribution']
        print("  游程分布:")
        for length in sorted(run_dist.keys())[:5]:  # 只显示前5种长度
            count_0 = run_dist[length]['0']
            count_1 = run_dist[length]['1']
            print(f"    长度{length}: 0游程={count_0}, 1游程={count_1}")


def test_rc4_randomness():
    """测试RC4的随机性"""
    print("\n" + "=" * 60)
    print("RC4随机性测试")
    print("=" * 60)

    # 测试密钥
    key = b"TestKey123456789"

    print(f"使用密钥: {key}")
    rc4 = RC4(key)

    # 生成测试序列（字节）
    keystream = rc4.generate_keystream(100)

    # 将I,J,K数据输出到文本文件
    rc4.save_ijk_to_text("rc4_ijk_data.txt", 100)
    print("I,J,K数据已保存到: rc4_ijk_data.txt")

    # 将字节转换为比特序列进行检测
    bit_sequence = []
    for byte in keystream:
        for i in range(7, -1, -1):
            bit_sequence.append((byte >> i) & 1)

    # 随机性检测
    runs_result = RandomnessTest.runs_test(bit_sequence)
    autocorr_1 = RandomnessTest.autocorrelation_test(bit_sequence, 1)
    autocorr_10 = RandomnessTest.autocorrelation_test(bit_sequence, 10)

    print(f"  密钥流长度: {len(keystream)} bytes ({len(bit_sequence)} bits)")
    print(f"  总游程数: {runs_result['total_runs']}")
    print(f"  延迟1自相关: {autocorr_1:.4f}")
    print(f"  延迟10自相关: {autocorr_10:.4f}")

    # 字节分布统计
    byte_counts = [0] * 256
    for byte in keystream:
        byte_counts[byte] += 1

    expected_count = len(keystream) / 256
    chi_square = sum((count - expected_count) ** 2 / expected_count for count in byte_counts)

    print(f"  字节分布χ²检验: {chi_square:.2f}")
    print(f"  理想χ²值(255自由度): 293.25")
    print(f"  分布均匀性: {'通过' if chi_square < 293.25 else '未通过'}")

    return rc4


def file_encryption_demo():
    """文件加密演示"""
    print("\n" + "=" * 60)
    print("文件加密演示")
    print("=" * 60)

    # 创建测试文件
    test_content = b"This is a test file for stream cipher encryption.\n" + \
                   b"Stream ciphers are efficient for large data encryption.\n" + \
                   b"LFSR and RC4 are two important stream cipher algorithms."

    with open("test_input.txt", "wb") as f:
        f.write(test_content)

    print("原始文件内容:")
    print(test_content.decode())

    # 使用LFSR加密
    print("\n1. LFSR文件加密:")
    lfsr = LFSR("100011101", initial_state=0b11011010)  # x^8 + x^4 + x^3 + x^2 + 1
    lfsr_keystream = lfsr.generate_bytes(len(test_content))
    StreamCipherFile.encrypt_file("test_input.txt", "encrypted_lfsr.bin", lfsr_keystream)

    # 使用RC4加密
    print("2. RC4文件加密:")
    rc4 = RC4(b"MySecretKey123")
    rc4_keystream = rc4.generate_keystream(len(test_content))
    StreamCipherFile.encrypt_file("test_input.txt", "encrypted_rc4.bin", rc4_keystream)

    # 解密验证
    StreamCipherFile.decrypt_file("encrypted_lfsr.bin", "decrypted_lfsr.txt", lfsr_keystream)
    StreamCipherFile.decrypt_file("encrypted_rc4.bin", "decrypted_rc4.txt", rc4_keystream)

    # 验证解密结果
    with open("decrypted_lfsr.txt", "rb") as f:
        lfsr_decrypted = f.read()
    with open("decrypted_rc4.txt", "rb") as f:
        rc4_decrypted = f.read()

    print(f"LFSR加解密验证: {'成功' if lfsr_decrypted == test_content else '失败'}")
    print(f"RC4加解密验证: {'成功' if rc4_decrypted == test_content else '失败'}")

    # 显示加密后的文件大小
    import os
    print(f"\n文件大小统计:")
    print(f"  原始文件: {os.path.getsize('test_input.txt')} bytes")
    print(f"  LFSR加密: {os.path.getsize('encrypted_lfsr.bin')} bytes")
    print(f"  RC4加密: {os.path.getsize('encrypted_rc4.bin')} bytes")


def main():
    """主函数"""
    print("流密码原理与编程模拟实验")
    print("=" * 60)

    # 1. LFSR随机性测试
    test_lfsr_randomness()

    # 2. RC4随机性测试
    rc4 = test_rc4_randomness()

    # 3. 文件加密演示
    file_encryption_demo()

    # 4. 可视化
    print("\n" + "=" * 60)
    print("可视化分析")
    print("=" * 60)

    # LFSR序列可视化
    lfsr_viz = LFSR("1011", initial_state=0b1101)
    lfsr_sequence = lfsr_viz.generate_sequence(50)
    Visualization.plot_lfsr_sequence(lfsr_sequence, "LFSR序列示例 (多项式: x^4 + x + 1)")

    # RC4状态变化可视化（前100步）
    rc4_viz = RC4(b"VisualizationKey")
    rc4_viz.generate_keystream(100)  # 生成100字节来记录状态
    Visualization.plot_rc4_states(rc4_viz, 100)

    # 保存RC4状态日志
    rc4_viz.save_state_log("rc4_state_log.csv")
    rc4_viz.save_ijk_to_text("rc4_ijk_detailed.txt", 100)
    print("RC4状态日志已保存到: rc4_state_log.csv")
    print("RC4 IJK详细数据已保存到: rc4_ijk_detailed.txt")
    print("可以使用Excel打开CSV文件进行进一步分析")

    print("\n实验完成！")
    print("生成的文件:")
    print("  - rc4_ijk_data.txt: RC4 I,J,K数据文件")
    print("  - rc4_ijk_detailed.txt: RC4 I,J,K详细数据文件")
    print("  - rc4_state_changes.png: RC4内部状态变化图")
    print("  - lfsr_sequence.png: LFSR序列图")
    print("  - rc4_state_log.csv: RC4状态日志(CSV格式)")
    print("  - 各种加密测试文件")


if __name__ == "__main__":
    main()