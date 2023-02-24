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

<!--
Here's a good argument-starting question: which is faster and/or better, hardware RAID or software RAID?
-->

<!--
A lot of conventional wisdom says hardware RAID, but I mostly disagree. Let's ask the inverse question: how (or when) can hardware RAID be faster than software RAID?
-->

<!--
If you're doing RAID-5, the hardware could do XOR faster than your CPU can. But in modern systems XOR performance is pretty much constrained by the memory bandwidth, not CPU power. It is possible to have better memory bandwidth than the CPU (graphics cards do), but it's not cheap.
-->

<!--
If you're doing RAID-1, hardware RAID can reduce the bus bandwidth needed for writes from N DMA transfers to N disks to one DMA transfer to itself. But for this to make your system faster, you need to be saturating the PCI bus bandwidth with write traffic, which is not exactly common. (In theory you might see this with RAID-5 too.)
-->

<!--
I believe that's it. (Additions and corrections welcome.)
-->

<!--
The usual retort for all this is that while hardware RAID may be no faster than software RAID, at least you're offloading the work from your main CPU so the system's overall speed goes up. However, for this to matter your system needs to be CPU constrained and doing significant write IO (if you only have insignificant write IO, the extra CPU usage for software RAID will also be small). This is not exactly common either.
-->

<!--
There is one downside for software RAID: the operating system has to be running in order to use it, which can complicate early boot. But software RAID also has a lot of upsides, including hardware independence. (You're dependent on software, but you pretty much are anyways; only a few crazy people try moving filesystems between different operating systems.)
-->

<!--
The one wildcard I can see in hardware RAID's favour is virtualization, which might deliver a future of heavily used hardware running close to both CPU and IO saturation.
-->

<!--
(This entry is brought to you by the Tivoli Storage Manager documentation I was plowing through today, which made me grind my teeth by tossing off a 'hardware RAID is better than software RAID' bit in passing.)
-->