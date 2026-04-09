#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描data目录下的所有.md文件，生成索引文件data/index.json
"""

import os
import json
import re

def generate_index():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    index_file = os.path.join(data_dir, 'index.json')
    
    # 获取所有.md文件
    md_files = []
    if os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            if filename.endswith('.md'):
                # 提取日期（假设文件名格式为 YYYY-MM-DD.md）
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})\.md$', filename)
                if date_match:
                    md_files.append(date_match.group(1))
    
    # 排序
    md_files.sort()
    
    # 写入索引文件
    index_data = {
        "files": md_files,
        "lastUpdated": ""
    }
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"索引文件已生成: {index_file}")
    print(f"共发现 {len(md_files)} 个MD文件:")
    for f in md_files:
        print(f"  - {f}.md")

if __name__ == '__main__':
    generate_index()
