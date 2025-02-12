---
title: "Using Jujutsu With Mozilla Unified"
date: 2025-02-12T15:19:55-05:00
tags: [jujutsu, mozilla]
slug: jujutsu-with-mozilla-unified
draft: false
---

With Mozilla's migration from `hg.mozilla.org` to Github drawing near, the clock
is ticking for developers still using Mercurial to find their new workflow. I
previously blogged about how [Jujutsu can help here], so please check that post
out first if you aren't sure what Jujutsu is, or whether it's right for you. If
you know you want to give it a shot, read on for a tutorial on how to get
everything set up!

We'll start with an existing Mercurial clone of [mozilla-unified], convert it to
use [git-cinnabar] and then set up [Jujutsu] using the co-located repo method.
Finally I'll cover some tips and tricks for using some of the tooling that
relies on version control.

[Jujutsu can help here]: https://ahal.ca/blog/2024/jujutsu-mercurial-haven/
[mozilla-unified]: https://hg.mozilla.org/mozilla-unified/
[git-cinnabar]: https://github.com/glandium/git-cinnabar
[Jujutsu]: https://github.com/jj-vcs/jj

<!--more-->

Backup Your Repo
----------------

First things first, backup your `.hg` directory! This way if anything goes wrong
or you decide that Jujutsu is just not for you, you'll be able to restore your
repo back to a known good state. This tutorial assumes you'll be running all
commands from the root of your `mozilla-unified` clone.

```console
$ cp -r .hg ~/backup/hg
```

With backup ready, let's get started!

Convert Bookmarks to Tags
-------------------------

When you first clone `mozilla-unified`, the different Firefox trees (like
`autoland`, `central`, `beta`, etc) will be represented as Mercurial bookmarks.
This is fine and will work, but it will result in overly verbose refs when
converting the repo over to Git via `git-cinnabar`. It'll make things much nicer
if you first convert them to tags:

1. Make sure you have the [firefoxtree] extension installed. You can verify
   whether it's installed by running `hg fxheads`. If the command is not found,
   you'll need to install it by running:
   
   ```console
   $ ./mach vcs-setup
   ```

3. Pull in all Firefox trees that you want to have a ref for in Git. Typically
   you'll want at least `central` and `autoland`, but you might as well have one
   for all active trees:

   ```console
   $ echo "autoland central beta release esr128 esr115" | xargs hg pull
   ```

   Pulling each of these trees in will cause the `firefoxtree` extension to
   create a tag for it in your local repo. Verify the set of tags match what you
   expect by running `hg fxheads`.

2. Now delete all bookmarks referencing Firefox trees, they are no longer needed:

   ```console
   $ hg bookmark -T "{bookmark}\n" | grep -P 'aurora|autoland|beta|central|esr\d+|fx-team|inbound|release' | xargs hg bookmark -d
   ```

[firefoxtree]: https://mozilla-version-control-tools.readthedocs.io/en/latest/hgmozilla/firefoxtree.html


Convert Your Repo to Git
------------------------

Next we'll convert the repo to Git using `git-cinnabar`. These instructions are
borrowed from Glandium's post titled *[How I (kind of) killed Mercurial at
Mozilla]*, a great read diving into the history of VCS at Mozilla.

Warning: Many of these steps will take some time, so be sure to have your coffee
apparatus of choice on standby.

1. Install `git-cinnabar` if needed:

   ```console
   $ mkdir -p ~/.mozbuild/git-cinnabar
   $ cd ~/.mozbuild/git-cinnabar
   $ curl -sOL https://raw.githubusercontent.com/glandium/git-cinnabar/master/download.py
   $ python3 download.py && rm download.py
   ```

   Add `~/.mozbuild/git-cinnabar` to your `$PATH` in your `~/.bashrc` file or equivalent.

2. Initialize a Git repo and point origin to the Mercurial remote:

   ```console
   $ git init
   $ git remote add origin https://github.com/mozilla/gecko-dev
   $ git remote update origin
   $ git remote set-url origin hg::https://hg.mozilla.org/mozilla-unified
   $ git config --local remote.origin.cinnabar-refs bookmarks
   $ git remote update origin --prune
   ```

3. Fetch Mercurial refs to bring over your WIP changes. If you use Mercurial
   bookmarks to track all your feature branches, this is easy. Simply run:

   ```console
   $ git -c cinnabar.refs=bookmarks fetch hg::$PWD refs/heads/*:refs/heads/hg/*
   ```

   However if you have any unnamed heads you want to carry over, things are a
   bit trickier. You can create refs for them in Git by running:

   ```console
   $ git -c cinnabar.refs=heads fetch hg::$PWD refs/heads/default/*:refs/heads/hg/*
   ```

   However this has the unfortunate consequence of also pulling in every head
   from the entirety of Mozilla's history, most of which will not be owned by
   you. If this doesn't bother you then go for it! But personally I recommend
   making sure that every WIP feature branch you have is associated with a
   bookmark, then import the refs as bookmarks above. Either way works.

4. Checkout the proper working commit:

   ```console
   $ git reset $(git cinnabar hg2git $(hg log -r . -T '{node}'))
   ```

   At this point, you should have a working Git checkout of `mozilla-unified`!
   Run `git branch` and verify that the refs you imported all show up as
   branches with an `hg/` prefix.

5. Lastly remove Mercurial:

   ```console
   $ rm -rf .hg
   ```

   Good night sweet prince.

[How I (kind of) killed Mercurial at Mozilla]: https://glandium.org/blog/?p=4346


Setup Jujutsu
-------------

Now for the last bit, setting up Jujutsu! If you haven't already, make sure you
[have it installed]. Be sure to install at least version `0.26`.

1. Initialize a co-located repository:

   ```console
   $ jj git init --git-repo .
   ```

   Co-location simply means that the `.jj` and `.git` directories will both be
   present at the repo root. This is especially important for `mozilla-unified`
   as there is a lot of tooling that assumes you are working with Git. By
   leaving the `.git` directory around, this tooling mostly just continues to
   work out of the box!

2. Set the trunk and immutable heads revsets. First run:

   ```console
   $ jj config edit --repo
   ```

   Then add the following:

   ```toml
   [git]
   subprocess = true

   [revset-aliases]
   "trunk()" = "central@origin"
   "immutable_heads()" = '''
   builtin_immutable_heads()
   | remote_bookmarks('aurora')
   | remote_bookmarks('autoland')
   | remote_bookmarks('beta')
   | remote_bookmarks('esr')
   | remote_bookmarks('fx-team')
   | remote_bookmarks('inbound')
   | remote_bookmarks('release')
   '''
   ```
   
   Setting `git.subprocess=true` tells Jujutsu to shell out to Git rather than
   relying on libgit2. Without this change, running `jj git fetch` will fail as
   it can't understand the `hg::` urls. This option will default to `true` in a
   future release anyway.

   As far as the revset aliases go, the first alias tells Jujutsu which
   bookmark contains the mainline development, in this case the `central`
   branch. The second revset provides a list of changes that should be
   considered immutable. In our case, that's anything under one of the Firefox
   trees in `mozilla-unified`.

3. Track remote bookmarks. This is optional, but I like to track any remote
   bookmarks that I might be working with. Mainly because I like to exclude
   `untracked_remote_bookmarks()` from my default log revset, but also because
   it makes the log look a little cleaner. Run:

   ```console
   $ jj bookmark track autoland@origin central@origin beta@origin release@origin
   ```

   You can track which ever remote bookmarks you like.

And you're done! You've now converted your Mercurial repo to a Jujutsu repo
backed by Git. Run `jj` to see the log, it should look similar to the `hg wip`
alias that `./mach vcs-setup` created for you. If all went well, you should see
all your WIP bookmarks that you converted from Mercurial.

I've decided that going into details on how to use Jujutsu is out of scope for
this tutorial. Instead take a look at Steve Klabnik's [Jujutsu Tutorial]. I do
want to touch on a few `mozilla-unified` specific points though, so read on for
that.

[have it installed]: https://jj-vcs.github.io/jj/latest/install-and-setup/
[Jujutsu Tutorial]: https://steveklabnik.github.io/jujutsu-tutorial/

Jujutsu in mozilla-unified
--------------------------

Generally commands like `mach build` or `mach test` that don't rely on version
control will work just as before. But there's a few workflows that do rely on
version control, and it's worth noting a couple things about them.

#### Pushing to Try

Whatever modifications you have in your working copy commit in Jujutsu, will
appear as uncommitted changes in the Git backend. So when you push to try, you
might see:

```console
$ ./mach try empty
ERROR please commit changes before continuing
```

Even though in Jujutsu, your changes are *always* committed. The workaround to
this is simply to make sure you're on an empty change before pushing:

```console
$ jj new
$ ./mach try empty
```

If you use the [squash workflow] (which I highly recommend), you should be on an
empty change most of the time anyway.

[squash workflow]: https://steveklabnik.github.io/jujutsu-tutorial/real-world-workflows/the-squash-workflow.html

#### Using moz-phab

The `moz-phab` tool has a similar caveat, but as long as you run it from an
empty commit, submitting should mostly work just fine. However `moz-phab patch`
tends to not work very well.

Erich Gubler has a [moz-phab fork] that fixes both these things. It allows you
to run `moz-phab submit` without being on an empty commit, and it also fixes
`moz-phab patch`. I'm not sure what the plan is for getting this upstreamed, but
if you want to use it in the meantime, you can do so with:

```console
$ pip install MozPhab@git+https://github.com/erichdongubler-mozilla/review@refs/pull/1/head
```

[moz-phab fork]: https://github.com/erichdongubler-mozilla/review/pull/1


#### Fixing Lint Issues

The `mach lint` command works just fine out of the box, but Jujutsu provides a
convenience wrapper for fixing issues with `jj fix`. The benefit of using `jj fix`
is that it will step through all the mutable changes in your feature branch, and
apply fixes to the files each change touches one by one. This means you'll never
have a lint issue fixed in a commit that didn't introduce the issue ever again.

You can integrate `mach lint` with `jj fix` by following [these instructions].
Once set up, get in the habit of running `jj fix` before running `mach lint`.

[these instructions]: https://firefox-source-docs.mozilla.org/code-quality/lint/usage.html#jujutsu-integration


#### Get in Touch

The last tip is to get in touch with the Mozilla Jujutsu community. There's more
and more of us hanging out in `#jj` on Slack, where we share tips, ask questions
and help each other out. Come drop by!
