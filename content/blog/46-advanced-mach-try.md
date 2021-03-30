---
title: "Advanced Mach Try"
date: 2021-03-30T9:30:00-04:00
tags: [mozilla, tools-tip-tuesday, try]
slug: advanced-mach-try
---

Following up [last week's post](https://ahal.ca/blog/2021/understanding-mach-try/) on some `mach
try` fundamentals, I figured it would be worth posting some actual concrete tips and tricks. So
without further ado, here are some things you can do with `./mach try` you may not have known about
in rapid fire format.

<!--more-->

### Dependencies are Automatically Selected

Let's start with a basic one. Assuming you aren't worried about breaking a build, you don't need to
explicitly select them in `mach try fuzzy` or `mach try chooser`. Just pick the test task and the
required build will automatically get filled in. Same goes for any other dependencies.

### Mastering FZF

In my opinion, the most powerful and useful selector is `./mach try fuzzy`. It can precisely select
any combination of tasks, or whole swathes of tasks with ease. To accomplish this it uses the
wonderful [fzf](https://github.com/junegunn/fzf) project under the hood. Learning how to use fzf's
features can go a long way to improving your `mach try` usage. A good place to start is the [mach
try fuzzy](https://firefox-source-docs.mozilla.org/tools/try/selectors/fuzzy.html) documentation.

### Run Specific Tests

This one is also pretty commonly known, but it's so useful it's worth mentioning. You can specify a
directory, test file or test manifest as an argument to `mach try` to only run those tests:

```bash
# only run tests under caps directory
$ ./mach try fuzzy caps

# only run tests in browser.ini
$ ./mach try fuzzy caps/tests/mochitest/browser.ini

# only run test_origin.js
$ ./mach try fuzzy caps/tests/unit/test_origin.js
```

Specifying a path only displays tasks that run a suite that contains at least one test that matches
the path. Using the above example, the caps directory contains xpcshell, mochitest-plain and
mochitest-browser-chrome tests. So you would only see tasks that run those corresponding suites in
your `./mach try fuzzy` interface.

Also, specifying a path means that *only those specific tests* will actually run. To accomplish
this we assume that everything you select can run in chunk 1. If you select a path with a ton of
tests, you may see a timeout.

### Mastering Presets

Most selectors support
[presets](https://firefox-source-docs.mozilla.org/tools/try/presets.html#presets) to remember a
given query and quickly execute it again later. You can use both local presets, as well as the
shared ones checked in to `tools/tryselect/try_presets.yml`. But what if you want to add or remove a
few tasks on top of the base preset? Luckily [mach try
fuzzy](https://firefox-source-docs.mozilla.org/tools/try/selectors/fuzzy.html#modifying-presets) has
you covered:

```bash
# selects all perf tasks plus all mochitest-chrome tasks
$ mach try fuzzy --preset perf -q "mochitest-chrome"

# adds tasks to the perf preset interactively
$ mach try fuzzy --preset perf -i

# limits perf tasks to windows only
$ mach try fuzzy --preset perf -xq "windows"

# limits perf tasks interactively
$ mach try fuzzy --preset perf -xi
```

### Setting Environment Variables

Environment variables can be set in tasks like so:

```bash
$ ./mach try fuzzy --env 'MOZ_LOG="timestamp,glean::*:5"' --env "FOO=BAR"
```

### Running Tasks Multiple Times

Sometimes you are trying to check for intermittents. The rebuild feature comes in handy here:

```bash
$ ./mach try fuzzy --rebuild 3
```

This will run all selected tasks three times. Dependencies will only be run once.

### Re-run the Previous Push

Sometimes you push, see a failure, fix, need to push again. To run an identical push as last time:

```bash
$ ./mach try again
```

### Analyzing your Push with Pernosco

If you make use of the [pernosco](https://pernos.co/) service you can easily tell it to scan your
try push by passing in the `--pernosco` flag. Once the task and analysis have finished, Pernosco
will e-mail you a link to the trace. Make sure you select a [supported
platform](https://pernos.co/faq/) and are using an @mozilla.com e-mail.

### Run Tasks from Another Branch

As outlined [last time](https://ahal.ca/blog/2021/understanding-mach-try/), `./mach try` sources the
list of tasks from the taskgraph, which in turn uses parameters to provide the context. The
parameters `mach try` uses can be set right from the command line. There's even a shortcut to
download a parameters file from CI. For instance, to get the set of tasks that run on beta:

```bash
# download parameters.yml from latest beta push
$ ./mach try fuzzy --parameters project=mozilla-beta

# pass in a custom parameters.yml
$ ./mach try fuzzy --parameters parameters.yml
```

Note that if you are running this from a mozilla-central base, you'll likely see failures due to
differences in the code base and task configuration. So be sure to update to beta first! You can
also craft your own `parameters.yml` file and pass it in directly:

### Generating the Task Graph in the Background

While generating tasks on the fly gives us an up to date picture of the CI system, it can also take
awhile which is annoying. `mach try` will automatically cache the taskgraph result until the next
time a file is modified under the `taskcluster` directory, but that directory changes frequently so
generation is still incurred pretty often.

It's possible to use [watchman](https://facebook.github.io/watchman) to detect when that directory
has changed and automatically kick off generation in the background. Follow [these
instructions](https://firefox-source-docs.mozilla.org/tools/try/tasks.html#configuring-watchman) to
set it up. Watchman is kind of finicky to set up, so if you follow along I'd love to hear from you
(whether successful or not).

### Future Ideas

Because `mach try` runs a local taskgraph generation, it means *anything* that can be set in the
task configurations, can also be set via `mach try`. It just needs to be implemented. So if you can
think of any ideas you would like to see, please file a bug under `Firefox Build System :: Try` and
CC me. Also, if you have any other try tips I may have neglected, please feel free to add them in
the comments!
