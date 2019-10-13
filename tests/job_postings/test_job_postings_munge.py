import pytest

import msvdd_bloc


GITHUB_EXAMPLE = {
    'id': '1234567',
    'type': 'Full Time',
    'url': 'https://jobs.github.com/positions/1234567',
    'created_at': 'Sun Oct 13 14:59:07 UTC 2019',
    'company': 'Foo, Inc.',
    'company_url': 'https://www.foo.com/',
    'location': 'Chicago, IL',
    'title': 'Data Scientist',
    'description': '<p>Fake company with fake data seeks <strong>fake data scientist</strong> for fake hacks.</p>\n\n<p>Your fake new career opportunity awaits!</p>',
    'how_to_apply': '<p>Apply Online: <a href="https://www.foo.com/jobs/fake">https://www.foo.com/jobs/fake</a></p>\n',
    'company_logo': 'https://jobs.github.com/rails/active_storage/blobs/foo.jpg',
}

INDEED_EXAMPLE = {
    'jobtitle': 'Data Scientist',
    'company': 'Foo, Inc.',
    'city': 'Chicago',
    'state': 'IL',
    'country': 'US',
    'language': 'en',
    'formattedLocation': 'Chicago, IL',
    'source': 'Indeed',
    'date': 'Sun Oct 13 14:59:07 2019',
    'snippet': 'Fake company with fake data seeks fake data scientist for fake hacks.\n\nYour fake new career opportunity awaits!',
    'url': 'http://www.indeed.com/rc/clk?jk=1234567&atk=',
    'onmousedown': "indeed_clk(this,'');",
    'latitude': 41.970180,
    'longitude': -87.660400,
    'jobkey': '1234567',
    'sponsored': False,
    'expired': False,
    'indeedApply': True,
    'formattedLocationFull': 'Chicago, IL 60640',
    'formattedRelativeTime': '2 days ago',
    'stations': '',
    'recommendations': [],
}

THEMUSE_EXAMPLE = {
    'contents': '<p><span>Fake company with fake data seeks <strong>fake data scientist</strong> for fake hacks.\xa0</span></p>\n\n<p><span>Your fake new career opportunity awaits!</span></p>',
    'name': 'Data Scientist',
    'type': 'external',
    'publication_date': '2019-10-13T14:59:07.708280Z',
    'short_name': 'data-scientist',
    'model_type': 'jobs',
    'id': 1234567,
    'locations': [{'name': 'Chicago, IL'}],
    'categories': [{'name': 'Data Science'}],
    'levels': [],
    'tags': [],
    'refs': {'landing_page': 'https://www.themuse.com/jobs/foo/data-scientist'},
    'company': {'id': 12345, 'short_name': 'foo', 'name': 'Foo, Inc.'},
}


@pytest.fixture(scope="module")
def schema():
    return msvdd_bloc.schemas.JobPostingSchema()


class TestGithub:

    def test_munge_job_posting(self, schema):
        result = msvdd_bloc.job_postings.munge_job_posting_github(GITHUB_EXAMPLE)
        assert isinstance(result, dict)
        assert not schema.validate(result)

    def test_munge_job_posting_empty(self, schema):
        result = msvdd_bloc.job_postings.munge_job_posting_github({})
        assert isinstance(result, dict)
        validation_errors = schema.validate(result)
        assert isinstance(validation_errors, dict)
        assert len(validation_errors) > 0


class TestIndeed:

    def test_munge_job_posting(self, schema):
        result = msvdd_bloc.job_postings.munge_job_posting_indeed(INDEED_EXAMPLE)
        assert isinstance(result, dict)
        assert not schema.validate(result)

    def test_munge_job_posting_empty(self, schema):
        result = msvdd_bloc.job_postings.munge_job_posting_indeed({})
        assert isinstance(result, dict)
        validation_errors = schema.validate(result)
        assert isinstance(validation_errors, dict)
        assert len(validation_errors) > 0


class TestTheMuse:

    def test_munge_job_posting(self, schema):
        result = msvdd_bloc.job_postings.munge_job_posting_themuse(THEMUSE_EXAMPLE)
        assert isinstance(result, dict)
        assert not schema.validate(result)

    def test_munge_job_posting_empty(self, schema):
        result = msvdd_bloc.job_postings.munge_job_posting_themuse({})
        assert isinstance(result, dict)
        validation_errors = schema.validate(result)
        assert isinstance(validation_errors, dict)
        assert len(validation_errors) > 0
