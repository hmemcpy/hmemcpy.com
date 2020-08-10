---
title: Running Postgres integration tests easily with TestContainers and ZIO Test
date: 2020-10-04 09:36:33
tags:
---
Integration/end-to-end testing is considered one of the best indicators that your code functions correctly, and everything is wired up as it should. [Testcontainers](https://www.testcontainers.org/) is a wonderful library for creating and running embeddable Docker containers that can run alongside your tests, so you can have real implementations of your third-party dependencies, instead of relying on fragile mocks. Testcontainers is a mature Java library that comes out of the box with integrations for Postgres, Kafka, RabbitMQ, and [many more](https://www.testcontainers.org/modules/databases/), as well as support for many test runners and even ports to [other languages](https://github.com/testcontainers).

In this short post, I'll explain how to integrate Testcontainers (the [Scala flavor](https://github.com/testcontainers/testcontainers-scala)) to play nicely with ZIO Test, showcasing some of the great composability features ZIO provides.

I will use a Postgres Testcontainer and [Flyway](https://flywaydb.org/) to perform migrations, intializing the databse schemas.

## Getting started

To play nicely with ZIO Test, we need to expose the Testcontainer as a [ZLayer](https://zio.dev/docs/howto/howto_use_layers), so it can be added to ZIO's [Test Environment](https://zio.dev/docs/howto/howto_test_effects#using-test-environment).

We'll need to add the following dependencies to our `build.sbt`:

```scala
"org.flywaydb"   % "flyway-core"                      % flywayVersion,
"ch.qos.logback" % "logback-classic"                  % logbackVersion,
"com.dimafeng"   %% "testcontainers-scala-postgresql" % testContainersVersion % Test
```

This adds Flyway to perform the actual migrations, Logback to print useful output messages from the container, and the Scala wrapper of the Postgres Test container. Replace the `*Version` values with the actual latest versions available for these dependencies.

Next, let's add introduce Testcontainers to ZIO:

```scala
import com.dimafeng.testcontainers.PostgreSQLContainer
import zio.blocking.{effectBlocking, Blocking}
import zio._

object TestContainer {
  type Postgres = Has[PostgreSQLContainer]
  
  def postgres(imageName: Option[String] = Some("postgres")): ZLayer[Blocking, Nothing, Postgres] =
    ZManaged.make {
      effectBlocking {
        val container = new PostgreSQLContainer(
          dockerImageNameOverride = imageName,
        )
        container.start()
        container
      }.orDie
    }(container => effectBlocking(container.stop()).orDie).toLayer
}
```

By default, the Scala Postgres container wrapper will fetch version 9 of PostgreSQL, you can get a specific version by specifying the `imageName` parameter with a specific tag, e.g. `postgres:12.3`, or leaving `postgres` to fetch the `latest`.

We use ZIO's [ZManaged](https://zio.dev/docs/datatypes/datatypes_managed) to wrap the creation and disposal of the container, wrapping the actual creation and shutdown in `effectBlocking` to signal to ZIO that this should be done on the blocking thread pool. This makes our ZLayer require the `Blocking` service. On shutdown, we stop the container. If creating or stopping fails for any reason, we'd like our test to terminate, which we do with `.orDie`, making any potential failures to be treated as defects, causing ZIO to shut down. Finally, we turn the ZManaged into a ZLayer by calling `toLayer` on it.

And that's it! We now have a Postgres layer to plug into the ZIO tests.

## Performing migrations

Once our container has started, we want to populate the database with our schema, before the tests are run. For this, ZIO Tests provides a mechanism called [Test Aspects](https://zio.dev/docs/howto/howto_test_effects#test-aspects), which allows, among other things, to execute an action *before* executing the tests. We can create a Test Aspect that runs the migration:

```scala
object MigrationAspects {
  def migrate(schema: String, paths: String*) = {
    val migration = for {
      pg <- ZIO.service[PostgreSQLContainer]
      _  <- runMigration(pg.jdbcUrl, pg.username, pg.password, schema, paths: _*)
    } yield ()

    before(migration.orDie)
  }

  private def runMigration(
    url: String,
    username: String,
    password: String,
    schema: String,
    locations: String*
  ) =
    effectBlocking {
      Flyway
        .configure()
        .dataSource(url, username, password)
        .schemas(schema)
        .locations(locations: _*)
        .load()
        .migrate()
    }
}
```

Here we define a function `migrate` that takes in the name of the `schema` for the migration, as well as the paths where the migration scripts are located. Because the container assigns a random port each time it starts, we fetch the container service and perform the migration using its parameters (such as the `jdbcUrl`). Again, because `Flyway` is a Java API, we wrap it with `effectBlocking` to ensure ZIO runs it on the blocking thread pool.

## Putting it all together

Finally, we can put it all together into a test that looks like this:

```scala
object MyPostgresIntegrationSpec extends DefaultRunnableSpec {
  val postgresLayer = Blocking.any >>> TestContainer.postgres()
  val testEnv = zio.test.environment.testEnvironment ++ postgresLayer

  val spec = suite("Postgres integration") {
    testM("Can create and fetch a customer") {
      for {
        userId <- CustomerService.create("testUser", "testPassword")
        result <- CustomerService.find(userId)

      } yield assert(result.id)(equalTo(userId)) &&
              assert(result.username)(equalTo("testUser"))
    }
  }.provideCustomLayer(testEnv) @@ migrate("customers", "filesystem:src/customers/resources/db/migration")
```

We create a test environment `testEnv` by combining the default ZIO Test environment layer with the Postgres layer, and passing it to the test suite using `provideCustomLayer`. In addition, we perform the migration at the start of each test by applying `migrate` using the `@@` operator. Finally, depending on the organization of your modules, you can specify custom paths to your migration scripts, as well as the schema name.

And that's it, we now have an integration test that starts Postgres, performs the migration, and runs your test. When it's finished, ZIO gracefully shuts down the container!

## Bonus: making it nicer

Here are a few tweaks you can do to the above setup:

### Specifying a default schema

By default, the Postgres Testcontainer does not provide a way to specify a `currentSchema` parameter on the JDBC URL. We can fix this with some good, old-fashioned inheritance:

```scala
final class SchemaAwarePostgresContainer(
  dockerImageNameOverride: Option[String] = None,
  databaseName: Option[String] = None,
  pgUsername: Option[String] = None,
  pgPassword: Option[String] = None,
  mountPostgresDataToTmpfs: Boolean = false,
  currentSchema: Option[String] = None
) extends PostgreSQLContainer(
      dockerImageNameOverride,
      databaseName,
      pgUsername,
      pgPassword,
      mountPostgresDataToTmpfs
    ) {
  override def jdbcUrl: String =
    currentSchema.fold(super.jdbcUrl)(schema => s"${super.jdbcUrl}&currentSchema=$schema")
  }
```

We'll extend `PostgreSQLContainer` to allow specifying the `currentSchema` as a constructor argument (in addition to all the others), and will override `jdbcUrl` to append it to the URL (if was specified). Now, let's replace our creation function with the new class:

```scala
  def postgres(currentSchema: Option[String] = None): ZLayer[Blocking, Nothing, Has[SchemaAwarePostgresContainer]] =
    ZManaged.make {
      effectBlocking {
        val container = new SchemaAwarePostgresContainer(
          dockerImageNameOverride = Some("postgres"),
          currentSchema = currentSchema
        )
        container.start()
        DockerLoggerFactory.getLogger(container.container.getDockerImageName).info(s"⚡ ${container.jdbcUrl}")
        container
      }.orDie
    }(container => effectBlocking(container.stop()).orDie).toLayer
```

Note that the parameter to `postgres()` now accepts the schema name instead of the docker image name, the container will fetch the latest available PostgresSQL image. Tweak this according to your needs. 

In addition, I've added an log output line using the Testcontainer's Docker logger to print out the JDBC URL for easier debugging.

### Creating an `ITSpec` for easier integration tests

Last thing we can do is to create a base class to hide all this work, allowing us to write integration tests without adding any of the boilerplate. This was adapted from an excellent library called [tranzactio](https://github.com/gaelrenoux/tranzactio) by Gaël Renoux, which helps Doobie (and Anorm) play nice with ZIO:

```scala
object ITSpec {
  type ITEnv = TestEnvironment with Logging with Postgres
}

abstract class ITSpec(schema: Option[String] = None) extends RunnableSpec[ITEnv, Any] {
  type ITSpec = ZSpec[ITEnv, Any]

  override def aspects: List[TestAspect[Nothing, ITEnv, Nothing, Any]] =
    List(TestAspect.timeout(60.seconds))

  override def runner: TestRunner[ITEnv, Any] =
    TestRunner(TestExecutor.default(itLayer))

  val itLayer: ULayer[ITEnv] = {
    val postgres = Blocking.live >>> TestContainer.postgres(schema)
    val logging = Slf4jLogger.make(LogFmtRenderer())
    ... // other services you might want to create for testing
    testEnvironment ++ logging ++ postgres
  }.orDie
}
```

Which allows us to create Postgres-powered integration specs like this:

```scala
object MyITSpec extends ITSpec(Some("schemaName")) {
  val spec: ITSpec = suite("Integration suite")(
    testM("...") { }
  ) @@ migrate("schemaName", "filesystem:path/to/resources/for/migration")
}
```

And the `ITSpec` base suite will provide all the necessery environments for us! Note that `val spec: ITSpec` must have `ITSpec` type ascription, otherwise Scala will not be able to correctly infer all the requirements.

Happy testing!