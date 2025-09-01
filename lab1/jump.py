# -*- coding: utf-8 -*-
"""
实验：简化版“跳一跳”计分
目标：使用 while 循环与状态变量计算总分

输入与规则：
- 循环逐次输入 1/2/0，0 表示结束（本题使用 while True + break 结构）
- 1：加 1 分；并将“中心加分”重置为 2
- 2：加“中心加分”（初始为 2）；若本次为连续中心，下次中心加分在此基础上 +2
- 0：结束输入，输出总分
"""

def compute_score() -> int:
    """交互式读取每次跳跃结果并返回总分。"""
    total = 0
    center_bonus = 2   # “中心加分”的当前值。首次中心得 2 分，之后连续中心每次 +2

    while True:  # 主要循环框架
        s = input("请输入本次跳跃(1=非中心, 2=中心, 0=结束)：").strip()
        # 将输入转换为整数
        try:
            a = int(s)
        except ValueError:
            print("输入无效，请输入 0/1/2。")
            continue

        if a == 0:
            # 游戏结束
            break
        elif a == 1:
            total += 1
            center_bonus = 2
            # 非中心：加 1 分，并重置中心加分为 2
            # TODO：补全加分与重置逻辑
        elif a == 2:
            total += center_bonus
            center_bonus += 2
            # 中心：加“中心加分”；若再次中心，应让中心加分在此基础上 +2
            # TODO：补全加分与“连续中心时 +2 递增”的逻辑
        else:
            print("输入超出范围，请输入 0/1/2。")
            continue

    return total


def main():
    print("简化跳一跳：逐次输入 1/2，输入 0 结束并输出总分。")
    score = compute_score()
    print(score)
    # TODO：打印总分



if __name__ == "__main__":
    main()
