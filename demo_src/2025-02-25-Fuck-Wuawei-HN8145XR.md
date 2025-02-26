---
layout: post
title: HN8145XR光猫-河南移动-资料整理
slug: fuck-wuawei-hn8145xr
date: 2025-02-26 11:30
status: publish
author: Poly000
categories: 
  - Modem
tags: 
  - Moden
  - CMCC
---

# 前言

本人有幸用上了 河南移动 网络接入，我们井盖省的网络封闭程度一直是内地省份中数一数二。

相关软件会放在 [fuck-wuawei-modem](https://github.com/mokurin000/fuck-wuawei-modem)


## 还原可用的Shell环境

> 来源: [分享HN8145XR开telnet及补全shell个人心得][1]
>
> Telnet用户：root
> Telnet密码：`adminHW`, `Hw8@cMcc` 等

0. 启动 `ONT_telnet_enable.exe`
1. 网线连接光猫和电脑/笔记本
2. 打开使能工具，选择对应有线网卡，展开设备列表
3. 断开光猫电源
4. 选择“V5使能”，点击启动
5. 恢复光猫电源，等待出现“Failed”字样，不用管；待到光猫LED灯全部熄灭，点击停止。不要退出使能工具
> 此处可以检查 telnet 是否已经可以连接。
6. 选择“升级”，版本包选择 `shell9.bin`
7. 点击开始，再次重启光猫电源
8. 等待光猫LED再次全部熄灭（除下行光），出现 “Failed” ，点击停止，退出使能工具。

## 基于Telnet获取超管密码

> 参考：[通过telnet取得华为HN8145XR超级密码][3]

```bash
telnet 192.168.1.1
# -> root
# -> (telnet密码)
su
shell
cd /mnt/jffs2/
cp hw_ctree.xml myconf.xml.gz
aescrypt2 1 myconf.xml.gz tmp # 此处tmp被忽略了
zcat myconf.xml.gz  | grep 'UserName="CMCCAdmin"' | cut -d " " -f 5 | cut -d = -f 2
```

可以得到如下结果：

```text
Password="$2...............$"
```

使用 `WW_Dollar2.exe` ，点击计算，可以解密 $2 密文。

得到的密文可以需要拼接上 `CMCCAdmin` / `CMCCAdmin#` ，如果是中国移动版

作者这里得到了一串sha256sum (-_-||| ) 还好是电话要的密码

考虑到河南移动的做法是 CMCCAdmin + 八位随机字符，目前时代个人算力暂不可能爆破。

## 从hash后的宽带密码/超级密码计算原密码

> 来源：PurePeace 的 [获取移动光猫（如HS8545M5等设备）pppoe密码明文][0]，略有修改
>
> Rust写了[一份][4]，可以用来试试看更长的密码
> 另外，移动似乎倾向于设置为手机号后六位。
>
> 更建议的方式：通过手机营业厅重置密码，获取新的 PPPoE 拨号密码
> 移动可以发送 `CZKDMM` 到 10086，[发送短信](sms:+10086?&body=CZKDMM)

```python
from sys import argv
import hashlib


def sha256(todo: str):
    return hashlib.sha256(str(todo).encode()).hexdigest()


def md5(todo: str):
    return hashlib.md5(str(todo).encode()).hexdigest()


def find_target(secret: str):
    # 生成六位密码
    for value in range(1000000):
        value = f"{value:06}"
        s = sha256(md5(value))
        if s == secret:
            return value
    return None


if __name__ == "__main__":
    try:
        secret = argv.pop(1)
    except IndexError:
        print("Usage:")
        print(f"    {argv[0]} <sha256hashsecret>")
        exit(1)
    target = find_target(secret)
    print(target if target is not None else "")
```

## 恢复华为公版界面

> 参考：[折腾HN8145XR（恢复华为界面 等）][2]

> 需要先备份好 宽带帐户，宽带密码，ONT认证密码
>
> 如果只修改界面，不直接 restore_xxx.sh ，可能可以保留下来ONT认证密码
>
> 作者的OTN注册方式是 Password

1. 启动 `WW_Dollar2.exe`
2. 在你的电脑启动 ncat:

> 如果没有ncat，可以 `scoop install nmap`。

```bash
ncat -l -p 9999 > hw_boardinfo
```

3. 在光猫，使用 busybox nc 把 hw_boardinfo 传过来：
> 此处 192.168.1.4 为电脑的局域网IP

```bash
busybox nc 192.168.1.4 9999 < /mnt/jffs2/hw_boardinfo
```

4. 备份一份 `hw_boardinfo`
5. 打开 `hw_boardinfo` ，修改：

```text
obj.id = "0x0000001a"; obj.value = "COMMON";
obj.id = "0x0000001b"; obj.value = "COMMON";
obj.id = "0x00000031"; obj.value = "NOCHOOSE"; 
```

6. 把修改后的 hw_boardinfo 传回覆盖 `/mnt/jffs2/hw_boardinfo` 和 `/mnt/jffs2/hw_boardinfo.bak` 。

[0]: https://blog.csdn.net/qq_26373925/article/details/112798210
[1]: https://www.right.com.cn/forum/thread-8339357-1-1.html
[2]: https://www.chinadsl.net/thread-172911-1-1.html
[3]: https://www.silencetime.com/index.php/archives/359/
[4]: https://github.com/mokurin000/hw-hash-bruteforce