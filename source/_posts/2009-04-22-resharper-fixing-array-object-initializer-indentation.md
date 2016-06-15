---
title: 'ReSharper: Fixing array and object initializer indentation'
date: 2009-04-22T04:55:49+00:00
---
There are tons of options when it comes to configuring your coding style in ReSharper. Somehow I managed to screw the indentation of array and object initializers' variables. This is what it looked like (I use **At Next Line (BSD style)** setting):</p> 

<!-- more -->

```csharp
int[] array = new int[]
{
1, 2, 3
}
```

To fix this, go to **Formatting Style -> Other**, and set the *Continuous line indent multiplier* to 1 (mine was 0)
{% asset_img image.png %}

And now it's back to normal:
  
```csharp
int[] array = new int[]
{
  1, 2, 3
}
```