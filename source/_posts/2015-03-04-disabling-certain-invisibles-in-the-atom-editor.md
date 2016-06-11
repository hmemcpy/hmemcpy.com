---
title: 'Disabling certain "invisibles" in the Atom Editor'
date: 2015-03-04T15:00:27+00:00
---
I recently started using GitHub's [Atom editor](https://atom.io/), and other than the [slow-ish startup time](https://github.com/atom/atom/issues/2654), I love it very much!

<img style="float: right; padding: 5px;" src="{% asset_path image.png %}" />One of the things I hate most is redundant whitespaces, so in all editors I use, I try to work with visible whitespace enabled, so I can keep those tiny dots in check. In the Atom editor, this feature is called **Show Invisibles**, however by default it shows _all_ the invisible characters, including endof and newline characters. There's no UI (yet?) to toggle which ones you want to see, but luckily, Atom is completely *hackable*, allowing us to do change about anything!

<!-- more -->

To remove the EOL/newline characters, go to **File &ndash; Open your Config**. The configuration file will open in a new tab, where you can modify the `invisibles:` entry like so:

```js
"*":
  editor:
    invisibles: 
      eol: false
      cr: false
    ...
```

Upon saving the file, Atom will immediately reload the configuration, and only the whitespace dots will remain visible!

For more information about what can be changed, check out [Customizing Atom](https://atom.io/docs/latest/customizing-atom).
