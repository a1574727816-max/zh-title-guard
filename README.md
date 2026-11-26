# zh-title-guard（中文标题守护）

一个轻量的 **Google Antigravity** 全局规则插件，解决「明明用中文提问，但只要夹杂英文软件名/技术词，侧边栏对话标题就会自动生成英文」的问题。

## 为什么会这样？

Antigravity 会在新对话开始时由后台独立模型生成侧边栏标题（`annotations.title`）。当首条消息中出现 `OpenWrt`、`WireGuard`、`Excel`、`Docker`、`Git` 等英文术语时，后台标题模型容易整体切换到英文输出，且客户端目前没有“锁定标题语言”的开关。

## 插件如何工作

插件仅包含一条全局规则（`rules/AGENTS.md`）与一个零依赖 Python 标准库脚本（`scripts/title_guard.py`）：

1. 当你用中文开启一个**新对话**时，Agent 会在**首轮回复结束前**执行一次检查脚本，调用本地 `ConversationService/GetConversation` 查看当前标题。
2. 若当前标题已包含中文（输出 `OK: ...`）或当前是子代理（输出 `SKIP_SUBAGENT`），直接跳过，不做任何修改。
3. 若当前标题为空或纯英文（输出 `NEEDS_ZH: ...`），Agent 会根据对话主题提炼一个 6–18 字的简体中文标题，并通过 `ConversationService/UpdateConversation` 自动写入侧边栏。
4. 后续轮次不会重复检查。

## 目录结构

```text
zh-title-guard/
├── plugin.json            # 插件清单
├── rules/
│   └── AGENTS.md          # 全局规则（首轮自检 + 简体中文回复约束）
├── scripts/
│   └── title_guard.py     # 本地 ConversationService 读写脚本（仅使用 Python 标准库）
└── README.md
```

## 安装方式

要求本机已安装 Python 3.8+。

### 方式一：克隆到 Antigravity 全局插件目录（推荐）

**Windows (PowerShell):**

```powershell
git clone https://github.com/a1574727816-max/zh-title-guard.git "$env:USERPROFILE\.gemini\config\plugins\zh-title-guard"
```

**macOS / Linux:**

```bash
git clone https://github.com/a1574727816-max/zh-title-guard.git ~/.gemini/config/plugins/zh-title-guard
```

### 方式二：直接让 Antigravity Agent 帮你安装

把下面这句话发给 Antigravity 即可：

> 请帮我安装这个 Antigravity 插件：https://github.com/a1574727816-max/zh-title-guard ，克隆到 `~/.gemini/config/plugins/zh-title-guard` 并验证已加载。

安装后无需重启，从下一个新建对话起自动生效；也可在 **Customizations** 面板中随时开启、关闭或卸载。

## License

MIT
