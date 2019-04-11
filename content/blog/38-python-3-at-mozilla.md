---
title: "Python 3 at Mozilla"
date: 2019-04-30T15:25:50-04:00
tags: [mozilla, python, jetty]
slug: python-3-at-mozilla
draft: true
---

Mozilla uses a lot of Python. Most of our build system, CI configuration, test harnesses, command
line tooling and countless other scripts, tools or Github projects are all handled by Python. In
mozilla-central there are over 3500 Python files (excluding third party files), comprising roughly
230k lines of code. Additionally there are [462 repositories][0] labelled with Python in the Mozilla
org on Github (though many of these are not active). That's a lot of Python, and most of it is
Python 2.

With Python 2's exaugural year well underway, it is a good time to take stock of the situation and
ask some questions. How far along has Mozilla come in the Python 3 migration? Which large work items
lie on the critical path? And do we have a plan to get to a good state in time for Python 2's EOL on
January 1st, 2020?

<!--more-->

[0]: https://github.com/mozilla?utf8=%E2%9C%93&q=&type=&language=python


### The Second Best Time to Plant a Tree

But before tackling those questions, I want to address another one that often comes up right off the
bat: Do we need to be 100% migrated by Python 2's EOL?

Technically, no. It will still be possible to install Python 2, and packages will still be available
on PyPi. But punting the migration into the indefinite future would be a big mistake, and here's
why:

1. Python 2 will no longer receive security fixes. While the risk of an issue being discovered that
   impacts Mozilla adversely may be slim, considering all of the mission critical uses of Python at
   Mozilla (e.g, signing builds), even the slightest risk deserves serious attention. Consider that
   there were [three CVE's][1] filed against Python 2.7 in 2018. Also consider that if I'm an
   attacker sitting on a Python 2 vulnerability with the foreknowledge of an EOL date, I'm going to
   shelve the vulnerability until after that date has passed.

2. Perhaps more importantly, all of the third party packages we rely on (and there are a lot of
   them) will also stop being supported (assuming they haven't dropped support already). There is a
   much higher potential for vulnerabilities and bugs in the broader package ecosystem, [getting
   security right][2] is hard. *Using Python 2 and its package ecosystem for mission critical
   applications beyond 2020 is asking for trouble.*

3. Delaying means more code to migrate. When you want to interface with a large Python 2 code base,
   you need to write code that is compatible with Python 2. While its possible to write Python code
   that is compatible with both 2 and 3, the incentives to do so are not always evident. Or the
   know-how is missing. As of today, most of the Python code we write at Mozilla is only Python 2
   compatible. The longer we delay the migration, the more gargantuan the task becomes.

4. There is an ongoing opportunity cost. Python 3 was first released in 2008 and in that time there
   have been a huge number of features and improvements that are not available in Python 2. Things
   like async/await, exception chaining, type hints and unicode handling. With the time Mozilla
   developers have spent dealing with that last item alone, we probably could have completed the
   entire migration.

So is January 1st, 2020 a hard deadline? No. But that shouldn't stop us from moving forward with the
migration as fast as we're able. Not for the sake of a deadline, but because it will give Mozilla
the best chance at success.

The best time to get serious about migrating to Python 3 was five years ago. The second best time is
now.

[1]: https://www.cvedetails.com/vulnerability-list/vendor_id-10210/product_id-18230/version_id-92056/Python-Python-2.7.html
[2]: https://hackernoon.com/10-common-security-gotchas-in-python-and-how-to-avoid-them-e19fbe265e03


### Where are We?

Right, now that we've established migrating to Python 3 is important and worthwhile, let's get into
the details. The rest of this article is only going to focus on *mozilla-central*. Not because the
Python in our external repos isn't important, but simply because mozilla-central is what I'm
qualified to talk about. Here is some of the progress we've made so far:

* We added the ability to run python tests with Python 3 in CI. This gives us a back stop, once a
  module's unit tests are passing under Python 3, we can be relatively confident that we won't cause
  Python 3 regressions to that module in the future (assuming adequate test coverage).

* We stood up some linters. One linter that makes sure Python files can at least get imported in
  Python 3 without failing, and another that makes sure Python 2 files use appropriate `__future__`
  statements to make migrating that file slightly easier in the future. Though these linters haven't
  been enabled on all the files that they should.

* Finally, we started porting ``mozbase``. A suite of packages that are used all over the place in
  our build, test and CI infrastructure. Getting these modules completely migrated is a
  prerequisite to almost everything else.

While the progress made so far is not insignificant, it's only a small fraction of the overall work
that needs to get done. So what comes next?


### The Next Major Hurdle

The initial focus was on adding the ability to run tests with Python 3, which is accomplished
(though we aren't entirely happy about the mechanism used to do this, more on that later). But even
though we are running tests and linters to catch potential Python 3 related problems, we aren't
*actually* using Python 3 by default anywhere. So the next major hurdle is this, *run a trivial
mach command (like `mach google`) with Python 3*. On the surface this sounds like an easy thing to
accomplish, after all `mach google` is only [four lines of code][3]. But in reality, it is a very
large project that I'm going to devote most of the rest of this post towards.

Running mach commands with Python 3 means that not only do the commands themselves need to be
Python 3 compatible, but so do all of the dependencies. Pretty much every command (including `mach
google`) depends on two major libraries: `python/mach` and `python/mozbuild`. Getting those modules
(or at least the bits used by most mach commands) to work with Python 3 is the first major blocker
here. But while prepping mach and mozbuild for Python 3 is not a trivial task, it is a
straightforward one. The path is clear, we just need someone to roll up their sleeves and get the
job done. I estimate it wouldn't be more than a weeks worth of work (again just for the parts needed
by `mach google`).

Another blocker is bootstrapping. We verify that developers have a supported version of Python
installed when they run `mach bootstrap`. We'll need to agree on a minimum viable version (`3.5`
seems likely), and then modify our bootstrap script to make sure developers have both a compatible
version of Python 2 as well as Python 3. But this is also not a terribly difficult task.

The third and final piece to this milestone is to actually implement the plumbing in mach. To grow
the ability to introspect a command and determine whether it needs to run with Python 2 or Python 3.
This is where the complexity lies.

Let's dig into this a little and break down the problems that we'll need to overcome. The underlying
assumption here is that the tree is too vast to convert to Python 3 all at once. There is just too
much code, too much potential for bitrot and too much risk of breaking things without noticing. We
*must* be able to slowly convert commands one at a time.

[3]: https://searchfox.org/mozilla-central/rev/6dab6dad9cc852011a14275a8b2c2c03ed7600a7/tools/mach_commands.py#81


### The Invocation Problem

With that in mind, the first problem we encounter is the invocation problem. In mach, commands are
registered via decorators on actual Python classes. If you've ever looked at a `mach_commands.py`
file before, you might have noticed `@CommandProvider`, `@Command` and `@CommandArgument`
decorators.  These provide a very convenient way for tool authors to register their commands and the
arguments they use. But it comes with a big downside: every `mach_commands.py` is imported on every
invocation of mach. It's the only way mach can obtain the necessary command metadata to figure out
what to do.

So in a nutshell, we use Python to parse all available commands, then dispatch to the one the user
specified. But now the command we're dispatching to might need a different Python than the one
we're currently running.

##### Option 1

If we don't change how registration works, that means two things:

1. Every `mach_commands.py` and everything they import at the top-level needs to at least be
   parseable in Python 3 (this is likely easy to accomplish).
2. We'll need to spawn two separate Python intepreters for commands that use the opposite Python
   used to run `mach_bootstrap`. For example, if we use Python 3 to parse the decorators, then
   we'd spawn a second Python process for commands requiring Python 2 (or vice versa).

Although we'll need to implement the actual mechanics for invoking a second Python process this is
the simplest solution.

##### Option 2

Alternatively, we could change how command registration works. Instead of (or in addition to) using
decorators, we could register the command metadata needed for dispatching (e.g name and module path)
in some central file. Maybe we could have a top-level `mach_commands.json` file that looks something
like this:

```json
{
  "build": {
    "python": 2,
    "help": "Build Firefox",
    "path": "python/mozbuild/mozbuild/mach_commands.py"
  },
  "google": {
    "python": 3,
    "help": "Run a Google search",
    "path": "tools/mach_commands.py"
  },
  "..."
}
```

The `mach` binary has a bit of a clever hack inside, it is both valid Python and valid shell. When
you execute `./mach` it first runs as a shell script, finds the appropriate Python executable, then
re-executes itself as a Python script. With this proposal, the shell portion of the mach driver
would instead:

1. Parse cli to determine the desired subcommand.
2. Parse `mach_commands.json`.
3. Find Python executable based on the `python` key.
4. Re-excute self with appropriate Python.

This is a lot more complicated than Option 1, but it avoids both of the caveats. Namely, we don't
need to worry about making everything Python 3 importable and we don't need to run two separate
Python processes.

Now normally, I'd say the complexity of this approach is nowhere near worth those two meager
benefits. But this option is made much more attractive because [this is something we've long talked
about doing anyway][4]. There is a third much larger benefit to this option, albeit completely
unrelated to the Python 3 migration. We wouldn't need to load every `mach_commands.py` on every
`mach` invocation. All of the necessary information to dispatch and run `mach help` could be
obtained without importing the world. This would substantially speed up mach invocations.

The upshot is that both of these options are viable. If we want to be laser focused on the Python 3
migration, I'd choose Option 1. But Option 2 remains attractive as it might give us an excuse to
solve two substantial problems at once. As of this writing I'm not sure which option I'd choose.

[4]: https://bugzilla.mozilla.org/show_bug.cgi?id=1388894


### The Dependency Problem

When you run execute a mach command, a [virtualenv][5] will be created containing a set of "base"
packages that live scattered across mozilla-central. We call this the "initial" virtualenv. Some
commands with more complicated needs do create their own virtualenvs on top of this base layer, but
barring that, this "init" virtualenv is the one that gets activated by default. Of course, the set
of packages we install inside this virtualenv will be different depending on whether we run with
Python 2 or Python 3. We can't install a Python 2 only package inside a Python 3 virtualenv (or vice
versa).

The solution here is very simple. We can maintain two separate manifests to populate
the two necessary virtualenvs. One for Python 2 and one for Python 3. Some modules (or even most)
might show up in both manifests. But there's something else to consider here. We have a similar but
tangential problem that we need to solve in mozilla-central: dependency locking.

Depdendency locking is making sure that all consumers of a tool use the exact same versions as
everyone else. This keeps things reproducible and explicit, prevents mitm attacks by verifying
hashes and is widely considered best practice in any package ecosystem. The reason it's worth
considering is that the tools that handle dependency locking, also tend to handle virtualenv
management. In fact we use one such tool, Pipenv, to handle our current dependency locking needs.
Since we're using these types of tools anyway, it's worth spending some time looking into whether or
not they can help us with our Python 3 dependencies. So let's take a look.

[5]: https://docs.python.org/3/glossary.html#term-virtual-environment


##### Pipenv

[Pipenv][6] was the darling of the Python community for a few years and we use it in a variety of
places:

1. When vendoring third party packages.
2. When running `mach python-test` to switch between Python 2 / 3 (it might even be able to help with
   the invocation problem).
3. For commands that need to install additional external packages at runtime (gives us dependency
   locking there).

At the time Dave Hunt and I were implementing these things, it was the only game in town. We made it
all work, but the road was a bit bumpier than we would have liked. We ended up implementing things
that were "good enough", but not polished to the level we would have liked. There are a few reason
I'm not personally sold on Pipenv for use in a large monorepo like ours:

1. The maintainer is less than accomodating to outside change, we had several seemingly reasonable
   PRs closed without explanation (a trend many would-be Pipenv contributors have noticed).
2. While we were developing these systems, several bugs and backwards incompatible changes were
   introduced. This is more a problem around us using Pipenv before it had stabilized, but the
   versioning and docs lead one to assume a certain level of stability that didn't exist.
3. It felt a bit sluggish.
4. It has a lot of baked in assumptions that you are working on a single Python package (rather than
   tooling for a large monorepo). We had to contort it into directions it didn't want to go.

I'd be remiss not to mention that it's been about a year since we last looked at these systems, and
the version of Pipenv we're using is equally old. It's possible that things have improved since
then. Nonetheless, I wouldn't recommend using Pipenv to help us here. However..

[6]: https://github.com/pypa/pipenv


##### Poetry

[Poetry][7] was created in response to some of the aforementioned shortcomings in Pipenv. I
personally use it in several of my own projects and think it is a fantastic tool. It feels much
snappier and more lightweight, the maintainer is at least open to discussion on proposed new
features and I have never encountered a bug or backwards incompatible change while using it (though
it hasn't yet reached 1.0, so backwards incompatible changes should still be expected).

Poetry is everything that I was hoping for in Pipenv, but it does still share one large drawback: it
also assumes you are working with a single Python package. It even goes one step beyond Pipenv and
forces you to supply metadata like the package name and version. This pretty much precludes it from
being useful as a tooling backend for a large monorepo. So why bother mentioning it at all?

[7]: https://github.com/sdispater/poetry


##### Jetty

[Jetty][8] is a little experiment I've been building. It is a very thin wrapper around Poetry itself
that attempts to make it more useful for use in a monorepo like mozilla-central. It does a few
things:

1. Removes the requirement to specify package metadata.
2. Removes package management commands (e.g for version bumping a package), leaving just the
   dependency and virtualenv management stuff.
3. Provides a programmatic API for calling the various commands (so we don't have to run it in a
   subprocess).

It seems to work fairly well. My next step is to experiment with replacing our in-tree Pipenv usage
with Jetty. If all goes well, it might be a viable way to handle our Python 3 depdendencies.

[8]: https://github.com/ahal/jetty


For all this talk about Pipenv/Poetry/Jetty, they are tangential to the problem at hand. We could
solve everything we need without them, and that's probably the wisest course of action for now. I
just wanted to mention them as they do attempt to solve many of the same problems we are facing.
They are at least worth considering.


### Conclusion and Concrete Steps

To summarize, the next major hurdle is to start running specific mach commands with Python 3 (in
addition to running others with Python 2). Here are some of the concrete steps we can take right now
to get the ball moving:

1. Run the `python/mach` and `python/mozbuild` unittests with Python 3.
2. Enable the [py3][9] linter on as many things as possible (preferably everything).
3. Temporarily hack the `mach` binary to point at Python 3 and try to get a very basic command (e.g
   `mach google`) to run.
4. Add Python 3 to our bootstrapping process.

Parallel to those things, there are some larger problems that need to be solved. Namely the
invocation and depdencency problems. In both cases there is a quick and dirty solution, and a longer
but possibly better solution. Both cases will require a certain level of planning and coordination.

I want to close by answering one of the questions I asked at the beginning. Do we have a plan to get
to a good state in time for Python 2's EOL on January 1st, 2020? I would answer no. This post might
be the very rough outline of a plan, but it only talks about the next major step. After this step,
we still have the actual work of converting everything. Plus this post doesn't even touch on the
Python that lives in Github. Another reason to answer "no", is that while some engineers and teams
do recognize the importance of this work, it isn't something that's on upper management's radar. We
just don't have the resources necessary allocated towards fixing it and I'm not aware of it being on
anybody's official roadmap.

That being said, I am optimistic that this is work that can get done in time if we prioritize it.
If we don't, I'm still optimistic that it will be done eventually. Just maybe not in time for
January 1st, 2020.

[9]: https://searchfox.org/mozilla-central/source/tools/lint/py3.yml
