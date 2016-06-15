---
title: 'C# Puzzle: What does this program do?'
date: 2010-07-13T07:04:11+00:00
---
Consider the following code:

```csharp
class Woot
{
    private static float PI;
    private static bool initialized = doInitialize();

    private static bool doInitialize()
    {
        if (!initialized)
        {
            var thread = new Thread(() => { PI = 3.14f; });
            thread.Start();
            thread.Join();
        }
        return true;
    }

    public static void Main(string[] args)
    {
        Console.WriteLine(PI);
    }
}
```
What is the output of this program? Is it:

<!-- more -->

 1. 3.14
 2. 0
 3. Throws exception
 4. None of the above
  
To find out the answer to this puzzle, as well as many others, watch the [C# Puzzlers](http://streaming.ndc2010.no/tcs/?id=E915B78B-D9B7-4CE9-96DA-2B794391AD2F) talk with <a href="http://blogs.msdn.com/b/ericlippert/">Eric Lippert</a> and <a href="http://gafter.blogspot.com/">Neal Gafter</a> from NDC 2010. How many did you get right?
