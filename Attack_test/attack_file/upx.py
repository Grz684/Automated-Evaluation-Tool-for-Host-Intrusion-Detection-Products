import subprocess
import os

def upx_pack_elf(input_file, output_file=None):
    if not output_file:
        output_file = input_file + ".packed"
    
    # 检查 UPX 是否已经安装
    upx_path = "/usr/bin/upx"  # 在大多数系统上，UPX 可执行文件位于系统 PATH 中
    if not os.path.exists(upx_path):
        raise Exception("UPX not found. Please install UPX and ensure it's in your PATH.")
    
    # 调用 UPX 命令行工具进行加壳
    try:
        cmd = [upx_path, "-o", output_file, input_file]
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(f"File packed successfully. Output: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"UPX encountered an error: {e.output.decode('utf-8')}")

if __name__ == "__main__":
    input_file = "malware_test"  # 你要加壳的 ELF 文件路径
    upx_pack_elf(input_file)

