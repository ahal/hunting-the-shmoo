---
title: A New Look and Feel (and everything else)
date: 2018-05-14
tags: [website, hugo, staticman]
slug: website-refresh

---

I've recently redone my website and wanted to document a few of the changes and motivations behind
them.

<!--more-->

### Backend

Previously I was running Django on my Linode VPS, now there is no backend. The site is entirely
static, generated with [Hugo][1] and served over [Github Pages][2]. The source now lives [here][3]
and the generated HTML lives in a separate repository [here][4]. The latter is a sub-repository of
the former and I have a deploy script to re-generate and push the static HTML in one go.

There were a few motivations for this change:

1. There was absolutely no need for my website to have a database.
2. Maintenance. While the old website was dockerized and maintenance was minimal, it did exist.
3. Cost. I've now downgraded my Linode, though I probably could have done this anyway.

But the biggest reason is simplicity. My old site was a fairly complicated Django app using a lot of
custom models, templating and CSS (true fact, I didn't use a single theming library). Plus the blog
engine it was based on, `django-articles`, has been defunct for many years. This led to an attitude
of "never ever touch anything unless it was absolutely necessary". I've long wished I would blog
more often, and I realized my website itself was a bit of a barrier to that.


### Look and Feel

I'm using the [hugo-theme-bootstrap4-blog][5] theme for my site. I've modified it to look fairly
similar to the old site, keeping some things I enjoyed and getting rid of others I didn't. Overall
I'm liking the new look a lot better, and it's much easier to modify and maintain. There is a bit of
functionality that got lost, things like the article summary pages and RSS links. But this isn't the
fault of Hugo or the theme, rather than laziness on my part. I plan to eventually re-implement some
of it in the future.


### Comments

I'm no longer using Disqus! This might be the change I'm the happiest about. Not only does Disqus
take forever to load, but it tracks and sells our data. This is something I've always felt bad
about, but not bad enough to do the work of hosting my own commenting system (sorry!). I figured
that having Disqus and letting people choose whether commenting was worth it or not was better than
having no comment system at all.

But recently I stumbled across [staticman][6]. Now when you comment, a pull request will
automatically be opened on my Github repo. Then I can merge or discard it. I love this because just
like my website, comments are truly static. In order for this to work, the form will POST the
comment to staticman's servers. So unfortunately it doesn't completely cut out the middleman. At
least staticman is open source and promises [not to do any tracking][7]. I realize it's still
entirely possible they do, but at least I trust them a lot more than I trust Disqus.

One last note here, since migrating I've lost the ability to have threaded comments. Again, this
isn't the fault of staticman, but rather threaded comments is something I'd need to implement
myself. It is possible though it looks like a fair bit of work. I'll see how it goes, maybe I'll end
up implementing this eventually. At the very least I plan to spend a bit more time improving the
comment styling.


### Content

I've removed all extra content except for the blog itself. I found I never updated the other stuff
and likely no one will miss it (maybe I'll add a `Contact` page back in). I do want to start
dabbling in screencasts, so look for a new `Casts` content section sometime in the next couple of
months.


### Hunting the Shmoo

I've called my blog `Hunting the Shmoo` internally ever since I first created it, however I've never
used that text anywhere on screen (though the favicon has been picture of a shmoo forever). Now it's
official, `Hunting the Shmoo` is in the `<title>`! So I figure it's worth explaining.

A [shmoo][8] is a cartoon character from the 50s. They are short and fat creatures who are both
delicious and love to be eaten. When a human is hungry, they'll butter themselves up and jump right
into the frying pan. It follows that hunting these animals is no challenge at all.

To me, the name `Hunting the Shmoo` references our (as programmers) innate desire to follow the easy
path. Why write code when someone else has already written a better library to accomplish the same
thing? Why maintain a service when others can maintain it for us (see: this website)? The name also
hints at the irony in that sometimes finding the "easy" path ends up being the hardest part. You
have to hunt for that library or that tool or that service. You have to hunt for the shmoo.

Personally, I tend to obsess over this search for the easiest possible path. I tweak my workflow
incessantly, I try a never ending parade of tools on the off chance one of them might offer some
miniscule improvement, and I write my own scripts and programs to automate tasks that I'll only ever
need to execute twice.

I think it's an apt name because that's what this blog tends to be about. Tools, tricks and workflow
hacks that I've stumbled across in my never ending hunt.


[1]: http://gohugo.io/
[2]: https://pages.github.com/
[3]: https://github.com/ahal/hunting-the-shmoo
[4]: https://github.com/ahal/ahal.github.io
[5]: https://github.com/alanorth/hugo-theme-bootstrap4-blog
[6]: https://staticman.net/
[7]: https://staticman.net/sponsors
[8]: https://en.wikipedia.org/wiki/Shmoo
