# -*- coding: utf-8 -*-
"""Sample Configuration
"""

# For Maverick
site_prefix = "/"
template = "Kepler"
index_page_size = 10
archives_page_size = 30
fetch_remote_imgs = False
enable_jsdelivr = {
    "enabled": False,
    "repo": "AlanDecode/Maverick@gh-pages"
}
locale = "Asia/Shanghai"
category_by_folder = False

# For site
site_name = "poly000客栈"
site_logo = "${static_prefix}android-chrome-512x512.png"
site_build_date = "2020-09-29:00+08:00"
author = "poly000"
email = "1348292515@qq.com"
author_homepage = "https://poly000.github.io"
description = "poly000 的碎碎念"
key_words = ["poly000", "blog"]
language = 'chinese'
external_links = [
    {
        "name": "liolok",
        "url": "https://liolok.com/",
        "brief": "liolok的博客"
    },
    {
        "name": "Integral",
        "url": "https://blog.i7.homes/",
        "brief": "Integral 的博客"
    },
    {
        "name": "Leon Cha",
        "url": "http://leoncha.online/",
        "brief": "Leon Cha 的博客"
    },
    {
        "name": "aidenpers",
        "url": "https://www.aidenpers.xyz",
        "brief": "aidenpers的博客"
    },
    {
        "name": "ControlNet",
        "url": "https://controlnet.space/",
        "brief": "ControlNet的博客"
    },
    {
        "name": "Sbchild",
        "url": "https://sbchild.top/blog/",
        "brief": "色妹妹的船新博客"
    },
    {
        "name": "HypengW",
        "url": "https://blog.bluempty.com/",
        "brief": "HypengW的博客"
    }
]
nav = [
    {
        "name": "Home",
        "url": "${site_prefix}",
        "target": "_self"
    },
    {
        "name": "Archives",
        "url": "${site_prefix}archives/",
        "target": "_self"
    },
    {
        "name": "About",
        "url": "${site_prefix}about/",
        "target": "_self"
    }
]

social_links = [
    {
        "name": "GitHub",
        "url": "https://github.com/poly000",
        "icon": "gi gi-github"
    },
    {
        "name": "Twitter",
        "url": "https://twitter.com/_poly000",
        "icon": "gi gi-twitter"
    },
    {
        "name": "Bilibili",
        "url": "https://space.bilibili.com/25382793",
        "icon": "gi gi-bilibili"
    }
]

valine = {
    "enable": True,
    "el": '#vcomments',
    "appId": "IKRAfuPq0zrz6Wfje8ahHAIP-gzGzoHsz",
    "appKey": "lFaCWkd4xCs0Ng5UWs1eHNwU",
    "visitor": True,
    "recordIP": True
}

head_addon = ''

footer_addon = ''

body_addon = ''
