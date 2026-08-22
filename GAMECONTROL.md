# GameControl MultiMode

唯一对外配置：

`ACL4SSR_Online_Full_GameControl_MultiMode.ini`

## 基础

底板使用 ACL4SSR 官方：

`ACL4SSR_Online_Full_MultiMode.ini`

官方多模式保持原样：

- `custom_proxy_group=🔯 故障转移` 使用 `fallback` + `.*`
- `custom_proxy_group=🔮 负载均衡` 使用 `load-balance` + `.*`
- 不增加国家锁定故障转移组

## 游戏分流

- `🎮 游戏下载`：默认 DIRECT
- `🎮 Steam 商店/社区`：默认节点选择
- `🎮 游戏平台`：默认 DIRECT

规则顺序固定：

`游戏下载` → `Steam 商店/社区` → `游戏平台`

## 安全

`GameDownload.list` 继续排除：

- `dl.delivery.mp.microsoft.com`
- `tlu.dl.delivery.mp.microsoft.com`

避免把 Windows Update / Microsoft Store 的共享下载流量错误归类为游戏下载。

## 自动更新

唯一工作流：

`.github/workflows/update-game-control.yml`

唯一生成器：

`scripts/generate_game_control.py`