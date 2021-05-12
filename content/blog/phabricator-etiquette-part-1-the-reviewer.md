---
title: "Phabricator Etiquette Part 1: The Reviewer"
date: 2021-04-13T15:42:41-04:00
tags: [phabricator, mozilla, tips-and-tricks]
slug: phabricator-etiquette-part-1-the-reviewer
---

In the next two posts we will examine the etiquette of using Phabricator. This post will examine
tips from the reviewer's perspective, and next week will focus on the author's point of view.
While the social aspects of etiquette are incredibly important, we should all be polite and
considerate, these posts will focus more on the mechanics of using Phabricator. In other words, how
to make the review process as smooth as possible without wasting anyone's time.

Let's dig in!

<!--more-->

### Never Leave a Review in an Ambiguous State

Phabricator is all about eliminating the uncertainty around who is on the hook for moving the
revision forward. When it is in the `Needs Review` state it will show up in the reviewer's queue.
When it is in the `Needs Revision` state, it will show up in the author's queue. Many reviewers /
authors only look at their queues and can miss a request entirely if a revision is in an ambiguous
state!

Ambiguous states happen when the revision requires action from someone but it doesn't show up in
their queue. The most common way a reviewer can cause an ambiguous state is by requesting changes
but not setting the state to `Needs Revision`. For example, the reviewer:

1. Sets the state to `Accepted` but asks for issues to be fixed prior to landing (e.g "r+ with
   nits")
2. Asks for changes but leaves the state unchanged (so it is still in the `Needs Review` state)

Both of these cases are bad because the reviewer is relying on the author to see their comment, even
though Phabricator will not indicate that any changes are needed.

The first case especially is very common. Reviewers sometimes use "r+ with nits" to speed up the
process and avoid another round of review. But when authors look at their queue, they'll only see
that the revision is ready to land and can easily do so without noticing that changes have been
requested. Even the most trivial of unfixed nits can cause problems. E.g a typo in a comment can
cause the `codespell` linter to fail and the revision to be backed out. So it's best to simply avoid
"r+ with nits" altogether.


### Only Review Code you are Comfortable With

The biggest disservice you can do to the patch author, is to review a patch without fully
understanding what it is doing. If you don't feel comfortable with the review, then remove yourself
from the reviewers list! If you are an appropriate reviewer for only part of the patch, then add
another **blocking** reviewer who can handle the part you aren't comfortable with (and change
yourself to blocking while you're at it).

Note: Blocking reviewers are reviewers whose review are *required* to proceed. Patches with
non-blocking reviewers can proceed as long as someone has given an r+, effectively making
non-blocking reviews optional. Revisions will also be removed from the queues of non-blocking
reviewers as soon as they are `Accepted` by someone else.

There are a few exceptions to this rule:

1. When a module is unowned and no one would be comfortable with the code.
2. When the module expert is the one asking you for review (i.e they need a rubberstamp and have no
   one else to turn to).

In these cases you should still spend some effort learning about the code touched by the patch,
use your judgement based on the complexity of the review.


### Find Appropriate Reviewers on the Author's Behalf

If you think that you are not an appropriate reviewer, don't simply unassign the review from
yourself, add the appropriate reviewer on the author's behalf. This is especially important if the
review is coming from a contributor. Besides if the author mis-assigned the review, they likely
*are* even less familiar with the module than you are!

Even if you're equally clueless around who should do the review, check who touched the file last in
version control history and pick someone. It speeds up efficiency by eliminating one communication
cycle. Rather than:

1. Author requests review
2. You unassign yourself
3. Author requests another review

It becomes:

1. Author requests review
2. You unassign yourself and request another review

Because of Mozilla's global nature, this simple step could allow the patch to land a full day
earlier than it otherwise would have.


### Don't Leave Optional Comments

Leaving optional comments shifts the burden of review from the reviewer back onto the author (who is
often much less knowledgeable in the area). As the reviewer, decide whether the issue should block
landing or not. Nine times out of ten, "optional" comments are better left to follow-up bugs (and as
an author I will ignore them).

It's ok to make the comment anyway to raise the point, just be sure to include something like "This
is better left to a follow-up, but it would be nice if ...". This way the expectations are clear for
everyone.


### Set the Testing Tag

In mozilla-central there is a [testing
policy](https://firefox-source-docs.mozilla.org/testing/testing-policy/index.html) and all revisions
are supposed to be marked with one of those tags. As a reviewer, failing to set a tag means the
author has to check a box when landing acknowledging that the tag is missing. This again leaves the
revision in a bit of an ambiguous state (should I go back and add tests? Is it ok to check this
box?).

Since one of the reviewer or the author is going to need to make any extra click anyway, it might as
well be the person which the policy intends (the reviewer). Reviewers working in mozilla-central
should install the
[phab-test-policy](https://addons.mozilla.org/en-US/firefox/addon/phab-test-policy/) for a reminder
to add the tag and an easier UI for doing so.


### Review in a Timely Manner

Reviewers should always strive to get their reviews done in a timely manner. I've heard some
people say 24hrs should be the maximum. Others argue for 48hrs. But it should never take longer than
that. The excuse of having a long review queue is not valid since the total time spent doing reviews is
the same whether you do them all in a big batch at the end of the week, or whether you do them in
smaller batches at the end of the day. If you are reading this and have a long review queue, I'd
encourage you to try and burn through it and then adapting your workflow to ensure it never gets
that long in the first place. The amount of work you do will be the same, but you'll be making those
who rely on you more productive.

However sometimes long review queues are simply unavoidable (like when you get back from a PTO, or
you need to go into emergency mode for a few days). If you are overwhelmed by reviews, or something
comes up, you should do one of two things:

1. Assign the review to someone else who has more time than you.
2. Failing that, comment on the revision with a rough estimate on when you will be able to get to
   it.

If you are consistently overwhelmed by reviews, then it's time to have a conversation with your
manager and ask for help :).


### Replace Review Groups with Your Name

If you are part of a "review group" (e.g, `firefox-build-system-reviewers`) and a revision requests
review from said group, then replace the group with yourself when you decide to take it. This way
you remove the revision from the queues of all the other reviewers in the group and eliminate the
risk of two people unnecessarily reviewing the same things.

This will also have the added bonus of cleaning up the commit message.


### Conclusion

That's all I can think of for now. If you have any other tips for reviewers, feel free to leave them
in the comments!
