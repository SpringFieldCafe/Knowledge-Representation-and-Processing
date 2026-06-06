# （1）从neomodel包导入类
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config

# （2）连接Neo4j图形数据库。
config.DATABASE_URL = 'bolt://neo4j:12345678@localhost:7687'

# （3）编写节点类。
class Plant(StructuredNode):
    name = StringProperty(unique_index=True)
    has1 = RelationshipFrom('Tree', 'AKO')
    has2 = RelationshipFrom('Grass', 'AKO')
    have1 = RelationshipTo('Leaf', 'Have')
    have2 = RelationshipTo('Root', 'Have')


class Tree(StructuredNode):
    name = StringProperty(unique_index=True)
    ako = RelationshipTo('Plant', 'AKO')
    have = RelationshipFrom('Fruiter', 'AKO')


class Grass(StructuredNode):
    name = StringProperty(unique_index=True)
    ako = RelationshipTo('Plant', 'AKO')
    has = RelationshipFrom('Waterweeds', 'AKO')


class Leaf(StructuredNode):
    name = StringProperty(unique_index=True)
    have = RelationshipFrom('Plant', 'Have')


class Root(StructuredNode):
    name = StringProperty(unique_index=True)
    have = RelationshipFrom('Plant', 'Have')


class Waterweeds(StructuredNode):
    name = StringProperty(unique_index=True)
    ako = RelationshipTo('Grass', 'AKO')
    live = RelationshipTo('Water', 'Live')


class Water(StructuredNode):
    name = StringProperty(unique_index=True)
    have = RelationshipFrom('Waterweeds', 'Live')


class Fruiter(StructuredNode):
    name = StringProperty(unique_index=True)
    ako = RelationshipTo('Tree', 'AKO')
    can = RelationshipTo('Bear', 'Can')
    have = RelationshipFrom('Pear', 'AKO')


class Bear(StructuredNode):
    name = StringProperty(unique_index=True)
    have = RelationshipFrom('Fruiter', 'Can')


class Pear(StructuredNode):
    name = StringProperty(unique_index=True)
    ako = RelationshipTo('Fruiter', 'AKO')
    can = RelationshipTo('BearPear', 'Can')


class BearPear(StructuredNode):
    name = StringProperty(unique_index=True)
    have = RelationshipFrom('Pear', 'Can')


# （4）根据类生成实例。
plant = Plant(name="植物").save()
tree = Tree(name="树").save()
grass = Grass(name="草").save()
leaf = Leaf(name="叶").save()
root = Root(name="根").save()
waterweeds = Waterweeds(name="水草").save()
water = Water(name="水").save()
fruiter = Fruiter(name="果树").save()
bear = Bear(name="结果").save()
pear = Pear(name="梨树").save()
bearpear = BearPear(name="结梨").save()


# （5）创建实例之间的连接关系。
pear.ako.connect(fruiter)
pear.can.connect(bearpear)
fruiter.ako.connect(tree)
fruiter.can.connect(bear)
waterweeds.ako.connect(grass)
waterweeds.live.connect(water)
plant.have1.connect(leaf)
plant.have2.connect(root)
tree.ako.connect(plant)
grass.ako.connect(plant)