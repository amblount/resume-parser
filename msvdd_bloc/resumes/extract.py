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
