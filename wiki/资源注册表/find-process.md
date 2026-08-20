---
type: Registry
title: 如何找到进程与日志
description: 找不到服务、进程、目录或容器日志时，按集群或 VM 查找的入口。不存凭证。
domain: k8s
tags: [oncall, locator, logs]
status: draft
owner: infra
scope: [prod]
services: [rancher]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 资源

目标：某个微服务 / 守护进程的 **所在集群或主机、PID/容器、工作目录、日志路径**。本页是查找路径，不是某服务的专属台账。

# 环境

| 环境 | 集群 / 主机 | 备注 |
|------|-------------|------|
| 已纳管 k8s | 见 [Rancher](/系统与架构/rancher.md) | 先按 workload / 命名空间搜 |
| 未纳管 VM | `<env>` 下的主机清单（待补台账） | `ps` / 端口 / `/proc` |

# 入口

- 控制台：Rancher 集群搜索（URL 待写入该集群台账）
- 日志：容器内路径、宿主机 docker/containerd、kubelet、节点 `dmesg`、ELK（以实际接入为准，缺哪条写哪条待补）
- 进程 / 目录：VM 上 `ss`/`netstat` 对端口 → PID → `/proc/<pid>/cwd` 与 `root`

# 负责人

- 主责：该服务台账上的 owner（无台账则值班组）
- 升级：集群 / 中间件 owner

# 依赖

- 上游：Rancher 或 SSH 跳板权限（申请途径见下，不写密钥）
- 下游：日志系统

# 告警

- 本页不对应单一告警；常从「服务不可用 / 重启」工单进来。

# 凭证怎么申请

- Rancher：走团队权限申请，找 k8s 值班。
- 主机 SSH：走堡垒机 / 主机组申请，找 VM owner。
- 日志平台：走对应平台账号申请。

不要把密码、kubeconfig、token 写进本页。
