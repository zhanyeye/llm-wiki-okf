---
type: Configuration
title: 绿区转发代理
description: 绿区 Nginx / HAProxy 转发配置的适用范围、参数与变更验证。
domain: network
tags: [nginx, haproxy, proxy, network]
status: draft
owner: infra-network
scope: [通用区]
services: [nginx, haproxy]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 适用范围

- 环境：绿区 / 通用区入口（具体 VIP 与机器写注册表，本页不编造）。
- 组件：Nginx 或 HAProxy，以该入口实际组件为准。

# 参数表

| 参数 | 含义 | 典型值 | 备注 |
|------|------|--------|------|
| `listen` | 监听地址端口 | `<vip>:<port>` | |
| `backend` | 上游 | `<host>:<port>` | 与健康检查一起改 |
| `timeout` | 超时 | 按业务 SLA | 过小会误杀长请求 |

# 变更步骤

1. 备份：拷贝当前配置到带时间戳的文件。
2. 修改：只改工单中的 server/backend；语法检查（`nginx -t` 或 `haproxy -c -f <file>`）。
3. 生效：优雅 reload，避免 drop 已有连接（具体信号以该版本文档为准）。

# 验证

1. 配置测试命令退出码 0。
2. 从约定探测路径看 HTTP 状态与 upstream。
3. 相关证书未在本次误替换（证书切换另页，待入库）。

# 周边影响

- 可能影响到的服务：所有经该入口的微服务域名。
- DNS / 证书：本页只改转发；域名申请与证书切换不要混在一次变更里。
