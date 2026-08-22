# SUBWEB + subconverter-ng（飞牛）

当前端口：

```text
SUBWEB:          NAS:18088 -> container:80
subconverter-ng: NAS:25500 -> container:25500
```

局域网：

```text
http://192.168.50.149:18088
http://192.168.50.149:25500
```

如果使用 Nginx Proxy Manager，推荐前后端都走 HTTPS：

```text
sub.你的域名 -> 192.168.50.149:18088
subapi.你的域名 -> 192.168.50.149:25500
```

SUBWEB 的“自建本地服务”填写后端根地址，不要手动加 `/sub`。

新版外部配置规则填写：

```text
https://raw.githubusercontent.com/cainiao524/acl4ssr-steam/main/ACL4SSR_Online_Full_GameControl.ini
```
