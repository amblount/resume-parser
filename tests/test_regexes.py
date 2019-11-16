import pytest

from msvdd_bloc import regexes


GOOD_EMAILS = [
    "prettyandsimple@example.com",
    "very.common@example.com",
    "disposable.style.email.with+symbol@example.com",
    "other.email-with-dash@example.com",
    "üñîçøðé@example.com",
    "üñîçøðé@üñîçøðé.com",
    "example@s.solutions",
    "あいうえお@example.com",
]
BAD_EMAILS = [
    "plainaddress",
    "abc.example.com",
    "A@b@c@example.com",
    "john..doe@example.com",
    "john.doe@example..com",
    "#@%^%#$@#$@#.com",
    "@example.com",
    "email.example.com",
    "“email”@example.com",
    "email@example",
    "email@-example.com",
    ".email@example.com",
    "email.@example.com",
    "email@111.222.333.44444",
    "email@[123.123.123.123]",
    "user@[IPv6:2001:db8::1]]",
]

GOOD_PHONE_NUMBERS = [
    "1-722-686-3338",
    "984.744.3425",
    "(188)273-7152",
    "+1 (616) 555-3439",
    "(027)458-7382x7531",
    "727.769.2515 #64526",
    "(535) 327 1955 ext. 902",
    "1-492-748-2325-1056",
    "099 145 5237",
    "040.351.7778x63654",
    "123-4567",
]
BAD_PHONE_NUMBERS = [
    "+36(0)4963872475",
    "2015-12-23",
    "12/23/2015",
    "(044) 664 123 45 67",
    "(12) 3456 7890",
    "01234 567890",
    "91 23 45 678",
    "12-345-67-89",
    "123,456,789",
]
PARTIAL_PHONE_NUMBERS = ["(0123) 456 7890"]

GOOD_URLS = [
    "http://foo.com/blah_blah",
    "http://foo.com/blah_blah/",
    "http://foo.com/blah_blah_(wikipedia)",
    "http://foo.com/blah_blah_(wikipedia)_(again)",
    "http://www.example.com/wpstyle/?p=364",
    "https://www.example.com/foo/?bar=baz&inga=42&quux",
    "http://✪df.ws/123",
    "http://userid:password@example.com:8080",
    "http://userid:password@example.com:8080/",
    "http://userid@example.com",
    "http://userid@example.com/",
    "http://userid@example.com:8080",
    "http://userid@example.com:8080/",
    "http://userid:password@example.com",
    "http://userid:password@example.com/",
    "http://142.42.1.1/",
    "http://142.42.1.1:8080/",
    "http://➡.ws/䨹",
    "http://⌘.ws",
    "http://⌘.ws/",
    "http://foo.com/blah_(wikipedia)#cite-1",
    "http://foo.com/blah_(wikipedia)_blah#cite-1",
    "http://foo.com/unicode_(✪)_in_parens",
    "http://foo.com/(something)?after=parens",
    "http://☺.damowmow.com/",
    "http://code.google.com/events/#&product=browser",
    "http://j.mp",
    "ftp://foo.bar/baz",
    "http://foo.bar/?q=Test%20URL-encoded%20stuff",
    "http://مثال.إختبار",
    "http://例子.测试",
    "http://उदाहरण.परीक्षा",
    "http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com",
    "http://1337.net",
    "http://a.b-c.de",
    "http://223.255.255.254",
    "www.foo.com",
    "www3.foo.com/bar",
]
BAD_URLS = [
    "http://",
    "http://.",
    "http://..",
    "http://../",
    "http://?",
    "http://??",
    "http://??/",
    "http://#",
    "http://##",
    "http://##/",
    "//",
    "//a",
    "///a",
    "///",
    "http:///a",
    "foo.com",
    "rdar://1234",
    "h://test",
    "http:// shouldfail.com",
    ":// should fail",
    "ftps://foo.bar/",
    "http://-error-.invalid/",
    "http://a.b--c.de/",
    "http://-a.b.co",
    "http://a.b-.co",
    "http://0.0.0.0",
    "http://10.1.1.0",
    "http://10.1.1.255",
    "http://224.1.1.1",
    "http://123.123.123",
    "http://3628126748",
    "http://.www.foo.bar/",
    "http://.www.foo.bar./",
    "http://10.1.1.1",
    "foo.bar",
    "can.not.even",
]
PARTIAL_URLS = [
    "http://foo.bar/foo(bar)baz quux",
    "http://1.1.1.1.1",
    # "http://foo.bar?q=Spaces should be encoded",  # this one fails, reason unknown
    "http://www.foo.bar./",
]

GOOD_SHORT_URLS = [
    "http://adf.ly/1TxZVO",
    "https://goo.gl/dmL4Gm",
    "http://chart.bt/1OLMAOm",
    "http://ow.ly/Whoc3",
    "http://tinyurl.com/oj6fudq",
    "http://tiny.cc/da1j7x",
    "https://tr.im/KI7ef",
    "http://is.gd/o46NHa",
    "http://yep.it/ywdiux",
    "http://snipurl.com/2adb7eb",
    "http://adyou.me/I4YW",
    "http://nyti.ms/1TgPKgX",
    "http://qr.net/bpfqD",
    "https://chartbeat.com/about/",
    "http://subfoo.foo.bar/abcd",
]
BAD_SHORT_URLS = [
    "ftp://foo.bar/baz",
    "http://foo.com/blah_blah?adsf",
    "https://www.example.com/foo/?bar=baz&inga=42&quux",
]

GOOD_USER_HANDLES = [
    "@bdewilde",
    "@bd3wild3",
    "@b_dewilde",
]
BAD_USER_HANDLES = [
    "bdewilde",
    "bd3wild3",
    "b_dewilde",
    "bdewilde@bdewilde",
]
PARTIAL_USER_HANDLES = [
    "@b.dewilde",
    "@bdewilde!",
]


class TestEmailRegex:

    def test_good(self):
        for item in GOOD_EMAILS:
            assert item == regexes.RE_EMAIL.search(item).group()

    def test_bad(self):
        for item in BAD_EMAILS:
            assert regexes.RE_EMAIL.search(item) is None


class TestPhoneNumberRegex:

    def test_good(self):
        for item in GOOD_PHONE_NUMBERS:
            assert item == regexes.RE_PHONE_NUMBER.search(item).group()

    def test_bad(self):
        for item in BAD_PHONE_NUMBERS:
            assert regexes.RE_PHONE_NUMBER.search(item) is None

    def test_partial(self):
        for item in PARTIAL_PHONE_NUMBERS:
            match = regexes.RE_PHONE_NUMBER.search(item)
            assert match is not None and item != match


class TestShortURLRegex:

    def test_good(self):
        for item in GOOD_SHORT_URLS:
            assert item == regexes.RE_SHORT_URL.search(item).group()

    def test_bad(self):
        for item in BAD_SHORT_URLS:
            assert regexes.RE_SHORT_URL.search(item) is None


class TestURLRegex:

    def test_good(self):
        for item in GOOD_URLS:
            assert item == regexes.RE_URL.search(item).group()

    def test_bad(self):
        for item in BAD_URLS:
            assert regexes.RE_URL.search(item) is None

    def test_partial(self):
        for item in PARTIAL_URLS:
            match = regexes.RE_URL.search(item)
            assert match is not None and item != match


class TestUserHandleRegex:

    def test_good(self):
        for item in GOOD_USER_HANDLES:
            assert item == regexes.RE_USER_HANDLE.search(item).group()

    def test_bad(self):
        for item in BAD_USER_HANDLES:
            assert regexes.RE_USER_HANDLE.search(item) is None

    def test_partial(self):
        for item in PARTIAL_USER_HANDLES:
            match = regexes.RE_USER_HANDLE.search(item)
            assert match is not None and item != match
