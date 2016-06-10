---
title: Running multithreaded unit tests with FakeItEasy
date: 2012-12-11T21:39:08+00:00
---
While running some of my tests today, I suddenly got an `IndexOutOfRangeException`, with the following stack trace:

<!-- more -->

```
   at System.Collections.Generic.List`1.Add(T item)
   at FakeItEasy.Core.FakeScope.AddInterceptedCall(FakeManager fakeManager, ICompletedFakeObjectCall call)
   at FakeItEasy.Core.FakeManager.RecordInterceptedCall(InterceptedCallAdapter interceptedCall)
   at FakeItEasy.Core.FakeManager.Intercept(IWritableFakeObjectCall fakeObjectCall)
   at FakeItEasy.Core.FakeManager.Proxy_CallWasIntercepted(Object sender, CallInterceptedEventArgs e)
   at FakeItEasy.Creation.CastleDynamicProxy.CastleDynamicProxyGenerator.ProxyInterceptor.RaiseCallWasIntercepted(IInvocation invocation)
   at FakeItEasy.Creation.CastleDynamicProxy.CastleDynamicProxyGenerator.ProxyInterceptor.Intercept(IInvocation invocation)
   at Castle.DynamicProxy.AbstractInvocation.Proceed()
   at Castle.Proxies.ObjectProxy_3.Info(String format, Object[] args)</pre>
```

The code under test was using Tasks to do some work in the background, and was using a fake instance of an `ILogger`, which was created with [FakeItEasy](https://github.com/FakeItEasy/FakeItEasy) and passed to the code under test.

The above stack trace shows a classic symptom of a thread-safety issue. Searching for this issue led me to [this bug report](http://code.google.com/p/fakeiteasy/issues/detail?id=31), where a similar problem was described. Patrik HÃ¤gne, the creator of FakeItEasy, argues that using threading in tests is always problematic, however provides a nice and elegant solution to work around the problem.

The problem, of course, that the fake instance of the logger was not thread-safe, causing the underlying interceptor to incorrectly record the calls made to the fake logger object. However, when creating fake objects with FakeItEasy, it's possible to specify build options for the fake instance. This is where Patrik's solution comes in: wrap the fake instance with a syncronization interceptor, which can be applied in the following way:

```csharp
    A.Fake<ILogger>(x => x.Synchronized());
```

Where `Synchronized()` is an extension method you can define in your tests:

```csharp
public static class MyPersonalFakeExtensions
{
  public static IFakeOptionsBuilder Synchronized(this IFakeOptionsBuilder builder)
  {
    return builder.OnFakeCreated(fake =&gt; 
	Fake.GetFakeManager(fake).AddInterceptionListener(new CallSynchronizer()));
  }
}
```

And `CallSynchronizer` is an implementation of `IInterceptionListener`, which simply adds locking around method execution:

```csharp
public class CallSynchronizer : IInterceptionListener
{
  private static readonly object synchronizationLock = new object();

  public void OnBeforeCallIntercepted(IWritableFakeObjectCall call)
  {
    Monitor.Enter(synchronizationLock);
  }

  public void OnAfterCallIntercepted(IWritableFakeObjectCall call)
  {
    Monitor.Exit(synchronizationLock);
  }	
}
```

And that's it &ndash; using this code you can create a thread-safe fake objects to use in your tests, if you require.
