---
title: "Phabricator Etiquette Part 2: The Author"
date: 2021-04-27T09:33:31-04:00
tags: [phabricator, mozilla, tools-tip-tuesday]
slug: phabricator-etiquette-part-2-the-author
---

[Last time](https://ahal.ca/blog/2021/phabricator-etiquette-part-1-the-reviewer/) we looked at some
ways reviewers can keep the review process moving efficiently. This week, let's put on our author
hats and do the same thing.

<!--more-->

### Never Leave a Revision in an Ambiguous State

Just as with reviewers, the author is also responsible for making sure the revision is in the
appropriate state. As a reminder, ambiguous states happen when the revision needs action from
someone, but doesn't show up in their queue.

As the author, a common way to get into this predicament is failing to re-request review when no
changes are submitted. A typical review might start with the revision in `Needs Review` (in the
reviewer's queue). The reviewer may request some changes and set it to `Needs Revision`, which is
now back in the author's queue. The author will then fix the problems and re-submit their patch.
Importantly, `moz-phab` (or maybe Phabricator itself?) will automatically set the state back to
`Needs Review` and all is right with the world.

But what happens if the reviewer's requests are misguided? Or they were based on a counterfactual
(if X is true, then you need to do this)? In these cases the author may decide to resolve the
comments by replying with an explanation on why they don't need to address them. Crucially the
author *is not* pushing up a new change, so the state won't automatically get set back to `Needs
Review`. If the author fails to do this manually, then the revision won't show up in the reviewer's
queue and the reviewer may not even realize that the author is still waiting on them to provide an
r+. Revisions can sit in states like this for days, until the author inevitably pings the reviewer
out of band and asks why the review is taking so long to which the reviewer replies "what review?".

### Request Blocking Reviews

Another variant of an ambiguous state can arise from a misunderstanding of how requesting multiple
reviews works. It's common for an author to have a patch that touches multiple areas of the code
base. These areas may have different owners / experts who the author would want to request review
from. In other words, they want *both* reviews before they proceed with landing.

Unfortunately Phabricator's default state is to treat reviews as either or. As soon as one reviewer
provides an r+, the revision is now in the `Accepted` state and it gets removed from the other
reviewer's queue. However the author may not realize this fact. Again causing the scenario above
where the reviewer asks why the review is taking so long, only to get "what review?" as a response.
Luckily Phabricator has the concept of a "blocking" reviewer to handle the case when multiple
reviews are needed. So if you need more than one review, make sure to set it as "blocking" (either
by choosing the `blocking: <nick>` variant from the Phabricator UI, or by appending `!` to the nick
in the commit message.

Another reason some authors request multiple non-blocking reviews is if they aren't sure who to ask.
But this should also be avoided because it can waste reviewers' time. There is a good chance
both reviewers will start reviewing it at the same time, when only a single review would have
sufficed. Instead authors should make a guess and if the reviewer isn't a suitable for the patch
they should ideally re-assign the review on your behalf (see previous post).

Personally I can't think of any scenario to request a non-blocking review over a blocking one.
Thankfully, `moz-phab` has a configuration that can make all your reviews blocking by default. Open
your config file (default `~/.moz-phab-config`) and set:

```ini
[submit]
always_blocking = true
```

When this is set to `true` adding `r?<nick>` will request a blocking review and `r?<nick>!` will
request a non-blocking one.

### Mark In-Line Comments as Done

When a reviewer leaves an in-line comment, the author will have the option of checking a little
"Done" checkbox in the top right. While doing so has no bearing on the revision's state and is
entirely optional, it's still a good idea both for yourself as the author and for the reviewer's
benefit.

Revisions that have many issues quickly become cluttered to the point where the code is unreadable.
For that reason, Phabricator gives us various ways to hide issues (such as "Older", "Collapsed" or
"All"). But my favourite way is using the "Hide Done Inlines" toggle, which hides any issue that has
been marked as done.

This makes it easy for both the author and the reviewer to keep track of what work is left to
complete. If the author doesn't mark their review comments "Done", then the reviewer needs to keep a
mental map of which comments were fixed and which weren't. While reviewers should always verify that
the revision adequately addresses their concerns, sometimes the revision will undergo multiple
rounds of review. Maybe the reviewer already verified a comment was addressed in a previous round
but now needs to recall this fact days later.

So even if you don't personally find it useful, mark your inlines done! Your reviewers will thank
you.

### Ensure Revisions are Readable and High Quality

This one isn't Phabricator specific but it's worth talking about anyway. As a reviewer, the worst
feeling is opening up a revision and seeing a giant patch with dozens of modified files and little to
no explanation. As the author, you should spend time making sure your revision(s) are easy to
understand and high quality. This means:

1. Commits should be as large as they need to be and no larger. That is to say, A) each commit
   should be capable of landing on its own without breaking any tests or linters and B) each commit
   should make the state of the tree slightly better than the prior one. But as long as those two
   conditions are satisfied, make them as small as possible! This makes them much easier to review
   and reason about. To avoid headaches, [plan your
   commits](https://www.assertnotmagic.com/2017/05/05/plan-your-commits/) ahead of time! If you
   forget to plan ahead and end up with a mess of spaghetti, spend some time learning how to pull it
   apart with your version control tool (e.g, `hg split` or `git rebase -i main`).
2. Never move and modify, this is the cardinal sin. Have one commit to move, and a second commit to
   modify (or vice versa).
3. Use a [descriptive commit message](https://chris.beams.io/posts/git-commit/).
4. Document functions and use comments where appropriate.
5. Include tests if appropriate (or a comment explaining why you didn't add them). This takes some
   pressure off the reviewer to hassle you for them.
6. Ensure [lint issues are fixed](https://ahal.ca/blog/2021/hide-your-lint-errors/) and tests pass
   prior to submitting.
7. Check if there is any documentation to update alongside the changes (reviewers should remember to
   check this as well).

All of this is a significant amount of work! But with practice it'll become second nature. Code
quality will be higher, reviewers will be happier and so will you.

### Conclusion

Thanks for reading! If you have any other tips for patch authors, feel free to leave them in the
comments.
