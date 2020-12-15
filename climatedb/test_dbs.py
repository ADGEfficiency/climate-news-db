from shutil import rmtree

from climatedb.database import File, Folder


newspapers = [
    {
        'body': 'I am an article.',
        'article_url': 'other-article.html',
        'article_id': 1,
        'newspaper_id': 'a',
        'search_time_UTC': '2020-01-01T00:05:00',
    },
    {
        'body': 'I am an article.',
        'article_url': 'other-article.html',
        'article_id': 2,
        'newspaper_id': 'b',
        'search_time_UTC': '2020-01-01T00:15:00',
    }
]


def test_files_db():
    fi = File("test.data")
    payload = ['line1', 'line2', 'line3']
    fi.add(payload)
    data = fi.get(2)
    assert data == payload[1:]
    fi.data.unlink()


newspapers = [
    {'fldr': 'A', 'fi': 0},
    {'fldr': 'A', 'fi': 1},
    {'fldr': 'B', 'fi': 0}
]


def test_folders_db():
    db = Folder(
        'test/articles',
        folder_key='fldr',
        file_key='fi'
    )

    db.add(newspapers)
    a = db.get('A')
    assert len(a) == 2

    b = db.get('B')
    assert len(b) == 1
    rmtree(db.name)
