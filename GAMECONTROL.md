# ACL4SSR Full GameControl

这是在原有 `ACL4SSR_Online_Full_SteamSplit.ini` 之外新增的 **全游戏平台控制版**。

## 保留旧版

旧文件完全不需要删除：

```text
ACL4SSR_Online_Full_SteamSplit.ini
```

旧版仍可作为稳定回滚入口。

## 新版配置地址

推送本目录文件到仓库 `main` 后使用：

```text
https://raw.githubusercontent.com/cainiao524/acl4ssr-steam/main/ACL4SSR_Online_Full_GameControl.ini
```

## 策略组

- `🎮 游戏下载`：默认 `DIRECT`，统一控制 Steam / Epic / EA / Battle.net / Ubisoft / Xbox / Rockstar / GOG / Riot 等明确下载 CDN。
- `🎮 Steam 商店/社区`：默认 `🚀 节点选择`。
- `🎮 游戏平台`：默认 `DIRECT`，承接登录、客户端服务、商店/API、联机基础设施等不应粗暴归为下载的流量。

## 规则顺序

```text
🎮 游戏下载
→ 🎮 Steam 商店/社区
→ 🎮 游戏平台
→ 其余 ACL4SSR Full 规则
```

Clash/Mihomo 按从上到下第一个命中规则执行，因此顺序不能交换。

## 安全策略

`GameDownload.list` 使用保守模式。明确排除：

```text
dl.delivery.mp.microsoft.com
tlu.dl.delivery.mp.microsoft.com
```

这两个域可能与 Windows Update / Microsoft Store 通用下载共用，避免用户将 `🎮 游戏下载` 切换到代理时误把系统下载一起代理。

## 自动更新

新工作流：

```text
.github/workflows/update-game-control.yml
```

每天自动执行：

1. 校验 blackmatrix7 各游戏平台上游；
2. 生成安全的 `rules/GameDownload.list`；
3. 生成 `rules/GameSteamWeb.list`；
4. 获取 ACL4SSR 官方最新 `ACL4SSR_Online_Full.ini`；
5. 仅替换游戏平台部分，生成 `ACL4SSR_Online_Full_GameControl.ini`；
6. 校验危险宽域、关键下载 CDN 和规则顺序；
7. 有变化才自动提交。

旧的 `update-steam-rules.yml` 不需要删除，两套版本可以并存。
