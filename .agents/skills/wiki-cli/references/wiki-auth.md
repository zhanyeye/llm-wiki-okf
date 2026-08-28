# wiki auth — 认证管理

所有 wiki 命令（除 `auth` 自身、`--version`、`completion`、`update`、`uninstall`）执行前都会检查认证状态，未认证时退出码 3。

## 两种认证模式

| 模式 | 适用场景 | 启用方式 | 凭证存储 |
|-|-|-|-|
| **A1 帐密模式** | 本地开发、交互式终端 | `wiki auth login` 按提示输入工号 + 密码 | 本地凭证文件（由 `wiki_cli.config.auth` 管理） |
| **A2 token 模式** | CI/CD、远程容器、无人值守 | `wiki auth token` 按提示输入工号 + A2 token | 本地凭证文件  |

## 命令

```bash
# A1 帐密模式登录（交互式，按提示输入工号 + 密码）
wiki auth login

# A2 token 模式设置（交互式，按提示输入工号 + A2 token）
wiki auth token

# 查看认证状态（模式 + 是否有效）
wiki auth status

# 退出登录（清除本地凭证）
wiki auth logout
```

## 决策树

1. **用户是windows环境** → A1 帐密模式：`wiki auth login`
2. **用户是linux环境** → A2 token 模式：`wiki auth token`，并需告知用户手动生成token指导文档链接：https://wki.test.com/domains/3679/wiki/345613/WIKI2026060811388935
3. **不确定当前是哪种模式** → `wiki auth status` 查看
