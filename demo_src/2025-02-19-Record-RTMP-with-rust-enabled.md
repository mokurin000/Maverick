---
layout: post
title: 基于 Xiu 和 ffmpeg 的局域网录像机平替方案
slug: xiu-ffmpeg-based-lan-video-recorder
date: 2025-02-21 13:07
status: publish
author: Poly000
categories: 
  - RTMP
tags: 
  - RTSP
  - RTMP
  - ffmpeg
  - webcam
---

# 硬件需要

## 路由器/无线光猫

- 需要可以绑定 MAC 到 LAN IP

## 摄像头

### 丐版 (本教程)

- 一部可以长期供电、固定录制的手机
  > 如果充电不够稳定，可能会出现 ffmpeg 在手机重启、重新开始推送服务后仍然挂起的状态
  >
  > 考虑为 ffmpeg 对应服务设置 RuntimeMaxSec 来减少空白期
- 一台 10w-20w 功率的LED灯，提供手动补光（一体式约15~20 CNY）
- 一根足够稳定，不会摔坏你手机的摄像支架

### 家庭版

> 听闻只有乐橙的网络摄像机不是云存储服务的副产品,
> 包括 rtsp流/ONVIF 都是公开的。

- 一台乐橙网络摄像机，需支持接入你的局域网

### 企业方案

- 一台专业的，包含 RTSP 协议透明引出的“企业用”溢价的业内品牌网络摄像机

## 录像机

- 一台可以长期供电，带有停电时自动关机（你的笔记本电池，何尝不是UPS？）的电脑
    - 最好带有可用的硬件视频编码支持。
    > 本教程只考虑了 intel QuickSyncVideo / NVIDIA NVENC
    > 可以自行调整 AMD 支持参数


# 软件需要

## 摄像手机

[IP摄像头]: https://play.google.com/store/apps/details?id=com.pas.webcam
[SpyNET Camera]: https://apt.izzysoft.de/fdroid/index/apk/com.spynet.camtest

- [SpyNET Camera]，开源软件，2017停更
- [IP摄像头]，广告软件

## 录像机

[nssm]: https://nssm.cc/

- 运行有 Systemd-based 发行版，或 Windows（自行使用 [nssm] 管理服务）

### Xiu 配置文件

```bash
${EDITOR:-nano} ~/xiu.toml
```

```toml
[rtmp]
enabled = true
port = 1935
gop = 1

[hls]
enabled = true
port = 8080
need_record = true

[authsecret]
key = ""
password = ""
```

### ffmpeg 推流+时间戳脚本

> 此处以 nushell 为例，你可以把它改写成 bash 脚本等

```bash
${EDITOR:-nano} ~/rtsp-to-rtmp.nu
```

#### QuickSync

```nushell
#!/usr/bin/nu

# 填入你的 RTSP 推流地址
let rtsp_addr = "rtsp://192.168.xxx.xxx:8080/h264.sdp";
# 填入你的摄像头名称
let camera_prefix = "";

ffmpeg -hwaccel qsv -i $rtsp_addr -framerate 30 -video_size 1920x1080 -c:v h264_qsv -global_quality 30 -f flv -ar 22050 ( "rtmp://127.0.0.1/live/" + $camera_prefix + ( date now | format date "%Y-%m-%d_%H-%M-%S" ))
```

#### NVENC

```nushell
#!/usr/bin/nu

# 填入你的 RTSP 推流地址
let rtsp_addr = "rtsp://192.168.xxx.xxx:8080/h264.sdp";
# 填入你的摄像头名称
let camera_prefix = "";

ffmpeg -hwaccel cuda -i $rtsp_addr -framerate 30 -video_size 1920x1080 -c:v h264_nvenc -rc:v vbr_hq -cq 30 -f flv -ar 22050 ( "rtmp://127.0.0.1/live/" + $camera_prefix + ( date now | format date "%Y-%m-%d_%H_%M_%S" ))
```

### Systemd 服务项

#### 建立目录

```bash
mkdir -p ~/.local/share/systemd/user
```

#### Xiu

```bash
${EDITOR:-nano} ~/.local/share/systemd/user/xiu.service
```

```ini
[Unit]
Description=Xiu Service
After=network-manager.service

[Service]
# user 改为你的用户名
ExecStart=/usr/bin/xiu -c /home/user/xiu.toml
# 此目录为存储 ./live/<时间戳>/*.{ts,m3u8} 的目录
WorkingDirectory=/mnt/Data/monitor
Restart=always

[Install]
WantedBy=default.target
```

```bash
systemctl enable --user --now xiu.service
```

#### FFmpeg 转发流

```bash
${EDITOR:-nano} ~/.local/share/systemd/user/rtmp-to-rtsp.service
```

```ini
[Unit]
Description=RTSP Push to RTMP Service
After=network-manager.service

[Service]
# user 改为你的用户名
ExecStart=/home/user/rtsp_push_rtmp.nu
Restart=always
# 每小时分一次 vod_[...].m3u8
RuntimeMaxSec=3600

[Install]
WantedBy=default.target
```

```bash
systemctl enable --user --now rtmp-to-rtsp.service
```

# 尾声

现在 `xiu` 就可以在你设置好的存储位置自动产出动态 `.m3u8` 文件和（每当 Xiu退出/串流停止推往Xiu 时生成）的总 `vod_<...>.m3u8` 。

使用以下命令将 H264 编码的 `*.ts` 文件合并为 `.mp4` 格式，以使 mpv 可以正常seek视频。

```bash
ffmpeg -i vod_2025-02-19_16_47_38.m3u8 -c copy output.mp4
```

或者使用 nushell 脚本：

```nushell
# 此处 live 之前改为你的视频存储路径
cd /mnt/Data/monitor/live

for $it in (fd '^vod_.*\.m3u8$' | lines) {
    # 提取文件名部分，这里是配合产生的 `<时间戳>/vod_<时间戳>.m3u8` 路径格式
    let name = ($it | str replace --regex "/.*" "");
    
    # 合并 .m3u8 视频，不进行重编码
    ffmpeg -i $it -codec copy ($name + ".mp4")
    
    # 清理合并成功的 .ts 视频分片
    if ($env.LAST_EXIT_CODE == 0) {
        rm -rf $name
    }
}
```