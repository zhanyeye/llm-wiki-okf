---
type: Atomic
id: atomic:network:demo-enterprise-dns
layer: atomic
title: 企业 DNS
description: 完全虚构的 DemoDNS 职责、内部解析方式与稳定约束。
domain: network
tags: [完全虚构, demo, network-pilot]
status: draft
generated:
  by: agent/cursor
  at: 2026-09-02T09:47:00Z
stale_after: 2027-03-01T00:00:00Z
sources:
  - raw/02-DNS证书资产草稿.md
kind: platform
aliases: [DemoDNS]
---


## 定义

本页及其中所有名称、地址、负责人和流程均完全虚构，仅用于 demo 试点，严禁用于生产。

DemoDNS 是完全虚构的 `demo` 内部名称解析平台。

## 职责与边界

它负责 `demo.example.invalid` 的内部解析，不承诺公网解析，也不代表任何真实企业 DNS。

## 公司内使用方式

试点服务通过 DemoDNS 解析内部演示域名；虚构控制台是 `https://dns-console.example.invalid`。

## 稳定约束

`demo.example.invalid` 记录的演示 TTL 为 60 秒。变更只允许由虚构负责人 `demo-dns-team` 在 demo 控制台完成。 ^demo-dns-ttl

## 关系

[[虚构域名 api.green.demo.example.invalid#依赖]] 是该能力的虚构 Registry 示例；HTTPS 还需 [[内部证书#定义]]。
