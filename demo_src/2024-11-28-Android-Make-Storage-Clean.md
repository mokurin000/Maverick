---
layout: post
title: Android 如何保持眼中存储干净
slug: android-make-storage-clean
date: 2024-11-28 13:27
status: publish
author: Poly000
categories: 
  - Android
tags: 
  - Android
  - Magisk
  - KernelSU
  - Xposed
  - Storage_Management
---

## [存储空间隔离](https://sr.rikka.app/zh-hans/)

> 由 RikkaApps 开发。
> 
> 由于基于目录重定向，垃圾文件实际上是放在了独立的空间

### 优点

- 较为可控的目录限制
- 可以阻止访问主用户隐私数据
- 不同应用之间，无法基于内置存储中的垃圾文件追踪用户

### 缺点

- 付费闭源软件
- 需要 Magisk/KernelSU/Xposed
- 常年未更新，Android 14+ 支持未来堪忧
- 非 Google Play 渠道购买，均为限制单手机使用

## [IsLand](https://play.google.com/store/apps/details?id=com.oasisfeng.island)

> 开发者同《绿色守护》
> 
> 隔离环境，把国产软件塞一起；
>
> 基于Work Profile实现，国产ROM兼容性不一定好

### 优点

- 也可用于反取证
- 单空间使用，无需 Root
- 可以阻止访问主用户隐私数据
- (root+放弃支付软件) 不同应用之间，无法基于内置存储中的垃圾文件追踪用户

### 缺点

- 新版本转为闭源软件
- 需要Root才能开启多个工作资料，互相隔离不同国产应用
- 输入法、支付应用调用都是分割的，这一点会影响上一条

## [Insular](https://secure-system.gitlab.io/Insular/)

> [#IsLand](#island) 的开源复刻实现。

## [black_and_white_list](https://github.com/Petit-Abba/black_and_white_list)

> 代码质量极差，但是目前没人写类似的打包了的东西
>
> 定期清理，最原始的方式

### 优点

- 较为灵活
- 提供了白名单，避免误删
- 应用无关，单纯写路径规则
- 不同应用之间，无法基于内置存储中的垃圾文件追踪用户

### 缺点

- 久年未更
- 未提供图形化设置方式
- 配置文件为未知文本解析方式
- 依赖 Magisk 和大量不规范行为
- 基于 crond ，古老的定时服务方式
  
## [garbage-remove](https://github.com/mokurin000/garbage-remove)

> Rust实现
> 
> 同样是定期清理

### 优点

- 无需Root
- 高性能，高可读日志
- 配置文件为 toml 格式
- 默认不允许删除相对路径
- 不同应用之间，无法基于内置存储中的垃圾文件追踪用户

### 缺点

- 未提供图形化设置方式
- 过度优化的实现，使用mpmc+多线程删除
- 未提供模块服务方式运行，需要手动保活

## 买台 iPhone 备用机

> 终极方案，长久有效

### 优点

- 隐私保护最好的方式
- 省心，不会遇到各种风控过不去
- 环境物理隔离，不再担心侧漏检测

### 缺点

- 成本较高
