# 完全虚构来源：demo DNS 与证书资产草稿

> 本文中的域名、URL、证书、人员和日期均完全虚构，只能用于 demo，严禁用于生产。

虚构企业 DNS `DemoDNS` 负责 `demo.example.invalid` 的内部解析，控制台为 `https://dns-console.example.invalid`，负责人是 `demo-dns-team`。绿区演示域名 `api.green.demo.example.invalid` 的记录由它托管，请求路径是“演示客户端 → DemoDNS → 绿区演示 API”。TTL 固定为 60 秒，只用于试点验证。该域名使用下述虚构内部证书。

虚构内部证书能力 `DemoCA` 只签发 demo 服务证书，不签发公网证书。证书实例 `demo-green-wildcard-cert` 覆盖 `*.green.demo.example.invalid`，演示到期时间为 2027-06-30T00:00:00Z，负责人 `demo-pki-team`，申请入口 `https://pki-request.example.invalid`。私钥不得进入知识库；试点只记录申请入口。证书观测页为 `https://cert-dashboard.example.invalid`。

草稿还写到：若 DNS 能解析但 HTTPS 报证书不受信任，应先确认 demo 客户端是否安装 DemoCA 的虚构信任包；它不是生产故障处置建议。
