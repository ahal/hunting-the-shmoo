---
title: "Managing Multiple Mozconfigs"
date: 2021-03-16T09:48:48-04:00
tags: [mozilla, mozconfigwrapper, tools-tip-tuesday]
slug: managing-multiple-mozconfigs
---

Mozilla developers often need to juggle multiple build configurations in their day to day work.
Strategies to manage this sometimes include complex shell scripting built into their mozconfig, or a
topsrcdir littered with `mozconfig-*` files and then calls to the build system like
`MOZCONFIG=mozconfig-debug ./mach build`. But there's another method (which is basically just a
variant on the latter), that might help make managing mozconfigs a teensy bit easier:
[mozconfigwrapper](https://github.com/ahal/mozconfigwrapper).

In the interest of not documenting things in blog posts (and because I'm short on time this
morning), I invite you to read the README file of the repo for installation and usage instructions.
Please file issues and don't hesitate to reach out if the README is not clear or you have any
problems.

<!--more-->

This tip is almost as old as the hills, but part of the motivation behind this [tips
series](https://ahal.ca/tags/tools-tip-tuesday/) is to not take for granted that developers are
aware of all the tools available to them. Maybe you are one of the many new folks who joined Mozilla
since I [last blogged](https://ahal.ca/blog/2011/mozconfigwrapper-introduction/) about this, or
maybe you are just one of today's [lucky 10,000](https://xkcd.com/1053/) (or more like lucky
handful).
