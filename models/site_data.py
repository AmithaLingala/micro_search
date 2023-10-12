from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.ddl import DDLElement, DDL
from sqlalchemy.ext.compiler import compiles

db = SQLAlchemy()

class CreateFtsTable(DDLElement):
    """Represents a CREATE VIRTUAL TABLE ... USING fts5 statement, for indexing
    a given table.
    """

    def __init__(self, table, version=5):
        self.table = table
        self.version = version

@compiles(CreateFtsTable)
def compile_create_fts_table(element, compiler, **kw):
    tbl = element.table
    version = element.version
    preparer = compiler.preparer

    vtbl_name = preparer.quote(tbl.__table__.name + "_idx")

    columns = [x.name for x in tbl.__mapper__.columns]
    columns.append('tokenize="porter unicode61"')
    columns = ', '.join(columns)

    return f"CREATE VIRTUAL TABLE IF NOT EXISTS {vtbl_name} USING FTS{version} ({columns})"

SiteDataFts = None
def get_fts_references(target: db.Table, connection, **kwargs):
    base_model = next(c.entity for c in db.Model.registry.mappers if c.mapped_table.name == target.name)
    _temp_fts = db.Table(target.name+'_fts', db.metadata,
                         db.Column('url', db.Text(), key='url', primary_key=True),
                         db.Column('title', db.Text()),
                         db.Column('summary', db.Text()),
                         db.Column('tags', db.Text()),
                         db.Column('content', db.Text()))
    globals()[base_model.__name__+'Fts'] = db.aliased(globals()[base_model.__name__], _temp_fts, adapt_on_names=True)

class SiteData(db.Model):
    __tablename__ = 'site_data'
    url = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=True)
    summary = db.Column(db.String, nullable=True)
    tags = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)

update_fts = DDL('''CREATE TRIGGER site_data_update AFTER INSERT ON site_data
  BEGIN
    INSERT INTO site_data_idx (url, title, summary, tags, content) 
    VALUES (new.url, new.title, new.summary, new.tags, new.content);
  END;''')

db.event.listen(SiteData.__table__, 'after_create', CreateFtsTable(SiteData))
db.event.listen(SiteData.__table__, 'after_create', update_fts)
db.event.listen(SiteData.__table__, 'after_create', get_fts_references)

def __init__(self, url, title, summary, tags, content):
      self.url = url
      self.title = title
      self.summary = summary 
      self.tags = tags
      self.content = content
     
def json(self):
    return {
      "url": self.url,
      "title": self.title,
      "summary": self.summary, 
      "tags": self.tags, 
      "content": self.content    
      }