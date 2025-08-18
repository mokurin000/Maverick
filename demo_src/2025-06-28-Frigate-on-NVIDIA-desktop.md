---
layout: post
title: Frigate + NVIDIA 显卡笔记本的部署
slug: frigate-on-linux-laptop-with-nvidia
date: 2025-06-28 12:11
status: publish
author: Poly000
categories: 
  - RTMP
tags: 
  - RTSP
  - RTMP
  - webcam
  - frigate
---

## 软件前置

```bash
sudo pacman -Syu docker docker-compose nvidia-container-toolkit
sudo systemctl enable --now docker
# 确保 docker0 已经被代理或已设置好连接代理
```

## 硬件要求

该方案相比于之前的丐版方案，需要更新的硬件才能解决种种兼容或性能问题。

笔者测试的环境：

```text
                   -`
                  .o+`
                 `ooo/
                `+oooo:
               `+oooooo:                 poly@mokurin-arch 
               -+oooooo+:                ----------------- 
             `/:-:++oooo+:               OS: Arch Linux x86_64 
            `/++++/+++++++:              Host: Dell G15 5520 
           `/++++++++++++++:             Kernel: 6.15.2-arch1-1 
          `/+++ooooooooooooo/`           Uptime: 22 hours, 2 mins 
         ./ooosssso++osssssso+`          Packages: 2766 (pacman), 8 (flatpak) 
        .oossssso-````/ossssss+`         Shell: zsh 5.9 
       -osssssso.      :ssssssso.        Resolution: 1920x1080 
      :osssssss/        osssso+++.       DE: Plasma 6.3.5 
     /ossssssss/        +ssssooo/-       WM: kwin 
   `/ossssso+/:-        -:/+osssso+-     Theme: Materia [GTK2/3] 
  `+sso+:-`                 `.-/+oso:    Icons: breeze-dark [GTK2/3] 
 `++:.                           `-/+/   Terminal: vscode 
 .`                                 `/   CPU: 12th Gen Intel i7-12700H (20) @ 4.600GHz 
                                         GPU: Intel Alder Lake-P GT2 [Iris Xe Graphics] 
                                         GPU: NVIDIA GeForce RTX 3060 Mobile / Max-Q 
                                         Memory: -- MiB / 15669MiB 
```

## 使用的文件

- `init.sh`

```bash
mkdir -p config storage
mkdir -p config/model_cache/jinaai/jina-clip-v1
# btrfs 改善 sqlite 的性能
chattr -R +C config storage
cp --reflink=auto config.yaml config/
cp --reflink=auto yolo_nas_s.onnx config/

# optional, useless semantic search
# cp --reflink=auto *_fp16.onnx config/model_cache/jinaai/jina-clip-v1/

docker-compose up -d
```

- `yolo_nas_s.onnx`

该文件由于禁止分发转换模型，建议使用 [colab](https://colab.research.google.com/github/blakeblackshear/frigate/blob/dev/notebooks/YOLO_NAS_Pretrained_Export.ipynb) 运行获取。

- `docker-compose.yml`

> `-tensorrt` 只有用N卡加速才需要，AMD / Intel 卡不需要。

```yaml
services:
  frigate:
    container_name: frigate
    restart: unless-stopped
    stop_grace_period: 30s
    image: ghcr.io/blakeblackshear/frigate:stable-tensorrt
    volumes:
      - ./config:/config
      - ./storage:/media/frigate
      - type: tmpfs # Optional: 1GB of memory, reduces SSD/SD Card wear
        target: /tmp/cache
        tmpfs:
          size: 1000000000
    cap_add:
      - CAP_PERFMON
    ports:
      - "8971:8971"
      - "8554:8554" # RTSP feeds
    runtime: nvidia # migrate to CDI for newest nvidia driver
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['0']
              capabilities: [gpu, video]
```

- config.yaml

> 此处以乐橙为例子。大多摄像头可以在 iSpy 的文档找到需要的链接。
>
> 顺便一提，乐橙摄像头要求 WIFI 密码必须是字母加数字，否则不可能连接成功。

frigate 在这方面的文档出奇的烂。你需要综合翻阅 [完整参考配置](https://docs.frigate.video/configuration/reference/) 和小节甚至 issues 。

```yaml
version: 0.15-1
# 关闭 mqtt 消息队列
mqtt:
  enabled: false
# 关闭 TLS 连接（端口不变）
tls:
  enabled: false
# 关闭网页验证
auth:
  # 如果启用，admin密码会在首次启动时输出到日志。
  # 错过了没关系，看 `docker-compose logs` 输出。
  enabled: false 

ffmpeg:
  # 如果遇到 hardware capacity xxxx 问题，
  # 可以通过官方工具设置使用 H264 编码传输。
  hwaccel_args: preset-nvidia
  # IMOU 的摄像头rtsp流，udp传输时很容易丢包、重复包、断流。
  input_args: -rtsp_transport tcp


# 保留录制历史，1天的全部视频和30天的警告/识别片段。
record:
  enabled: true
  retain:
    days: 1
    mode: all
  alerts:
    retain:
      days: 30
      mode: motion
  detections:
    retain:
      days: 30
      mode: motion

cameras:
  backyard:
    enabled: true
    ffmpeg:
      inputs:
        - path: 
            # 此处 PASSWORD 和乐橙 app 中设置的一致。
            # CAMIP 即为你的摄像头绑定的 ip 地址。
            rtsp://admin:PASSWORD@CAMIP:554/cam/realmonitor?channel=1&subtype=0
          roles:
            - detect
    detect:
      enabled: true
    # 上下左右。请勿尝试通过 onvif 启用 autotracking ，乐橙这种情况会死机。
    onvif:
      host: CAMIP
      port: 80
      user: admin
      password: PASSWORD


    motion:
      # mask掉乐橙的时间戳区域。
      mask: 0.015,0.041,0.268,0.041,0.267,0.086,0.014,0.089
      threshold: 40 # 减少树叶抖动导致的不必要 detect。
      contour_area: 10
      improve_contrast: true

# 注意：部分旧版显卡可能会遇到 onnxruntime 不支持对应 kernel 版本的问题
# 如果有 Intel CPU 可以考虑 OpenVINO - CPU 运行。
detectors:
  onnx:
    type: onnx

# 此处识别高宽和之前 ipynb 运行时设置一致。
model:
  model_type: yolonas
  width: 320 # <--- should match whatever was set in notebook
  height: 320 # <--- should match whatever was set in notebook
  input_pixel_format: bgr
  input_tensor: nchw
  path: /config/yolo_nas_s.onnx
  labelmap_path: /labelmap/coco-80.txt
```

## 如何彻底关闭服务

```bash
docker-compose down
```

## 如何通过命令行重启服务 (不推荐)

```bash
docker-compose stop
sleep 2
docker-compose start
```