## DATA

Getting started:

1. Make two directories: `postings` and `resumes`
2. Go to the project OneDrive folder, and download the files therein
   - `github_jobs.json`, `indeed_jobs.json`, and `themuse_jobs.json` go into `postings`
   - `fellows_resumes.zip` and `bonus_resumes.zip` go into `resumes`
3. Unzip the two zip files to access the resume datasets as a collection of text files (if you prefer direct file-system access to the data)

If you create derivative datasets, add them to a `processed` sub-directory with descriptive filenames. If you have to bring in data from third-party sources, add them to an `external` sub-directory. Be sure to document their contents below!

Contents:

- résumés
    - `resumes/fellows_resumes.zip`: ~125 text files in a zip archive containing résumé texts extracted from PDFs created by Bloc Fellows
    - `resumes/bonus_resumes.zip`: ~2400 text files in a zip archive containing résumé texts acquired by Amina through _as-yet mysterious means_
- job postings
    - `postings/github_jobs.json`: ~70 job postings for tech+data roles in several major U.S. cities pulled from the GitHub jobs API, with metadata and full text of the job descriptions
    - `postings/indeed_jobs.json`: ~4200 job postings for tech+data roles in several major U.S. cities pulled from the indeed.com API, with metadata and short text snippets of the job descriptions
    - `postings/themuse_jobs.json`: ~570 job postings for tech+data roles in several major U.S. cities pulled from the themuse.com API, with metadata and full text of the job descriptions
