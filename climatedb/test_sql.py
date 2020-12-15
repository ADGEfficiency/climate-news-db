from climatedb.database import SQLiteDatabase, format_schema


schema = [
    ('url', 'TEXT'),
    ('id', 'INT')
]

data = [
    {'url': 'A', 'id': 1},
    {'url': 'A', 'id': 1},
    {'url': 'B', 'id': 0},
]

def test_add_get():
    db = SQLiteDatabase('test', schema=schema, db=':memory:')
    db.add(data)
    ds = db.get()
    assert ds == data

