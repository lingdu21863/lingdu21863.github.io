import os
import re
from pathlib import Path

data_dir = Path('data')

# Markdown转HTML函数
def md_to_html(md_text):
    html = md_text
    
    # 先处理表格
    lines = html.split('\n')
    result = []
    in_table = False
    table_lines = []
    table_count = 0
    
    for line in lines:
        stripped = line.strip()
        # 检查是否是表格行
        if '|' in stripped and (stripped.startswith('|') or stripped.endswith('|')):
            if all(c in '|-: ' for c in stripped.replace('|', '')):
                in_table = True
                table_lines.append(line)
            else:
                in_table = True
                table_lines.append(line)
        else:
            if in_table:
                if len(table_lines) >= 2:
                    # 构建表格
                    html_table = '<!-- TABLE_START --><table style="border-collapse: collapse; width: 100%; margin: 15px 0;">'
                    for i, row in enumerate(table_lines):
                        cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                        if i == 0:
                            html_table += '<tr>'
                            for cell in cells:
                                html_table += f'<th>{cell}</th>'
                            html_table += '</tr>'
                        elif i == 1:
                            continue
                        else:
                            html_table += '<tr>'
                            for cell in cells:
                                html_table += f'<td>{cell}</td>'
                            html_table += '</tr>'
                    html_table += '</table><!-- TABLE_END -->'
                    result.append(html_table)
                table_lines = []
                in_table = False
            result.append(line)
    
    if in_table and len(table_lines) >= 2:
        html_table = '<!-- TABLE_START --><table style="border-collapse: collapse; width: 100%; margin: 15px 0;">'
        for i, row in enumerate(table_lines):
            cells = [cell.strip() for cell in row.split('|') if cell.strip()]
            if i == 0:
                html_table += '<tr>'
                for cell in cells:
                    html_table += f'<th>{cell}</th>'
                html_table += '</tr>'
            elif i == 1:
                continue
            else:
                html_table += '<tr>'
                for cell in cells:
                    html_table += f'<td>{cell}</td>'
                html_table += '</tr>'
        html_table += '</table><!-- TABLE_END -->'
        result.append(html_table)
    
    html = '\n'.join(result)
    
    # 标题
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体和斜体
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # 代码
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # 链接
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # 引用块
    html = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 分割线
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)
    
    # 无序列表
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\* (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 有序列表
    html = re.sub(r'^\d+\. (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 段落处理 - 跳过表格区域
    lines = html.split('\n')
    in_paragraph = False
    in_table = False
    result = []
    
    for line in lines:
        stripped = line.strip()
        if '<!-- TABLE_START -->' in stripped:
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            in_table = True
            result.append(line.replace('<!-- TABLE_START -->', ''))
        elif '<!-- TABLE_END -->' in stripped:
            in_table = False
            result.append(line.replace('<!-- TABLE_END -->', ''))
        elif in_table:
            result.append(line)
        elif stripped == '':
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append('')
        elif (stripped.startswith('<h') or stripped.startswith('<table') or 
              stripped.startswith('<ul') or stripped.startswith('<ol') or 
              stripped.startswith('<li') or stripped.startswith('<pre') or 
              stripped.startswith('<code') or stripped.startswith('<blockquote') or
              stripped.startswith('<hr')):
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append(line)
        else:
            if not in_paragraph:
                result.append('<p>')
                in_paragraph = True
            result.append(line)
    
    if in_paragraph:
        result.append('</p>')
    
    html = '\n'.join(result)
    
    return html

# 处理所有md文件
for md_file in data_dir.glob('*.md'):
    print(f'Processing {md_file}...')
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = md_to_html(md_content)
    
    html_file = data_dir / f'{md_file.stem}.html'
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'Created {html_file}')

print('Done!')
