+++
title = "Working with shared dependencies in ZIO Test"
date = 2021-11-20T10:08:54Z
+++
ZIO Test is a [testing library](https://zio.dev/datatypes/test/) in which all suites and individual tests are regular ZIO values. This means that all composition features that apply to ZIO also apply to tests, in particular-dependency management via the environment.

In this post, I will explain how dependencies are used in ZIO Test, how to provide shared dependencies between tests, and how to modify them using Test Aspects. But first, let's understand how ZIO Test works under the hood.

<!-- more -->

If you're already familiar with ZIO Test and Test Aspects, feel free to [skip to the last section](#Modifying-shared-dependencies-for-each-test).

# Introduction to ZIO Test

> **Note**: the following applies to ZIO 1.x. ZIO 2.0 introduces significant syntactic changes to the structure of the tests, though most details about the internals still apply.

While ZIO Test (zio-test) is the library name, the tests themselves are broken into two categories: *Suites* and *Tests*. Suites are containers of tests; each suite may contain 0 or more tests inside of it. 

Here is the canonical "Hello world" ZIO Test. Let's break it down:

```scala
import zio.console._
import zio.test._
import zio.test.environment.TestConsole

object MySpec extends DefaultRunnableSpec {                 // (1)
  def spec = suite("My spec")(                              // (2)
    testM("Hello world") {                                  // (3)
      for {
        _     <- putStrLn("Hello world!")
        lines <- TestConsole.output                         // (4)
      } yield assertTrue(lines.contains("Hello world!\n"))  // (5)
    },
    ...                                                     // (6)
  )
}
```

1. In ZIO Test, it's common to refer to suites of tests as Specs, here we extend `DefaultRunnableSpec` which is responsible for several things. More on that later.
2. The abstract value `spec` must be implemented here by providing it with a `suite` containing tests or additional (nested) suites.
3. The `test`/`testM` definition describes tests that perform or don't any ZIO effects, respectively.
4. Part of ZIO Test's in-memory implementations of base services, here-a test console allowing to capture the output as a `Vector[String]`
5. The assertion syntax of [Smart Assertions](https://zio.dev/reference/test/assertions/smart-assertions/), which are technically a part of ZIO 2.0, but were backported to ZIO 1.x due to their extreme usefulness.
6. Additional tests or suites, separated by commas.

# Anatomy of a ZIO Test

Most specs will typically extend [`DefaultRunnableSpec`](https://github.com/zio/zio/blob/06259b1bc79ddf548943486aed20d2b455e162be/test/shared/src/main/scala/zio/test/DefaultRunnableSpec.scala#L28), a base class provided by the ZIO Test library, which is, in fact, a *standalone application*, implementing a `main()` method, which means it can be executed on the command line from `java -jar`. `DefaultRunnableSpec` extends a base trait `RunnableSpec[R, E]`, providing it with a common `TestEnvironment` in `R`:

```scala
type TestEnvironment =
  Annotations
    with Live
    with Sized
    with TestClock
    with TestConfig
    with TestConsole
    with TestRandom
    with TestSystem
    with ZEnv
```

The `TestEnvironment` consists of test implementations for all services required by `ZEnv`, in addition to test-specific services such as a `TestConsole` for capturing and manipulating console output, `TestClock` for setting and controlling the passage of time, and others.

Under the hood, the `RunnableSpec` implementation calls the actual [`TestRunner`](https://github.com/zio/zio/blob/06259b1bc79ddf548943486aed20d2b455e162be/test/shared/src/main/scala/zio/test/TestRunner.scala#L42) instance associated with it, which runs the tests in the spec *in parallel* (with up to 4 tests by default), and each test is executed by a [`TestExecutor`](https://github.com/zio/zio/blob/06259b1bc79ddf548943486aed20d2b455e162be/test/shared/src/main/scala/zio/test/TestExecutor.scala#L34-L36):

```scala
def run(spec: ZSpec[R, E], defExec: ExecutionStrategy): UIO[ExecutedSpec[E]] =
  spec.annotated
    .provideLayer(environment)
    .foreachExec(defExec) ...
  ... 
```

Here, the `environment` is the "live" instance of our `TestEnvironment`, and it is provided to the spec using `provideLayer` (non-shared), which means that each test *gets a fresh copy* of the environment! It makes sense since we don't want to re-use the `Random` instance, for example, between two tests, so each test gets a fresh copy of Random.

If we want to share a (stateful) value/service between the tests in the suite (for integration purposes, for instance), we need to provide it as *shared*, using one of the `provide*Shared` variants.

# Using shared dependencies in ZIO Test

For illustration, here's what using a shared value between tests looks like:

```scala
object MySharedService {
  val live: ULayer[Has[UUID]] = UIO(UUID.randomUUID()).toLayer    // (1)
}

object MySpec extends DefaultRunnableSpec {
  def spec = suite("My suite")(
    testM("test1") {
      for {
        uuid <- ZIO.service[UUID]                                 // (2)
        _    <- putStrLn(uuid.toString)
      } yield assertCompletes
    },
    testM("test2") {
      for {
        uuid <- ZIO.service[UUID]                                 // (2)
        _    <- putStrLn(uuid.toString)
      } yield assertCompletes
    }
  ).provideSomeLayerShared[TestEnvironment](MySharedService.live) // (3)
```

Here we're doing the following:

1. A service layer definition. Here we're using `UUID` as the service for illustration
2. Get the UUID service (causing the test to require `Has[UUID]` in addition to `TestEnvironment`) and print it out to the console
3. Provide the UUID service layer as a partial *shared* layer, satisfying/eliminating the requirement for `Has[UUID]`

The last point is often a source of confusion, so let's expand on it:

In ZIO, the `provide*Some*` variants are used to satisfy/eliminate partial requirements and specify the *remainder* to be satisfied by the caller, higher up. In our example above, our tests have the type

```scala
ZIO[TestEnvironment, E, zio.test.TestResult]
```
but requiring `Has[UUID]` (due to the use of `ZIO.service`) caused it to be typed as:
```scala
ZIO[TestEnvironment with Has[UUID], E ,zio.test.TestResult]
```

To (partially) satisfy this requirement, we can provide the `Has[UUID]` part ourselves, and the remaining `TestEnvironment` will be provided by the `DefaultRunnableSpec` itself.

Finally, by using the `provideSomeLayerShared` variant on the *suite* level, we're providing a layer that is *shared* between all the tests in that suite, and if we run this spec, we will see that the output is as follows:

```
Testing started at 15:20 ...
fc71c273-3824-46b2-8929-409544a19fa5
fc71c273-3824-46b2-8929-409544a19fa5
```

This means that the service layer was created just once (creating a single UUID value), and all tests now accessing this value get the same one! What actually happens is that each test in the suite gets a *copy* of the suite's environment, along with any shared values in it.

# Modifying shared dependencies for each test

Now that we know how to provide shared dependencies to tests, sometimes there's a need to modify a value/service in the test before it's executed (think of creating a fresh database per-test for Postgres Testcontiner integration tests, which is the subject of an upcoming post!).

This is done with [Test Aspects](https://zio.dev/version-1.x/howto/test-effects/#test-aspects). You can think of aspects as functions `ZIO => ZIO`, applying some transformation to the effect before/after its execution. Test Aspects cannot be used to *provide* or *eliminate* requirements from tests, but they can be used to *modify* the environment contained within the test!

Taking inspiration from the [existing aspects](https://github.com/zio/zio/blob/06259b1bc79ddf548943486aed20d2b455e162be/test/shared/src/main/scala/zio/test/TestAspect.scala), we can create the following *per-test* aspect called `newUuid`:

```scala
def newUuid = new PerTest.AtLeastR[Has[UUID]] {
  override def perTest[R <: Has[UUID], E](test: ZIO[R, TestFailure[E], TestSuccess]) =
    for {
      randomUuid <- UIO(UUID.randomUUID())
      updated    <- test.updateService[UUID](_ => randomUuid)
    } yield updated
}
```

This aspect states that an environment containing *at least* `Has[UUID]` is required (and recall that by using `ZIO.service[UUID]` in our tests, we now require it). In the `perTest` method of the aspect, we are given the test as a ZIO effect and can perform any operation on it!

In particular, we can call `updateService` on it, *replacing* the existing UUID service value with the one we created in the line above! This means that the original (shared) uuid is replaced with this fresh one, and because this is a per-test aspect, it will be applied to each test individually, resulting in:

```
Testing started at 15:23 ...
dc723d70-83c1-4c6c-9478-7a2087533bb4
728ed277-7d49-4b22-a5a3-6db3d32ff7b0
```

Meaning that each test got a fresh value for UUID, despite it being provided as shared initially.

Finally, putting it all together looks like this:

```scala
object MySharedService {
  val live: ULayer[Has[UUID]] = UIO(UUID.randomUUID()).toLayer
}

object MySpec extends DefaultRunnableSpec {
  def spec = (suite("My suite")(
    testM("test1") {
      for {
        uuid <- ZIO.service[UUID]
        _    <- putStrLn(uuid.toString)
      } yield assertCompletes
    },
    testM("test2") {
      for {
        uuid <- ZIO.service[UUID]
        _    <- putStrLn(uuid.toString)
      } yield assertCompletes
    }
  ) @@ newUuid).provideSomeLayerShared[TestEnvironment](MySharedService.live)
```

# Summary

This post's goal was to provide the background and motivation to using and modifying shared dependencies in ZIO Tests. In my upcoming post, I will explain how to take advantage of this technique to improve upon [integration testing with Postgres Testcontainers](https://hmemcpy.com/2020/08/running-postgres-integration-tests-easily-with-testcontainers-and-zio-test/) by over **70%**, by re-using a single Testcontainer instance for all the tests, giving each a fresh copy of the database for complete isolation!