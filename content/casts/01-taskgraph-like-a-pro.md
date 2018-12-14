---
title: "Taskgraph Like a Pro"
date: 2018-12-14T12:21:21-05:00
tags: ["mozilla", "taskgraph", "fzf"]
slug: taskgraph-like-a-pro
draft: false
---

Have you ever needed to inspect the taskgraph locally? Did you have a bad time? Learn how to inspect
the taskgraph like a PRO. For the impatient skip to the installation instructions below.


<iframe src="https://player.vimeo.com/video/306431059" width="720" height="405" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
<br>

<!--more-->

#### Installation

First you'll need to install [fzf][0], if you've used `mach try fuzzy` before, it's already
on your system under `~/.mozbuild/fzf`, just make sure it's on your `$PATH`.

Next install `fx`:

```bash
$ npm install fx
```

Finally, add the following shell function to your `~/.bashrc` or equivalent:

```bash
tf () {
	fx "tg => String(require(\"child_process\").spawnSync(\"fzf\", [\"-f\", \"$1\"], {\"input\": Object.keys(tg).join(\"\n\")}).output).split(\"\n\").reduce((obj, key) => { obj[key] = tg[key]; return obj; }, {})" | fx
}
```

That's it!


#### Usage

Simply pipe the output of `mach taskgraph full -J` into the `tf` function (preferably saving it to a
file first:

```bash
$ ./mach taskgraph full -J > full.taskgraph
$ cat full.taskgraph | tg "win64 mochitest | reftest -1$"
```

The above will filter down all chunk 1 mochitest and reftest tasks on win64. The query syntax is
identical to the one used with `mach try fuzzy`. See `man fzf` for more details.

Happy inspecting!

[0]: https://github.com/junegunn/fzf
