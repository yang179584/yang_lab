#!/usr/bin/env bash

# 统计现在机器上有多少"在跑 Python 的用户"

count=$(ps -eo user,args | awk 'tolower($2) ~/^python/ {print $1}' | sort | uniq | wc -l)
echo "$count"
