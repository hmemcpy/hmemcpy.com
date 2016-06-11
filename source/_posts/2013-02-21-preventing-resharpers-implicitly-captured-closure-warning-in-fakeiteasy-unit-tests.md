---
title: "Preventing ReSharper's 'implicitly captured closure' warning in FakeItEasy unit tests"
date: 2013-02-21T14:08:51+00:00
---
I noticed that some of my unit tests have a [ReSharper](http://www.jetbrains.com/resharper/) warning on the `A.CallTo()` methods of [FakeItEasy](https://github.com/FakeItEasy/FakeItEasy), suggesting that some local variables are captured implicitly by the lambda expression.

<!-- more -->

<img title="" style="border-left-width: 0px; border-right-width: 0px; background-image: none; border-bottom-width: 0px; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-top-width: 0px" border="0" alt="" src="http://i0.wp.com/hmemcpy.com/wp-content/uploads/2013/02/image.png?resize=504%2C65" data-recalc-dims="1" />

This warning appears since ReSharper doesn't know that the lambda expression is executed immediately when the `A.CallTo` method is invoked. Fortunately, with the help of [External Annotations](http://www.jetbrains.com/resharper/webhelp/Code_Analysis__External_Annotations.html), in particular, the **InstantHandle** annotation, we can teach ReSharper about it!

The InstantHandle annotation tells ReSharper that the method parameter is completely handled when the invoked method is on the stack. If the parameter is a delegate (which in our case, it is), it indicates that the delegate is executed when the method is executed.

To add this information about FakeItEasy's `A.CallTo()` overloads that accept delegates, we can create an external XML file, which looks like this:

<div id="scid:f32c3428-b7e9-4f15-a8ea-c502c7ff2e88:7686fbc8-e740-476e-a89b-40eda4c1a306" class="wlWriterEditableSmartContent" style="float: none; padding-bottom: 0px; padding-top: 0px; padding-left: 0px; margin: 0px; display: inline; padding-right: 0px">
  <pre class="brush: xml;">&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;assembly name="FakeItEasy"&gt;
  &lt;member name="M:FakeItEasy.A.CallTo(System.Linq.Expressions.Expression{System.Action})"&gt;
    &lt;parameter name="callSpecification"&gt;
      &lt;attribute ctor="M:JetBrains.Annotations.InstantHandleAttribute.#ctor" /&gt;
    &lt;/parameter&gt;
  &lt;/member&gt;
  &lt;member name="M:FakeItEasy.A.CallTo``1(System.Linq.Expressions.Expression{System.Func{``0}})"&gt;
    &lt;parameter name="callSpecification"&gt;
      &lt;attribute ctor="M:JetBrains.Annotations.InstantHandleAttribute.#ctor" /&gt;
    &lt;/parameter&gt;
  &lt;/member&gt; 
&lt;/assembly&gt;</pre>
</div>

Download the XML via [GitHub Gist](https://gist.github.com/hmemcpy/5003775),

This instructs ReSharper to add an instance of the InstantHandleAttribute to a parameter called callSpecification of two CallTo method overloads, once which takes an `Expression<Action>`, the other, which takes an `Expression<Func<T>>`. Save this file as **FakeItEasy.ExternalAnnotations.xml** and place it **_alongside_&nbsp;**FakeItEasy.dll (inside libNET40 of your NuGet package, for example). Reload your solution, and the warnings will now disappear!

Stay tuned, as I explain in the next blog post how to create those XML annotations easily with a little known ReSharper trick!
