---
type: Architecture
title: MinIO
description: 对象存储：职责边界、请求链路，以及相关注册表与手册。
domain: storage
tags: [minio, storage]
status: draft
owner: infra-storage
scope: [prod]
services: [minio]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 职责与边界

- 负责：对象存储（桶、发布件/缓存等业务数据）。细节以落地环境为准。
- 不负责：块存储、NFS 文件共享。NFS 相关见 [数据回传 NFS 卡住](/案例与复盘/nfs-stuck.md)。
- 适用 / 不适用：选型背景见 [MinIO 对象存储](/架构决策记录/minio-object-storage.md)。

# 拓扑 / 请求路径 / 数据流

1. 业务或流水线客户端（S3 API）
2. 负载入口（若有）→ MinIO 节点
3. 后端磁盘 / 纠删或副本

具体主机与控制台入口写在注册表，不在本页编造地址。

# 依赖

- 相关注册表：待补 MinIO 台账页
- 依赖：磁盘容量、网络、证书（若 TLS 终结在入口）

# 相关文档

- 手册：[磁盘满](/操作手册/disk-full.md)
- 排查：发布件非最新等案例待迁入
- 决策：[MinIO 对象存储](/架构决策记录/minio-object-storage.md)
