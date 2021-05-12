---
title: "A Better Replacement for ls"
date: 2021-04-06T11:05:21-04:00
tags: [mozilla, tips-and-tricks]
slug: ls-replacement
---

> If it ain't broke don't fix it.

This old addage is valuable advice that has been passed down through
generations. But it hasn't stopped these people from [rewriting command line
tools](https://zaiste.net/posts/shell-commands-rust/) perfected 30+ years ago in Rust.

This week we'll take a quick look at [exa](https://the.exa.website/), a replacement for `ls`. So why
should you ignore the wise advice from the addage and replace `ls`? Because there are marginal
improvements to be had, duh! Although the improvements in this case are far from marginal.

<!--more-->

So why is `exa` more than marginally better than `ls`?

* Saner defaults, e.g human readable file sizes by default
* Beautiful colours
  - Including the ability to customize colours by file type
* Git status integration with `--git`
* Tree view with `-T/--tree`
* Long grid view with `--grid --long`
* Icons with `--icons` (needs font that supports them, check out the
  [nerdfonts](https://www.nerdfonts.com) project to obtain one)
* The `--color` flag can also be written as `--colour` (us Canadians understand why this is
  important)
* and more!

If you still aren't convinced, check out the [features](https://the.exa.website/features) page for
a deep dive into any of the above.

Take a look at the [installation instructions](https://the.exa.website/install). It exists in many
package managers, you can use `cargo install exa` or simply download the binary and drop it in your
`$PATH`. Because I can't think of any reason to use `ls` after installing `exa`, I've also added:

```bash
alias ls="exa"
```

to my shell's profile (muscle memory is hard to overcome). Enjoy!
