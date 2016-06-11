---
title: How Nancy made .NET Web development fun!
date: 2014-03-17T15:35:48+00:00
---
Let's get this out of the way first: this is **not** a post about how to use [Nancy](http://nancyfx.org/) &ndash; there are lots of blog posts out there, written by people far better at it than me!

I am not a web developer. During my career I mostly worked on desktop applications (with occasional dab in the database land, typical CRUD stuff). Over the years my passion for development shifted towards building development tools (Visual Studio, ReSharper plugins), and my dayjob now having a blast building [OzCode](http://www.oz-code.com/), a debugging productivity tool for Visual Studio.

<!-- more -->

So I never had the chance to *do* web development. Every time I tried to do it, I gave up quickly, because I could never get the hang of it! I don't know JavaScript, and ASP.NET (even MVC and even Web API) make a lot of assumptions about how to structure and build web apps. Same goes for other web frameworks and languages &ndash; they're all great(!), but just not for me. Anything I ever tried to build, I quickly gave up (due to being stuck, or otherwise losing interest).

Enter Nancy.

When I first heard about Nancy, I was intrigued &ndash; an entire web application that fits in a tweet! If, in a highly unlikely event, you're reading about Nancy for the first time in this blog post, here's the canonical *hello world* app:

```csharp
public class SampleModule : Nancy.NancyModule
{
    public SampleModule()
    {
        Get["/"] = _ => "Hello World!";
    }
}
```

And with [ScriptCS](http://scriptcs.net/) being the hot new thing, hosting Nancy apps [does not even require Visual Studio](https://github.com/adamralph/scriptcs-nancy)!

So what makes Nancy so appealing to me, a non-web developer? First and foremost &ndash; the people behind it! Nancy is a perfect example of the Open Source spirit &ndash; with [more than 160 contributors](http://nancyfx.org/contribs.html), making it a fun, well-documented, well-tested, accessible framework for everyone and everything!

But what I like most about Nancy has nothing to do with its actual application &ndash; it has to do with the way it works under the covers. Demonstrated by one of Nancy's lead developers, Andreas Håkansson ([@TheCodeJunkie](https://twitter.com/TheCodeJunkie) on twitter), in the [Guerilla Framework Design](https://www.youtube.com/watch?v=7jg0u-YaRxQ) talk at DevDay, Nancy uses lots of cool C# language hacks to achieve simplicity and make using of the framework as simple as possible!

Want examples? Let's start with the *hello world* app above: there are at least 3 cool things that don't require you to understand exactly how they work. For example, the funky `= _ =>` *smiley face*. While aesthetically pleasing, this is a lambda expression, defining the body of the HTTP Get method, with the route */*. This lambda passes a parameter which is a dynamic dictionary (specified by underscore in the above example). This dictionary contains, among other things, the URL parameters, so they can be used immediately inside the method body, e.g.:

```csharp
Get["/greet/{name}"] = parameters => "Hello " + parameters.name;
```

Here, the underscore has been replaced with the named argument `parameters`, and now, everyone who issues an HTTP GET to the address /greet/Igal, for example, the value *Igal* will be captured in the parameter `name` in the dynamic dictionary, and will just be there, available to use!

Another thing to note is that the lambda returns a string, but it somehow renders fine in the browser. The `Get` property (along with other HTTP verbs that Nancy provides) expects a `Func<dynamic, dynamic>` as a return result of the lambda, so it doesn't really matter. The conversion is taken care under the hood of Nancy, which defines a lot of [implicit conversions](http://msdn.microsoft.com/en-us/library/z5z9kes2.aspx) to covert strings to valid response content, and integers to valid HTTP codes! This means that you can simply *`return 404;`* from a body of a Nancy route, and it will auto-magically transform into `HttpStatusCode.NotFound` that Nancy understands.

Everything in Nancy is expandable, configurable and overridable. Nancy is built with testability, extensibility and pluggability in mind, which means that almost everything you need it to do (support another View engine, hosting platform, custom IoC container, etc.) is just a NuGet package away. Which is just awesome, as there are [tons of things](https://www.nuget.org/packages?q=nancy) you can add to Nancy.

Finally, no post of mine can be complete without mentioning tooling. I love productivity addins, and I believe there should be a tool for anything! This is why I created [a plugin for ReSharper](https://github.com/hmemcpy/Nancy.ReSharper), bringing some of ReSharper's goodness to Nancy! It adds support to navigating and creating to Views, code completion and other validations. Everything that was until now available only in ASP.NET MVC (with ReSharper's help), is now also available for Nancy!

In conclusion, if you're dabbling in web development, you should definitely give Nancy a try! It's the only framework that made someone like me, a complete web development noob, be productive and actually create something useful!

Happy hacking!
