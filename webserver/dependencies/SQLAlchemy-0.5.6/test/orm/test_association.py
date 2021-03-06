
from sqlalchemy.test import testing
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.test.schema import Table
from sqlalchemy.test.schema import Column
from sqlalchemy.orm import mapper, relation, create_session
from test.orm import _base
from sqlalchemy.test.testing import eq_


class AssociationTest(_base.MappedTest):
    run_setup_classes = 'once'
    run_setup_mappers = 'once'

    @classmethod
    def define_tables(cls, metadata):
        Table('items', metadata,
            Column('item_id', Integer, primary_key=True),
            Column('name', String(40)))
        Table('item_keywords', metadata,
            Column('item_id', Integer, ForeignKey('items.item_id')),
            Column('keyword_id', Integer, ForeignKey('keywords.keyword_id')),
            Column('data', String(40)))
        Table('keywords', metadata,
            Column('keyword_id', Integer, primary_key=True),
            Column('name', String(40)))

    @classmethod
    def setup_classes(cls):
        class Item(_base.BasicEntity):
            def __init__(self, name):
                self.name = name
            def __repr__(self):
                return "Item id=%d name=%s keywordassoc=%r" % (
                    self.item_id, self.name, self.keywords)

        class Keyword(_base.BasicEntity):
            def __init__(self, name):
                self.name = name
            def __repr__(self):
                return "Keyword id=%d name=%s" % (self.keyword_id, self.name)

        class KeywordAssociation(_base.BasicEntity):
            def __init__(self, keyword, data):
                self.keyword = keyword
                self.data = data
            def __repr__(self):
                return "KeywordAssociation itemid=%d keyword=%r data=%s" % (
                    self.item_id, self.keyword, self.data)

    @classmethod
    @testing.resolve_artifact_names
    def setup_mappers(cls):
        items, item_keywords, keywords = cls.tables.get_all(
            'items', 'item_keywords', 'keywords')

        mapper(Keyword, keywords)
        mapper(KeywordAssociation, item_keywords, properties={
            'keyword':relation(Keyword, lazy=False)},
               primary_key=[item_keywords.c.item_id, item_keywords.c.keyword_id],
               order_by=[item_keywords.c.data])

        mapper(Item, items, properties={
            'keywords' : relation(KeywordAssociation,
                                  cascade="all, delete-orphan")
        })

    @testing.resolve_artifact_names
    def test_insert(self):
        sess = create_session()
        item1 = Item('item1')
        item2 = Item('item2')
        item1.keywords.append(KeywordAssociation(Keyword('blue'), 'blue_assoc'))
        item1.keywords.append(KeywordAssociation(Keyword('red'), 'red_assoc'))
        item2.keywords.append(KeywordAssociation(Keyword('green'), 'green_assoc'))
        sess.add_all((item1, item2))
        sess.flush()
        saved = repr([item1, item2])
        sess.expunge_all()
        l = sess.query(Item).all()
        loaded = repr(l)
        eq_(saved, loaded)

    @testing.resolve_artifact_names
    def test_replace(self):
        sess = create_session()
        item1 = Item('item1')
        item1.keywords.append(KeywordAssociation(Keyword('blue'), 'blue_assoc'))
        item1.keywords.append(KeywordAssociation(Keyword('red'), 'red_assoc'))
        sess.add(item1)
        sess.flush()

        red_keyword = item1.keywords[1].keyword
        del item1.keywords[1]
        item1.keywords.append(KeywordAssociation(red_keyword, 'new_red_assoc'))
        sess.flush()
        saved = repr([item1])
        sess.expunge_all()
        l = sess.query(Item).all()
        loaded = repr(l)
        eq_(saved, loaded)

    @testing.resolve_artifact_names
    def test_modify(self):
        sess = create_session()
        item1 = Item('item1')
        item2 = Item('item2')
        item1.keywords.append(KeywordAssociation(Keyword('blue'), 'blue_assoc'))
        item1.keywords.append(KeywordAssociation(Keyword('red'), 'red_assoc'))
        item2.keywords.append(KeywordAssociation(Keyword('green'), 'green_assoc'))
        sess.add_all((item1, item2))
        sess.flush()

        red_keyword = item1.keywords[1].keyword
        del item1.keywords[0]
        del item1.keywords[0]
        purple_keyword = Keyword('purple')
        item1.keywords.append(KeywordAssociation(red_keyword, 'new_red_assoc'))
        item2.keywords.append(KeywordAssociation(purple_keyword, 'purple_item2_assoc'))
        item1.keywords.append(KeywordAssociation(purple_keyword, 'purple_item1_assoc'))
        item1.keywords.append(KeywordAssociation(Keyword('yellow'), 'yellow_assoc'))

        sess.flush()
        saved = repr([item1, item2])
        sess.expunge_all()
        l = sess.query(Item).all()
        loaded = repr(l)
        eq_(saved, loaded)

    @testing.resolve_artifact_names
    def test_delete(self):
        sess = create_session()
        item1 = Item('item1')
        item2 = Item('item2')
        item1.keywords.append(KeywordAssociation(Keyword('blue'), 'blue_assoc'))
        item1.keywords.append(KeywordAssociation(Keyword('red'), 'red_assoc'))
        item2.keywords.append(KeywordAssociation(Keyword('green'), 'green_assoc'))
        sess.add_all((item1, item2))
        sess.flush()
        eq_(item_keywords.count().scalar(), 3)

        sess.delete(item1)
        sess.delete(item2)
        sess.flush()
        eq_(item_keywords.count().scalar(), 0)


