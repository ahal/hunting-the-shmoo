---
title: "The Cost of Fragmented Communication"
date: 2019-05-06T14:41:33-04:00
tags: [mozilla]
slug: fragmented-communication
draft: true
---

Mozilla [recently announced][0] that we are planning to de-commission ``irc.mozilla.org`` in favour
of a yet to be determined solution. As a long time user and supporter of IRC, this decision causes
me some melancholy, but I 100% believe that it is the right call. Moreover, having had an inside
glimpse at the process to replace it, I'm supremely confident whatever Mike and company choose will
be the best option for Mozilla's needs.

I'm not here to argue why deprecating IRC is a good idea. [Many][1] [other][2] [people][3] have
already done so much more eloquently than I ever could have. I'm also not here to push for a
specific replacement. Arguing over chat applications is like arguing over editors or version
control. Yes, there are real and important differences from one application to the next, but if
there's one thing we're spoiled for in 2019 it's chat applications. Besides, Mike has spent so much
time thinking about the [requirements][4], there's nothing anyone could say on the matter that he
hasn't already spent hours considering.

No. This post is about an unrelated, and yet adjacent issue. An issue that began when
``mozilla.slack.com`` first came online, an issue that will likely persist long after
``irc.mozilla.org`` rides off into the sunset. An issue I don't think is brought up enough, and
which I'm hoping to start some discussion on now that communication is on everyone's mind. I'm
talking about using two communication platforms at once. For now Slack and IRC, soon to be Slack and
something else.

Different platform, same problem.

<!--more-->

### Modes of Communication

Mozilla walks the walk when it comes to involving the community. Much of our communication, decision
making and implementation all happens right out in the open. Anyone can go back and read almost
everything I've ever posted to Bugzilla, every [message I left on IRC][5], every post I've made to
the newsgroups, every patch I've submitted or review I've conducted. It's all out there in the
public. For most, this is a very strange concept. But it allows Mozilla to bring community into the
conversation unlike anywhere else I've ever seen at this scale. This is a feature, a huge
competitive advantage.

But like any organization, some things need to be kept out of the public eye. Whether that's
information on critical security bugs, confidential partner agreements or product announcements
carefuly timed for marketing impact. Other conversations have no reason to be public, office
channels and catching up with colleagues, anything that might touch on something personal.

In the old days, the only way to talk in private was either e-mail or password protected IRC
channels (which were nowhere near suitable for the purposes they were being used). After much
frustration, someone set up a Slack instance and solved the issue in one fell swoop. Constantly
being in the public eye can be unnerving, and now there was a safe space one could chat with their
colleagues. A place Mozillians could be themselves without needing to worry (as much) about what
they said. This was a very good thing.

Now Mozilla had (and still has) two communication platforms. IRC for openm community facing
discussions, Slack for private, NDA'ed only discussions. Both fill very important purposes, but the
fact that they are different is a problem.

Hosting discussion on multiple platforms has real and detrimental impacts on planning and
productivity.


### Cults of Preference



 Your response to this on #cccc was that you
are not convinced that context switching between apps is a major burden.
I tend to agree with this point, it might be a mild annoyance, but nothing
more. But the real cost here isn't the physical act of switching from one app
to another. It's the fragmented communication itself.

Given two communication platforms A and B, some percentage of people
will prefer A and the rest will prefer B. Even if everyone at Mozilla has both
A and B installed (I know of people who outright refuse to use either Slack
or IRC for one reason or another), they will have an inherent bias towards
one side.

Using myself as an example, I tend to prefer IRC over Slack. Even though
I'm on Slack, I don't spend nearly as much time searching for and
monitoring relevant channels as I do on IRC. As a result, I'm missing out
on a lot of communication that would be highly relevant to my interests and
expertise. Someone may have asked a question I know the answer to
off-hand, but since I didn't see it they wasted 4 hours figuring it out on their
own. Someone else may have asked for input on a design document, but
because I didn't see it, the implementation ended up being sub- optimal and
caused problems in the future. Conversely the questions I ask on IRC might
not be seen by people who prefer Slack. Compound this across 1000+
employees and we are talking about a huge drawback for Mozilla.

With two communication platforms, there is a very high risk relevant stake-
holders are not participating in the discussions that they need to.

This finally brings me back to the jumbled point I was trying to make on
#cccc. We have an opportunity here to fix this (what I would call disastrous)
situation. We can either:

A) Choose a chat app that can support both public and confidential
communication at the same time (thereby removing "personal bias"
altogether)

or

B) Choose a second chat app and use policy to very strongly mandate that
the confidential app *only* be used for confidential communication (though
using policy to mandate things is not Mozilla's forte).

I am very sympathetic to the fact that the problem I'm describing here is
not the problem you are trying to solve. I only bring this up because I see
an opportunity to fix both problems at the same time, and think this second
problem should at least factor into the process.

Having said my piece, don't feel the need to type out a lengthy reply. If
your answer is "solving this is out of scope", that's fine. We can file the
process equivalent of a follow-up bug on it.

[0]: http://exple.tive.org/blarg/2019/04/26/synchronous-text/
[1]: http://exple.tive.org/blarg/2018/11/09/the-evolution-of-open/
[2]: https://blog.humphd.org/irc-mozilla-org/
[3]:
[4]: http://exple.tive.org/blarg/2019/05/03/goals-and-constraints/
[5]: https://mozilla.logbot.info/ateam/20100325#c4178
