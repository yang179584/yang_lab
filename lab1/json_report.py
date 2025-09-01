# -*- coding: utf-8 -*-
"""
实验四：函数与文件操作（JSON 版）
目标：学会函数定义与文件读写 + 基础 JSON 数据处理（不使用正则）

数据约定：
- 输入 JSON 文件为“交易列表”，每个元素形如：
  {"id": 1, "category": "food", "amount": 23.5}

任务：
1) 创建一个示例 sample.json（交易列表）:
cat > sample.json << 'EOF'
[
  {"id": 1, "category": "food",   "amount": 23.5},
  {"id": 2, "category": "books",  "amount": 45},
  {"id": 3, "category": "food",   "amount": 12.3},
  {"id": 4, "category": "travel", "amount": 120.0},
  {"id": 5, "category": "books",  "amount": 30}
]
EOF

2) 定义 load_data(filename)：读取 JSON 并返回 Python 对象（list[dict]）
3) 定义 summarize(data)：返回汇总 dict，包含：
   - count: 交易条数
   - total_amount: 金额合计
   - avg_amount: 平均金额（保留两位小数）
   - max_transaction: 金额最大的那条交易（dict 或 None）
   - by_category: 各类别计数（dict）
4) 定义 save_report(report, out_filename)：把汇总写到 JSON 文件
5) 从命令行参数接收文件名，调用以上函数，并提示报告已保存  

示例：
运行命令python json_report.py sample.json
"""


import sys
import json
from collections import Counter
from typing import List, Dict, Any


def load_data(filename: str) -> List[Dict[str, Any]]:
    """读取 JSON 文件并返回数据列表。"""
    # ===== 步骤 1：读取文件并 json.load（已留指引）=====
    # TODO：完成读取与解析
    with open (filename ,'r',encoding = 'utf-8') as f:
        data = json.load(f)
    return data


def summarize(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """对交易数据做汇总统计。"""
    count = len(data)

    # ===== 步骤 2：提取金额并计算 total / avg（挖空）=====
    # 提示：用列表推导提取 amount；注意空列表时 avg 设为 0.0
    # TODO：
    total = sum([item['amount'] for item in data])
    if count == 0:
        avg = 0.0
    else:
        avg = round( total / count ,2)

    # ===== 步骤 3：找到金额最大的交易（挖空）=====
    # TODO：使用 max(data, key=...)；空数据时返回 None
    if count == 0:
        max_tran = None
    else:
        max_tran = max(data, key = lambda x: x['amount'])

    # ===== 步骤 4：按类别计数（挖空）=====
    # TODO：从每个 tx 中取出 category，使用 Counter 统计后转为普通 dict
    category = [tx['category'] for tx in data]
    tx_count = Counter(category)
    by_category = dict(tx_count)

    # TODO：组合为报告字典并返回
    report = {
        'count': count,
        'total_amount': total,
        'avg_amount': avg,
        'max_transaction': max_tran,
        'by_category': by_category
    }


def save_report(report: Dict[str, Any], out_filename: str = "report.json") -> None:
    """将汇总结果写入 JSON 文件。"""
    # ===== 步骤 5：写文件（挖空）=====
    # TODO：使用 json.dump 保存，确保使用 UTF-8，缩进 2，ensure_ascii=False
    with open ( out_filename,'w',encoding = 'utf-8' ) as f:
        json.dump (report ,f ,indent = 2 ,ensure_ascii = False)


def main():
    # ===== 命令行参数处理（已写好）=====
    if len(sys.argv) < 2:
        print("用法：python json_report.py <json文件>")
        return
    filename = sys.argv[1]

    try:
        data = load_data(filename)
        report = summarize(data)
        save_report(report, "report.json")
        print("已生成报告：report.json")  # 本实验只提示保存成功，不打印详细数据

    except FileNotFoundError:
        print(f"文件未找到：{filename}")
    except json.JSONDecodeError:
        print("JSON 解析失败：请检查文件是否为合法 JSON。")


if __name__ == "__main__":
    main()
