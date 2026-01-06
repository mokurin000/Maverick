---
layout: post
title: 远程桌面控制软件-二开
slug: remote-desktop-make-in-1-day
date: 2026-01-03 14:00
status: publish
author: mokurin000
categories: 
  - Coding
tags: 
  - rustdesk
  - flutter
  - Rust
  - Development
---

## 前言

该博文会收录一些关于某远程软件二次开发需要的操作，请大家修改后遵循 GPLv3 要求！

## 官方高级设置

官方的高级设置均可以对应到 `hbb_common::config::keys::OPTION_` 系列变量

## hide-tray

`src/tray.rs::start_tray` 负责启动托盘图标，其在 macos 会强要求托盘图标启动

## s/RustDesk/XXXXDesk

```text
# 写死在一些翻译中
src/lang.rs
 -> translate_locale
    - 此处的 s.replace 会判断 upgrade_rustdesk_server_pro* 和
      powered_by_me 两个特殊字段，需要修改 APP_NAME 才会判定需要替换。
# 程序 App name
libs/hbb_common
 -> src/config.rs
    - APP_NAME
```

## 替换服务器

```text
libs/hbb_common
 -> src/config.rs
    - RENDEZVOUS_SERVERS
    - RS_PUB_KEY
```

## 固定密码

```text
libs/hbb_common
 -> src/config.rs
    - get_permanent_password
```

## 免安装启动器

> 注意：修改图标后可能由于 Windows 资源管理器图标缓存而仍显示为原本图标

Runner 本身的其他信息：

```text
flutter/windows/runner/Runner.rc
```

使用 `libs/portable` 前需要放入 `Runner.res` ，res中的图标会被它的 `build.rs` 忽略。

Runner 和本体的图标：

```text
res/icon.ico
flutter/windows/runner/resources/app_icon.ico
```

打包时，

```bash
# 包含 flutter runtime, 打印机驱动等, librustdesk.{dll,dylib,so} 的文件夹
build_dir=...
python3 ./generate.py -f ../../${build_dir}/ -o . -e ../../${build_dir}/XXXXDesk.exe
```

或者于CI中移除 `skip_portable_pack` 。

## 输入事件

Rustdesk 有多种不同输入方式，其中 `LegacyMode` 全权使用 `enigo`，翻译和 1:1 模式则混合使用 `enigo` 或 `rdev`。

顺带一提，Linux 平台下，Rustdesk 可能会启动输入服务并且通过IPC发送输入按键。

`src/ui_session_interface.rs` 中， `get_keyboard_mode` 负责返回会话使用的键盘模式。

