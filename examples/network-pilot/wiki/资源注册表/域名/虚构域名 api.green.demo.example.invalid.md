---
type: Registry
id: asset:domain:api-green-demo-example-invalid
layer: registry
title: 虚构域名 api.green.demo.example.invalid
description: 完全虚构的 demo 绿区 API 域名注册信息。
domain: network
tags: [完全虚构, demo, network-pilot]
status: draft
generated:
  by: agent/cursor
  at: 2026-09-02T09:47:00Z
stale_after: 2027-03-01T00:00:00Z
sources:
  - raw/01-网络边界与出口讨论.md
  - raw/02-DNS证书资产草稿.md
asset_kind: domain
name: api.green.demo.example.invalid
environment: demo
owner: fictional-demo-dns-team
technology:
  - "[[企业 DNS#定义]]"
depends_on:
  - "[[虚构黄绿区网络模型#^demo-zone-boundary]]"
  - "[[虚构证书 demo-green-wildcard-cert#资产]]"
dns: DemoDNS（完全虚构）
certificate: "[[虚构证书 demo-green-wildcard-cert#资产]]"
entries:
  url: https://api.green.demo.example.invalid
source_of_truth: 完全虚构的 network-pilot raw 来源
sync_mode: manual
---


## 资产

本页及其中所有名称、地址、负责人和流程均完全虚构，仅用于 demo 试点，严禁用于生产。

`api.green.demo.example.invalid` 是虚构绿区演示 API 的稳定域名。

## 位置与环境

环境为 `demo`；位于虚构绿区，不对应任何真实地址。

## 入口

演示 URL：`https://api.green.demo.example.invalid`。

## 负责人

`fictional-demo-dns-team`，该名称完全虚构。

## 依赖

DNS 使用 [[企业 DNS#定义]]；证书使用 [[虚构证书 demo-green-wildcard-cert#资产]]；请求路径为“演示客户端 → DemoDNS → 绿区演示 API”。

## 观测与告警

来源未写告警；只规定通过虚构 DNS 控制台观察记录。

## 生命周期

仅随 network-pilot 的 demo 环境存在，试点结束后删除。

## 凭证怎么申请

不适用；域名本身无凭证，控制台权限由虚构负责人审批。
