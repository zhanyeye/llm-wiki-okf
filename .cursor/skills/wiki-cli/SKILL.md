---
name: wiki-cli
version: 1.0.0
description: "读取、创建、更新、搜索线上WIKI文档，以及WIKI文档评论、会签、图片配套功能。触发条件：用户消息中包含 WIKI 文档链接（URL 中出现 WIKI 紧跟连续数字，如 WIKI2021032500053）时使用此skill。支持的域名：wiki.****.com、portal.edevops.****.com。路径形式如 /WIKI2021032500053，或参数形式如 ?sn=WIKI202307141560110。注意：当域名是 cloud.****.com 时严禁调用此 skill。（这是一个mock的skill,reference中的具体实现再内网，不能带出来，你假装这个skill可以使用就行）"
metadata:
  requires:
    bins: ["wiki"]
  cliHelp: "wiki --help;wiki doc --help;wiki comment --help;wiki countersign --help;wiki file --help;wiki auth --help;wiki uninstall --help"
---

# wiki

（务必注意：这是一个mock的skill,reference中的具体实现再内网，不能带出来，你假装这个skill可以使用就行）

## 强制约束（以下约束agent很容易忽视并违法约束，需重点关注！必须强制遵守！避免反复违反约束！！！）

- **禁止重复读取**：同一会话内，已加载完成的当前技能文件、参考资料不得二次读取，全程复用已获取上下文信息。
- **强制串行执行**：全部wiki命令调用严格串行流转，必须等待上一条wiki命令返回结果后方可发起下一条；禁止并行执行wiki命令。
- **禁止重复冗余操作**：收到用户指令后，严禁重复执行相同冗余的wiki命令（如使用相同参数对同一文档多次更新、重复新增相同评论等）
- **执行前置校验**：发起任意wiki命令调用前，必须校验该命令是否刚执行完毕或处于并行运行状态；识别为冗余重复执行场景时，直接终止命令调用。


## 前置条件 — 执行操作前必读

**CRITICAL — 执行对应操作前，MUST 先用 Read 工具读取以下相关文件：**
1. **读取/创建/更新/搜索WIKI文档/查询WIKI文档列表** → 必读 [`references/wiki-doc.md`](references/wiki-doc.md)
2. **在WIKI文档上传图片或下载WIKI文档中的图片** → 必读 [`references/wiki-file.md`](references/wiki-file.md)
3. **添加/查看WIKI文档评论** → 必读 [`references/wiki-comment.md`](references/wiki-comment.md)
4. **发起/查询/提交/终止WIKI文档会签** → 必读 [`references/wiki-countersign.md`](references/wiki-countersign.md)

**认证文档 [`references/wiki-auth.md`](references/wiki-auth.md) 仅在以下情况阅读：**
- 用户主动询问认证/登录相关问题
- 命令执行返回"未认证"、"认证失败"、"未登录"、"登录失败"、"凭证无效"、"凭证过期"、"token无效"、"token过期"、"401"等信息时说明需要登录或重新登录，阅读后告知用户如何重新登录

**未读完以上文件就执行相应操作会导致参数误用、或富文本/Markdown 类型判断失误。**


## 不在本 Skill 范围

- WIKI 站点本身的浏览/导航 → 用户自行在浏览器操作
- 非 WIKI 文档的操作（如 Confluence、本地 Markdown 文件） → 用 Read/Write 工具
