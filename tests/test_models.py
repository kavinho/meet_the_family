import unittest
from family_tree import models

class TestModels(unittest.TestCase):

    def test_spouse(self):
        # arrange
        king1 = models.Node('K1')
        queen1 = models.Node('Q1', gender=models.Gender.Female)
        # act        
        king1.set_spouse(queen1)
        # assert
        self.assertEqual(queen1, king1.get_spouse())
        self.assertEqual(king1, queen1.get_spouse())

    def test_all_relationships(self):
        # arrange
        king1 = models.Node('K1')
        queen1 = models.Node('Q1', gender=models.Gender.Female)
        king1.set_spouse(queen1)
        # act
        son = models.Node('lucky')
        queen1.add_child(son)
        daugther = models.Node('lucia', gender=models.Gender.Female)
        queen1.add_child(daugther)
        # assert
        self.assertEqual([son, daugther], king1.get_children())
        self.assertEqual([son, daugther], queen1.get_children())
        self.assertEqual([daugther], queen1.get_children(gender=models.Gender.Female))

        self.assertEqual(queen1, son.get_mother())
        self.assertEqual(king1, son.get_father())
        self.assertEqual([daugther],son.get_siblings())
        self.assertEqual([daugther],son.get_siblings(gender=models.Gender.Female))
        self.assertEqual([],son.get_siblings(gender=models.Gender.Male))

