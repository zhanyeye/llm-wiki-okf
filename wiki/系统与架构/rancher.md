---
type: Architecture
title: Rancher
description: Kubernetes 集群纳管入口：职责、用法边界与相关操作。
domain: k8s
tags: [rancher, k8s]
status: draft
owner: infra-k8s
scope: [prod]
services: [rancher]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 职责与边界

- 负责：导入/纳管集群、工作负载与项目视图、部分权限入口。
- 不负责：宿主机 OS、物理/虚拟机生命周期（见 VM 相关手册，待入库）。
- 适用 / 不适用：集群已接入 Rancher 时，优先从这里找 workload；未纳管的 VM 走 [如何找到进程与日志](/资源注册表/find-process.md)。

# 拓扑 / 请求路径 / 数据流

1. 浏览器 / API → Rancher
2. Rancher → 目标集群 kube-apiserver
3. 调度到节点上的 Pod / 进程

控制台 URL、集群名列表放注册表，本页不写死内网地址。

# 依赖

- 相关注册表：[如何找到进程与日志](/资源注册表/find-process.md)
- 依赖：目标集群 API、认证源

# 相关文档

- 手册：导入集群、部署 Rancher（存量标题，待迁入）
- 排查：[Helm 部署失败](/故障排查/helm-deploy-fail.md)
