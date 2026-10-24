# GameControl 规则报告

> 此文件由 `scripts/generate_game_control.py` 自动生成。

| 数据源 | 规则数 |
| --- | ---: |
| GameDownload | 39 |
| GameDownloadCN | 16 |
| Steam | 69 |
| SteamCN | 17 |
| Epic | 15 |
| EA | 165 |
| Blizzard | 62 |
| UBI | 5 |
| Xbox | 42 |
| PlayStation | 4 |
| Nintendo | 126 |
| Riot | 55 |
| Rockstar | 5 |
| Gog | 4 |
| Garena | 15 |

## 最终输出

- `GameDownload.list`: **76** 条
- `GameSteamWeb.list`: **31** 条
- 平台覆盖：Steam / SteamCN / Epic / EA / Blizzard / Ubisoft / Xbox / PlayStation / Nintendo / Riot / Rockstar / GOG / Garena
- 安全排除：`dl.delivery.mp.microsoft.com`、`tlu.dl.delivery.mp.microsoft.com` 不进入游戏下载组，避免把 Windows Update / Microsoft Store 通用下载错误归类。
