#!/usr/bin/env python3
"""检测所有 .md/.py 文件是否为干净 UTF-8（无 BOM、无 GBK 污染）
用法: python check_encoding.py [目录]
退出码 0 = 全部干净; 1 = 发现问题
"""
import sys
from pathlib import Path

UTF8_BOM = bytes([0xEF, 0xBB, 0xBF])


def check_file(path):
    """返回 (is_clean, message)"""
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except Exception as e:
        return False, "读取失败: " + str(e)

    # 检查 BOM
    if data.startswith(UTF8_BOM):
        return False, "含 UTF-8 BOM"

    # 严格 UTF-8 解码
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as e:
        return False, "非 UTF-8 字节 (pos " + str(e.start) + "): " + str(e)

    # 检查典型乱码特征
    garbled_markers = ['锟斤拷', '锟斤', '缃戠粶', '鏂囧啓', '璺敱']
    for marker in garbled_markers:
        if marker in text:
            return False, "含乱码特征: " + marker

    return True, "OK"


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    exts = {'.md', '.py', '.json', '.yaml', '.yml'}
    bad = []
    ok_count = 0

    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        # 跳过备份目录、.git、自身
        if '_damaged_backup' in p.parts or '.git' in p.parts:
            continue
        if p.name == 'check_encoding.py':
            continue
        is_clean, msg = check_file(p)
        if is_clean:
            ok_count += 1
        else:
            bad.append((p, msg))
            print("BAD: " + str(p) + " - " + msg)

    print("")
    print("检查完成: " + str(ok_count) + " OK, " + str(len(bad)) + " BAD")
    if bad:
        print("")
        print("建议修复:")
        for p, msg in bad:
            print("  - " + str(p) + ": " + msg)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
