from family_tree import models

class RelationshipExplorer(object):
    """
        Explores relationships between people
    """

    def __init__(self, tree_builder):

        self.builder = tree_builder
        self.functions_map = {
            'Paternal-Uncle': self.get_paternal_unlce,
            'Maternal-Uncle': self.get_maternal_unlce,
            'Paternal-Aunt': self.get_paternal_aunt,
            'Maternal-Aunt': self.get_maternal_aunt,
            'Sister-In-Law': self.get_sister_in_law,
            'Brother-In-Law':self.get_brother_in_law,
            'Son':self.get_sons,
            'Daughter':self.get_daughters,
            'Siblings':self.get_siblings,
        }

    def explore(self, name, relationship_name):
        """
        gets the people matching the relationship_name relative to "name"
        the term subject seen in most of methods mean the person of interest.
        """
        node = self.builder.get_node(name)
        if not node:
            raise models.PersonNotFoundException()

        func = self.functions_map.get(relationship_name, None)
        if func:
            result = func(node)
            return result
        else:
            return []

    def get_children_of(self, node, gender=None):
        return node.get_children(gender=gender)

    def get_sons(self, subject):
        return self.get_children_of(subject, gender=models.Gender.Male)

    def get_daughters(self, subject):
        return self.get_children_of(subject, gender=models.Gender.Female)

    def get_siblings(self, subject):

        mother = subject.get_mother()
        children = mother.get_children()
        # remove the original child
        return [ch for ch in children if ch != subject]

    def get_maternal_unlce(self, subject):

        mother = subject.get_mother()
        uncles = mother.get_siblings(gender=models.Gender.Male)
        return uncles

    def get_paternal_unlce(self, subject):

        father = subject.get_father()
        uncles = father.get_siblings(gender=models.Gender.Male)

        return uncles

    def get_maternal_aunt(self, subject):

        mother = subject.get_mother()
        siblings = mother.get_siblings(gender=models.Gender.Female)
        return siblings

    def get_paternal_aunt(self, subject):

        father = subject.get_father()
        siblings = father.get_siblings(gender=models.Gender.Female)

        return siblings

    def _get_in_law_by_gender(self, subject, in_law_gender):

        spouse_sibling_gender = in_law_gender
        sibling_spouse_gender = in_law_gender.not_()
        in_laws = []

        spouse = subject.get_spouse()    
        if spouse:
            in_laws.extend(spouse.get_siblings(gender=spouse_sibling_gender))

        for sibling in subject.get_siblings(gender=sibling_spouse_gender):
            b_spouse = sibling.get_spouse()
            if b_spouse:
                in_laws.append(b_spouse)
        return in_laws                

    def get_sister_in_law(self, subject):
        return self._get_in_law_by_gender(subject, models.Gender.Female)

    def get_brother_in_law(self, subject):
        return self._get_in_law_by_gender(subject, models.Gender.Male)
