---
type: Registry
id: asset:certificate:demo-green-wildcard-cert
layer: registry
title: 虚构证书 demo-green-wildcard-cert
description: 完全虚构的 demo 绿区通配证书注册信息。
domain: network
tags: [完全虚构, demo, network-pilot]
status: draft
generated:
  by: agent/cursor
  at: 2026-09-02T09:47:00Z
stale_after: 2027-03-01T00:00:00Z
sources:
  - raw/02-DNS证书资产草稿.md
asset_kind: certificate
name: demo-green-wildcard-cert
environment: demo
owner: fictional-demo-pki-team
technology:
  - "[[内部证书#定义]]"
covered_domains:
  - "*.green.demo.example.invalid"
expires_at: 2027-06-30T00:00:00Z
runbooks:
  - "[[绿色区域服务访问外部网络#前置检查]]"
entries:
  request: https://pki-request.example.invalid
  dashboard: https://cert-dashboard.example.invalid
source_of_truth: 完全虚构的 network-pilot raw 来源
sync_mode: manual
---


## 资产

本页及其中所有名称、地址、负责人和流程均完全虚构，仅用于 demo 试点，严禁用于生产。

`demo-green-wildcard-cert` 是由虚构 DemoCA 签发的演示证书，覆盖 `*.green.demo.example.invalid`。

## 位置与环境

仅用于 `demo` 绿区；私钥位置不记录，也不存在真实私钥。

## 入口

虚构申请入口：`https://pki-request.example.invalid`；观测入口：`https://cert-dashboard.example.invalid`。

## 负责人

`fictional-demo-pki-team`，该名称完全虚构。

## 依赖

依赖 [[内部证书#定义]]；被 [[虚构域名 api.green.demo.example.invalid#依赖]] 使用。

## 观测与告警

通过虚构证书观测页查看到期状态；来源未写告警规则。

## 生命周期

演示到期时间为 `2027-06-30T00:00:00Z`；续期流程来源未写，当前由虚构负责人手工处理。

## 凭证怎么申请

通过虚构申请入口提出 demo 请求；不得在知识库中提交私钥或令牌。
