import os
import re
import shutil
import yaml
from datetime import datetime, date

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SITE_DIR, '_site')

def parse_frontmatter(text):
    if not text.startswith('---\n'):
        return {}, text
    end = text.find('\n---\n', 4)
    if end == -1:
        end = text.find('\n---', 4)
    if end == -1:
        return {}, text
    fm = yaml.safe_load(text[4:end])
    content = text[end + 4:].strip()
    return fm or {}, content

def markdown_to_html(text):
    lines = text.split('\n')
    result = []
    in_list = False
    in_code = False
    code_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('```'):
            if in_code:
                code = '\n'.join(code_lines)
                result.append(f'<pre><code>{escape_html(code)}</code></pre>')
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        
        if line.startswith('| ') and '|' in line[2:] and i + 1 < len(lines) and re.match(r'^\|[\s\-:]+\|', lines[i + 1]):
            result.append('<table>')
            headers = [c.strip() for c in line.split('|')[1:-1]]
            result.append('<tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>')
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].split('|')[1:-1]]
                result.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')
                i += 1
            result.append('</table>')
            continue
        
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            result.append(f'<h{level}>{title}</h{level}>')
            i += 1
            continue
        
        if line.startswith('> '):
            result.append(f'<blockquote>{process_inline(line[2:])}</blockquote>')
            i += 1
            continue
        
        if re.match(r'^[\-\*\+] ', line):
            result.append('<ul>')
            while i < len(lines) and re.match(r'^[\-\*\+] ', lines[i]):
                item = re.sub(r'^[\-\*\+] ', '', lines[i])
                result.append(f'<li>{process_inline(item)}</li>')
                i += 1
            result.append('</ul>')
            continue
        
        if re.match(r'^\d+\. ', line):
            result.append('<ol>')
            while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
                item = re.sub(r'^\d+\. ', '', lines[i])
                result.append(f'<li>{process_inline(item)}</li>')
                i += 1
            result.append('</ol>')
            continue
        
        if line.startswith('---'):
            result.append('<hr>')
            i += 1
            continue
        
        if line.strip() == '':
            result.append('')
            i += 1
            continue
        
        result.append(f'<p>{process_inline(line)}</p>')
        i += 1
    
    return '\n'.join(result)

def process_inline(text):
    text = escape_html(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', text)
    return text

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def render_template(template, variables):
    result = template
    for key, value in variables.items():
        result = result.replace('{{ ' + str(key) + ' }}', str(value))
        result = result.replace('{{ ' + str(key) + ' | ', '')
    result = re.sub(r'\{\{.+?\}\}', '', result)
    result = re.sub(r'\{\%.+?\%\}', '', result)
    return result

def load_config():
    config_path = os.path.join(SITE_DIR, '_config.yml')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}

def load_layout(name):
    path = os.path.join(SITE_DIR, '_layouts', name + '.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        fm, html = parse_frontmatter(content)
        return html or content
    return '{{ content }}'

def build_page(page_path, output_path, config, posts=None):
    with open(page_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    fm, md_content = parse_frontmatter(text)
    html_content = markdown_to_html(md_content)
    layout_name = fm.get('layout', 'default')
    layout = load_layout(layout_name)
    
    if posts and layout_name == 'home':
        posts_html = build_posts_list(posts)
        html_content = build_home_content(fm, posts)
    
    title = fm.get('title', config.get('title', ''))
    site_title = config.get('title', '')
    
    page_vars = {
        'content': html_content,
        'title': fm.get('title', ''),
        'date': str(fm.get('date', '')),
        'categories': ', '.join(fm.get('categories', [])),
        'tags': ', '.join(fm.get('tags', [])),
        'excerpt': fm.get('excerpt', ''),
        'description': fm.get('description', config.get('description', '')),
        'author': fm.get('author', config.get('author', '')),
    }
    
    site_vars = {
        'site.title': site_title,
        'site.description': config.get('description', ''),
        'site.author': config.get('author', ''),
        'site.time': datetime.now(),
        'site.lang': config.get('lang', 'zh-CN'),
        'page.url': '/' + os.path.relpath(output_path, OUTPUT_DIR).replace('\\', '/'),
    }
    
    full_content = layout
    
    if '{% if page.title %}' in full_content:
        if title:
            full_content = full_content.replace(
                '{% if page.title %}{{ page.title }} | {{ site.title }}{% else %}{{ site.title }}{% endif %}',
                f'{title} | {site_title}'
            )
        else:
            full_content = full_content.replace(
                '{% if page.title %}{{ page.title }} | {{ site.title }}{% else %}{{ site.title }}{% endif %}',
                site_title
            )
    
    full_content = full_content.replace('{{ page.title | default: site.title }}', title or site_title)
    full_content = full_content.replace('{{ page.title }}', title)
    full_content = full_content.replace('{{ page.description | default: site.description }}', fm.get('description', config.get('description', '')))
    full_content = full_content.replace('{{ page.excerpt | strip_html | truncatewords: 50 }}', fm.get('excerpt', ''))
    full_content = full_content.replace('{{ page.author }}', fm.get('author', config.get('author', '')))
    full_content = full_content.replace('{{ site.time | date: "%Y" }}', str(datetime.now().year))
    full_content = full_content.replace('{{ site.title }}', site_title)
    full_content = full_content.replace("{{ site.lang | default: 'zh-CN' }}", 'zh-CN')
    
    if '{{ content }}' in full_content:
        full_content = full_content.replace('{{ content }}', html_content)
    
    full_content = full_content.replace("{{ '/' | relative_url }}", '/')
    full_content = full_content.replace("{{ '/about/' | relative_url }}", '/about/')
    full_content = full_content.replace("{{ '/words/' | relative_url }}", '/words/')
    
    full_content = re.sub(r'\{\{ site\.\w+ \| date: [^}]+\}\}', '', full_content)
    full_content = re.sub(r'\{\{ [^}]+\}\}', '', full_content)
    full_content = re.sub(r'\{\%[^%]*\%\}', '', full_content)
    full_content = re.sub(r'\| [^}]+\}\}', '}}', full_content)
    
    if '{% seo %}' in full_content:
        full_content = full_content.replace('{% seo %}', '')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

def build_posts_list(posts):
    html = '<ul class="post-list card">\n'
    for post in posts:
        date_str = post['date'].strftime('%Y年%m月%d日') if isinstance(post['date'], (date, datetime)) else str(post['date'])
        html += '    <li>\n'
        html += f'        <h2 class="post-title"><a href="{post["url"]}">{post["title"]}</a></h2>\n'
        html += f'        <div class="post-meta"><time>{date_str}</time>'
        if post.get('categories'):
            html += f' · {", ".join(post["categories"])}'
        if post.get('tags'):
            html += f' · {", ".join(post["tags"])}'
        html += '</div>\n'
        if post.get('excerpt'):
            html += f'        <p class="post-excerpt">{post["excerpt"]}</p>\n'
        html += f'        <a href="{post["url"]}" class="read-more">阅读全文 →</a>\n'
        html += '    </li>\n'
    html += '</ul>'
    return html

def build_home_content(fm, posts):
    html = '<div class="card">\n'
    html += f'    <h1 class="page-title">{fm.get("title", "最新文章")}</h1>\n'
    if fm.get('description'):
        html += f'    <p class="post-excerpt">{fm["description"]}</p>\n'
    html += '</div>\n'
    html += build_posts_list(posts)
    return html

def get_posts():
    posts_dir = os.path.join(SITE_DIR, '_posts')
    posts = []
    if os.path.exists(posts_dir):
        for fname in sorted(os.listdir(posts_dir), reverse=True):
            if fname.endswith('.md'):
                fpath = os.path.join(posts_dir, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    text = f.read()
                fm, _ = parse_frontmatter(text)
                if fm:
                    name = fname.replace('.md', '')
                    parts = name.split('-', 3)
                    if len(parts) >= 3:
                        slug = parts[3] if len(parts) > 3 else name
                        fm['url'] = f'/posts/{parts[0]}/{parts[1]}/{parts[2]}/{slug}/'
                    else:
                        fm['url'] = f'/{name}.html'
                    fm['_file'] = fpath
                    fm['date'] = fm.get('date', datetime.now())
                    posts.append(fm)
    return posts

def build_post(post, config):
    fpath = post['_file']
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    fm, md_content = parse_frontmatter(text)
    html_content = markdown_to_html(md_content)
    layout = load_layout('post')
    
    title = fm.get('title', '')
    site_title = config.get('title', '')
    date_str = ''
    if fm.get('date'):
        d = fm['date']
        if isinstance(d, (date, datetime)):
            date_str = d.strftime('%Y年%m月%d日')
        else:
            date_str = str(d)
    
    full_content = layout.replace('{{ content }}', html_content)
    full_content = full_content.replace('{{ page.title }}', title)
    full_content = full_content.replace('{{ page.date | date: "%Y年%m月%d日" }}', date_str)
    full_content = full_content.replace('{{ page.author }}', str(fm.get('author', config.get('author', ''))))
    full_content = full_content.replace('{{ page.categories | join: ", " }}', ', '.join(fm.get('categories', [])))
    full_content = full_content.replace('{{ page.tags | join: ", " }}', ', '.join(fm.get('tags', [])))
    full_content = full_content.replace('{{ page.date | date_to_xmlschema }}', '')
    full_content = re.sub(r'\{\{ [^}]+\}\}', '', full_content)
    
    page_vars = {
        'title': title,
        'site.title': site_title,
        'site.time': datetime.now(),
        'content': html_content,
    }
    
    default_layout = load_layout('default')
    default_layout = default_layout.replace('{{ content }}', full_content)
    default_layout = default_layout.replace('{{ page.title | default: site.title }}', title or site_title)
    default_layout = default_layout.replace('{{ page.title }}', title)
    default_layout = default_layout.replace('{{ page.description | default: site.description }}', fm.get('description', config.get('description', '')))
    default_layout = default_layout.replace('{{ site.title }}', site_title)
    default_layout = default_layout.replace("{{ site.lang | default: 'zh-CN' }}", 'zh-CN')
    default_layout = default_layout.replace("{{ '/' | relative_url }}", '/')
    default_layout = default_layout.replace("{{ '/about/' | relative_url }}", '/about/')
    default_layout = default_layout.replace("{{ '/words/' | relative_url }}", '/words/')
    default_layout = default_layout.replace("{{ site.time | date: '%Y' }}", str(datetime.now().year))
    default_layout = re.sub(r'\{\{ [^}]+\}\}', '', default_layout)
    default_layout = re.sub(r'\{\%.+?\%\}', '', default_layout)
    
    if '{% seo %}' in default_layout:
        default_layout = default_layout.replace('{% seo %}', '')
    
    output_path = os.path.join(OUTPUT_DIR, post['url'].lstrip('/'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if output_path.endswith('/'):
        output_path = os.path.join(output_path, 'index.html')
    if not output_path.endswith('.html'):
        output_path = os.path.join(output_path, 'index.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(default_layout)

def main():
    print("Building site...")
    
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    config = load_config()
    posts = get_posts()
    
    for post in posts:
        build_post(post, config)
    print(f"  Built {len(posts)} posts")
    
    build_page(os.path.join(SITE_DIR, 'index.md'), os.path.join(OUTPUT_DIR, 'index.html'), config, posts)
    print("  Built index.html")
    
    build_page(os.path.join(SITE_DIR, 'about.md'), os.path.join(OUTPUT_DIR, 'about', 'index.html'), config)
    print("  Built about/index.html")
    
    for folder in ['words']:
        src = os.path.join(SITE_DIR, folder)
        dst = os.path.join(OUTPUT_DIR, folder)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  Copied {folder}/")
    
    print(f"\nSite built in {OUTPUT_DIR}")
    print("Run: python -m http.server 4000 -d _site")

if __name__ == '__main__':
    main()