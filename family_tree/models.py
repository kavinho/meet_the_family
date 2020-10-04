from enum import Enum
import operator

class AddChildException(Exception):
    pass

class PersonNotFoundException(Exception):
    pass

class Gender(Enum):
    def not_(self):
        return Gender(int(not bool(self.value)))
    Male=1
    Female=0

class EdgeType(Enum):
    """
    Represents type of basic relationship between to people.
    """
    Child='child'
    Spouse='spouse'

class Node(object):
    """
    Represents person's basic relationship with others.
    Did not add create_node here , then would have lost quick access to node by name
    """
    def __init__(self, name, gender=Gender.Male):
        self.name = name
        self.gender = gender
        self.edges = []
   
    def set_spouse(self, spouse):

        edge = Edge(EdgeType.Spouse)
        # putting this restrcition, eliminates many 'if's later
        if self.gender == Gender.Male:    
            edge.start_node = self
            edge.end_node = spouse

        else:
            edge.start_node = spouse
            edge.end_node = self
        
        self.edges.append(edge)
        spouse.edges.append(edge)

        return edge

    def add_child(self, child):
        if self.gender == Gender.Female:
            edge = Edge(EdgeType.Child)
            edge.start_node = self
            edge.end_node = child
            self.edges.append(edge)
            child.edges.append(edge)

            return edge
        else:   
            raise AddChildException('CHILD_ADDITION_FAILED')

    def get_spouse(self):

        for edge in self.edges:
            if edge.edge_type == EdgeType.Spouse:
                # return the other end
                return edge.end_node if edge.start_node == self else edge.start_node
        return None
           
    def get_mother(self):

        for edge in self.edges:
            if edge.edge_type == EdgeType.Child and edge.end_node == self:
                return edge.start_node

        return None

    def get_father(self):
        mom = None
        for edge in self.edges:
            if edge.edge_type == EdgeType.Child and edge.end_node == self:
                mom = edge.start_node
                break
        if mom:
            return mom.get_spouse()        
        return None

    def get_children(self, gender=None):
        result = []
        if self.gender == Gender.Male:
            node = self.get_spouse()        
        else:
            node = self

        for edge in node.edges:
            if (edge.edge_type == EdgeType.Child and edge.start_node == node) and \
               ((edge.end_node.gender == gender) or (gender is None)):

                result.append(edge.end_node)
        
        return result

    def get_siblings(self, gender=None):
        mom = self.get_mother()
       
        if mom is None:
            return []
       
        children = mom.get_children(gender=gender)
        return [ch for ch in children if ch != self]

class Edge(object):
    """
    Represents actual basic relationship between to people.
    """

    def __init__(self, edge_type, start_node=None, end_node=None):
        self.edge_type = edge_type
        self.start_node = start_node # parent or king
        self.end_node = end_node     # child or queen

