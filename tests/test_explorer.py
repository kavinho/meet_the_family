import unittest
from family_tree import models, explorer, tree_builder

class TestExplorer(unittest.TestCase):

    def get_basic_family(self):

        # king + queen
        # [son1, son2, daugther1,daugther2]     

        king_name = 'K_J'
        queen_name = 'Q_J'
        tr_b = tree_builder.TreeBuilder(king_name, queen_name)
        queen = tr_b.queen
        son = tr_b.create_node('KQ_Son1')
        queen.add_child(son)

        son = tr_b.create_node('KQ_Son2')
        queen.add_child(son)

        daugther = tr_b.create_node('KQ_Da1',gender=models.Gender.Female)
        queen.add_child(daugther)

        daugther = tr_b.create_node('KQ_Da2',gender=models.Gender.Female)
        queen.add_child(daugther)

        return tr_b

    def get_family_with_unlces_aunts(self):
        # old queen1 ,        old queen 2
        #   |-------------|         |------------|
        # [queen10,     king10]  [queen20,    king20]
        #                 |___________|    
        #                       |
        #                   [daugther30]     

        # Dynasty 1
        tr_b = tree_builder.TreeBuilder("_", 'old_q_1')

        queen = tr_b.queen
        ch = tr_b.create_node('king10')
        queen.add_child(ch)

        ch = tr_b.create_node('queen10', gender=models.Gender.Female)
        queen.add_child(ch)
        #
        # Dynasty 2

        queen = tr_b.create_node('old_q_2', gender=models.Gender.Female)
        ch = tr_b.create_node('king20')
        queen.add_child(ch)
        ch = tr_b.create_node('queen20', gender=models.Gender.Female)
        queen.add_child(ch)

        # marriage to strengthen bonds
        king = tr_b.get_node('king10')
        queen = tr_b.get_node('queen20')
        king.set_spouse(queen)

        # there we go
        daugther = tr_b.create_node('da30')
        queen.add_child(daugther)

        return tr_b

    def test_immediate_family(self):

        # Arrange
        tr_b = self.get_basic_family()
        rel = explorer.RelationshipExplorer(tr_b)

        # action 
        sons = rel.explore(rel.builder.queen.name,"Son")
        daugthers = rel.explore(rel.builder.queen.name,"Daughter")
        siblings = rel.explore('KQ_Son2',"Siblings")
        # Assert
        self.assertEqual(['KQ_Son1', 'KQ_Son2'], [s.name for s in sons])
        self.assertEqual(['KQ_Da1', 'KQ_Da2'], [s.name for s in daugthers])       
        self.assertEqual(['KQ_Son1', 'KQ_Da1','KQ_Da2'], [s.name for s in siblings])        

    def test_unlces_aunts(self):

        # arrange
        tr_b = self.get_family_with_unlces_aunts()
        rel = explorer.RelationshipExplorer(tr_b)

        # action 
        maternal_uncles = rel.explore('da30', "Maternal-Uncle")
        maternal_aunts = rel.explore('da30', "Maternal-Aunt")
        paternal_uncles = rel.explore('da30', "Paternal-Uncle")
        paternal_aunts = rel.explore('da30', "Paternal-Aunt")

        # assert

        #   |---------------|       |---------------|
        # (queen10 ,     king10) (queen20,        king20)
        #                       |
        #                   daughter30
        self.assertEqual(['king20'], [s.name for s in maternal_uncles])
        self.assertEqual([], [s.name for s in maternal_aunts])
        self.assertEqual([], [s.name for s in paternal_uncles])
        self.assertEqual(['queen10'], [s.name for s in paternal_aunts])
        
        # action 
        in_laws = rel.explore('queen20', "Sister-In-Law")
        # assert
        self.assertEqual(['queen10'], [s.name for s in in_laws])

        # action 
        in_laws = rel.explore('queen10', "Sister-In-Law")
        # assert
        self.assertEqual(['queen20'], [s.name for s in in_laws])

        # action 
        in_laws = rel.explore('king10', "Brother-In-Law")
        # assert
        self.assertEqual(['king20'], [s.name for s in in_laws])

        # action 
        in_laws = rel.explore('king20', "Brother-In-Law")
        # assert
        self.assertEqual(['king10'], [s.name for s in in_laws])


