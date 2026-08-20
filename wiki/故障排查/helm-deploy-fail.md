---
type: Playbook
title: Helm 部署失败
description: Helm 安装或升级失败时，复现命令、核对模板与集群组件是否匹配。
domain: k8s
tags: [helm, k8s, oncall]
status: draft
owner: infra-k8s
scope: [prod]
services: [rancher]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 症状

`helm install` / `helm upgrade` 报错；或 Rancher/流水线里工作负载达不到 Ready；事件中有钩子失败、校验失败、镜像拉不下来等。

# 影响

- 范围：该 release 所在 namespace / 环境。
- 严重度：视是否挡住发版；生产升级失败先评估回滚。

# 排查 / 止损路径

1. 先止损（若生产已半升级）：`helm rollback <release> <revision>`（revision 来自 `helm history`，不要猜）。
2. 在同一 kube-context 复现失败命令（加 `--debug`），保存完整 stderr。
3. 核对：集群版本与 chart `kubeVersion`；CRD / Ingress / StorageClass 是否存在；values 中的镜像仓库本环境是否可达。
4. 看 release 相关 Pod 事件与 [如何找到进程与日志](/资源注册表/find-process.md)。

集群入口见 [Rancher](/系统与架构/rancher.md)。不要在未写入 wiki 的情况下假设 chart 仓库地址。

# 常见根因

- values 与当前集群组件不匹配（Ingress class、CSI、准入 webhook）。
- 镜像或依赖 chart 在内网拉不到。
- 钩子 Job 失败但主负载看似已创建。

# 升级条件

- 回滚后仍失败，或涉及集群级 CRD/准入：升级 k8s 值班，带上 `helm history`、失败日志、目标集群名。

# 相关文档

- 手册：待补各业务 chart 的发版 Runbook
- 架构：[Rancher](/系统与架构/rancher.md)
