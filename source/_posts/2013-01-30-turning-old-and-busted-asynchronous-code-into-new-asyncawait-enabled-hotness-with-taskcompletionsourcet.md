---
title: 'Turning old and busted asynchronous code into new async/await-enabled hotness with TaskCompletionSource<T>'
date: 2013-01-30T22:38:36+00:00
---
While working with a client to create a new version of their software, one of the tasks was creating a service that talked to a hardware laser tracker, a device which allows tracking certain points (*targets*) over a large distance.

<!-- more -->

The API provided by the manufacturer was not ideal, to say the least. The API consisted of a managed wrapper over two classes, we'll call them Request and Response, providing asynchronous request and callback operations. For each operation on the Request object, a corresponding Answer operation would arrive asynchronously on the Response object, e.g. if a `GetPosition` method was called on Request, sometime later an `OnGetPositionAnswer` method would arrive on the Response object, containing the relevant information.

One of the requirements was to be able to wait for several of such callbacks to arrive, before doing another operation. Several options were considered, among them [Reactive Extensions (Rx)](http://www.introtorx.com/) and [TPL Dataflow](http://msdn.microsoft.com/en-us/devlabs/gg585582.aspx). In the end, I chose an approach based on the [`TaskCompletionSource<T>`](http://msdn.microsoft.com/en-us/library/dd449174.aspx) class (part of the TPL), which I describe below.

Having exposed a .NET event in the Response object for each of the callbacks we were interested in, I defined a following method, returning a `Task<T>`, where `T` was the object that contained the data I required:

```csharp
public Task<PositionData> GetPositionAsync()
{
    var tcs = TaskCompletionSourc<PositionData>();

    // subscribe to the callback before firing the request
    _response.GetPositionAnswer += (sender, args) =&gt;
    {
        PositionData data = ... // translate position data from the event's arguments
	
        tcs.SetResult(data);
    };

    // perform the actual operation (method is asynchronous, returns immediately)
    _request.GetPosition();

    return tcs.Task;
}
```

And it worked great! The caller of `GetPositionAsync` now had a task which he can either `await` (if using .NET 4.5, or in .NET 4.0 using Async Targeting Pack (now known as [Microsoft.Bcl.Async](http://nuget.org/packages/Microsoft.Bcl.Async)), but only if running in Visual Studio 2012), or using plain old methods, available on the Task object.

However, upon calling this method a second time, an `InvalidOperationException` ***An attempt was made to transition a task to a final state when it had already completed.*** was thrown on the `tcs.SetResult(data)` line. It took me a second to realize the bug, can you see it?

The problem occurred because the event handler was not unsubscribed from, after the task had completed! Since the handler is a lambda expression, it captured the variable `tcs` when it was created. When we called `GetPositionAsync()` the second time, we made another subscription to the event handler, but when it fired, the first subscription was handled first, attempting to set the result of the **first** `TaskCompletionSource` instance, which had, of course, already finished.

Unsubscribing from an anonymous method (or a lambda expression) is possible, but not very pretty. It requires a small abuse of the C# syntax, to have the handler stored in a local variable, then subscribed and unsubscribed from. After a bit of tweaking, this was the end result, solving the problem:

```csharp
public Task<PositionData> GetPositionAsync()
{
    var tcs = new TaskCompletionSource<PositionData>();
   
    // Declare and initialize a local variable of type EventHandler to null
    // This is needed to use the variable inside the lambda expression body
    EventHandler handler = null;
    handler += (sender, args) => 
    {
        PositionData data = ... // get the data from event args
        
        tcs.SetResult(data);
        
        // unsubscribe from the event handler when task is complete
        _response.GetPositionAnswer -= handler;
    };
    
    // subscribe to the event handler before executing the operation
    _response.GetPositionAnswer += handler;
    
    _request.GetPosition();
    
    return tcs.Task;
}
```

It's not very pretty, but it does the job. If anyone has a better suggestion, please leave a comment!

Until next time, happy asyncing!
