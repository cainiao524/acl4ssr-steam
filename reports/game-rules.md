# GameControl 规则报告（初始基线）

初始基线：2026-08-22。

## 当前输出

- `GameDownload.list`：61 个唯一规则值。
- `GameSteamWeb.list`：24 个唯一规则值。
- `ACL4SSR_Online_Full_GameControl.ini`：13 个游戏平台上游规则集。

## 平台覆盖

Steam / SteamCN / Epic / EA / Battle.net / Ubisoft / Xbox / PlayStation / Nintendo / Riot / Rockstar / GOG / Garena。

## 安全处理

- 游戏下载组默认 `DIRECT`。
- Steam 商店/社区默认 `🚀 节点选择`。
- 游戏平台默认 `DIRECT`。
- 微软共享系统下载域不进入 `GameDownload.list`，避免切换游戏下载策略时误影响 Windows Update / Microsoft Store 通用下载。
- `fanatical.com`、`humblebundle.com`、`steamunlocked.net` 不进入新版 Steam 官方网页规则。

后续 GitHub Actions 会由 `scripts/generate_game_control.py` 自动重写本报告。
