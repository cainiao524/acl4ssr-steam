#!/usr/bin/env python3
from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from urllib.request import Request, urlopen
import sys

ROOT = Path(__file__).resolve().parents[1]
RULE_DIR = ROOT / "rules"
REPORT_DIR = ROOT / "reports"
OUT_CONFIG = ROOT / "ACL4SSR_Online_Full_GameControl_MultiMode.ini"

ACL4SSR_FULL = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full_MultiMode.ini"
ACL4SSR_GAME_DOWNLOAD = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GameDownload.list"
BM = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash"

SOURCES = OrderedDict([
    ("GameDownload", f"{BM}/Game/GameDownload/GameDownload.list"),
    ("GameDownloadCN", f"{BM}/Game/GameDownloadCN/GameDownloadCN.list"),
    ("Steam", f"{BM}/Steam/Steam.list"),
    ("SteamCN", f"{BM}/SteamCN/SteamCN.list"),
    ("Epic", f"{BM}/Epic/Epic.list"),
    ("EA", f"{BM}/EA/EA.list"),
    ("Blizzard", f"{BM}/Blizzard/Blizzard.list"),
    ("UBI", f"{BM}/UBI/UBI.list"),
    ("Xbox", f"{BM}/Xbox/Xbox.list"),
    ("PlayStation", f"{BM}/PlayStation/PlayStation.list"),
    ("Nintendo", f"{BM}/Nintendo/Nintendo.list"),
    ("Riot", f"{BM}/Riot/Riot.list"),
    ("Rockstar", f"{BM}/Rockstar/Rockstar.list"),
    ("Gog", f"{BM}/Gog/Gog.list"),
    ("Garena", f"{BM}/Garena/Garena.list"),
])

MIN_COUNTS = {
    "GameDownload": 20,
    "GameDownloadCN": 10,
    "Steam": 40,
    "SteamCN": 10,
    "Epic": 10,
    "EA": 100,
    "Blizzard": 20,
    "UBI": 4,
    "Xbox": 30,
    "PlayStation": 4,
    "Nintendo": 100,
    "Riot": 40,
    "Rockstar": 5,
    "Gog": 4,
    "Garena": 10,
}

REQUIRED = {
    "GameDownload": {"download.epicgames.com", "steampipe.akamaized.net", "packagespc.xboxlive.com"},
    "GameDownloadCN": {"assets1.xboxlive.cn", "steampipe.steamcontent.tnkjmec.com"},
    "Steam": {"steamcommunity.com", "steampowered.com", "steampipe.akamaized.net"},
    "SteamCN": {"steamcontent.com", "cm.steampowered.com"},
    "Epic": {"epicgames.com"},
    "EA": {"ea.com", "origin.com"},
    "Blizzard": {"battle.net", "blizzard.com"},
    "UBI": {"ubisoft.com", "uplay.com"},
    "Xbox": {"xbox.com", "xboxlive.com"},
    "PlayStation": {"playstation.com", "playstation.net"},
    "Nintendo": {"nintendo.com", "nintendo.net"},
    "Riot": {"riotgames.com", "riotcdn.net"},
    "Rockstar": {"rockstargames.com"},
    "Gog": {"gog.com"},
    "Garena": {"garena.com"},
}

# 这些微软下载域与 Windows Update / Microsoft Store 共用，不能安全地归类为“游戏下载”。
EXCLUDE_DOWNLOAD_VALUES = {
    "dl.delivery.mp.microsoft.com",
    "tlu.dl.delivery.mp.microsoft.com",
}

# 如果这些宽域意外进入下载列表，说明上游/分类逻辑出现危险变化。
FORBIDDEN_BROAD_DOWNLOAD = {
    "epicgames.com", "ea.com", "origin.com", "xbox.com", "xboxlive.com",
    "playstation.com", "playstation.net", "nintendo.com", "nintendo.net",
    "ubisoft.com", "uplay.com", "battle.net", "blizzard.com", "riotgames.com",
    "rockstargames.com", "gog.com", "garena.com", "steampowered.com",
    "steamcommunity.com", "steamchina.com", "steamserver.net",
}

# Steam 中不属于官方 Steam 平台基础设施的第三方条目，不纳入新版 Steam 网页组。
EXCLUDE_STEAM_WEB = {
    "fanatical.com",
    "humblebundle.com",
    "steamunlocked.net",
}

# 这些属于客户端连接/中国区平台基础设施，而不是商店社区网页。
STEAM_PLATFORM_VALUES = {
    "cm.steampowered.com",
    "steamserver.net",
    "steamchina.com",
    "wmsjsteam.com",
    "csgo.wmsj.cn",
    "dota2.wmsj.cn",
}

STEAM_DOWNLOAD_HINTS = (
    "steampipe",
    "steamcontent",
    ".qtlglb.com",
    "steam.cdn.",
    ".content.steamchina.com",
    "edge.steam-dns.top.comcast.net",
    "f3b7q2p3.ssl.hwcdn.net",
    "dl.steam.",
    "st.dl.",
)

STEAM_DOWNLOAD_EXACT = {
    "xz.pphimalayanrt.com",
}

PLATFORM_RULE_URLS = [
    SOURCES["Steam"], SOURCES["SteamCN"], SOURCES["Epic"], SOURCES["EA"],
    SOURCES["Blizzard"], SOURCES["UBI"], SOURCES["Xbox"], SOURCES["PlayStation"],
    SOURCES["Nintendo"], SOURCES["Riot"], SOURCES["Rockstar"], SOURCES["Gog"],
    SOURCES["Garena"],
]

ALLOWED = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6"}


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "acl4ssr-gamecontrol-generator/2.0"})
    with urlopen(req, timeout=45) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status}: {url}")
        data = resp.read()
    text = data.decode("utf-8-sig")
    if not text.strip():
        raise RuntimeError(f"上游返回空文件: {url}")
    return text


def parse(text: str) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        kind = line.split(",", 1)[0].strip().upper()
        if kind not in ALLOWED:
            continue
        if line not in seen:
            seen.add(line)
            out.append(line)
    return out


def value_of(rule: str) -> str:
    parts = rule.split(",", 2)
    return parts[1].strip().lower() if len(parts) > 1 else ""


def has_value(rules: list[str], value: str) -> bool:
    v = value.lower()
    return any(value_of(r) == v for r in rules)


def dedupe(lines: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            out.append(line)
    return out


def validate_source(name: str, rules: list[str]) -> None:
    minimum = MIN_COUNTS[name]
    if len(rules) < minimum:
        raise RuntimeError(f"{name} 上游异常：仅 {len(rules)} 条，最低要求 {minimum}")
    for value in REQUIRED[name]:
        if not has_value(rules, value):
            raise RuntimeError(f"{name} 上游缺少关键规则 {value}")


def is_strong_steam_download(rule: str) -> bool:
    value = value_of(rule)
    if value in STEAM_PLATFORM_VALUES or value in EXCLUDE_STEAM_WEB:
        return False
    return value in STEAM_DOWNLOAD_EXACT or any(h in value for h in STEAM_DOWNLOAD_HINTS)


def render_list(name: str, purpose: str, rules: list[str]) -> str:
    header = [
        f"# NAME: {name}",
        f"# PURPOSE: {purpose}",
        "# GENERATED: scripts/generate_game_control.py",
        "# DO NOT EDIT: generated file",
        f"# TOTAL: {len(rules)}",
        "",
    ]
    return "\n".join(header + rules) + "\n"


def build_download(source_rules: dict[str, list[str]], acl_download: list[str]) -> list[str]:
    # 专用下载表是主依据；ACL4SSR 作为冗余补充。
    base = source_rules["GameDownload"] + source_rules["GameDownloadCN"] + acl_download
    out: list[str] = []
    for rule in base:
        value = value_of(rule)
        kind = rule.split(",", 1)[0].upper()
        if kind in {"IP-CIDR", "IP-CIDR6"}:
            continue
        if value in EXCLUDE_DOWNLOAD_VALUES:
            continue
        out.append(rule)

    # Steam 额外 ISP/CDN：只接受强下载特征，避免把 CM/登录/网站归入下载。
    for rule in source_rules["SteamCN"] + source_rules["Steam"]:
        if is_strong_steam_download(rule):
            out.append(rule)

    out = dedupe(out)
    values = {value_of(r) for r in out}
    bad = sorted(values & FORBIDDEN_BROAD_DOWNLOAD)
    if bad:
        raise RuntimeError(f"游戏下载列表出现危险宽域: {', '.join(bad)}")

    required = {
        "steamcontent.com", "steampipe.akamaized.net", "download.epicgames.com",
        "download.dm.origin.com", "packagespc.xboxlive.com", "cdn.ubi.com",
        "dyn.riotcdn.net", "gamedownloads-rockstargames-com.akamaized.net",
        "blzddist1-a.akamaihd.net",
    }
    for value in required:
        if value not in values:
            raise RuntimeError(f"游戏下载列表缺少关键规则 {value}")
    if len(out) < 45:
        raise RuntimeError(f"游戏下载列表异常：仅 {len(out)} 条")
    return out


def build_steam_web(source_rules: dict[str, list[str]], download: list[str]) -> list[str]:
    download_values = {value_of(r) for r in download}
    out: list[str] = []
    for rule in source_rules["SteamCN"] + source_rules["Steam"]:
        kind = rule.split(",", 1)[0].upper()
        if kind not in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"}:
            continue
        value = value_of(rule)
        if value in download_values:
            continue
        if value in STEAM_PLATFORM_VALUES:
            continue
        if value in EXCLUDE_STEAM_WEB:
            continue
        out.append(rule)
    out = dedupe(out)

    required = {"steamcommunity.com", "steampowered.com", "steam-chat.com", "steamusercontent.com"}
    for value in required:
        if not has_value(out, value):
            raise RuntimeError(f"Steam 网页列表缺少关键规则 {value}")
    if len(out) < 20:
        raise RuntimeError(f"Steam 网页列表异常：仅 {len(out)} 条")
    return out


def game_rules_block() -> list[str]:
    lines = [
        "; ===== GameControl 全游戏平台智能分流（自动生成） =====",
        "; 顺序：游戏下载 > Steam 商店/社区 > 游戏平台。",
        "ruleset=🎮 游戏下载,https://raw.githubusercontent.com/cainiao524/acl4ssr-steam/main/rules/GameDownload.list",
        "ruleset=🎮 Steam 商店/社区,https://raw.githubusercontent.com/cainiao524/acl4ssr-steam/main/rules/GameSteamWeb.list",
    ]
    for url in PLATFORM_RULE_URLS:
        lines.append(f"ruleset=🎮 游戏平台,{url}")
    return lines


def build_full_config(base: str) -> str:
    lines = base.splitlines()
    result: list[str] = []
    inserted_rules = False
    inserted_groups = False
    removed_platform_rules = 0
    removed_steamcn_direct = 0

    for line in lines:
        stripped = line.strip()

        # 官方 Full 中 SteamCN 原本直连；新版必须交给更精细的游戏规则。
        if stripped.startswith("ruleset=🎯 全球直连,") and stripped.endswith("/Clash/Ruleset/SteamCN.list"):
            removed_steamcn_direct += 1
            continue

        # 用统一 GameControl 规则块替换官方所有“游戏平台”规则行。
        if stripped.startswith("ruleset=🎮 游戏平台,"):
            removed_platform_rules += 1
            if not inserted_rules:
                result.extend(game_rules_block())
                inserted_rules = True
            continue

        # 保留官方游戏平台策略组选项，并在其前后插入新策略组。
        if stripped.startswith("custom_proxy_group=🎮 游戏平台`"):
            result.append("custom_proxy_group=🎮 游戏下载`select`[]DIRECT`[]🚀 节点选择`[]♻️ 自动选择`[]🔯 故障转移`[]🔮 负载均衡`[]🇭🇰 香港节点`[]🇨🇳 台湾节点`[]🇸🇬 狮城节点`[]🇯🇵 日本节点`[]🇺🇲 美国节点`[]🇰🇷 韩国节点`[]🚀 手动切换")
            result.append("custom_proxy_group=🎮 游戏平台`select`[]DIRECT`[]🚀 节点选择`[]♻️ 自动选择`[]🔯 故障转移`[]🔮 负载均衡`[]🇺🇲 美国节点`[]🇭🇰 香港节点`[]🇨🇳 台湾节点`[]🇸🇬 狮城节点`[]🇯🇵 日本节点`[]🇰🇷 韩国节点`[]🚀 手动切换")
            result.append("custom_proxy_group=🎮 Steam 商店/社区`select`[]🚀 节点选择`[]♻️ 自动选择`[]🔯 故障转移`[]🔮 负载均衡`[]🇭🇰 香港节点`[]🇨🇳 台湾节点`[]🇸🇬 狮城节点`[]🇯🇵 日本节点`[]🇺🇲 美国节点`[]🇰🇷 韩国节点`[]🚀 手动切换`[]DIRECT")
            inserted_groups = True
            continue

        result.append(line)

        if stripped == ";acl4SSR规则":
            result.append(";GameControl MultiMode 自动生成版：以 ACL4SSR 官方 Full_MultiMode 为底，仅替换游戏平台分流")
            result.append(";仓库仅保留 ACL4SSR_Online_Full_GameControl_MultiMode.ini 一个远程配置")

    if not inserted_rules or removed_platform_rules < 1:
        raise RuntimeError("未找到 ACL4SSR 官方游戏平台 ruleset 锚点，拒绝生成")
    if not inserted_groups:
        raise RuntimeError("未找到 ACL4SSR 官方游戏平台策略组锚点，拒绝生成")
    if removed_steamcn_direct != 1:
        raise RuntimeError(f"SteamCN 直连锚点数量异常：{removed_steamcn_direct}")

    text = "\n".join(result).rstrip() + "\n"
    validate_config(text)
    return text


def validate_config(text: str) -> None:
    required = [
        "ruleset=🎮 游戏下载,",
        "ruleset=🎮 Steam 商店/社区,",
        "custom_proxy_group=🎮 游戏下载`select`[]DIRECT",
        "custom_proxy_group=🎮 Steam 商店/社区`select`[]🚀 节点选择",
        "ruleset=🎮 游戏平台,",
    ]
    for token in required:
        if token not in text:
            raise RuntimeError(f"生成 INI 缺少 {token}")
    if "ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/SteamCN.list" in text:
        raise RuntimeError("生成 INI 仍包含官方 SteamCN 提前直连规则")

    i_download = text.index("ruleset=🎮 游戏下载,")
    i_web = text.index("ruleset=🎮 Steam 商店/社区,")
    i_platform = text.index("ruleset=🎮 游戏平台,")
    if not (i_download < i_web < i_platform):
        raise RuntimeError("GameControl 规则顺序错误")
    if text.count("ruleset=🎮 游戏平台,") < 10:
        raise RuntimeError("游戏平台覆盖不足")


def report(source_rules: dict[str, list[str]], download: list[str], web: list[str]) -> str:
    rows = [
        "# GameControl 规则报告",
        "",
        "> 此文件由 `scripts/generate_game_control.py` 自动生成。",
        "",
        "| 数据源 | 规则数 |",
        "| --- | ---: |",
    ]
    for name, rules in source_rules.items():
        rows.append(f"| {name} | {len(rules)} |")
    rows += [
        "",
        "## 最终输出",
        "",
        f"- `GameDownload.list`: **{len(download)}** 条",
        f"- `GameSteamWeb.list`: **{len(web)}** 条",
        f"- 平台覆盖：Steam / SteamCN / Epic / EA / Blizzard / Ubisoft / Xbox / PlayStation / Nintendo / Riot / Rockstar / GOG / Garena",
        "- 安全排除：`dl.delivery.mp.microsoft.com`、`tlu.dl.delivery.mp.microsoft.com` 不进入游戏下载组，避免把 Windows Update / Microsoft Store 通用下载错误归类。",
        "",
    ]
    return "\n".join(rows)


def main() -> int:
    source_rules: dict[str, list[str]] = {}
    for name, url in SOURCES.items():
        rules = parse(fetch(url))
        validate_source(name, rules)
        source_rules[name] = rules
        print(f"{name}: {len(rules)}")

    acl_download = parse(fetch(ACL4SSR_GAME_DOWNLOAD))
    if len(acl_download) < 15:
        raise RuntimeError(f"ACL4SSR GameDownload 异常：仅 {len(acl_download)} 条")

    download = build_download(source_rules, acl_download)
    steam_web = build_steam_web(source_rules, download)
    full = build_full_config(fetch(ACL4SSR_FULL))

    RULE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (RULE_DIR / "GameDownload.list").write_text(
        render_list("GameDownload", "全游戏平台下载/更新 CDN（保守安全模式）", download),
        encoding="utf-8", newline="\n"
    )
    (RULE_DIR / "GameSteamWeb.list").write_text(
        render_list("GameSteamWeb", "Steam 商店/社区/聊天/网页资源", steam_web),
        encoding="utf-8", newline="\n"
    )
    OUT_CONFIG.write_text(full, encoding="utf-8", newline="\n")
    (REPORT_DIR / "game-rules.md").write_text(report(source_rules, download, steam_web), encoding="utf-8", newline="\n")

    print(f"GameDownload: {len(download)}")
    print(f"GameSteamWeb: {len(steam_web)}")
    print(f"Config: {OUT_CONFIG.name}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
