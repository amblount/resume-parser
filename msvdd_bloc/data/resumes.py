import io
import re

import ftfy
from faker import Faker


RE_NAME = re.compile(r"^(([(\"][A-Z]\w+[)\"]|[A-Z]\w+|[A-Z])[.,]?[ -]?){2,5}$", flags=re.UNICODE)
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
RE_STREET_ADDRESS = re.compile(
    # r"[ \w]{3,}([A-Za-z]\.)?([ \w]*\#\d+)?,?[ \w]{3,}, [A-Za-z]{2} \d{5}(-\d{4})?",
    r"(\d+ ((?! \d+ ).)*?) [A-Za-z]{2} \d{5}(-\d{4})?",
    flags=re.UNICODE,
)


def extract_text_from_pdf(filepath, *, min_len=150):
    """
    Extract text from a PDF at ``filepath`` using the first package
    to get the job done in extracting at least ``min_len`` chars.

    Args:
        filepath (str)
        min_len (int)

    Returns:
        str
    """
    text = ""
    funcs = (extract_text_tika, extract_text_pdfminer, extract_text_textract)
    for func in funcs:
        _text = func(filepath)
        if len(_text) >= min_len:
            text = _text
            break
    return text


def extract_text_textract(filepath):
    """
    Extract text from a PDF at ``filepath`` using ``textract`` + ``pdftotext``.

    Args:
        filepath (str)

    Returns:
        str
    """
    # hiding the import so folks don't have to worry about installing it
    import textract

    return textract.process(
        filepath, method="pdftotext", encoding="utf-8"
    ).decode("utf-8").strip()


def extract_text_pdfminer(filepath):
    """
    Extract text from a PDF at ``filepath`` using ``yapdfminer``.

    Args:
        filepath (str)

    Returns:
        str
    """
    # hiding the import so folks don't have to worry about installing it
    import pdfminer.converter
    import pdfminer.layout
    import pdfminer.pdfinterp
    import pdfminer.pdfpage

    laparams = pdfminer.layout.LAParams(boxes_flow=0.5)
    retstr = io.StringIO()
    rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
    device = pdfminer.converter.TextConverter(
        rsrcmgr, retstr, codec="utf-8", laparams=laparams)
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)
    fp = io.open(filepath, mode="rb")
    for page in pdfminer.pdfpage.PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text.strip()


def extract_text_tika(filepath):
    """
    Extract text from a PDF at ``filepath`` using ``python-tika``.

    Args:
        filepath (str)

    Returns:
        str
    """
    # hiding the import so folks don't have to worry about installing it
    from tika import parser

    result = parser.from_file(filepath)
    return result["content"].strip()


def clean_fellows_text(text):
    """
    Correct any encoding / mojibake / unicode weirdness, and remove
    superfluous numbering at the end of the résumé.

    Args:
        text (str)

    Returns:
        str
    """
    text = ftfy.fix_text(text)
    text = re.sub(r"\s+\d+\s*?$", "", text)
    return text


def clean_bonus_text(text):
    """
    Correct any encoding / mojibake / unicode weirdness, and remove
    superfluous "resumes (in)" lines at the end of the résumé.

    Args:
        text (str)

    Returns:
        str
    """
    text = ftfy.fix_text(text)
    text = re.sub(r"([\w]+ ?){1,3}resumes( in ([\w,]+ ?){1,3})?\n", "", text)
    return text


def replace_pii(text, *, faker=None):
    """
    Replace personally-identifying information in ``text``
    with randomly generated fake equivalents.

    Args:
        text (str)
        faker (:class:`Faker`)

    Returns:
        str
    """
    if faker is None:
        faker = Faker(locale="en_US")
    # let's start with names, which are usually on the first line
    first_line, *the_rest = text.split("\n", maxsplit=1)
    first_line = RE_NAME.sub(faker.name(), first_line.strip())
    text = "\n".join([first_line] + the_rest)
    # next, let's replace emails, urls, and addresses
    # which are usually in the first "chunk" of info
    # first_chunk, *the_rest = re.split(r"\n{2,}", text, maxsplit=1)
    first_chunk = text[:150]
    the_rest = text[150:]
    first_chunk = RE_PHONE_NUMBER.sub(faker.phone_number(), first_chunk)
    first_chunk = RE_EMAIL.sub(faker.email(), first_chunk)
    first_chunk = RE_URL.sub(faker.url(), first_chunk)
    first_chunk = RE_STREET_ADDRESS.sub(faker.address().replace("\n", " "), first_chunk)
    text = first_chunk + the_rest
    return text
