.. _getting-started:

Getting Started
---------------

The ``msvdd_Bloc`` project is focused, fundamentally, on representing résumés and
job postings as structured data. To that end, it includes functionality for

- defining and validating structured data for both résumés and job postings,
  based on general-purpose community standards
- fetching job postings data, including unstructured text, from external APIs
- extracting unstructured text data from PDF files (for résumés, but the process is general)
- cleaning and standardizing messy data, aka "data munging"
- segmenting résumé texts into lines and assigning them to separate sections,
  such as "education" or "work"
- splitting section lines into constituent words, turning those words into a set of
  numeric features, predicting which field of a given section each word belongs to,
  then parsing those predictions to produce structured data
- generating and augmenting fake-but-realistic data, as well as labeling real data,
  for training section-specific parsing models

Assuming all parsing models are trained and ready, a résumé PDF can be transformed into
structured data like so:

.. code-block:: pycon

    >>> import msvdd_bloc.resumes
    >>> resume_text = msvdd_bloc.resumes.extract_text_from_pdf("/path/to/resume.pdf")
    >>> resume_data = msvdd_bloc.resumes.parse_text(resume_text)

The underlying functionality powering this workflow is split into two main parts:
the ``msvdd_bloc/`` directory contains "lib" code, which is installable and importable
for use in a Python environment; and the ``scripts/`` directory contains executable code
with command line interfaces for common use cases, built upon corresponding lib code.

scripts
```````

- ``generate_job_postings_dataset.py``: Generate a job postings dataset. Fetch data
  from a specified API source matching query criteria, then save the deduplicated set
  of results to disk in a .json file.
- ``generate_resumes_dataset.py``: Generate a résumés dataset. From a directory of .pdf
  files, extract and clean up texts, then save the collection of .txt files to disk
  in a single, compressed .zip archive.
- ``label_training_dataset.py``: Label training examples for a given résumé section.
  Manually label each line of text according to a specified labeling scheme, then
  save the collection of labeled lines to disk in a .jsonl file.
- ``generate_fake_training_dataset.py``: Generate fake training examples for a given
  résumé section. Randomly generate and optionally augment a specified number of examples,
  then save the collection to disk in a .jsonl file.
- ``train_parser.py``: Train a CRF parser from labeled training data. Specify the model's
  configuration and the constraints on its training, then save the trained model to disk
  in a .crfsuite file.

``msvdd_bloc`` lib
``````````````````

- top-level modules:

  - ``about.py``: package metadata, primarily for use in installation
  - ``fileio.py``: functions for saving/loading data to disk in relevant formats, and for
    iterating over collections of such files
  - ``regexes.py``: variety of compiled regular expressions, for use in parsing and
    validating fields with a high degree of consistent structured
  - ``schemas.py``: schemas for defining and validating structured data representations
    of résumés and job postings
  - ``tokenize.py``: functionality for splitting text strings into constituent tokens
  - ``utils.py``: general-purpose utility functions, used as needed throughout the code

- ``job_postings/``: Basic functionality for fetching and munging job postings data.
  It is intended to be built upon, following the same general form (and possibly sharing
  some functionality) already implemented for résumés data.

  - ``fetch.py``: functions for fetching job postings from external API data sources,
    such as GitHub Jobs, Indeed.com, and The Muse
  - ``munge.py``: functions for cleaning and standardizing field keys and values from
    each data source to produce consistent structured outputs, regardless of the source

- ``resumes/``: Extensive functionality for representing résumés as structured data.
  It includes top-level modules for section-agnostic text extraction, data munging,
  section segmentation, fake data generation and augmentation, and parsing; plus
  consistently structured but section-specific subpackages for tailoring functionality
  to the particular needs of a section. For full details, check out :ref:`api-reference`
  and :ref:`api-reference-resumes`.

notebooks
`````````

Be sure to check out the interactive guide in `notebooks/getting-started.ipynb`.
It explains and demonstrates the above concepts in a way that's equal parts "show"
and "tell". There are also a bunch of other notebooks in there from DataDive participants,
but they're mostly scratch work and not particularly helpful in understanding the code
as it exists after so much subsequent development.
