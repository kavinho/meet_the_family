from . import models

class TreeBuilder(object):
    """
    Faciliates building a family tree.
    Important data are king, queen, and the name_node_map for quick access.
    """
    def __init__(self, king_name='Arthur', queen_name='Margret'):
        # enables quick access for name to node. given names are unique.        
        self.name_node_map = {}
        self.king = None
        self.queen = None
        if king_name:
            self.king = self.create_node(king_name)

        if queen_name:
            self.queen = self.create_node(queen_name, models.Gender.Female) 
        if self.king and self.queen:            
            self.king.set_spouse(self.queen) 

    def set_spouce(self, man, woman):
        """ node, node"""
        man.set_spouse(woman)

    def create_node(self, name, gender = models.Gender.Male):
        node = models.Node(name, gender)
        self.name_node_map[name] = node
        return node

    def get_node(self, name):
        return self.name_node_map.get(name, None)

    def add_child(self, mother , child):
        if mother:
            return mother.add_child(child)
        else:
            raise models.AddChildException('PERSON_NOT_FOUND')