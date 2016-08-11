---
title: 'Wanted: a maintainer for Agent Mulder (and other ReSharper plugins)'
date: 2016-08-09 11:12:01
tags:
---
Sometime in 2011, I've seen a cool feature of [Castle Windsor IoC container](https://github.com/castleproject/Windsor/) - the ability to create [typed factories based on an interface](https://github.com/castleproject/Windsor/blob/master/docs/typed-factory-facility-interface-based.md), without any implementation. That day I realized 2 things: a) containers are magic, and b) such magic would never be allowed in production.

<!-- more -->

An idea was formed in my mind: what if my [favorite IDE extension](https://www.jetbrains.com/resharper/) could visualize types that are created in such magical ways, by the IoC/DI frameworks? If it were less magical, perhaps it could be used more. And thus, [Agent Mulder plugin for ReSharper](https://github.com/hmemcpy/AgentMulder) was born - it analyzes container registration code in your solution, and provides navigation to and finding usages of types registered or resolved via those containers.

Here's an old demo of it in action:
{% vimeo 41113265 %}

It was a great experience to write, and even greater experience to have Agent Mulder be one of the most popular ReSharper plugins of all time.

## I need your help

It's 2016, and [I haven't fixed your issue yet](http://www.michaelbromley.co.uk/blog/529/why-i-havent-fixed-your-issue-yet). It's not that I don't want to, but... I don't want it to die either. Writing and maintaining plugins for ReSharper is not an easy task, but not impossible either.

I'm looking for YOU to take over [my ReSharper plugins](https://resharper-plugins.jetbrains.com/profiles/hmemcpy/) (Agent Mulder, Xao, InternalsVisibleTo Helper, and others), and keep them safe! If you're interested, please drop me a line on twitter, comments, email.

Whoever you are, I'll make sure to walk you through the mess.

Thank you!
