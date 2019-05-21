---
title: "The Cost of Fragmented Communication"
date: 2019-05-06T14:41:33-04:00
tags: [mozilla]
slug: fragmented-communication
---

Mozilla [recently announced][0] that we are planning to de-commission ``irc.mozilla.org`` in favour
of a yet to be determined solution. As a long time user and supporter of IRC, this decision causes
me some melancholy, but I 100% believe that it is the right call. Moreover, having had an inside
glimpse at the process to replace it, I'm supremely confident whatever is chosen will be the best
option for Mozilla's needs.

I'm not here to explain why deprecating IRC is a good idea. [Other][1] [people][2] have
already done so much more eloquently than I ever could have. I'm also not here to push for a
specific replacement. Arguing over chat applications is like arguing over editors or version
control. Yes, there are real and important differences from one application to the next, but if
there's one thing we're spoiled for in 2019 it's chat applications. Besides, so much time has been
spent thinking about the [requirements][4], there's little anyone could say on the matter that
hasn't already been considered for hours.

This post is about an unrelated, but adjacent issue. An issue that began when ``mozilla.slack.com``
first came online, an issue that will likely persist long after ``irc.mozilla.org`` rides off into
the sunset. An issue I don't think is brought up enough, and which I'm hoping to start some
discussion on now that communication is on everyone's mind. I'm talking about using two
communication platforms at once. For now Slack and IRC, soon to be Slack and something else.

Different platform, same problem.

<!--more-->

### Two Modes of Communication

Mozilla walks the walk when it comes to involving the community. Much of our communication, decision
making and implementation all happens right out in the open. Anyone can go back and read almost
everything I've ever posted to Bugzilla, every [message I left on IRC][5], every post I've made to
the newsgroups, every patch I've submitted or review I've conducted. It's all out there in the
public. For most, this level of openness is a very strange concept. For many it's unsettling. But
it allows Mozilla to bring community into the conversation unlike anywhere else I've ever seen at
this scale. This is a feature, a huge competitive advantage.

But like any organization, some things need to be kept out of the public eye. Whether that's
information on critical security bugs, confidential partner agreements or product announcements
carefuly timed for marketing impact. Other conversations have no reason to be public, office
channels, lunch plans and catching up with colleagues, anything that might touch on something
personal.

In the old days, the only way to talk in private was either e-mail or password protected IRC
channels (which were nowhere near suitable for the purposes they were being used). After much
frustration, someone set up a Slack instance and solved the issue in one fell swoop. Constantly
being in the public eye can be unnerving, and now there was a safe space one could chat with their
colleagues. A place Mozillians could be themselves without needing to worry (as much) about what
they say. This was a very good thing.

Now Mozilla had (and still has) two communication platforms. IRC for public community facing
discussions, Slack for private, NDA'ed only discussions. As I mentioned, both modes of communication
are essential, and IRC is not capable of fulfilling the latter adequately. So what's the problem?


### Cultures of Preference

The problem is that the usage divide between these platforms *does not* follow the public/private
guideline I outlined above. Most of the conversation I see on Slack has no reason to be private (and
some of the conversation I see on IRC *should* be private, albeit much less than the other way
around). Everyone has inherent biases. Given two communication platforms A and B, some percentage of
people will prefer A and the rest will prefer B. Even assuming that everyone still uses both A and B
to some degree (which I know from experience is not a valid assumption in our case), this is a big
problem.

The first thing that might pop into your head is the cost of context switching between chat apps.
While there is a certain cognitive burden associated with adding yet another app to your workflow,
I'm not convinced that it's significant. So for the sake of argument, I'm going to assume that there
aren't any drawbacks from the *actual use* of two apps.

The real cost comes from missed connections. It's best to illustrate some of these costs in a case
study. I'll use the case study of someone I can speak for authoritatively, myself.


### Missed Connections

I have fond memories stumbling into my first IRC channel to play a text-based online space battle
game called Star Fury. The openness of the communication was also something that really impressed me
when I first joined Mozilla as an intern. It's something I took to heart and try to use myself
whenever possible. Suffice to say, I am personally biased towards IRC.

That's not to say that I refuse to use Slack. I use both, and when someone pings me I'm equally
responsive on either platform. But I spend more time in IRC, I read more scrollback, I actively
search out channels that might be relevant to my interests, I set up notifications for terms that I
might be able to help out with. Very often I am able to help someone in need without being
explicitly pinged.

I don't do any of these things on Slack. How many relevant conversations in channels I don't even
know exist am I missing? How many people spend hours figuring out an unanswered question that I knew
off the top of my head? Conversely, when I ask a question in IRC, how many people who have a bias
towards Slack could have helped me out but didn't? Mozilla has a cultural problem that needs
solving. Developers with a bias towards IRC are talking past developers with a bias towards Slack.
The same conversations are often being duplicated in both places.

Of course measuring the productivity impact of missed communication is more or less impossible.
There's no way of knowing just how big of a problem this is, though I suspect it is larger than one
might expect.


### Inclusion by Default

The previous section purposefully doesn't mention the words 'private' or 'public'. My hope is to
convince you that simply giving people a choice (regardless of the mode of communication) causes
problems worth solving in and of themselves. But remember that people usually tend to use Slack, not
because they are having private conversations, but because they prefer it to IRC. This is a problem
because Slack is exclusionary. Contributors can't access it without signing an NDA (which requires
employee intervention). These conversations exclude the wider Mozilla community, treating
contributors as second class citizens. Here is a quick anecdote.

There is both a `#python` channel on IRC and on Slack. The one on IRC is more or less dead, there is
hardly ever any conversation there. The one on Slack on the other hand has 3-4 times the number of
members and there is vibrant conversation happening daily. The vast majority of conversation there
is simply Python enthusiasts sharing tips and tricks, talking about new language features and
discussing new and cool packages discovered in the wild. In otherwords, exactly the kind of
conversations that might be beneficial to a contributor trying to learn the ropes. It saddens me
that these conversations, and conversations on many other channels like it, are not accessible to
the entire community.



### A Cause for Optimism, A Cause for Concern

To summarize, there are two distinct problems outlined here:

1. Missed and duplicated communication that arises from two factions of people having inherent
   preferences for a given platform.
2. Exclusive conversations that have no reason to be private, arising (presumably) when a critical
   mass of people prefer the closed platform to the open one.

Despite my misgivings, I'm optimistic for the future. The process to replace IRC should result in a
public communication platform that is more or less on par with Slack in terms of bells and whistles.
This should incentivize more people over to the side of public by default and reduce the impact of
both of the aforementioned problems.

But it needs to be noted that deprecating Slack is not in the cards (at least for now). Whatever
platform we end up choosing, Slack will continue to be the platform we use for our private NDA'ed
conversations. This means that the problem will still exist to some degree (some percentage of
people will always prefer it to the alternative). Ideally the IRC replacement will be able to handle
both public and private modes of communication. And ideally once the switch happens, we can start a
conversation about turning off Slack. I've heard one of the barriers to turning off Slack is that it
is the preferred method of communication amongst executives. I sincerely hope that after we switch
away from IRC that this is not the only barrier stopping this from happening.

Mozilla's productivity and inclusion are both on the line.


[0]: http://exple.tive.org/blarg/2019/04/26/synchronous-text/
[1]: http://exple.tive.org/blarg/2018/11/09/the-evolution-of-open/
[2]: https://blog.humphd.org/irc-mozilla-org/
[4]: http://exple.tive.org/blarg/2019/05/03/goals-and-constraints/
[5]: https://mozilla.logbot.info/ateam/20100325#c4178
