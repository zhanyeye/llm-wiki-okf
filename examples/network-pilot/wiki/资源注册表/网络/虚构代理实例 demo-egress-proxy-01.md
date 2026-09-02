---
type: Registry
id: asset:network:demo-egress-proxy-01
layer: registry
title: 虚构代理实例 demo-egress-proxy-01
description: 完全虚构的 demo 绿区统一出口代理实例。
domain: network
tags: [完全虚构, demo, network-pilot]
status: draft
generated:
  by: agent/cursor
  at: 2026-09-02T09:47:00Z
stale_after: 2027-03-01T00:00:00Z
sources:
  - raw/01-网络边界与出口讨论.md
  - raw/03-绿区访问演练记录.md
asset_kind: network
name: demo-egress-proxy-01
environment: demo
owner: fictional-demo-network-team
technology:
  - "[[统一出口代理#定义]]"
depends_on:
  - "[[企业 DNS#职责与边界]]"
runbooks:
  - "[[绿色区域服务访问外部网络#步骤]]"
entries:
  console: https://proxy-console.example.invalid
  dashboard: https://proxy-dashboard.example.invalid
  health: https://egress-health.example.invalid
source_of_truth: 完全虚构的 network-pilot raw 来源
sync_mode: manual
---


## 资产

本页及其中所有名称、地址、负责人和流程均完全虚构，仅用于 demo 试点，严禁用于生产。

`demo-egress-proxy-01` 是虚构绿区统一出口代理的唯一演示实例。

## 位置与环境

环境为 `demo`，虚构代理地址为 `demo-egress-proxy-01.demo.example.invalid:8443`。

## 入口

控制台 `https://proxy-console.example.invalid`；观测页 `https://proxy-dashboard.example.invalid`；健康页 `https://egress-health.example.invalid`。

## 负责人

`fictional-demo-network-team`，该名称完全虚构。

## 依赖

技术基线为 [[统一出口代理#定义]]，目标主机名解析依赖 [[企业 DNS#职责与边界]]。

## 观测与告警

虚构观测页记录目标主机名、结果和延迟；来源未写告警阈值。

## 生命周期

network-pilot 存续期间保留，试点结束删除。

## 凭证怎么申请

控制台权限由虚构负责人审批；来源没有也不应包含凭证。
