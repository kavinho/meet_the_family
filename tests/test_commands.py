"This is not a complete test set, just a demo of unit testing for this components, and mocking" 
import unittest
from unittest.mock import MagicMock

from family_tree.models import Gender, PersonNotFoundException, AddChildException
from family_tree.commands import AddPersonCommnad, AddChildCommnad, SetSpouseCommnad, GetRelationshipCommand
from family_tree.tree_builder import TreeBuilder

class TestCommands (unittest.TestCase):
    def test_add_person_command(self):
        trb_mock = TreeBuilder("_")
        trb_mock.create_node = MagicMock()
        command = AddPersonCommnad(trb_mock, ["joan", "Female"])
        result = command.execute()
        self.assertEqual("PERSON_ADDED", result)
        trb_mock.create_node.assert_called_with("joan", Gender["Female"])

    def test_add_child_command(self):
        trb_mock = TreeBuilder("k","q")
        trb_mock.add_child = MagicMock()
        command = AddChildCommnad(trb_mock, ["q", "joan", "Female"])
        result = command.execute()
        self.assertEqual("CHILD_ADDED", result)
        called_args = trb_mock.add_child.call_args_list[0]
        self.assertEqual("q", called_args[0][0].name)
        self.assertEqual("joan", called_args[0][1].name)

    def test_add_child_command_not_found(self):
        trb = TreeBuilder("k","q")
    
        command = AddChildCommnad(trb, ["not_exist", "joan", "Female"])
        self.assertRaises(PersonNotFoundException,command.execute)


    def test_add_child_command_add_failed(self):
        trb = TreeBuilder("k","q")
        command = AddChildCommnad(trb, ["k", "joan", "Female"])
        self.assertRaises(AddChildException, command.execute)
