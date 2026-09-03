# review

人工语义审核 `draft`、已过期或被更正的知识页。lint 通过只表示结构可解析；本流程判断知识是否完整、准确、原子化并正确关联。

## 列待审清单

1. 搜索 `wiki/` 中 `status: draft`、无 `verified`、`stale_after` 已过或来源刷新后被改回 draft 的页面。
2. 按关联的 `wiki/_meta/ingest/*.yaml` 聚合同一来源的产出，避免只看其中一页。
3. 每批默认最多 5 组来源；列出基础知识（Atomic）、Registry、Runbook/FAQ/ADR 产出、coverage gap 和原始来源。
4. 不读取无关页面；只沿 manifest、语义关系和 backlinks 打开审核所需内容。

## 审核清单

逐组来源核对：

### 来源覆盖

- manifest 的提取项确实覆盖来源中的实体、事实、命令、数字、限制、遗留项和不确定性。
- `compiled/duplicate` 目标表达与来源一致；`excluded/gap` 的理由成立。
- 没有为了简短而删除有效技术细节，也没有把模型常识写成内网事实。

### 原子边界

- Atomic（`wiki/基础知识/`）一页是一个内部概念或平台，不混入多个可独立更新的系统，也不写某套生产实例入口。
- 不把每句话拆成文件；页内标题/块是可复用、稳定的知识单元。
- 同一实体没有因不同来源生成平行副本；别名与同名异物已正确消歧。

### 分层与关系

- Registry 只写真实稳定资产/实例，`technology` 指向正确 Atomic。
- Runbook/FAQ/Decision 等上层页精确引用下层标题/块，没有复制出冲突定义。
- `depends_on`、`operates_on`、`answers_about`、`decides_for` 的关系方向与来源一致。
- 反向关系可由 backlinks 得出，不要求双写；同批/同目录没有被误当关系。

### 可运维性

- Registry 的入口、负责人、环境、观测、生命周期和资产种类画像完整；未知项明确标 gap。
- Runbook 有适用范围、前置、可执行步骤、验证、必要回滚和升级条件。
- 不含密码、密钥、token、kubeconfig；入口和申请方式可保留。

## 审核结果

只接受三种结果：

1. **通过**：人明确说“通过/OK”并给出可记录身份后，才将相关页改为 `status: stable`，写：

   ```yaml
   verified:
     by: human:<id>
     at: <ISO-8601>
   ```

   `stale_after` 按知识变化速度设置；Registry 通常短于稳定概念。

2. **需修改**：列出具体页面、标题/块和修改原因；页面保持 `draft`，按 ingest 用户更正流程修复并重跑 Validate/lint。
3. **废弃**：只有人明确确认后改 `status: deprecated`，正文说明替代页；不直接删除有历史引用的页面。

Agent 不得根据“lint 通过”、自己的判断或用户沉默写 `verified`。审核完成后按 `index-log.md` 追加一条一事的 Update/Deprecation 记录。
