---
layout: post
title: 软RAID vs 硬RAID
slug: software-raid-versus-hardware-raid
date: 2023-02-24 22:08
status: publish
author: Poly000
categories: 
  - RAID
tags: 
  - RAID
  - Storage_Management
---

## Credit

[原文地址](https://utcc.utoronto.ca/~cks/space/blog/tech/HardwareVsSoftwareRAID)

## 正文

一个很容易引起争论的问题：硬RAID和软RAID哪个更快和（或）更好？

很多传统观点认为是硬RAID，但我很不同意。让我们问一个相反的问题：硬件RAID如何（或何时）比软件RAID快？

如果你要用RAID-5，硬件可以比你的CPU更快XOR。但是，在现代系统中，XOR的性能基本上受制于内存带宽，而不是CPU的能力。你可能有比CPU更好的内存带宽（显卡就是这样），但这并不便宜。

如果你要用RAID-1，硬件RAID可以减少写的总线带宽，从N个DMA传输到N个磁盘到一个DMA传输到自己。但是，为了使你的系统更快，你需要用写流量使PCI总线带宽饱和，这并不常见。(理论上，你也可以在RAID-5中遇到这种情况）。

就是这样。(欢迎补充和更正）

通常的反驳是，虽然硬件RAID可能不比软件RAID快，但至少把负荷从你的主CPU上转移了，所以系统的整体速度提高了。然而，要达到这种情况，你的系统需要在CPU方面很差，并且要做大量的写入IO（如果你的写入IO不是特别多，那么软RAID的额外CPU使用率也会很小）。这种情况也不太常见。

软件RAID有一个缺点：启动操作系统后才可以使用。这会使早期启动变得复杂。但软件RAID也有很多优点，如不依赖硬件。

> The one wildcard I can see in hardware RAID's favour is virtualization, which might deliver a future of heavily used hardware running close to both CPU and IO saturation.

我认为虚拟化是硬RAID的优势所在，可以帮你压榨硬件，达到CPU和IO饱和。

DeepL翻译后润色。