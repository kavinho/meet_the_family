import sys
from family_tree import models
from family_tree.tree_builder import TreeBuilder
from family_tree.explorer import RelationshipExplorer
from family_tree.commands import CommandsManager

def load_with_file(file_name, commands_manager, after_execute=None):
    with open(file_name, 'r')  as f:
        while True:
            line = f.readline()
            
            if not line:
                break

            line = line.replace('\n','').rstrip()
            words = line.split(" ")
            command = commands_manager.get_command_for(words[0], words[1:])
            if command :
                try: 
                    out_come = command.execute()
                except models.AddChildException:
                    out_come = 'CHILD_ADDITION_FAILED'
                except models.PersonNotFoundException:
                    out_come = 'PERSON_NOT_FOUND'
            else:
                out_come ="COMMAND_NOT_FOUND " + words[0]    

            if after_execute:
                after_execute(out_come)

def main():

    # init 
    builder = TreeBuilder()
    relashions = RelationshipExplorer(builder)
    manager = CommandsManager(builder, relashions)
    load_with_file("./family_tree/default_input.txt", manager)

    # act
    if len(sys.argv) == 2 :

        input_file_name =sys.argv[1]
        load_with_file(input_file_name,manager, lambda x: print(x))
if __name__ == "__main__":
    main()
