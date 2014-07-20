from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, create_engine
from sqlalchemy.orm import sessionmaker, aliased, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Node(Base):
    __tablename__ = 'node'
    nid = Column(Integer, primary_key=True)
    uuid = Column(String(128))
    vid = Column(Integer)
    type = Column(String)

    # Refferer.
    field_data = relationship('NodeFieldData', backref='node')
    node__field_article = relationship('ArticleField', backref="node", foreign_keys='ArticleField.entity_id')
    node__field_image = relationship('ImageField', backref="node", foreign_keys='ImageField.entity_id')

    def __repr__(self):
        return "<Node(nid='%s', uuid='%s', vid='%s', type='%s')>" % (self.nid, self.uuid, self.vid, self.type)

class NodeFieldData(Base):
    __tablename__ = 'node_field_data'
    __table_args__ = (
        ForeignKeyConstraint(
          ['nid'],
          [Node.nid]
        ),
        PrimaryKeyConstraint('nid', 'langcode', name='nid_langcode')
    )
    nid = Column(Integer)
    vid = Column(Integer)
    langcode = Column(String(2))
    default_langcode = Column(Boolean)
    title = Column(String)
    uid = Column(Integer)
    status = Column(Boolean)
    created = Column(Integer)
    changed = Column(Integer)
    promote = Column(Boolean)
    sticky = Column(Boolean)

    def __repr__(self):
        return "<Node(nid='%s', lancode='%s', default_langcode='%s', title='%s', uid='%s', status='%s', created='%s', changed='%s', promote='%s', sticky='%s')>" %\
               (self.nid, self.langcode, self.default_langcode, self.title, self.uid, self.status, self.created, self.changed, self.promote, self.sticky)

class ArticleField(Base):
    __tablename__ = 'node__field_article'
    __table_args__ = (
        ForeignKeyConstraint(
          ['entity_id'],
          [Node.nid],
        ),
        ForeignKeyConstraint(
          ['field_article_target_id'],
          [Node.nid]
        ),
        PrimaryKeyConstraint('entity_id', 'langcode', name='entity_id_langcode')
    )
    bundle = Column(String)
    deleted = Column(Boolean)
    entity_id = Column(Integer)
    revision_id = Column(Integer)
    langcode = Column(String(2))
    delta = Column(Integer)

    field_article_target_id = Column(Integer)
    field_article_revision_id = Column(Integer)

    entity = relationship('Node', foreign_keys=[field_article_target_id],  backref='entity')

    def __repr__(self):
        return "<Node(bundle='%s', deleted='%s', entity_id='%s', revision_id='%s', langcode='%s', delta='%s', target_id='%s', revision_id='%s')>" %\
               (self.bundle, self.deleted, self.entity_id, self.revision_id, self.langcode, self.delta, self.field_article_target_id, self.field_article_revision_id)


class ImageField(Base):
    __tablename__ = 'node__field_image'
    __table_args__ = (
        ForeignKeyConstraint(
          ['entity_id'],
          [Node.nid],
        ),
        PrimaryKeyConstraint('entity_id', 'langcode', 'delta', name='entity_id_langcode_delta')
    )
    bundle = Column(String)
    deleted = Column(Boolean)
    entity_id = Column(Integer)
    revision_id = Column(Integer)
    langcode = Column(String(2))
    delta = Column(Integer)

    field_image_target_id = Column(Integer)
    field_image_alt = Column(String)
    field_image_title = Column(String)

    file = relationship('File', backref='field', uselist=False)

    def __repr__(self):
        return "{ bundle:'%s', deleted:'%s', entity_id:'%s', revision_id:'%s', langcode:'%s', delta:'%s', field_image_target_id:'%s', field_image_title:'%s', field_image_alt:'%s'}" %\
               (self.bundle, self.deleted, self.entity_id, self.revision_id, self.langcode, self.delta, self.field_image_target_id, self.field_image_title, self.field_image_alt)

class File(Base):
    __tablename__ = 'file_managed'
    __table_args__ = (
        ForeignKeyConstraint(
          ['fid'],
          [ImageField.field_image_target_id]
        ),
        PrimaryKeyConstraint('fid', 'langcode', name='fid_langcode')
    )
    fid = Column(Integer)
    uuid = Column(String(128))
    uid = Column(Integer)
    filename = Column(String)
    langcode = Column(String(2))
    uri = Column(String)
    filemime = Column(String)
    filesize = Column(Integer)
    status = Column(Boolean)
    timestamp = Column(Integer)

    def __repr__(self):
        return "<Node(fid='%s', uuid='%s', uid='%s', filename='%s', langcode='%s', uri='%s', filemime='%s', filesize='%s', status='%s', timestamp='%s')>" %\
               (self.fid, self.uuid, self.uid, self.filename, self.langcode, self.uri, self.filemime, self.filesize, self.status, self.timestamp)
