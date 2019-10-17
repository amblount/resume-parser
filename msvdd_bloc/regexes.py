import re


RE_BULLETS = re.compile(
    r"[\u2022\u2023\u2043\u204C\u204D\u2219\u25CF\u25E6\u29BE\u29BF\u30fb]",
    flags=re.UNICODE,
)

RE_BREAKING_SPACE = re.compile(r"(\r\n|[\n\v])", flags=re.UNICODE)

RE_NONBREAKING_SPACE = re.compile(r"[^\S\n\v]", flags=re.UNICODE)

RE_LINE_DELIM = re.compile(r"(\s+[\u30fb|-]\s+)|( {3,})")

RE_NAME = re.compile(
    r"^(([(\"][A-Z]\w+[)\"]|[A-Z]\w+|[A-Z])[.,]?[ -]?){2,5}$",
    flags=re.UNICODE,
)

RE_MONTH = re.compile(
    r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\.?|(january|february|march|april|may|june|july|august|september|october|november|december)",
    flags=re.IGNORECASE
)

RE_YEAR = re.compile(r"((19|20)\d{2})")

RE_URL = re.compile(
    r"(?:^|(?<![\w/.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?://|ftp://|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.UNICODE | re.IGNORECASE,
)

RE_SHORT_URL = re.compile(
    r"(?:^|(?<![\w/.]))"
    # optional scheme
    r"(?:(?:https?://)?)"
    # domain
    r"(?:\w-?)*?\w+(?:\.[a-z]{2,12}){1,3}"
    r"/"
    # hash
    r"[^\s.,?!'\"|+]{2,12}"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.UNICODE | re.IGNORECASE,
)

RE_EMAIL = re.compile(
    r"(?:mailto:)?"
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}"
    r"(?:$|(?=\b))",
    flags=re.UNICODE | re.IGNORECASE,
)

RE_PHONE_NUMBER = re.compile(
    # core components of a phone number
    r"(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?(\d{3}[ .-]?\d{4})"
    # extensions, etc.
    r"(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W))",
    flags=re.UNICODE | re.IGNORECASE,
)

RE_USER_HANDLE = re.compile(
    r"(?:^|(?<![\w@.]))@\w+",
    flags=re.UNICODE | re.IGNORECASE,
)

RE_FULL_ADDRESS = re.compile(
    # r"[ \w]{3,}([A-Za-z]\.)?([ \w]*\#\d+)?,?[ \w]{3,}, [A-Za-z]{2} \d{5}(-\d{4})?",
    r"(\d+ ((?! \d+ ).)*?) [A-Za-z]{2} \d{5}(-\d{4})?",
    flags=re.UNICODE,
)

RE_POSTAL_CODE = re.compile(r"\d{5}(\-\d{4})?")
