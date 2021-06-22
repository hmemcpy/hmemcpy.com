---
title: Scala 3 goodies for Scala 2 developers
date: 2021-06-22 10:45:02
tags:
---

Scala 3 is upon us, and the compiler team has been busy trying to make the migration process as smooth as possible. Scala 3 introduces new syntax for old things and deprecates some of Scala 2's infamous warts, many of which have been fixed (or made obsolete) by the new compiler. While some of the Scala 2 syntax still supported in Scala 3.0, it will be removed in Scala 3.1, so it's best to migrate as early as possible.

To make the process easier for Scala 2 users, the Scala compiler team have been [backporting](https://github.com/scala/scala/pull/9589) some of the new features to the Scala 2.x compiler, enabling them with the `-Xsource:3` compiler flag. In addition, users of the latest IntelliJ IDEA 2021.2 (in Early Access, at the time of writing) will get automatic refactoring suggestions, converting the old syntax to the new one.

<!-- more -->

{% asset_img intellij-refactor.gif %}

Here are the top features, enabled in Scala 2 by turning on the `-Xsource:3` compiler flag:
```scala
scalacOptions ++= Seq(
  ...
  "-Xsource:3"
)
```

After enabling this option, you might get lots of compiler warnings (or errors, depending on your configuration), explaining the deprecated features and suggesting ways to fix them. 

**Note**: although some Scala 3 features have been ported to the earlier versions of the Scala 2 compiler, the new syntax changes were added in the recently-released (at the time of writing) **2.13.6**. Please upgrade your Scala versions to get the latest available features.

Here are some of my favorites:

### `case class`es with a private constructor

If you're following the [Smart Constructor](https://tuleism.github.io/blog/2020/scala-smart-constructors/) pattern in Scala 2, you'll discover that making the constructor of a case class `private` is not enough - the companion `apply`, and the `copy` methods of the case class will still be public. There are ways to [work around it](https://gist.github.com/tpolecat/a5cb0dc9adeacc93f846835ed21c92d2) - but they are no longer needed with the `-Xsource:3` flag! Enabling it makes case classes behave *correctly*, like they do in Scala 3, disabling the companion `apply` and `copy` on any case class with a private constructor.

### Tuple destructuring in for-comprehensions

One common Scala 2 wart was the inability in most cases to destructure tuples during for-comprehensions, e.g.:
```scala
for {
  (name, age) <- getPerson()
  ...
} yield ...
```

This did not compile out of the box (due to the special requirement of having `withFilter`). To solve this (and other issues), a very popular compiler plugin called [better-monadic-for](https://github.com/oleg-py/better-monadic-for) (bm4 for short) was used. However, in Scala 3 this is supported by adding the keyword `case` in front of the tuple:
```scala
for {
  case (name, age) <- getPerson()
  ...
} yield ...
```

If you were using bm4 for this purpose - it is no longer required (and will make your migration to Scala 3 even easier, since Scala 3 does not support Scala 2's compiler plugins.)

### Miscellaneous syntax changes

Some other syntactic changes/improvements were backported in the latest Scala 2 versions:

#### `*` instead of `_` for wildcard imports

Scala 3 imports now use the `*` character for imports (and the use of `_` for imports will be removed in Scala 3.1), allowing you to write:

```scala
import scala.util.*
```

**Note**: Unfortunately, this change does not work for wildcards inside braces due to an issue that [was already fixed](https://github.com/scala/scala/pull/9639), but did not make it to the release as part of 2.13.6. It will be fixed in the next compiler release (2.13.7), when available. The following syntax:

```scala
import scala.util.{Try, *}
```
does not compile with Scala 2.13.6, failing with the error: `object * is not a member of package util`.

#### `as` instead of `=>` in import aliases

Additional change to how imports are handled is the use of the keyword `as` instead of `=>` when aliasing imported types.

Instead of:
```scala
import java.util.{List => JList}
```
Use:
```scala
import java.util.List as JList // braces not required for a single import alias
```

#### `?` instead of `_` for wildcard types

A less-used feature, but a notable change is the use of `?` in the following syntax:

Instead of:
```scala
val x: _ <: Any = ???
```
Use:
```scala
val x: ? <: Any = ???
```

#### `&` instead of `with` in compound type declarations:

Instead of:
```scala
val x: A with B = new A with B {}
```
we can now write:

```scala
val x: A & B = new A with B {}
```

#### vararg splice syntax (`*` instead of `:_*` and `@_*`)

One more simplification to the various ways of passing values into functions expecting variable arguments:

Instead of:
```scala
foo(s: _*)
```

Use:
```scala
foo(s*)
```

And instead of:
```scala
val Seq(a @_*) = ???
```

Use:
```scala
val Seq(a*) = ??? // RIP, 🐌 operator
```

More changes are being backported to Scala 2, I suggest keeping an eye on the release notes, and upgrading to the latest versions as soon as possible!