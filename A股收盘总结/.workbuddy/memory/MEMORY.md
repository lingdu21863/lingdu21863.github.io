# A股收盘总结 - 项目记忆

## 项目概述
- 每日生成A股收盘总结HTML报告，存放在项目根目录
- 文件命名格式：`A股收盘总结_YYYYMMDD.html`
- 报告格式：固定HTML模板，红色主题（涨红跌绿，中国股市惯例）

## 报告结构
1. 标题横幅（日期+核心摘要）
2. 主要指数收盘（9个指数卡片）
3. 市场统计（涨跌家数/涨停跌停/成交额）
4. 申万一级行业涨跌幅（条形图）
5. 热点概念板块追踪（表格）
6. 重点个股明细（表格）
7. 主力资金净流入TOP10（表格）
8. 市场催化因素（列表）
9. 机构观点（文本框）
10. 页脚（数据来源+免责声明）

## 数据获取方式
- **westock-data技能**：CLI路径为 `C:\Users\Administrator\AppData\Local\Programs\WorkBuddy\resources\app.asar.unpacked\resources\builtin-skills\westock-data\scripts\index.js`，需用 Node.js 运行（非全局命令）
- 常用命令：`quote`（指数/个股行情）、`market-overview`（大盘画像）、`changedist`（涨跌分布）、`sector ranking`（板块排名）、`hot stock`（热搜）、`fund flow`（资金流向）
- **WebSearch**：补充获取市场新闻、催化因素、机构观点等定性信息

## 关键指数代码
- sh000001(上证)、sz399001(深证成指)、sz399006(创业板)、sh000688(科创50)
- sh000300(沪深300)、sh000016(上证50)、sh000852(中证1000)、bj899050(北证50)
