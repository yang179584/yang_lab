# -*- coding: utf-8 -*-
"""
【实验题目】给定若干异常类型，学生只需补 try/except 串起主流程
【目的】
- 我们已经把“配置信息不对 / 数据不对 / 计算没法做”这三种情况的异常类写好；
- 读配置 → 读数据 → 过滤求平均 的函数也给你写好了；
- 在 main() 里基于try/except将整个流程串起来

【运行示例】
# 正常：
#   python 3.py --config config.json --csv values.csv
# 越界配置（触发配置异常）：
#   python 3.py --config config_bad.json --csv values.csv
"""

import argparse, json, sys
import pandas as pd


# ============== 异常类：简单实现（已完成） ==============
class AppError(Exception):
    """应用内通用异常基类（可选）。"""
    pass

class ConfigError(AppError):
    """配置相关错误：缺字段、类型不对、取值越界等。"""
    pass

class DataError(AppError):
    """数据相关错误：读文件失败、缺列、没有有效数字等。"""
    pass

class ComputationError(AppError):
    """计算阶段失败：例如过滤后无数据。"""
    pass


# ============== 功能函数：已实现好，无需学生修改 ==============
def load_config(path: str) -> dict:
    """读取并校验配置：threshold ∈ [0,100] 且 mode ∈ {'fast','accurate'}。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"配置文件不存在：{path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"配置文件不是合法 JSON：{e}")

    if "threshold" not in cfg or "mode" not in cfg:
        raise ConfigError("缺少 threshold 或 mode")

    # threshold 校验
    try:
        thr = float(cfg["threshold"])
    except Exception:
        raise ConfigError("threshold 必须是数字")
    if not (0 <= thr <= 100):
        raise ConfigError("threshold 必须在 [0,100] 内")

    # mode 校验
    mode = str(cfg["mode"]).lower()
    if mode not in {"fast", "accurate"}:
        raise ConfigError('mode 只能是 "fast" 或 "accurate"')

    return {"threshold": thr, "mode": mode}


def load_values(csv_path: str):
    """读取 CSV 的一列 x → 数值 → 去空；若无有效数据则抛 DataError。"""
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise DataError(f"数据文件不存在：{csv_path}")
    except Exception as e:
        raise DataError(f"读取 CSV 失败：{e}")

    if "x" not in df.columns:
        raise DataError("CSV 必须包含列名 'x'")

    x = pd.to_numeric(df["x"], errors="coerce").dropna()
    if x.empty:
        raise DataError("没有有效数据（列 x 转换后全是空）")

    return x


def compute(values, threshold: float, mode: str) -> float:
    """筛选 ≥threshold 后求平均；按 mode 决定保留小数位；空集抛 ComputationError。"""
    filt = values[values >= threshold]
    if filt.empty:
        raise ComputationError("过滤后无数据")
    mean = float(filt.mean())
    return round(mean, 4 if mode == "accurate" else 2)


# ============== 学生只需要在这里补 try/except ==============
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--csv", required=True)
    args = ap.parse_args()

    #TODO: 请在这里写 try/except，整个流程串起来
    try:
        cfg = load_config(args.config)         # 读配置
        vals = load_values(args.csv)           # 读数据
        result = compute(vals, cfg["threshold"], cfg["mode"])  # 计算
        print("平均值：", result)

    except ConfigError as e:
        print(f"配置错误:{e}")

    except DataError as e:
        print(f"数据错误：{e}")
        
    except ComputationError as e:
        print(f"计算错误：{e}")


if __name__ == "__main__":
    main()
