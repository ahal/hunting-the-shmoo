---
title: "Jujutsu: A Haven for Mercurial Users at Mozilla"
date: 2024-11-08T08:19:33-04:00
tags: [jujutsu, mozilla, productivity]
slug: jujutsu-mercurial-haven
---
One of the pleasures of working at Mozilla, has been learning and using the
[Mercurial] version control system. Over the past decade, I've spent countless
hours tinkering my worfklow to be *just so*. Reading docs and articles,
meticulously tweaking settings and even [writing an extension].

I used to be *very* passionate about Mercurial. But as time went on, the
culture at Mozilla started changing. More and more repos were created in
Github, and more and more developers started using [git-cinnabar] to work on
`mozilla-central`. Then my role changed and I found that 90% of my work was
happening outside of `mozilla-central` and the Mercurial garden I had created
for myself.

So it was with a sense of resigned inevitability that I took the news that
Mozilla would be [migrating mozilla-central to Git]. The fire in me was all but
extinguished, I was resigned to my fate. And what's more, I had to agree. The
time had come for Mozilla to officially make the switch.

Glandium wrote an [excellent post] outlining some of the history of the
decisions made around version control, putting them into the context of the
time. In that post, he offers some compelling wisdom to Mercurial holdouts like
myself:

> I'll swim against the current here, and say this: the earlier you can switch
> to git, the earlier you'll find out what works and what doesn't work for you,
> whether you already know Git or not.

When I read that, I had to agree. But, I just couldn't bring myself to do it.
No, if I was going to have to give up my revsets and changeset obsolesence and
my carefully curated workflows, then so be it. But damnit! I was going to
continue using them for as long as possible.

And I'm glad I didn't switch because then I stumbled upon Jujutsu.

[Mercurial]: https://www.mercurial-scm.org/
[writing an extension]: https://hg.sr.ht/~ahal/bookbinder
[migrating mozilla-central to Git]: https://groups.google.com/a/mozilla.org/g/firefox-dev/c/QnfydsDj48o/m/8WadV0_dBQAJ
[excellent post]: https://glandium.org/blog/?p=4346

<!--more-->

## What is Jujutsu?

[Jujutsu] is a new(ish) version control system originally developed by Martin
Von Zweigbergk of Google. Martin is a [long time contributor] to Mercurial on
behalf of Google. It's unclear to what degree Jujutsu is officially sanctioned
by Google vs Martin's personal project, but one thing that's clear is that he
poured his decade+ of Mercurial learnings into this project. Jujutsu is packed
with concepts that Mercurial users will be familiar with, such as nameless
heads, revsets, immutable commits and powerful history editing. But it also
borrows concepts from other modern DVCS like [Sapling] (remote bookmarks) and
[Pijul] (first class conflicts). It's also written in Rust, so doesn't suffer
from many of the performance woes that have long plagued Mercurial.

But here's the real kicker, the main reason Jujutsu is even worth considering at all:
**It uses Git as a backend**

That's right, you can initialize Jujutsu inside an existing Git repo, and the
other people working on that repo will be none the wiser. Git is so dominant,
that this capability should now be considered table stakes for any budding DVCS
projects out there. Without it, those projects will be doomed to obscurity.

Jujutsu does also have its own native backend, but the docs warn users away
from using it in production repos. For now, the native backend is more of a
proof of concept than anything.

[Jujutsu]: https://martinvonz.github.io/jj/latest/
[long time contributor]: https://repo.mercurial-scm.org/hg/log?rev=reverse(author(%22Martin%20Von%20Z%22))&revcount=1000
[Sapling]: https://sapling-scm.com/docs/introduction/
[Pijul]: https://pijul.org/

## Is it any good?

Yes.

## What makes Jujutsu good?

Great question! There are many standout features, but if I had to distill it
down, I'd say Jujutsu is good because it is equal parts simple and powerful.
Simple both in terms of the UI (which is stellar), but also in terms of
cognitive load (the ability to keep track of your changes). Powerful because
of the fantastic history re-writing and conflict resolution capabilities.

But I don't want to go too far into the details in this particular post. If
you're interested in learning more about what makes Jujutsu special, I'd
recommend reading [jj-init] by Chris Krycho. Or if you're more of a hands on
type of person, Steve Klabnik's [Jujutsu tutorial].

Instead I want to focus more on why Jujutsu should appeal to Mercurial users,
as this topic is currently extremely relevant to many of my colleagues at
Mozilla. So here goes.

[jj-init]: https://v5.chriskrycho.com/essays/jj-init/
[Jujutsu tutorial]: https://steveklabnik.github.io/jujutsu-tutorial/introduction/introduction.html


## Why Jujutsu should appeal to Mercurial users

The high level thesis here is that Jujutsu takes the vision that Mercurial was
striving for, and bumps it up a notch. This isn't to imply that Mercurial has
somehow failed to achieve their vision, quite the opposite. The Mercurial
project has done an absolutely *fantastic* job demonstrating what a modern DVCS
is capable of. But they have to do so within the confines of technical debt and
backwards compatibility. Jujutsu free of such shackles, is simply able to make
bolder decisions. To push the enveloppe a bit further. And the results are
exciting!

Here are some examples of what I mean.


### Changes vs Commits

Like Mercurial, Jujutsu distinguishes between a commit and a change. In
Mercurial, each changeset has both a _commit id_, which is a hash of all the
contents of the diff (just like Git), but also a _revision id_. This is simply
a counter that increments by one every time a new changeset is created. This
has a couple nice properties:

1. It's easier to refer to (revision ids are much smaller than commit ids).
2. It's easier to track the latest change via the `tip` label.
3. It's easier to tell at a glance the chronological order of changes (even
   across heads).

But Jujutsu kicks this up several notches. It too has a commit id, but instead
of a simple integer counter that increments, it assigns a _change id_ to each
change which stays static across the change's lifecycle. What does that mean?

Say you create a new change with `jj new`. It'll be assigned an identifier
consisting of random letters, e.g `oypoztxk` (the actual ID is longer, but
typically only the first eight characters are ever displayed). Now let's say
I amend the change by editing some files or creating a commit message. The 
change's _commit id_ will now be different (just like with Mercurial or Git),
but the _change id_ will be the same! It's still `oypoztxk`.

What's more, you only need to type the unique prefix of the change id. This
depends on the repo, but let's pretend the unique prefix of this change is
`oy`. This means I can do things like:

```console
jj rebase -b oy -d main
```

And it gets even better! When resolving prefixes, Jujutsu will first scan
your work in progress changes and their immutable parents. So even if you're
working on a massive repo like `mozilla-central`, the unique prefix for the
changes you care about are still only going to be 1-3 characters long
(depending on how many in-progress changes you have going at once). This
means that as you work on changes, you start to memorize their prefixes.

With Mercurial, I've historically been a very heavy bookmark user. I even
wrote [bookbinder] so I could stack my bookmarks on top of each other with
ease. But with Jujutsu, labelling your feature branches is (imo) completely
unnecessary. It is still possible to create bookmarks to track your feature
branches if you desire, just be aware that unlike Mercurial, they do not
automatically advance when you create a new change. I was _very_ skeptical of
the lack of automatic advancing when I first started using Jujutsu, and was
worried manually setting bookmarks was going to be a massive pain. But thanks
to change ids and their prefixes, I haven't even been using bookmarks at all.

[bookbinder]: https://hg.sr.ht/~ahal/bookbinder

### History Editing

Like Mercurial, Jujutsu has really nice history editing capabilities. There's
some things that are nicer, but also a few features missing. Most notably on
the missing front, are an equivalent to `hg histedit` (or `git rebase -i`) and
`hg absorb`. I think these just haven't been implemented yet, and I suspect
they'll make their way into the feature set eventually.

I wouldn't say that Jujutsu's history editing is much better than Mercurial's,
the latter's is already very very good. But there are a few things I appreciate
where Mercurial falls a bit short.

The first is simply making all the capabilities available out of the box. With
Mercurial, you need to enable a bunch of [extensions] to unlock its full
potential. I believe the rationale was to prevent footguns, but I think it just
made the tools more difficult to find.

The second thing I appreciate (which is also the reason that Jujutsu doesn't
need to care about footguns as much), is the _operation log_ (or _oplog_).
Basically every command you run is recorded in an operations log, and you can
jump back to an earlier state anytime you mess something up. Botch a rebase?
Just run `jj undo`. Abandon the wrong change? `jj undo`. Push to the wrong
remote? `jj un..` just kidding, you're screwed on that one. The _oplog_ is kind
of like Git's reflog, but transaction based instead of state based. You can
also restore to a prior state with Mercurial, but it's complicated enough that
I don't remember offhand how to do it. I'm not saying it's difficult, but it's
certainly not as easy as `jj undo`.

The third thing I appreciate is the UI around history re-writing. Mercurial's
UI is also very good, but Jujutsu just adds some extra niceities. Part of this
is the ease at which you can reference any individual change thanks to the
change id prefixes I talked about in the last section. But it's also the
thoughtfully designed cli. Such as the `-B/--insert-before` and
`-A/--insert-after` flags that many commands accept. I mentioned that there was
no equivalent to `hg histedit` or `git rebase -i` (yet), but it's not really a
problem. Need to re-order changes? It's a cinch with `jj rebase -r oy -B
ht`. Need to edit a change earlier in the stack? Simply run `jj edit ht`.
Accidentally forgot to update to a change before saving the file? No problem,
`jj squash --into ht`. The UI is simple, intuitive and powerful.

[extensions]: https://pypi.org/project/hg-evolve/

### Obsolete Changes

Mercurial and Jujutsu both have a concept of _obsolete_ changes. This is
related to history editing, but moreso around what happens afterwards. When you
edit a change, there's something going on under the hood! You're actually
creating a brand new change and the old one is being marked obsolete.

In Mercurial's implementation (called [changeset evolution]), it's possible to
have "orphan" changes. For example, if you have the history:

```text
A -> B -> C
```

Then you make a change to `B`, your history now looks like:

```text
A -> B -> C
 `-> B'
```

In Mercurial, `B` is now said to be "obsolete" and `C` is said to be "orphaned".
You as the user are now responsible for moving `C` on top of `B'` (either via
rebasing or special commands designed to deal with this scenario).

Jujutsu does the exact same thing, except the last step happens automatically.
You'll never see an orphaned change in the log because whenever you edit
history, the entire stack is implicitly rebased! In fact, if you push your
change to a Github pull request, then it merges to `main` and you fetch the
change back into your repo with `jj git fetch`, Jujutsu will detect that your
original change is now obsolete and automatically mark it as such! No need to
run commands like `hg prune` after landing (caveat: this particular feature
doesn't work well with Phabricator due to Phabricator editing the commit
message).

[changeset evolution]: https://wiki.mercurial-scm.org/ChangesetEvolution

### Revsets, Templates and Files

Mercurial users will rejoice to know that Jujutsu brings along the concept of
[revsets]. For those not in the know, revsets are a specification language to
select changes using logical operators and functions. In both Mercurial and
Jujutsu, nearly every command accepts a `-r/--revset` argument which allows you
to operate on one or more changes at once. Like Mercurial, Jujutsu also has a
[template language], and [file specification language].

I'll be honest here. So far I like Mercurial's revset and template languages
better. But I think this is mainly due to the fact that I'm used to them, and
Jujutsu's implementations are incomplete. I recently asked in the Jujutsu
Discord whether it was possible to accomplish something in the template
language. It wasn't, but a maintainer had a patch landed to implement the
missing feature the next day.

So as I get used to the syntax differences, and more features get implemented
here, I suspect I'll end up liking Jujutsu's revsets and templates just as
much as Mercurial's.

[revsets]: https://martinvonz.github.io/jj/latest/revsets/
[template language]: https://martinvonz.github.io/jj/latest/templates/
[file specification language]: https://martinvonz.github.io/jj/latest/filesets/

### Log

Back in 2014, I read a [blog post] from Jordi Gutiérrez Hermoso that blew my
mind. In it he demonstrates what Mercurial log could be made to do with heavy
use of revsets, templates and colours. I immediately implemented it and have
never looked back since. At Mozilla we thought this view was so useful that
we implemented a helper that set it up for all our developers automatically.

After many many years, a (imo less nice looking) version of this view was
implemented into Mercurial core under the command `hg show work`. This was a
fantastic step, but it was still kind of tucked out of the way in a little
known command.

Contrast this to running `jj log`:

![A screenshot of Jujutsu's log](/static/img/blog/2024/jj-log.png "jj log")

In fact, you can just type `jj` on its own to see it. This view is the single
most important view that any DVCS can show you. Jujutsu took an existing
feature pioneered at Mercurial, and made it as accessible as possible to its
users. That, and the default format looks great!

[blog post]: http://jordi.inversethought.com/blog/customising-mercurial-like-a-pro/

### Immutable Changes

Just like Mercurial, Jujutsu has immutable changes. But Jujutsu's approach is
far simpler (albeit less powerful). Mercurial implements immutability via
something called phases, changes can either be `draft`, `public` or `secret`.
Phase information can also be pushed to and pulled from the server, so in
theory it's possible to collaborate on draft commits with others before making
them public.

This is powerful, but also confusing and can lead to footguns. When pushing a
change, you need to be aware of whether the server is "publishing" or not. You
can get into situations that require manually changing the phase of a change.
And I still don't really know what a "secret" change is, I just ignored that
completely.

With Jujutsu, you define a revset called `immutable_heads()`, it defaults to
the `main`, `master` or `trunk` branches of Git remotes called `origin` or
`upstream`. But this can be overridden, e.g in `mozilla-central` you'd need to
tell it to select the `autoland`, `central`, `beta`, etc branches.

That's it. It's not as powerful, immutability status is not sent to the server
(and it will never be able to do this with the Git backend), but it's much
simpler and easier to understand. Plus, it should solve 99% of use cases and
reduce the number of footguns (as compared to both Mercurial and Git).

## Things that Jujutsu does Better

Up until now, I've been outlining many of the similiarities between Jujutsu
and Mercurial. In many cases, Jujutsu has made appreciable improvements on
top of features that were inspired by Mercurial.

But there are a couple places where Jujutsu is simply head and shoulders above
Mercurial.

### Defaults

I touched on this a bit in the _Log_ and _History Editing_ sections, but
Jujutsu has great defaults. Nothing is hidden behind extensions (built-in or
otherwise), no tweaks are needed to get a useful log. What you get out of the
box, is a very intuitive user experience.

As I said in the intro, I love to tinker with my workflows, but I can also
appreciate a well designed tool that needs little to no configuration. Jujutsu
is that. In my opinion, poor defaults (and a too strict adherence to preserving
backwards compatibility) is one of the reasons Mercurial failed to take off, so
I'm glad to see Jujutsu learning lessons here.

### Performance

Jujutsu is also much more performant than Mercurial. It's written in Rust (to
Mercurial's Python), so this isn't too surprising. To be fair to Mercurial,
performance has gotten a lot better over the years there as well. They've been
integrating Rust into their codebase, and using the `fsmonitor` extension along
with `chg`, can make Mercurial feel quite snappy (though Jujutsu also supports
file watching, which raises the bar even higher).

Ironically, one of the things I appreciate about Jujutsu, is that they _don't_
prioritize performance. There's lots of examples where Jujutsu makes a
conscious decision to prioritize ease of use over performance. I touched on one
example in the _Changeset Evolution_ section, where Jujutsu implicitly
rebases your stack anytime you re-write history. This prioritizes usability
over performance, but this trade-off is only possible thanks to how fast
Jujutsu already is. Mercurial simply couldn't make this trade-off, as rebasing
your stack is measured in seconds rather than milliseconds.

## A Piece of Wisdom

If you are a Mercurial user working on `mozilla-central` who is not looking
forward to the upcoming switch to Git, I hope this post has at least convinced
you to give Jujutsu a shot! It's absolutely possible to use Jujutsu in
`mozilla-central` via [git-cinnabar]. Also, if you're on Mozilla's internal
Slack instance, stop by `#jj` with any questions you might have!

I'll conclude with some words of wisdom I read somewhere once:

> I'll swim against the current here, and say this: the earlier you can switch
> to ~~git~~ Jujutsu, the earlier you'll find out what works and what doesn't work for you,
> whether you already know ~~Git~~ Jujutsu or not.

[git-cinnabar]: https://github.com/glandium/git-cinnabar
