---
title: "GitHub Pages + Jekyll 搭建博客教程"
date: 2025-06-17
categories: [技术]
tags: [GitHub, Jekyll, 教程]
excerpt: "详细记录使用 GitHub Pages 和 Jekyll 搭建个人博客的过程。"
---

## 前言

本文记录了使用 GitHub Pages 和 Jekyll 搭建个人博客的完整过程。

## 什么是 Jekyll？

Jekyll 是一个静态站点生成器，非常适合用于搭建博客。GitHub Pages 原生支持 Jekyll，无需额外配置即可使用。

## 搭建步骤

### 1. 创建仓库

在 GitHub 创建一个名为 `username.github.io` 的仓库。

### 2. 创建配置文件

创建 `_config.yml` 文件：

```yaml
title: "我的博客"
description: "记录学习与生活"
author: "username"
url: "https://username.github.io"
```

### 3. 创建布局文件

在 `_layouts` 目录下创建布局模板：

- `default.html` - 默认布局
- `post.html` - 文章布局
- `page.html` - 页面布局

### 4. 创建文章

在 `_posts` 目录下创建文章，文件名格式为 `YYYY-MM-DD-title.md`。

## 优点

- **免费托管**：GitHub Pages 完全免费
- **简单易用**：使用 Markdown 写作
- **版本控制**：文章有完整的版本历史
- **自定义域名**：支持绑定自定义域名

## 总结

Jekyll + GitHub Pages 是搭建个人博客的绝佳选择，简单、免费、高效。
