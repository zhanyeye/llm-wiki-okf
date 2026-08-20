---
type: Decision
title: MinIO 对象存储
description: DataOps 对象存储采用 MinIO 的选型背景、放弃项与后续约束。
domain: storage
tags: [minio, storage, dataops]
status: draft
owner: infra-storage
scope: [prod]
services: [minio]
generated: { by: human:infra-team, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources: []
---

# 背景

- 要解决的问题：DataOps / 流水线需要 S3 兼容对象存储（发布件、缓存、数据集）。对应存量「DataOps对象存储设计方案（MinIO）」。
- 约束：内网部署、与现有流水线凭证模型兼容、容量可扩。具体容量与集群数迁入时补，不在此编造。

# 决策与放弃项

- 选择：MinIO 作为对象存储，系统说明见 [MinIO](/系统与架构/minio.md)。
- 放弃：把对象语义做在 NFS 上 — 语义与并发不适合该负载；NFS 故障模式见 [NFS 卡住](/案例与复盘/nfs-stuck.md)。

# 影响与约束

- 对运维：按桶/前缀管理生命周期与容量；磁盘告警走 [磁盘满](/操作手册/disk-full.md) 时要分清文件服务器 vs MinIO 数据盘。
- 此后不能轻易改的前提：客户端按 S3 API 对接；更换实现需迁移全部 endpoint 与密钥申请流程（密钥本身不写进知识库）。

# 落地手册

- [MinIO](/系统与架构/minio.md)
- 负载均衡与可靠性分析（存量标题，待迁入）
