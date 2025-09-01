# -*- coding: utf-8 -*-
"""
实验三：条件判断与循环
目标：学习 if-else、for 和 while（本题侧重 while）

任务（猜数字）：
- 程序随机生成一个 1~100 的整数（使用 random 模块）
- 用户循环输入猜测，程序提示“大了”或“小了”
- 猜中时打印“恭喜！用时X次”并退出
"""

import random


def main():
    print("猜数字游戏：我想了一个 1~100 的整数。输入 q 可退出。")

    # ===== 步骤 1：生成目标数字（已写好）=====
    # TODO：使用random包随机生成一个1-100之间的整数
    target = random.randint(2,99)
    attempts = 0 # 创建统计猜测次数的变量

    # ===== 步骤 2：循环交互（while True）=====
    while True:
        # 获取用户输入（字符串）
        guess_str = input("你的猜测：")

        # 可选：允许用户主动退出（已写好）
        if guess_str.lower() in ("q", "quit", "exit"):
            print("已退出游戏。")
            break

        # ===== 步骤 3：将输入转换为整数（已写好，含异常处理）=====
        try:
            guess = int(guess_str)
        except ValueError:
            print("输入无效：请输入整数。")
            continue

        # 可选：范围检查（已写好）
        if not 1 <= guess <= 100:
            print("范围错误：请输入 1~100 之间的整数。")
            continue

        # ===== 步骤 4：计数（挖空）=====
        # 进行一次“有效猜测”（通过了转换与范围检查）后，attempts 自增 1
        # TODO：完成 attempts 的自增
        attempts += 1

        # ===== 步骤 5：比较并提示 =====
        # 已写好示例分支：比目标大
        if guess > target:
            print("大了")
            # 回到循环开头，继续下一轮
            continue

        # TODO：补全另外两个分支
        # 1) 若 guess < target，提示 "小了"
        elif guess < target:
            print("小了")
            continue
        # 2) 若 guess == target，打印 "恭喜！用时X次"（X 用 attempts 替换），并 break
        else:
            print(f"恭喜！用时{attempts}次")
            break


if __name__ == "__main__":
    # 在命令行执行：python guessnum.py
    main()
