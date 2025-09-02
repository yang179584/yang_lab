# -*- coding: utf-8 -*-
"""
【实验题目】用 pandas + lambda 清洗并分析一份学生成绩表
【实验目的】学会用 pandas 搞定常见的数据清洗（缺失值、数据类型）、打标签（及格/优秀等）、分组统计（每个班的情况），并导出结果文件。
【实验要求】
1. 读一个 CSV（默认叫 students.csv），里面至少有：name（姓名）、class（班级）、age（年龄）、score（分数）。
2. 先把 age 和 score 按“数字”来处理：有的单元格可能是空的、字符串乱写的。score 为空的整行不要；age 为空的，用“该同学所在班级的年龄中位数”补上。
3. 给每位同学贴两个标签：
   - passed：分数 ≥ 60 就 True，否则 False；
   - level：分数 ≥ 90 叫“优秀”；80–89 叫“良好”；60–79 叫“及格”；其他叫“不及格”。
4. 看各个班内部的分数标准化（z-score）：就是“(该同学分数 − 这个班平均分) / 这个班的标准差”，每个班单独算。遇到标准差为 0 的，别报错，直接把分母当 1。
5. 导出三份东西：
   - 每个班、每个 level 的平均年龄和平均分到 summary.csv；
   - 每个班分数 Top-K（默认 K=3，可以用命令行传 --topk 改）到 topk.csv；
   - 全量处理后的表到 students_processed.csv（能导 parquet 的话也顺便导一个）。
6. 命令行参数（--input 输入文件、--topk 取前 K、--outdir 输出目录）。

【运行样例】
# 运行示例：
# python 1.py --input students.csv --topk 2 --outdir out
# 期待 out/ 目录下出现：students_processed.csv、summary.csv、topk.csv（还有 parquet 视环境而定）
"""

import argparse
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="pandas + lambda 清洗与分组统计（学生版）")
    parser.add_argument("--input", required=True, help="输入 CSV 路径")
    parser.add_argument("--topk", type=int, default=3, help="每个班取前 K 名")
    parser.add_argument("--outdir", default=".", help="输出目录")
    args = parser.parse_args()

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    # 1) 读数据
    df = pd.read_csv(args.input)

    # 2) 把 score / age 变成数字；丢掉 score 为空的行；age 为空用“同班中位数”补齐
    # 说明：用 pd.to_numeric(errors='coerce') 把乱七八糟的文本变成 NaN；
    #       再 dropna(subset=['score']) 丢掉没分数的行；
    #       对 age 用 groupby('class') 后的 transform(median) 来补。
    # ——在这里按上面的思路写代码——

    df['score'] = pd.to_numeric(df['score'],errors='coerce')
    df['age'] = pd.to_numeric(df['age'],errors='coerce')
    df = df.dropna(subset=['score'])
    mid = df.groupby('class')['age'].transform('median')
    df['age'] = df['age'].fillna(mid)


    # 3) 打标签：passed，level
    df["passed"] = df["score"].apply(lambda s: s >= 60) 
    # level 的规则：>=90 优秀；80–89 良好；60–79 及格；其他 不及格
    # ——在这里用 Series.apply(lambda x: ...) 写出 level 列——

    df['level'] = df['score'].apply(lambda x:"优秀" if x>=90 else("良好" if x>=80 else("及格" if x>=60 else"不及格")))

    # 4) 每个班内部做 z-score
    # 做法：g = df.groupby('class')['score']; 取 mean 和 std（std=0 时当 1）；
    # 再按 (score - mean) / std 算一个新列 zscore，保留 3 位小数。
    # ——在这里把 zscore 算出来并写入 df['zscore']——

    mean = df.groupby('class')['score'].transform('mean')
    std = df.groupby('class')['score'].transform('std')
    std = std.fillna(1)
    df['zscore'] = (df['score'] - mean) / std
    df['zscore'] = [round(x,3) for x in df['zscore']]

    # 5) 统计与导出
    # (a) (class, level) 的 avg_age / avg_score → summary.csv
    # 思路：groupby(['class','level']).agg({'age':'mean', 'score':'mean'}) 或者 groupby+apply
    # ——在这里把 summary 算好并 to_csv(outdir/'summary.csv')——

    result = df.groupby(['class','level']).agg({'age':'mean','score':'mean'})
    result.to_csv(outdir/'summary.csv')

    # (b) 每班 Top-K
    topk = (df.sort_values(["class", "score"], ascending=[True, False])
              .groupby("class")
              .head(args.topk))
    topk.to_csv(outdir / "topk.csv", index=False)

    # (c) 导出全量结果
    df.to_csv(outdir / "students_processed.csv", index=False)
    try:
        df.to_parquet(outdir / "students_processed.parquet", index=False)
    except Exception:
        pass

    # 打印一个简要榜单
    for cls, sub in topk.groupby("class"):
        names = ", ".join(f"{r.name}({r.score})" for r in sub.itertuples(index=False))
        print(f"class {cls} Top{args.topk}: {names}")

if __name__ == "__main__":
    main()
