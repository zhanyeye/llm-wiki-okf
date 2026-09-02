# network-pilot 查询验收

> 本验收使用完全虚构的 demo 数据，严禁作为生产运维依据。

## 1. 查概念与具体约束

问题：`黄区和绿区有什么区别，绿区可以直接访问公网吗？`

预期检索：

1. 命中 `wiki/原子知识/虚构黄绿区网络模型.md`。
2. 引用 `#定义` 与 `#^demo-zone-boundary`，回答两区职责和禁止直连公网。
3. 仅在需要解释实现时沿关系到 `[[统一出口代理#稳定约束]]`。

通过条件：答案来自 Atomic 的具体标题/块，不从 Registry 推测概念，也不引入真实网络信息。

## 2. 查资产并回到技术定义

问题：`demo 出口代理是哪一套、入口和负责人在哪？`

预期检索：

1. 命中 `wiki/资源注册表/网络/虚构代理实例 demo-egress-proxy-01.md`。
2. 从 Registry 返回 `environment`、`owner` 和 `entries`。
3. 用户追问“它是什么”时沿 `technology` 到 `[[统一出口代理#定义]]`。

通过条件：实例事实来自 Registry，技术定义来自 Atomic，两者不混写。

## 3. 查操作并追溯依赖

问题：`demo 绿区服务怎样访问外部 HTTPS，失败后怎么回滚？`

预期检索：

1. 命中 `wiki/操作手册/绿色区域服务访问外部网络.md`。
2. 返回前置、步骤、验证和回滚，不省略“仅限 demo 绿区”的适用边界。
3. 沿 `operates_on` 找代理实例和区域规则，沿 `depends_on` 找 DNS 与证书约束。

通过条件：Runbook 可执行部分完整，所有稳定定义均链接到 L0/L1，没有复制出第二套规则。

## 4. FAQ 反向定位

问题：`黄区服务能不能照搬绿区外联流程？`

预期检索：

1. 命中 `wiki/常见问题/黄区服务能否使用绿区外联流程.md`。
2. 通过 `answers_about` 回到黄绿区规则块。
3. 明确回答“不能”，并链接适用的 Runbook 说明其边界，而不是建议修改真实网络。

## 机械验证

从父仓库根运行：

```powershell
python tools/okf-lint/okf_lint.py --root examples/network-pilot
```

预期结果：`0 error(s), 0 warning(s)`。
