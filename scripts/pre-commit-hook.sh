#!/bin/sh
# pre-commit hook: 检查所有暂存的文本文件是否为干净 UTF-8
# 安装: cp scripts/pre-commit-hook.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
# 或用 pre-commit 框架: 见 .pre-commit-config.yaml

# 找到仓库根目录
REPO_ROOT=$(git rev-parse --show-toplevel)

# 获取暂存的文件列表（只检查 .md/.py/.json/.yaml/.yml）
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -iE '\.(md|py|json|ya?ml)$')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# 运行编码检测（仅检查暂存文件）
EXIT_CODE=0
for file in $STAGED_FILES; do
    FULL_PATH="$REPO_ROOT/$file"
    if [ ! -f "$FULL_PATH" ]; then
        continue
    fi
    # 跳过备份目录
    case "$file" in
        _damaged_backup/*) continue ;;
    esac
    # 用 python 检测
    RESULT=$(python -c "
import sys
path = sys.argv[1]
try:
    with open(path, 'rb') as f:
        data = f.read()
    if data.startswith(b'\xef\xbb\xbf'):
        print('BOM')
        sys.exit(1)
    data.decode('utf-8')  # 严格模式
    for marker in ['锟斤拷', '缃戠粶', '鏂囧啓', '璺敱']:
        if marker.encode('utf-8') in data:
            print('garbled:' + marker)
            sys.exit(1)
    sys.exit(0)
except UnicodeDecodeError as e:
    print('bad_utf8:' + str(e)[:50])
    sys.exit(1)
" "$FULL_PATH" 2>&1)
    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "ENCODING ERROR: $file - $RESULT"
        EXIT_CODE=1
    fi
done

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "编码检测失败！请修复以上文件后重新提交。"
    echo "提示: 运行 python scripts/check_encoding.py . 查看完整报告"
    exit 1
fi

exit 0
