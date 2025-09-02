# -*- coding: utf-8 -*-
"""
【实验题目】用 *args / **kwargs 做三个小工具：拼 URL、一起处理多列、把好几个字典合成一个
【实验目的】
- 你经常会遇到“不确定有多少个参数”的情况，这就需要会用 *args（装一串位置参数）和 **kwargs（装一堆 key=value）。
- 本实验让你做三个特别常用的小工具：把网址拼起来、把好几列数据一口气处理、把配置/结果合成一个“总字典”。

【你要做什么（一步步来）】

1) 写 multi_map(func, *iterables, **kwargs)：
   - 给你好几个长度一样的序列（比如两列数字），你要“按位置一一配对”交给 func 处理，然后把每次的结果收集到一个列表里返回。
   - 举例：func 是 (x*y)*scale，两个输入序列是 [1,2,3] 和 [4,5,6]，scale=10，就得到 [40,100,180]。

2) 写 deep_merge(*dicts, list_policy="extend")：
   - 好几个字典，从左到右合并：
     * 同一个 key，如果对应的值“还是字典”，就继续往里合（递归）；
     * 如果它们是“列表”，看策略：
         - "extend"：直接拼接起来（a + b）
         - "overwrite"：后者把前者覆盖掉
     * 其他类型（比如数字、字符串）直接“后者覆盖前者”。
   - 返回一个“合成大字典”。

【运行示例】
# 直接运行本文件：
#   python 2.py
# 你应该能在终端看到两段输出：
#   1) multi_map 的结果
#   2) deep_merge 合并后的字典

【小贴士】
- *args 就是把“多出来的位置参数”都收集起来变成一个元组；
- **kwargs 就是把“多出来的 key=value”都收集起来变成一个字典；
- zip 可以把多个序列“按位置对齐”。
"""

from urllib.parse import quote_plus



def multi_map(func, *iterables, **kwargs):
    # 把多个等长序列 zip 起来，逐组喂给 func，并把结果装进列表
    return [func(*items, **kwargs) for items in zip(*iterables)]

def deep_merge(*dicts, list_policy="extend"):
    # 写一个内部的 merge(a, b) 来干活
    # 逻辑（人话版）：
    # - 如果 a 和 b 都是“字典”：那就“逐个 key”进去合并（递归）
    # - 如果 a 和 b 都是“列表”：要么拼接（extend），要么直接用 b 覆盖（overwrite）
    # - 其他类型：直接 b 覆盖 a
    # ——在这里实现 merge，并从左到右把所有 dict 合起来——

    def merge(a,b):
        result = a.copy()

        for key,value in b.items():
            if key in result:
                if isinstance (result[key],dict) and isinstance (value,dict):
                    result[key] = merge(result[key],value)

                elif isinstance (result[key],list) and isinstance (value,list):
                    if list_policy =="extend":
                        result[key] = result[key] + value
                    elif list_policy =="overwrite":
                        result[key] = value
                
                else:
                    result[key] = value
            else:
                result[key] = value

        return result

    final_result = {}
    for x in dicts:
        final_result = merge(final_result,x)  

    return final_result  # TODO: 把合并后的大字典返回

if __name__ == "__main__":

    # 测试 1：multi_map（点积 * 10 → [40, 100, 180]）
    print(multi_map(lambda x, y, scale=1: (x * y) * scale,
                    [1, 2, 3], [4, 5, 6], scale=10))

    # 测试 2：deep_merge（b 覆盖 a 的冲突项；列表按策略处理）
    a = {"a": 1, "b": {"x": [1], "y": 2}}
    b = {"b": {"x": [2, 3], "y": 9}, "c": 7}
    print(deep_merge(a, b, list_policy="extend"))
