"""
extract
-------

Extract résumé text from a PDF file, using multiple methods applied in order of confidence.
"""
import io


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
    funcs = (
        extract_text_from_pdf_tika,
        extract_text_from_pdf_pdfminer,
        extract_text_from_pdf_textract,
    )
    for func in funcs:
        _text = func(filepath)
        if len(_text) >= min_len:
            text = _text
            break
    return text


def extract_text_from_pdf_tika(filepath):
    """
    Extract text from a PDF at ``filepath`` using ``python-tika``.

    Args:
        filepath (str)

    Returns:
        str
    """
    # hiding the import so folks don't have to worry about installing it
    # pip install tika
    from tika import parser

    result = parser.from_file(filepath)
    return result["content"].strip()


def extract_text_from_pdf_pdfminer(filepath):
    """
    Extract text from a PDF at ``filepath`` using ``yapdfminer``.

    Args:
        filepath (str)

    Returns:
        str
    """
    # hiding the yapdfminer import so folks don't have to worry about installing it
    # note: this is a fork of pdfminer3, which is a fork of pdfminer.six, which is a fork of pdfminer
    # pip install yapdfminer
    import pdfminer.converter
    import pdfminer.layout
    import pdfminer.pdfinterp
    import pdfminer.pdfpage

    laparams = pdfminer.layout.LAParams(
        line_overlap=0.5,
        char_margin=2.0,
        word_margin=0.1,
        line_margin=0.5,
        boxes_flow=0.5,
        all_texts=False,
    )
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


def extract_text_from_pdf_textract(filepath):
    """
    Extract text from a PDF at ``filepath`` using ``textract`` + ``pdftotext``.

    Args:
        filepath (str)

    Returns:
        str
    """
    # hiding the import so folks don't have to worry about installing it
    # https://textract.readthedocs.io/en/stable/installation.html
    import textract

    return textract.process(
        filepath, method="pdftotext", encoding="utf-8"
    ).decode("utf-8").strip()
