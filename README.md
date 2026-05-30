# lingdu21863.github.io

零度的个人博客，使用 Jekyll 搭建，部署在 GitHub Pages 上。

## 🌟 站点功能

### 📝 博客

记录学习与生活的点滴，分享知识和经验。

- 文章列表展示
- 分类标签支持
- 代码语法高亮
- 响应式设计

### 📖 单词朗读器

在线英语单词朗读工具，支持：

- **7 种词库**：初中、高中、四级、六级、考研、托福、SAT
- **语音朗读**：使用 Web Speech API
- **自动播放**：可调节间隔时间
- **语速调节**：0.5x - 2.0x
- **键盘快捷键**：↑↓ 切换单词，空格播放/暂停

访问地址：[https://lingdu21863.github.io/words/](https://lingdu21863.github.io/words/)

## 📁 目录结构

```
├── _config.yml          # Jekyll 配置文件
├── _layouts/            # 布局模板
│   ├── default.html     # 默认布局
│   ├── home.html        # 首页布局
│   ├── post.html        # 文章布局
│   └── page.html        # 页面布局
├── _posts/              # 博客文章
├── index.md             # 首页
├── about.md             # 关于页面
├── words/               # 单词朗读器
│   ├── index.html
│   ├── style.css
│   └── script.js
└── *.txt                # 词库文件
```

## 🚀 本地运行

### 前置要求

- Ruby 2.5.0 或更高版本
- RubyGems
- GCC 和 Make

### 安装步骤

1. 安装 Jekyll 和 Bundler：
   ```bash
   gem install jekyll bundler
   ```

2. 克隆仓库：
   ```bash
   git clone https://github.com/lingdu21863/lingdu21863.github.io.git
   cd lingdu21863.github.io
   ```

3. 安装依赖：
   ```bash
   bundle install
   ```

4. 启动本地服务器：
   ```bash
   bundle exec jekyll serve
   ```

5. 浏览器访问 `http://localhost:4000`

## ✍️ 写作指南

### 创建新文章

在 `_posts` 目录下创建文件，命名格式为 `YYYY-MM-DD-title.md`：

```markdown
---
title: "文章标题"
date: 2025-06-15
categories: [分类]
tags: [标签1, 标签2]
---

文章内容...
```

### 创建新页面

在根目录创建 `.md` 文件：

```markdown
---
layout: page
title: "页面标题"
---

页面内容...
```

## 🛠️ 技术栈

- [Jekyll](https://jekyllrb.com/) - 静态站点生成器
- [GitHub Pages](https://pages.github.com/) - 免费托管
- [Markdown](https://www.markdownguide.org/) - 文章写作
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) - 语音合成

## 📄 许可证

MIT License
