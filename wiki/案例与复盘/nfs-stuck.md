---
type: Incident
title: 数据回传 NFS 卡住
description: NFS 卡住导致数据回传失败的复盘骨架。可复用检查项应回写手册。
domain: storage
tags: [nfs, storage, oncall]
status: draft
owner: infra-storage
scope: [prod]
services: [nfs]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 时间线

| 时间 | 事件 |
|------|------|
| <待补> | 业务报数据回传卡住 / 超时 |
| <待补> | 查客户端 D 状态、NFS server 负载与锁 |
| <待补> | 恢复（重启客户端挂载 / 处理 server 侧） |

本页是存量标题「数据回传-NFS卡住问题定位」的骨架，细节迁入时补时间与命令输出。不要编造已发生过的主机名。

# 根因

常见方向（写入时删掉不适用的）：客户端 RPC 超时、server 磁盘满（见 [磁盘满](/操作手册/disk-full.md)）、锁、网络抖动、nfsd 线程耗尽。

# 修复

当时采取的步骤（迁入时填写）。临时 umount/remount 前确认是否有未落盘写。

# 行动项

| 项 | 回写到 | 负责人 |
|----|--------|--------|
| 磁盘满时的标准清理 | [磁盘满](/操作手册/disk-full.md) | infra-storage |
| 卡住时的检查顺序 | 待建 Playbook：NFS 卡住 | infra-storage |
