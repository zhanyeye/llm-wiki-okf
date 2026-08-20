---
type: Runbook
title: 文件服务器磁盘满处理
description: 磁盘使用率告警后的定位、清理与验证步骤。
domain: storage
tags: [storage, disk, nfs, oncall]
status: draft
owner: infra-storage
scope: [prod]
services: [nfs, minio]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 触发条件

文件服务器或 NFS 数据盘使用率告警；或业务报无法写入、NFS 卡住（先排除 [NFS 卡住](/案例与复盘/nfs-stuck.md) 是否为锁/客户端问题）。

# 何时用 / 何时不用

- 用：确认是容量问题（`df` 高，且业务写失败与 inode/空间相关）。
- 不用：纯网络中断、权限、或 MinIO 逻辑层问题——改看 [MinIO](/系统与架构/minio.md) 与对应排查页。

# 前置检查

1. 环境 / 权限：能登录该文件服务器或管理节点（申请见注册表，不写密钥）。
2. 窗口 / 变更单：生产清理前确认可删目录清单，避免误删发布件。

# 步骤

在目标机执行（把 `<mount>` 换成实际挂载点）：

```bash
df -h <mount>
df -i <mount>
du -xhd1 <mount> | sort -h
```

按 `du` 结果逐层下钻。只删除事先约定的缓存/过期目录；不确定的路径停手并升级存储值班。

若对象存储侧空间问题，先看 [MinIO](/系统与架构/minio.md)，不要在本页假设桶名。

# 验证

1. `df -h` 回落到告警阈值以下。
2. 业务写探测或让报障方重试。

# 回滚

清理操作通常不可逆。若误删，走备份/快照恢复（恢复手册待补）。未删之前不要「先 rm 再说」。

# 相关系统

- [MinIO](/系统与架构/minio.md)
- [如何找到进程与日志](/资源注册表/find-process.md)（确认是哪台文件服务器）
