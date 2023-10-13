from dotenv import load_dotenv, dotenv_values
import peewee as pw
from playhouse.sqlite_ext import FTS5Model, SearchField, SqliteExtDatabase, SQL
import os

load_dotenv()
DATABASE = os.getenv("DB")
db = SqliteExtDatabase(DATABASE)
     
class SearchSiteData(FTS5Model):
    '''
    Virtual table with FTS5.
    '''
    # The `rowid` field is created automatically
    url = SearchField()
    content = SearchField()
    summary = SearchField()
    title = SearchField()
    tags = SearchField()

    class Meta:
        database = db
        options = {'tokenize': 'porter unicode61'}

    def to_json(self):
        return {
            "url": self.url,
            "title": self.title,
            "summary": self.summary,
            "tags": self.tags,
            "content": self.content
        }

