# ACL4SSR Steam 自动双分流

这个版本不手工维护 Steam 域名。

- 上游：blackmatrix7/ios_rule_script
- 输入：Steam.list + SteamCN.list
- 输出：
  - rules/SteamDownload.list
  - rules/SteamWeb.list
- 更新：GitHub Actions 每天自动检查
- 安全：上游为空、数量异常、关键规则消失或分类异常时，生成脚本直接失败，不覆盖线上规则

当前首版生成：
- SteamDownload.list: 43 条
- SteamWeb.list: 28 条

ACL4SSR 远程配置引用顺序：

```ini
ruleset=🎮 Steam 登录/下载,https://raw.githubusercontent.com/cainiao524/acl4ssr-steam/main/rules/SteamDownload.list
ruleset=🎮 Steam 商店/社区,https://raw.githubusercontent.com/cainiao524/acl4ssr-steam/main/rules/SteamWeb.list
```

下载组必须在网页组之前，以保证 `cm.steampowered.com` 等更具体规则优先于 `steampowered.com`。
