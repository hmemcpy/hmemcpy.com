---
title: Parsing character encoding-dependent protocols with scodec in Scala
date: 2021-11-19 13:29:31
tags:
---
At [work](https://unit.co), we have to handle and process many types of (sometimes archaic) financial protocols. One such protocol, Image Cash Letter (ICL, also known as ANSI DSTU X9.37 or X9.100-180), describes how cheques (or checks, for the US folks) are transmitted electronically between financial institutions.

X9.37 is one such archaic binary protocol still in use today. The specification allows this file to be encoded either in the 8-bit IBM [EBCDIC](https://en.wikipedia.org/wiki/EBCDIC) encoding or ASCII, and it contains both plain-text characters as well as TIFF image data. In Scala, one of the best ways to parse such protocols is to use a wonderful library called [scodec](https://github.com/scodec/scodec), a combinator library for creating codecs for binary data. I recommend reading about the library and getting familiarized with the syntax before reading further.

<!-- more -->

### The problem

Since both encodings are 8-bit, there's no way to distinguish between the files by size or contents. Fortunately, the specification explains how to detect the encoding:

{% blockquote %}
The coding scheme may be verified by inspecting the first two characters of
the X9.37 file that have the value '01' (File Header Record Type 01, Field 1).

The value '01' is defined in EBCDIC with the hexadecimal value 'F0F1'
and in ASCII with the hexadecimal value '3031'.
{% endblockquote %}

And indeed, inspecting such files in a hex editor reveals this difference:

| EBCDIC                                                 | ASCII                                                 |
|--------------------------------------------------------|-------------------------------------------------------|
| {% asset_img x9-ebcdic.png This is an example image %} | {% asset_img x9-ascii.png This is an example image %} |

Both values are located after the first 32-bit integer value specifying the File Header Record length (always 0x50).

### The solution

Armed with this knowledge, we can create a `Codec` to detect this encoding and expose it as a `java.nio.charset.Charset`. Fortunately, many scodec `string` combinators take `Charset` as an implicit parameter, allowing us to specify the encoding with which we wish to read the strings! The inspiration for this idea came from a [similar solution](https://github.com/scodec/scodec/blob/97e18b3f298397e670b7a99778eafdec76ea005e/unitTests/jvm/src/test/scala/scodec/examples/PcapExample.scala#L48)) of detecting byte ordering (endianness) in libpcap files.

The final codec looks like this:

```scala
import java.nio.charset.{Charset, StandardCharsets}

implicit val charsetCodec: Codec[Charset] = new Codec[Charset] {
  private val EbcdicEncoding = 0xF0F1.toShort // "01" in EBCDIC (IBM037)
  private val AsciiEncoding = 0x3031.toShort // "01" in ASCII (US_ASCII)

  override def sizeBound: SizeBound = SizeBound.exact(16)

  override def encode(charset: Charset): Attempt[BitVector] =
    string(charset).encode("01")

  override def decode(bits: BitVector): Attempt[DecodeResult[Charset]] =
    (ignore(32) ~> short16).decode(bits).flatMap {
      case DecodeResult(EbcdicEncoding, _) => Attempt.successful(DecodeResult(Charset.forName("IBM037"), bits))
      case DecodeResult(AsciiEncoding, _)  => Attempt.successful(DecodeResult(StandardCharsets.US_ASCII, bits))
      case DecodeResult(other, _) =>
        val hex = (other & 0xffff).toHexString.toUpperCase
        Attempt.failure(
          Err(s"Unable to detect the encoding using the values 0xF0F1 (EBCDIC) or 0x3031 (ASCII), found: 0x$hex")
        )
    }
}
```

This codec will now be passed implicitly to all other codecs requiring an implicit `Charset`, allowing us to decode the strings correctly for both encoding types!

#### Bonus: decoding a list of unknown length

In the most simplified form, the X9.37 protocol contains record sections, and each section contains a Header record, followed by several data records and a Control record containing checksums and other verification information. Here's an example in ASCII art form:

```
    ┌────────────────────────┬────────────────────────┐
    │                        │                        │
┌───┴────┐               ┌───┴───┐               ┌────┴───┐
│File    │               │┌──────┼┐              │File    │
│Header  │               ││Cash  ││              │Control │
│Record  │               ││Letter││              │Record  │
└────────┘               └┼──────┘│              └────────┘
                          └───────┘
```

Unfortunately, the protocol specifies neither in the Header nor Control records the actual number of these Cash Letter records, and all scodec combinators I found that deal with lists expect to take a number specifying the number of items to decode.

After a few iterations, I came up with the following function that tries to read a list of unknown size, and when it fails - returns the number of items it read so far:

```scala
/**
  * Decodes a list of unknown size, until the first failure, in which case returns the number of successful items.
  */
def tryList[A](codec: Codec[A]): Codec[List[A]] = new Codec[List[A]] {
  private val unboundedList = list(codec)

  override def sizeBound = unboundedList.sizeBound
  override def encode(list: List[A]) = unboundedList.encode(list)
  override def decode(buffer: BitVector) =
    unboundedList.decode(buffer) match {
      case s @ Attempt.Successful(_) => s
      case e @ Attempt.Failure(err) =>
        err.context match {
          case count :: _ => listOfN(provide(count.toInt), codec).decode(buffer)
          case _          => e
        }
    }
}
```

This did the job (and also got a thumbs up from Michael Pilquist, the creator of scodec, on the [scodec Discord](https://discord.gg/wKn3cpfRVz)!)

Finally, we can parse the X9.37 file using this top-level definition:

```scala
case class X937File(
  encoding: Charset,
  header: FileHeader,
  cashLetters: List[CashLetter],
  control: FileControl
)
object X937File {
  import scala.util.Using

  private val codec: Codec[X937File] =
    "X9.37 File"        | {
      ("Charset"        | Codec[Charset]).flatPrepend { implicit charset =>
      	("File Header"  | Codec[FileHeader]) ::
      	("Cash Letters" | tryList(Codec[CashLetter])) ::
      	("File Control" | Codec[FileControl])
      }
    }.as[X937File]

  def read(file: File): Either[Throwable, X937File] =
    Using(new FileInputStream(file))(read).toEither.flatten

  def read(in: InputStream): Either[Throwable, X937File] = {
    val bv = BitVector.fromInputStream(in)
    codec.decodeValue(bv).toTry.toEither
  }
```

Implementations of `FileHeader`, `CashLetter`, `FileControl` and others are left as an exercise to the reader 😄

Happy parsing!
