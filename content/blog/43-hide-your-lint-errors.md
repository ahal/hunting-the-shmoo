---
title: "Hide Your Lint Errors"
date: 2021-03-09T00:00:07-05:00
tags: [mozilla, productivity, tools-tip-tuesday]
slug: hide-your-lint-errors
draft: true
---

Have you ever submitted a patch to Phabricator only to have reviewbot reveal dozens of lint errors
all over? Or worse yet, have you landed before reviewbot had a chance to analyze your patch and been
backed out over lint failures? If so fear not, we've all been there. Still, it's hard not to feel a
little embarrassed when it happens. Luckily for you, it's pretty easy to eliminate the possibility
of it ever happening again!

<!--more-->

There are many places where one might want to run linters. In an editor for early and rapid
feedback. At commit or submit time in case you forgot to run it in an editor. At review time in case
you forgot to run it before submitting. Finally in CI in case all of the above fails. The key
area to focus on here is at submit time. While running linters in your editor or at commit time can
be beneficial, it's at submission that you'll want to have your backstop.

[Mozlint](https://firefox-source-docs.mozilla.org/code-quality/lint/mozlint.html) supports linting
files that have been touched in version control. Both outgoing changes that don't exist upstream
(via `./mach lint --outgoing`) and changes in your working directory that haven't been committed yet
(via `./mach lint --workdir`). At submit time, `--outgoing` is all we need. But how should you
run it?

Back in the reviewboard days, we used to recommend [setting up a VCS
hook](https://firefox-source-docs.mozilla.org/code-quality/lint/usage.html#using-a-vcs-hook). But
now that the `moz-phab` tool uploads a diff of your changes rather than pushing to a review repo,
that no longer works. And while you could still technically use a commit hook, I find `./mach lint`
isn't performant enough given how often I commit things. In the end, I use a simple shell alias:

```bash
alias review="mach lint -o && moz-phab submit"
```

Add the above to your `~/.bashrc` or equivalent. Now instead of running `moz-phab submit` to submit
to Phabricator, run `review` and you'll never accidentally submit with a lint error again.
