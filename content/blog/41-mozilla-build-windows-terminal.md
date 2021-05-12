---
title: "A Better Terminal for Mozilla Build"
date: 2021-03-02T09:00:00-05:00
tags: [mozilla, productivity, tips-and-tricks]
slug: mozilla-build-windows-terminal
---

If you're working with mozilla-central on Windows and followed the [official
documentation](https://firefox-source-docs.mozilla.org/setup/windows_build.html), there's a good
chance the MozillaBuild shell is running in the default `cmd.exe` console. If you've spent any
amount of time in this console you've also likely noticed it leaves a bit to be desired. Standard
terminal features such as tabs, splits and themes are missing. More importantly, it doesn't render
unicode characters (at least out of the box).

Luckily Microsoft has developed a [modern
terminal](https://www.microsoft.com/en-ca/p/windows-terminal/9n0dx20hk701) that can replace cmd.exe,
and getting it set up with MozillaBuild shell is simple.

<!--more-->

1. Open the Microsoft Store and search for "Windows Terminal".
2. Click "Get".
3. Open "Windows Terminal" (and create a shortcut while you're at it).
4. Click the dropdown arrow to the right of the current tab and choose "Settings"
5. Paste the following at the end of the `profiles.list` key in the JSON file that gets opened:

```json
    {
      "guid": "{6fee45ac-05f7-453c-93a3-761cd18b06ae}",
      "name": "MozillaBuild",
      "commandline": "<mozilla-build>\\start-shell.bat",
      "icon": "<mozilla-central>\\browser\\branding\\nightly\\firefox.ico"
    }
```

Replace `<mozilla-build>` with the path to your MozillaBuild directory, and `<mozilla-central>`
with the path to your mozilla-central clone. Also mind your trailing commas, it needs to be valid
JSON.

A great feature of Windows Terminal is that it can support cmd.exe, PowerShell and even WSL (which
gets added automatically if you enable WSL). So you can run WSL in one tab, PowerShell in a second and
the MozillaBuild shell in a third!

When you open a new tab, the first profile in the list will be chosen. If you'd like new tabs to
automatically open the MozillaBuild shell, you can add a top-level `defaultProfile` key like so:

```json
    {
        "defaultProfile": "{6fee45ac-05f7-453c-93a3-761cd18b06ae}",
    }
```

The guid just needs to match the guid you specified in the profiles list earlier. For more
information on Windows Terminal including how to use panes, see the [official
docs](https://docs.microsoft.com/en-us/windows/terminal/).

Enjoy!
