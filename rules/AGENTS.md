# 中文会话与侧边栏标题守护规则

1. **回复语言**：当用户使用中文交流时，始终使用自然流畅的简体中文回复（保留代码、命令、文件路径、专有名词及原文引用）。
2. **新对话首轮标题自检**（每个新对话仅在**首轮**执行一次，后续轮次与子代理无需重复执行）：
   - 当用户首条消息包含中文时，在首轮结束给出最终回复前，运行本插件 `scripts/title_guard.py`（默认位于 `~/.gemini/config/plugins/zh-title-guard/scripts/title_guard.py`）检查当前标题：
     `python -c "import os,runpy; runpy.run_path(os.path.expanduser('~/.gemini/config/plugins/zh-title-guard/scripts/title_guard.py'), run_name='__main__')"`
   - 若输出以 `OK:`、`SKIP` 开头，说明当前标题已包含中文或无需处理，直接结束即可。
   - 若输出以 `NEEDS_ZH:` 开头，请根据对话主题提炼一个简洁的简体中文标题（建议 6–18 字，可保留必要英文产品/技术名），再运行一次更新命令：
     `python -c "import os,sys,runpy; sys.argv=[os.path.expanduser('~/.gemini/config/plugins/zh-title-guard/scripts/title_guard.py'), '你的中文标题']; runpy.run_path(sys.argv[0], run_name='__main__')"`
