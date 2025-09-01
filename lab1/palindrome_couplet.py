# -*- coding: utf-8 -*-
"""
实验：判断是否为“回文联”（不限奇偶长度）
目标：使用函数与双指针（头尾遍历）判断字符串是否回文

定义：
- “回文联”：顺读与倒读完全一致（本实验不再要求偶数长度）

任务：
1) 编写函数 is_palindrome_couplet(s) -> bool
   - 双指针从两端向中间比较；遇到任一对字符不等即返回 False
   - 任意长度均可（奇数长度中间字符无需比较）
2) 从命令行参数读取一个字符串，并输出判断结果

示例运行：
python palindrome_couplet.py "处处飞花飞处处"
python palindrome_couplet.py "客上天然居居然天上客"

"""

import sys


def is_palindrome_couplet(s: str) -> bool:
    """判断 s 是否为回文联（不限长度）。"""

    # 可选预处理（按需启用）：
    # - 若希望忽略空格或标点，可在此处自行处理，例如：
    # s = s.replace(" ", "")   # 去掉空格
    # 注：本实验默认“逐字符严格比较”，不做任何预处理。

    # ===== 双指针从两端向中间比较 =====
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1

    return True


def main():
    # ===== 命令行参数处理（已写好）=====
    if len(sys.argv) < 2:
        print('用法：python palindrome_couplet.py "你的字符串"')
        return
    s = sys.argv[1]

    # ===== 调用函数并输出结果（挖空）=====
    
    result = is_palindrome_couplet(s)
    if result == 0:
        print("不是回文联")
    else:
        print("是回文联")


if __name__ == "__main__":
    main()
