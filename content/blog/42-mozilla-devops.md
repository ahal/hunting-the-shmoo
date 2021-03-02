---
title: "DevOps at Mozilla"
date: 2021-03-02T11:00:00-05:00
tags: [mozilla, devops]
slug: mozilla-devops
---

I first joined [Mozilla as an intern](https://ahal.ca/blog/2011/why-mozilla-is-awesome/) in 2010 for
the "Tools and Automation Team" (colloquially called the "A-Team"). I always had a bit of
difficulty describing our role. We work on tests. But not the tests themselves, the the thing that
runs the tests. Also we make sure the tests run when code lands. Also we have this dashboard to view
results, oh and also we do a bunch of miscellaneous developer productivity kind of things. Oh and
sometimes we have to do other operational type things as well, but it varies.

Over the years the team grew to a peak of around 25 people and the A-Team's responsibilities
expanded to include things like the build system, version control, review tools and
more. Combined with Release Engineering (RelEng), this covered almost all of
the software development pipeline. The A-Team was eventually split up into many smaller
teams. Over time those smaller teams were re-org'ed, split up further, merged and renamed over and
over again. Many labels were applied to the departments that tended to contain those teams. Labels
like "Developer Productivity", "Platform Operations", "Product Integrity" and "Engineering
Effectiveness".

Interestingly, from 2010 to present, one label that has never been applied to any of these teams is
"DevOps".

<!--more-->

### A Journey to Understanding DevOps

The term "DevOps" was [coined sometime around
2009](https://devops.com/the-origins-of-devops-whats-in-a-name/) and slowly gained traction before
exploding in popularity around the mid 2010s. I can't remember exactly when it entered my
consciousness, but I do remember being a bit dismissive initially. Maybe because there didn't seem
to be a clear and concise definition, what one company called DevOps might look nothing like DevOps
at another. Or maybe it just seemed too much like a buzzword. Whatever the reason, I didn't start
paying attention until the latter half of the decade. Gradually I started to understand what DevOps
was about and realized it espoused many beliefs that I held internally, but had not yet managed to
put into words. I started reading blog posts and listening to podcasts on the topic, and started to
bring the lessons learned to my own work.

But it wasn't until very recently that I stumbled across [this definition of
DevOps](https://www.imaginarycloud.com/blog/devops-engineer/) (uncoincidentally the inspiration for
this post), that it truly crystallized in my mind. Myself and all the teams today that can trace
their lineage back to the A-Team or RelEng are doing DevOps. We are DevOps engineers.

### Why It Matters

My first instinct was to acknowledge this and move on. Who cares what the role is called as long
as the job is being done? But upon further reflection I think it's worth more than a simple
acknowledgement. There are several reasons why recognizing our role as DevOps is important.

First, sharing a common vocabulary enables better external communication. For example, it allows you
to research industry best practices and connect with other practioners of your field. You can find
conferences, online communities, blogs and podcasts. It can also help you when searching for a job
(as many of my colleagues [found themselves doing last
year](https://blog.mozilla.org/blog/2020/08/11/changing-world-changing-mozilla/)). Calling yourself
a "DevOps Engineer" looks better on a resume than a minor essay attempting to describe what it is
exactly you did. Interesting side bar, DevOps engineers are the [highest paid ICs](https://stackoverflow.blog/2020/02/12/stack-overflow-salary-reports-are-out-now-how-does-your-company-compare/) in tech according to
StackOverflow.

A shared vocabulary can also help communication internally. A common struggle for many teams is
communicating their value up the chain of command. At a certain level of management, saying "We do
DevOps" might be more impactful than a deep dive on CI systems and SRE. It'll also make your team more
recognizable to others, opening up avenues of communication that may have otherwise been missed.

But I think the most important reason to recognize oursleves as DevOps is the opportunity for
self-improvement, both on an individual and organizational level. As an example on the individual
side, the [aforementioned DevOps definition](https://www.imaginarycloud.com/blog/devops-engineer/)
posits that "one of the most valuable skills [for a DevOps engineer] is excellent communication and
cooperation". These are areas that I've long known that I personally need to improve, but never seem
to make much headway on. Knowing these soft skills are specifically suited to my role, gives me an
extra bit of motivation to work on them.


### Organizational Improvement

As beneficial as individual improvement can be, at Mozilla I think there is even more potential for
improvement at the organizational level. For example, DevOps engineers are supposed to maintain a
holistic view of the entire development pipeline, then be able to ruthlessly identify and fix
bottlenecks. Since the A-Team was initially split up, we've lost that ability. Now there are
distinct teams that handle their own little slice of the pipeline (e.g, vcs, build, CI, release,
review). This has allowed us to get a lot of great focused work done, but it also means that we've
lost the ability to step back and look at the pipeline as whole. We can no longer point at a
particular area and temporarily divert resources to it (other than through hiring). When a
particularly motivated individual tries to drive processes or projects that span multiple areas of
the pipeline, they run into conflict caused by differing goals across a multitude of teams.

I want to be clear that I'm not advocating that everyone suddenly become holistic big picture
thinkers. Nor am I advocating that we all recombine into the A-Team (such a large team came with
its own set of issues). But I'm struck by the fact that we have very few (if any) engineers involved
in all parts of the development pipeline. How can we divert our resources to maximize the value we
can bring to Mozilla? Can we increase collaboration between teams? What *is* the most pressing
bottleneck? I don't have any answers here, and I don't think anyone else does either.
But if we can adopt more of a DevOps mentality, I think we could work together to figure them out.

### Conclusion

The purpose of this post is simply to point out that the work I and many of my
colleagues do would typically be classified as "DevOps" outside of Mozilla. It's also to point out
that there are likely lessons and best practices we can learn from the industry. And if I'm being
honest, the purpose is also to inspire others to begin their own DevOps journey.

I don't know exactly what the lessons to be learned are, but I'm excited to continue my own
journey and bring what I can back to Mozilla.
