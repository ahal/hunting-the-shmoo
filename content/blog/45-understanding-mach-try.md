---
title: "Understanding Mach Try"
date: 2021-03-23T10:51:01-04:00
tags: [mozilla, tips-and-tricks, try]
slug: understanding-mach-try
---

There is a lot of confusion around `mach try`. People frequently ask "How do I get task X in mach
try fuzzy?" or "How can I avoid getting backed out?". This post is not so much a tip, rather an
explanation around how `mach try` works and its relationship to the CI system (taskgraph). Armed
with this knowledge, I hope you'll be able to use `mach try` a little more effectively.

<!--more-->

## Coupling Mach Try to CI

In the old days of try syntax and the trychooser web page, the list of available tasks was entirely
decoupled from the CI system. This meant that every time we added a new task (or removed an old
one), someone would have to go and manually update trychooser and related docs to let everyone else
know about the new state of affairs. At first this wasn't such a huge deal as adding new tasks
wasn't *that common*. But as time progressed, and with the adoption of Taskcluster, we saw an
explosion of new tasks. As you might imagine these decoupled lists of tasks very quickly became
outdated. This meant folks would build a try syntax from the webpage only to get a failing decision
task. A very frustrating experience!

To solve this issue we decided to source the list of available tasks directly from the same command
that is used to generate tasks in CI, `./mach taskgraph`. That's why sometimes when you push you'll
see a message like:

```bash
$ ./mach try fuzzy
Task configuration changed, generating target task set
```

Followed by a (too long) delay while the set of tasks available on your current revision are
generated. To illustrate the point, if you run:

```bash
$ ./mach taskgraph target --fast --parameters project=mozilla-central
```

the command will output (almost) the exact same list that you would see in the `./mach try fuzzy`
interface. We'll get into the almost later.


## A Brief Primer on Task Generation

Establishing that `./mach try` sources its list of tasks from the taskgraph, unfortunately means
that to understand `./mach try` one must understand [taskgraph
generation](https://firefox-source-docs.mozilla.org/taskcluster/taskgraph.html#graph-generation).
Here's a simplified explanation.

1. Read all the `taskcluster/ci` configuration files and run them through
   [transforms](https://firefox-source-docs.mozilla.org/taskcluster/transforms.html) to produce a
   massive JSON object (4.3+ million lines when prettified) where each key represents a single task.
   This is called the "full task graph".
2. Prune tasks from the graph based on context from the
   [parameters](https://firefox-source-docs.mozilla.org/taskcluster/parameters.html). There are
   several filters, but most important is the one which determines which tasks should run on which
   project branches (autoland, mozilla-central, mozilla-beta, etc). This is called the "target task
   graph". This will contain the set of all tasks that are relevant to the current context (e.g
   branch, but also other things).
3. Apply further optimizations to the graph to prune out more tasks. This is called the "optimized
   task graph". Tasks pruned here are relevant to the current set of parameters, but might not be
   worth running for other reasons (e.g to save money, or because files affecting them weren't
   modified). This stage isn't relevant to `mach try`, I only mention it to raise the distinction
   between "target tasks" and "optimized tasks".

## Connecting the Dots

Let's revisit that taskgraph command that `./mach try` uses by default from earlier:

```bash
$ ./mach taskgraph target --fast --parameters project=mozilla-central
```

Applying our new found taskgraph knowledge, this means generate the "target tasks" using the
parameters file from the latest mozilla-central push. In other words, "get me all tasks that are
relevant on mozilla-central". So if you're searching for a task in the `./mach try fuzzy` interface
and you don't see it, it most likely means that the task isn't configured to run there (still
getting to that most likely).

In such a case, you may have been told to run `./mach try fuzzy --full`. This runs a taskgraph
command similar to:

```bash
$ ./mach taskgraph full --fast --parameters project=mozilla-central
```

The difference here is that we are generating the "full" set of tasks. That is, every single task
that exists! While using this flag can be handy to run a specific task no matter the context, care
must be taken since most of these tasks are not relevant to mozilla-central (and likely for a good
reason). They could be release tasks, or maybe they are running on platforms we've retired, or maybe
they are running in configurations that are completely busted. Expect try pushes with these types
of tasks to contain lots of failures that aren't your fault.

Note that I've been using `./mach try fuzzy` as an example here, but other selectors (such as
`./mach try chooser`) use the exact same logic to generate tasks as well. The only difference is the
interface to select them. The default `./mach try auto` selector is a whole other beast and does not
use local taskgraph generation.

## The Exception

I've alluded to an exception to the rules by using words like "almost" and "most likely". There are
a handful of tasks that are purposefully plucked out of the "target tasks" for a variety of reasons:

1. Sometimes we simply don't have enough capacity to allow people to use these resources heavily on
   try. A good example here is the `android-hw` platform which is just a few dozen phones running in
   a 3rd party device pool. If everyone started running their try pushes here it would easily be
   overwhelmed.
2. Sometimes certain configurations provide very little value. For example, shippable opt platforms.
   In this case, we've determined that there are essentially zero regressions that get caught on
   shippable opt that wouldn't have been caught with regular opt. So we hide these from try to avoid
   wasting resources in pushes that would inadvertently select both.
3. Sometimes tasks are just too expensive relative to the value they provide. An example here is all
   the ccov tasks. These take an extremely long time to run, and while we do want to keep them
   green, it's just too expensive relative to the few times they get broken on their own.

The full list of tasks that fall into this exception can be found
[here](https://searchfox.org/mozilla-central/source/taskcluster/taskgraph/target_tasks.py#23). We
realize that each and every one of these exceptions can result in backouts from otherwise well
tested pushes, which is super frustrating! I also think reasonable minds can disagree on which tasks
belong here and which ones don't. So if you feel like one of these exceptions is unreasonable,
please file a bug about it under `Firefox Build System :: Task Configuration`.

If you *really* need to see the exact set of tasks that could possibly cause you to get backed out,
there is a special flag to disable this exception. You can run it like so:

```bash
$ ./mach try fuzzy --disable-target-task-filter
```

But please use this flag sparingly! There are usually good reasons these tasks have been excluded
and the risk of being backed out has been factored into the decision.

## Summary

To summarize, the default set of tasks you see in `./mach try fuzzy` (and other selectors) are the
ones that run on mozilla-central, minus the tasks caught up in the exception. If you need to run a
task that doesn't run on central (e.g because you are developing it), you can use the `--full` flag
to see all available tasks. Just use it with caution, it has the potential to overselect *a lot* of
tasks.

This post was mostly about providing a general understanding of `mach try`. Look for a follow-up
post that builds on this understanding and provides some more advanced usage tips around `mach try`.

Thanks for reading!
