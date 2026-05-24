---
name: reasonix-git-ssh
description: Reasonix 仓库 git push 使用 SSH 而非 HTTPS
type: user
scope: global
created: 2026-05-24
---
`~/.reasonix/` 仓库的 remote 已改为 SSH（`git@github.com:791994545/reasonix-config.git`）。以后 git push 前先 `git -C ~/.reasonix push`，不需要改 remote。若 remote 被重置为 HTTPS，先改回 SSH 再推。
