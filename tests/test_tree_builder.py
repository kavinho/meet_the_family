import unittest
from family_tree.tree_builder import TreeBuilder


class TestTreeBuilder (unittest.TestCase):
    def test_one_node(self):
        king_name = "Jonnhy"
        trb = TreeBuilder(king_name)
        self.assertEqual(king_name, trb.king.name, "could not build one node tree")

    def test_couple_nodes(self):
        
        trb = TreeBuilder()
        relationhip = trb.king.edges[0]

        self.assertEqual(trb.king, relationhip.start_node)
        self.assertEqual(trb.queen, relationhip.end_node)

    def test_add_child(self):
        
        trb = TreeBuilder('_',"queen")
        son = trb.create_node("Bill")
        relationship = trb.add_child(trb.queen, son)
        self.assertEqual(trb.queen, relationship.start_node)
        self.assertEqual(son, relationship.end_node)
