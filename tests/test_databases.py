from shutil import rmtree

from climatedb import databases
from climatedb.config import DBHOME

import pytest


@pytest.fixture()
def setup():
    rmtree(DBHOME / 'temp', ignore_errors=True)
    (DBHOME / 'temp').mkdir()
    yield
    rmtree(DBHOME / 'temp', ignore_errors=True)


def test_urls_db(setup):
    db = databases.URLs(name='temp/test.jsonl', engine='jsonl', key='url')

    payload = [
        {'url': 'http://1.html', 'time': '2020-01-01'},
        {'url': 'http://2.html', 'time': '2020-01-02'},
        {'url': 'http://3.html', 'time': '2020-01-03'},
    ]

    #  check we don't add duplicates
    db.add(payload)
    db.add(payload)
    data = db.get()
    assert len(data) == 3

    #  check we only get the last record back
    data = db.get(1)
    assert len(data) == 1
    assert data[0] == payload[-1]

    #  check we only get the last two back
    data = db.get(2)
    assert len(data) == 2
    assert data == payload[-2:]


def test_articles_folders():

    payload = [
        {'id': '1', 'time': '2020-01-01', 'html': '<div>1</div>'},
        {'id': '2', 'time': '2020-01-02', 'html': '<div>2</div>'},
        {'id': '3', 'time': '2020-01-03', 'html': '<div>3</div>'},
    ]

    db = databases.ArticlesFolders(
        'temp',
        folder_key='time',
        file_key='id'
    )

    #  add data
    db.add(payload)

    #  test we get everything back
    data = db.get()
    assert data == payload

    #  check we don't add duplicates
    db.add(payload)
    db.add(payload)
    data = db.get()
    assert len(data) == 3

    #  check we get the correct data back
    for d in payload:
        assert d['html'] == db.filter('id', d['id'])[0]['html']


def test_articles_sqlite():

    payload = [
        {'id': 1, 'time': '2020-01-01', 'html': '<div>1</div>'},
        {'id': 2, 'time': '2020-01-02', 'html': '<div>2</div>'},
        {'id': 3, 'time': '2020-01-03', 'html': '<div>3</div>'},
    ]

    schema = (('id', 'INT'), ('time', 'TEXT'), ('html', 'TEXT'))

    db = databases.ArticlesSQLite(db='temp', schema=schema, index='id')

    #  add data
    db.add(payload)

    #  test we get everything back
    data = db.get()
    assert data == payload

    #  check we don't add duplicates
    db.add(payload)
    db.add(payload)
    data = db.get()
    assert len(data) == 3

    #  check we get the correct data back
    for d in payload:
        assert d['html'] == db.filter('id', d['id'])[0]['html']
