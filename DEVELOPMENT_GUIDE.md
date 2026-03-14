# Learning Check-in Skill 开发指南

> 📚 工具功能、架构设计和升级注意事项的完整文档  
> 目的：确保未来开发新功能时不再出错

---

## 📋 目录

1. [工具概述](#工具概述)
2. [核心功能](#核心功能)
3. [技术架构](#技术架构)
4. [版本管理](#版本管理)
5. [升级检查机制](#升级检查机制)
6. [升级注意事项](#升级注意事项)
7. [常见错误](#常见错误)
8. [新功能开发流程](#新功能开发流程)

---

## 工具概述

### 基本信息

| 项目 | 值 |
|------|-----|
| **名称** | Learning Check-in |
| **类型** | 学习打卡工具 |
| **版本** | v2.0.1 (当前最新) |
| **定位** | 纯本地、离线、隐私优先 |
| **依赖** | 仅 Python 标准库 |
| **平台** | Windows, Linux, macOS |

### 设计理念

```
✅ 100% 离线可用（核心功能不依赖网络）
✅ 零外部依赖（只用标准库）
✅ 隐私优先（所有数据本地存储）
✅ 简单易用（3 个核心命令）
✅ 轻量级检查更新（可选网络功能）
```

---

## 核心功能

### 用户命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `init` | 初始化新用户 | `--nickname`, `--country` | `python checkin_cli.py init --nickname Daisy --country CN` |
| `checkin` | 每日打卡 | `--note` (可选) | `python checkin_cli.py checkin --note "Studied Python"` |
| `status` | 查看状态 | 无 | `python checkin_cli.py status` |

### 数据存储

**存储位置：**
- Windows: `%APPDATA%\learning-checkin\`
- Linux/macOS: `~/.learning-checkin/`

**数据结构：**
```
learning-checkin/
├── user_config.json      # 当前用户配置
└── users/
    └── {user_id}/
        ├── profile.json  # 用户资料
        ├── streak.json   # 连续打卡记录
        └── checkins/
            └── YYYY-MM-DD.json  # 每日打卡记录
```

### 打卡规则

1. **每日至少打卡 1 次**
2. **连续打卡自动计数**
3. **每周 ≥2 天未打卡 = 任务失败**（v1.0.0 功能，v2.0.0 已移除）
4. **失败后可随时重新加入**

---

## 技术架构

### 文件结构

```
learning-checkin/
├── checkin_cli.py        # CLI 入口（含版本检查）
├── requirements.txt      # 依赖列表（空，无外部依赖）
├── setup.py             # 包安装配置
├── README.md            # 使用说明
├── SKILL.md             # Skill 描述
├── LICENSE              # MIT 许可证
├── .gitignore           # Git 忽略规则
└── src/
    ├── __init__.py      # 模块导出
    └── local_skill.py   # 核心业务逻辑
```

### 核心模块

#### 1. `checkin_cli.py` - CLI 入口

**职责：**
- 命令行参数解析
- 调用核心功能
- **自动检查更新**（v2.0.1+）

**关键代码：**
```python
# 版本号（⚠️ 每次发布必须更新！）
__version__ = "v2.0.1"
__repo__ = "daizongyu/learning-checkin"

def check_update():
    """检查 GitHub 最新版本"""
    try:
        import urllib.request
        url = f"https://api.github.com/repos/{__repo__}/releases/latest"
        # ... 2 秒超时，静默失败
    except Exception:
        pass  # 网络失败时不干扰主功能

def main():
    args = parser.parse_args()
    check_update()  # 每次运行都检查
    # ... 执行命令
```

#### 2. `src/local_skill.py` - 核心逻辑

**职责：**
- 用户初始化
- 打卡执行
- 状态查询
- 数据存储

**核心类：**
```python
class LocalCheckinSkill:
    def init_user(self, nickname, country) -> dict
    def do_checkin(self, user_id, note='') -> dict
    def get_status(self, user_id) -> dict
```

#### 3. `src/__init__.py` - 模块导出

```python
from .local_skill import LocalCheckinSkill
__version__ = "2.0.0"  # 注意：这里没有 v 前缀
```

---

## 版本管理

### 版本号规范

**格式：** `v{主版本}.{次版本}.{修订号}`

| 版本 | 说明 | 示例 |
|------|------|------|
| 主版本 | 重大变更，不向后兼容 | v1.0.0 → v2.0.0 |
| 次版本 | 新功能，向后兼容 | v2.0.0 → v2.1.0 |
| 修订号 | Bug 修复，向后兼容 | v2.0.0 → v2.0.1 |

### 版本历史

| 版本 | 日期 | 说明 | 状态 |
|------|------|------|------|
| v1.0.0 | 2026-03-13 | 网络版（GitHub 中心化仓库） | ❌ 已废弃 |
| v2.0.0 | 2026-03-14 | 纯本地版（移除所有网络功能） | ✅ |
| v2.0.1 | 2026-03-14 | 本地版 + 轻量级检查更新 | ✅ 最新 |

### 发布流程

```bash
# 1. 更新版本号（⚠️ 必须！）
# 编辑 checkin_cli.py: __version__ = "vX.Y.Z"

# 2. 提交更改
git add checkin_cli.py
git commit -m "fix: Update version to vX.Y.Z"
git push

# 3. 创建 tag（带注释）
git tag -a vX.Y.Z -m "Release description..."

# 4. 推送 tag
git push origin vX.Y.Z

# 5. 在 GitHub 创建 Release
# https://github.com/daizongyu/learning-checkin/releases/new
```

---

## 升级检查机制

### 工作原理

```
用户运行命令
    ↓
check_update() 被调用
    ↓
请求 GitHub API: /repos/{repo}/releases/latest
    ↓
获取最新 tag_name
    ↓
比较：latest_version != __version__ ?
    ↓
是 → 显示更新提示
否 → 静默继续
    ↓
（网络失败时静默忽略）
```

### 代码实现

```python
def check_update():
    """
    Check for updates from GitHub (lightweight, non-blocking)
    Uses urllib (standard library) - no external dependencies
    """
    try:
        import urllib.request
        
        url = f"https://api.github.com/repos/{__repo__}/releases/latest"
        
        # Set timeout to 2 seconds, fail silently
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Learning-Checkin-CLI'}
        )
        
        with urllib.request.urlopen(request, timeout=2) as response:
            data = json.loads(response.read())
            latest_version = data.get('tag_name', '')
            
            # Compare versions
            if latest_version and latest_version != __version__:
                print(f"\n💡 New version available: {latest_version} (current: {__version__})")
                print(f"   Update: git pull origin main")
                print(f"   Release: https://github.com/{__repo__}/releases/latest\n")
    except Exception:
        # Silently ignore any network errors
        pass
```

### 关键特性

| 特性 | 实现方式 |
|------|---------|
| **无外部依赖** | 使用 `urllib.request`（标准库） |
| **非阻塞** | 2 秒超时，不等待 |
| **静默失败** | 网络错误时不报错、不中断主功能 |
| **每次运行都检查** | 在 `main()` 中调用 |
| **仅提示不自动更新** | 用户手动 `git pull` |

---

## 升级注意事项 ⚠️

### 🚨 必须检查的清单

每次发布新版本前，**必须**完成以下检查：

#### 1. 版本号同步（❗ 最重要）

**检查位置：**
- [ ] `checkin_cli.py` 第 26 行：`__version__ = "vX.Y.Z"`
- [ ] `src/__init__.py`：`__version__ = "X.Y.Z"`（无 v 前缀）

**常见错误：**
```python
# ❌ 错误：忘记更新版本号
__version__ = "v2.0.0"  # 实际发布的是 v2.0.1

# 后果：用户下载 v2.0.1 后，每次运行都提示更新到 v2.0.1
```

**正确做法：**
```python
# ✅ 正确：版本号与 tag 一致
__version__ = "v2.0.1"  # 发布 v2.0.1 时
```

#### 2. Git Tag 管理

**检查清单：**
- [ ] 删除旧 tag（如果需要重新创建）
- [ ] 创建带注释的 tag：`git tag -a vX.Y.Z -m "..."`
- [ ] 推送 tag：`git push origin vX.Y.Z`
- [ ] 在 GitHub 创建 Release

**常见错误：**
```bash
# ❌ 错误：tag 指向旧 commit
git tag v2.0.1  # 没有 -a 注释
git push origin v2.0.1

# ✅ 正确：
git tag -a v2.0.1 -m "Release description..."
git push origin v2.0.1 --force  # 如果需要覆盖
```

#### 3. 依赖检查

**检查清单：**
- [ ] `requirements.txt` 保持为空（或仅注释）
- [ ] 没有添加 `import requests` 等外部库
- [ ] 只使用 Python 标准库

**允许的标准库：**
```python
✅ os, sys, json
✅ datetime
✅ urllib.request（用于检查更新）
✅ argparse
✅ typing
```

**禁止的外部库：**
```python
❌ requests
❌ urllib3
❌ aiohttp
❌ 任何需要 pip install 的库
```

#### 4. 网络功能检查

**检查清单：**
- [ ] 核心功能（init, checkin, status）不依赖网络
- [ ] 网络请求有超时设置（2 秒）
- [ ] 网络失败时静默处理（不报错）
- [ ] 用户可以在完全离线环境下使用

#### 5. 文档更新

**检查清单：**
- [ ] `README.md` 更新版本号和功能说明
- [ ] `SKILL.md` 更新版本信息
- [ ] Release Notes 描述新功能

---

## 常见错误

### 错误 1：版本号不匹配

**症状：** 用户下载最新版本后，每次运行都提示更新

**原因：** `__version__` 没有更新到最新 tag

**解决方案：**
```python
# 发布 v2.0.1 时，必须更新：
__version__ = "v2.0.1"  # ✅
```

**预防措施：**
- 在发布流程中，**先更新版本号，再创建 tag**
- 使用脚本自动检查版本号

### 错误 2：添加外部依赖

**症状：** 用户运行时报错 `ModuleNotFoundError: No module named 'requests'`

**原因：** 不小心使用了非标准库

**解决方案：**
```python
# ❌ 错误
import requests

# ✅ 正确（使用标准库）
import urllib.request
```

**预防措施：**
- 在 `requirements.txt` 中保持空文件
- 代码审查时检查 import 语句

### 错误 3：网络请求阻塞主功能

**症状：** 离线环境下命令执行很慢或报错

**原因：** 网络请求没有超时或异常处理

**解决方案：**
```python
# ✅ 正确：超时 + 静默失败
try:
    with urllib.request.urlopen(request, timeout=2) as response:
        # ...
except Exception:
    pass  # 不干扰主功能
```

### 错误 4：Tag 指向错误 commit

**症状：** Release 中的代码与实际发布的不一致

**原因：** 创建 tag 前没有提交最新代码

**解决方案：**
```bash
# ✅ 正确流程
git add .
git commit -m "..."
git push
git tag -a vX.Y.Z -m "..."  # 在最新 commit 上打 tag
git push origin vX.Y.Z
```

---

## 新功能开发流程

### 步骤 1：需求分析

```
□ 新功能是否违反"纯本地"原则？
□ 是否需要添加外部依赖？
□ 是否影响现有功能？
□ 是否需要更新文档？
```

### 步骤 2：开发实现

```
□ 在正确的文件中添加代码
□ 保持向后兼容
□ 添加适当的错误处理
□ 编写测试用例
```

### 步骤 3：版本号更新

```
□ 确定版本类型（主/次/修订）
□ 更新 checkin_cli.py 的 __version__
□ 更新 src/__init__.py 的 __version__
```

### 步骤 4：测试验证

```
□ 本地测试所有命令
□ 离线环境测试
□ 检查更新功能测试
□ 验证版本号显示正确
```

### 步骤 5：发布流程

```bash
# 1. 提交代码
git add .
git commit -m "feat: Add new feature"
git push

# 2. 更新版本号
# 编辑 checkin_cli.py: __version__ = "vX.Y.Z"
git add checkin_cli.py
git commit -m "fix: Update version to vX.Y.Z"
git push

# 3. 创建 tag
git tag -a vX.Y.Z -m "Release notes..."
git push origin vX.Y.Z

# 4. GitHub Release
# https://github.com/daizongyu/learning-checkin/releases/new
```

### 步骤 6：发布后验证

```
□ 下载 Release 源码测试
□ 验证版本号显示正确
□ 验证检查更新功能正常
□ 更新 ClawHub（如适用）
```

---

## 检查清单模板

### 发布前检查清单

```markdown
## 发布前检查

### 代码
- [ ] 所有新功能已测试
- [ ] 没有添加外部依赖
- [ ] 网络请求有超时和异常处理
- [ ] 核心功能可离线运行

### 版本号
- [ ] checkin_cli.py: __version__ = "vX.Y.Z"
- [ ] src/__init__.py: __version__ = "X.Y.Z"
- [ ] 版本号与即将创建的 tag 一致

### Git
- [ ] 所有更改已提交
- [ ] 已推送到 GitHub
- [ ] 创建带注释的 tag
- [ ] 推送 tag

### 文档
- [ ] README.md 已更新
- [ ] SKILL.md 已更新
- [ ] Release Notes 已编写

### 发布后
- [ ] 下载 Release 测试
- [ ] 验证版本号正确
- [ ] 验证检查更新功能
- [ ] 更新 ClawHub（如适用）
```

---

## 附录

### A. 关键文件路径

| 文件 | 路径 | 用途 |
|------|------|------|
| CLI 入口 | `checkin_cli.py` | 命令行接口、版本检查 |
| 核心逻辑 | `src/local_skill.py` | 打卡业务逻辑 |
| 模块导出 | `src/__init__.py` | 包初始化 |
| 依赖列表 | `requirements.txt` | 外部依赖（应保持为空） |
| 使用说明 | `README.md` | 用户文档 |
| Skill 描述 | `SKILL.md` | ClawHub 平台描述 |

### B. 常用命令

```bash
# 查看当前版本
python checkin_cli.py --version

# 查看 Git 历史
git log --oneline -5

# 查看当前 tag
git tag -l

# 查看最新 commit
git rev-parse HEAD

# 查看远程 tag
git ls-remote --tags origin
```

### C. 相关链接

- **GitHub 仓库**: https://github.com/daizongyu/learning-checkin
- **Releases**: https://github.com/daizongyu/learning-checkin/releases
- **ClawHub**: https://clawhub.ai/import

---

## 更新记录

| 日期 | 版本 | 更新内容 | 作者 |
|------|------|---------|------|
| 2026-03-14 | v1.0 | 初始版本 | 小龙虾 |
| 2026-03-14 | v1.1 | 添加版本管理注意事项 | 小龙虾 |
| 2026-03-14 | v1.2 | 添加常见错误和检查清单 | 小龙虾 |

---

**📌 重要提示：**

> 每次开发新功能前，**先阅读本文档**！  
> 特别是「升级注意事项」和「常见错误」章节。  
> 
> **记住：版本号同步是最重要的！** 🎯

---

*Learn every day, grow every day! 🦐📚✨*
