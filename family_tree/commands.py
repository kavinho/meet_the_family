from .tree_builder import TreeBuilder
from .explorer import RelationshipExplorer
from .models import Gender, AddChildException, PersonNotFoundException


class Command(object):
    """
        Represent a class matching incoming commands to build or analyse family tree.
    """
    def __init__(self, args):
        self.args = args
    def execute(self):
        pass

class BuilderCommand(Command):
    """
        Type of command that adss a node(person) and/or edge(relationship) to family tree
    """
    def __init__(self, tree_builder, args):
        super().__init__( args)
        self.tree_builder = tree_builder

class AddPersonCommnad(BuilderCommand):
    def execute(self):
        if len(self.args) == 2:

            name = self.args[0]
            gender_name = self.args[1]
            self.tree_builder.create_node(name, Gender[gender_name])
            return "PERSON_ADDED"

class AddChildCommnad(BuilderCommand):

    def execute(self):

        if len(self.args) == 3:
            mother_name = self.args[0]
            child_name = self.args[1]
            gender = self.args[2]
            mother = self.tree_builder.get_node(mother_name)
            
            if mother is None:
                raise PersonNotFoundException("PERSON_NOT_FOUND")

            child = self.tree_builder.create_node(child_name, Gender[gender])    
            self.tree_builder.add_child(mother, child)                

            return "CHILD_ADDED"

class SetSpouseCommnad(BuilderCommand):
    def execute(self):
        if len(self.args) == 2:
            name = self.args[0]    
            spouse_name = self.args[1]
            subject = self.tree_builder.get_node(name)            
            spouse = self.tree_builder.create_node(spouse_name, subject.gender.not_())
            self.tree_builder.set_spouce(subject, spouse)
            return "SPOUSE_ADDED"
        pass          

class GetRelationshipCommand(Command):
    """
        Discovers a people matching a relationship, given a persons name
    """
    def __init__(self, rel_explorer, args):
        super().__init__(args)
        self.relationship_explorer = rel_explorer

    def execute(self):
        result_string = ""

        if len(self.args)==2:
            name = self.args[0]
            relation = self.args[1]
            matches = self.relationship_explorer.explore(name, relation)
            if len(matches):    
                for m in matches:
                    result_string += " " +  m.name        
            else:
                result_string="None"        
        return result_string

    
class CommandsManager(object):
    """
        A central place for commands to be picked and excuted.
        Given we have input coming from text files, the command part of the 
        file must match the keys in the text_to_command map.
    """

    def __init__(self, tree_builder, relations_explorer):
        self.text_to_command = {
            "ADD_PERSON": self.add_person,
            "ADD_CHILD": self.get_add_child_command,
            "ADD_SPOUSE": self.get_add_spouse_command,
            "GET_RELATIONSHIP": self.get_add_relation_command
            }    
        self.tree_builder = tree_builder
        self.relations_explorer = relations_explorer

    def add_person(self, args):
        return AddPersonCommnad(self.tree_builder, *args[1:])

    def get_add_child_command(self, args):
        return AddChildCommnad(self.tree_builder, args)
        
    def get_add_spouse_command(self, args):
        return SetSpouseCommnad(self.tree_builder, args)        

    def get_add_relation_command(self, args):
        return GetRelationshipCommand(self.relations_explorer, args)

    def get_command_for(self, text, args):
        command_type = self.text_to_command.get(text, None)
        if command_type :
            return command_type(args)
        else:
            return None    
