# ACL4SSR GameControl MultiMode

本仓库只维护一个对外远程配置：

`ACL4SSR_Online_Full_GameControl_MultiMode.ini`

它以 ACL4SSR 官方 `ACL4SSR_Online_Full_MultiMode.ini` 为底板，保留官方多模式逻辑：

- `♻️ 自动选择`：url-test
- `🔯 故障转移`：fallback `.*`
- `🔮 负载均衡`：load-balance `.*`

本仓库只额外加入游戏平台三分流：

- `🎮 游戏下载`：默认 `DIRECT`
- `🎮 Steam 商店/社区`：默认 `🚀 节点选择`
- `🎮 游戏平台`：默认 `DIRECT`

规则优先级：

`🎮 游戏下载` → `🎮 Steam 商店/社区` → `🎮 游戏平台` → 其余 ACL4SSR 规则

唯一远程配置地址：

`https://raw.githubusercontent.com/cainiao524/acl4ssr-steam/main/ACL4SSR_Online_Full_GameControl_MultiMode.ini`

内部辅助规则：

- `rules/GameDownload.list`
- `rules/GameSteamWeb.list`

这两个 `.list` 是唯一 INI 的内部依赖，不是第二套远程配置。

GitHub Actions 每天自动从 ACL4SSR / blackmatrix7 上游更新并做安全校验。