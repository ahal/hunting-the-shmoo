---
title: "Your New Job is Integrating Code"
date: 2026-05-26T09:50:00-04:00
tags: [mozilla, llm, productivity]
slug: integrate
---

You felt it. *The shift*. That your role has fundamentally changed thanks to
LLMs. It first entered your subconscious when you realized how easily you can
now crank out PRs. You felt it more concretely (and less enthusiastically), as
a reviewer when you opened your laptop one morning and noticed your review
queue was double what it normally is thanks to everyone else cranking out PRs.
And you feel this pervasive, general sense of *friction*.

It's difficult to pinpoint exactly where this *friction* is coming from.
Depending on the repository size and CI setup, it will be slightly different
for everyone. It might involve longer review times or slipping review
standards. You might be noticing more merge conflicts and merge related CI
failures. Perhaps there are more failures sneaking through to `main` or CI is
taking longer to give you results. You almost certainly feel the *grind*.
People are on edge, tired; developers are pulling in opposite directions.

Here's what LLMs shifted. The bottleneck is no longer producing code. The
bottleneck is *integrating* it. The friction we're feeling is a result of more
PRs, more ideas, more reviews, more disagreements all made possible thanks
to LLMs. In short, the problem can best be summarized by Figure 1:

![Animated clip of germs getting stuck in a door from The Simpsons](/static/img/blog/2026/bottleneck.gif "Bottleneck")

But we're living in a moment where many folks haven't realized this yet, and
are still under the impression that their job is to produce code.

It's not. Your new job is to integrate it.

<!--more-->

## Why Does It Matter?

Your first instinct might be to dig in and go about your work as usual. This is
a very rational response, after all LLMs certainly aren't the first major
disruption to rock the tech industry, and this strategy has worked well in the
past. But it also comes with some pretty big risks. CEOs across the industry
have also felt the shift. And they're certainly taking action, by cutting jobs
[^1][^2][^3] to be precise. After all, there's no point in producing code
faster than you can ship it.

So what can *you* do about it? It's not possible to turn the tides against
LLMs, but you can control what's inside your sphere of influence. And that
starts with an honest reflection on your new role, and how to thrive within it.
Producing code is no longer the scarce resource it once was, what's scarce now
is the ability to integrate it.

## What is Integration?

Your new role is to integrate changes. That means getting changes through the
pipeline as efficiently as possible, while still maintaining a high bar of
quality. This can encompass work that happens before, during or after actually
implementing the changes.

Before implementation you have to draft a plan and advocate for it. You need to
work with stakeholders to negotiate the terms and priorities. You need to
coordinate with other teams to make sure you aren't pulling in different
directions. For more complex changes, you need to design and architect the
solution at a high level.

During implementation you need to guide the LLM down the correct path. You need
to help it come up with an acceptable implementation and understand its
tradeoffs. You need to review the LLM's output as it gets generated. You need
to test, validate and understand the changes well enough to explain them to
another reviewer. If necessary, you need to be ready to course correct and
shift the implementation down a completely different path.

And afterwards you need to actually merge the change. Monitor CI and metrics,
debug and fix issues. You need to be able to identify issues quickly and
back out the regressing changes.

## Adapting to the New Reality

In this new reality, process and pipelines will be king. Companies will put a
premium on DevOps / Platform Engineering type teams as they try to increase
their velocity. The bottleneck has moved from actually producing the code to
planning, coordination, review, CI and deployment.

The shape of that bottleneck will be different at every organization, but the
outcomes are the same. Wherever your team feels the most pain, whether it's
code review, or unclear direction, or lower quality, that's where LLMs have
outpaced your tools and process. That's where the work is.

The engineers who thrive in this new age are the ones who can identify and fix
those bottlenecks. That could mean writing better tooling, setting clearer
standards or being the person who keeps changes moving through the pipeline
efficiently.

The shift has happened. Now integrate it.

[^1]: [Block CEO Jack Dorsey lays off nearly half of his staff because of AI](https://fortune.com/2026/02/27/block-jack-dorsey-ceo-xyz-stock-square-4000-ai-layoffs/)
[^2]: [Meta slashes 8,000 jobs as it pivots towards AI](https://www.npr.org/2026/05/20/nx-s1-5826917/meta-layoffs-ai-jobs)
[^3]: [Big Tech layoffs 2026: Amazon, Meta, Microsoft and the AI trade-off](https://invezz.com/news/2026/05/04/is-big-techs-725b-ai-splurge-being-funded-by-mass-layoffs/)
