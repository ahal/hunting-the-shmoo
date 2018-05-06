---
title: Isolating Mozmill's Driver
date: 2011-10-20
tags: [mozilla, mozmill]
slug: isolating-mozmill-driver

---

At the beginning of September, I was asked to write [yet another automated test harness][1] for
testing user responsiveness. Among other things, the harness needed to be capable of automating a
wide range of user interactions in Firefox (such as opening context menus, clicking buttons etc). Oh
and by the way this needs to be finished as quickly as possible.

<!--more-->

It turns out that machines aren't very good at interacting with user interfaces designed for humans.
Properly automating a complex piece of software like Firefox would take ages as there's a whole
plethora of things to think about. Luckily, at Mozilla we already have a tool for automating user
interaction called [Mozmill][2]. The good news is that Mozmill's driver is excellent at automating
Firefox's UI. The bad news is that the test harness piece is very bulky and unwieldy.  Trying to use
a Mozmill test to drive Firefox is just an unpleasant experience all around.

So rather than re-write a driver from scratch, or be stuck trying to shoehorn my test harness into
Mozmill, I decided to do a little work and isolate Mozmill's driver from Mozmill's test harness.
Unlike the test harness, Mozmill's driver is lightweight and pure javascript (no python). I
documented how to [import the driver][3] into an extension on MDN, but the end result is that any
chrome scope JS can now import and use Mozmill's driver. For example: 

```js
// Import mozmill and initialize a controller object  
Components.utils.import('resource://mozmill/driver/mozmill.js');  
let controller = getBrowserController();  
  
// Open google  
controller.open('http://www.google.com');  
controller.waitForPageLoad();  
  
// Type in the search box  
let textbox = findElement.ID(controller.tabs.activeTab, 'lst-ib');  
let button = findElement.Name(controller.tabs.activeTab, 'btnK');  
textbox.sendKeys('foobar');  
button.click();
```

#### Next Steps

The process for importing mozmill still isn't as easy as I'd like. Ideally I'd like to have a
Makefile that compiles all of the Mozmill driver files into a single 'mozmill.js' file similar to
how jquery does it. If anyone has any experience or tips for getting something like this to work I'd
appreciate it.

[1]: https://wiki.mozilla.org/Auto-tools/Projects/peptest
[2]: https://developer.mozilla.org/en/Mozmill
[3]: https://developer.mozilla.org/en/Mozmill/Using_The_Driver
