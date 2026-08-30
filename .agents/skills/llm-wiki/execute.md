# execute

按 Runbook / Playbook 执行操作（「帮我跑磁盘水位脚本」「安装毕昇编译器」等）。这是查询之外的独立操作：查询找页，execute 改变被管系统。

1. 在 `wiki/` 找到对应 Runbook / Playbook 页面（走 [query.md](query.md) 查询流程）。
2. 检查 frontmatter `automation.ready`：
   - **`true`** → 读 `automation.script_ref`，用 Bash 执行 `script/<name>/<file>`，传参来自 `automation.params`，按 `automation.exit_codes` 判定执行结果
   - **`partial`** → 按正文步骤手动执行（命令逐条给用户确认或由 Agent 按参数组装命令）
   - **无 automation 块 / `false`** → 按正文步骤指导用户操作
3. 执行前确认前置条件（Runbook「前置检查」小节）。
4. 执行后运行验证步骤（Runbook「验证」/ Playbook 对应确认步骤）。
5. 执行结果按 `**Execution**` 动词追加到 `wiki/log.md`（格式见 [references/index-log.md](references/index-log.md)：链到对应 Runbook / Playbook 页，附退出码与一句话结果）。

**安全边界**：只读 / 低风险脚本可直接执行；涉及以下内容时需人工确认：

- 删除数据（`rm -rf`、`TRUNCATE`）
- 重启 / 停止服务或工作负载
- 对多台主机、多命名空间批量执行
- 修改认证/密钥配置
- 生产环境变更
- 没有回滚步骤的操作
