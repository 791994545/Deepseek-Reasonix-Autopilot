---
name: reasonix-git-ssh
description: Reasonix 仓库 git 设置 — SSH 配置、多仓库管理、push/pull 流程
type: user
scope: global
created: 2026-05-24
updated: 2026-05-24
---

# Reasonix Git & SSH 配置

## 仓库位置
`~/.reasonix/` 仓库的 remote 已设为 SSH：
```
git@github.com:791994545/reasonix-config.git
```

## 日常工作流
```bash
# 修改文件后
git -C ~/.reasonix add -A
git -C ~/.reasonix commit -m "..."
git -C ~/.reasonix push

# 拉取最新（换机或恢复时）
git -C ~/.reasonix pull
```

## SSH 故障恢复
若 `git push` 报 `Permission denied (publickey)`：
```bash
# 1. 检查当前 remote
git -C ~/.reasonix remote -v

# 2. 若被重置为 HTTPS，改回 SSH
git -C ~/.reasonix remote set-url origin git@github.com:791994545/reasonix-config.git

# 3. 检查 SSH key 是否已加载
ssh -T git@github.com
```
