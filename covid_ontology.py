from owlready2 import *


class covid_ontology:
    def __init__(self):
        self.ontology = get_ontology(os.path.basename("covid.owl")).load()
        self.dict_symptons = {}

    def get_symptoms_descriptions(self):
        dict_symptons_onto = {}

        for i in self.ontology.individuals():
            dict_symptons_onto[str(i)] = i.descrizione_sintomo
        for k in dict_symptons_onto.keys():
            k1 = k
            k1 = k1.replace("covid.istanza_", "")
            self.dict_symptons[k1] = dict_symptons_onto[k]

    def print_symptoms(self):
        i = 1
        dict_nums_symptons = {}
        dict_nums_keys = {}

        for k in self.dict_symptoms.keys():
            print("Sintomo [%d]: Nome: %s" % (i, k))
            dict_nums_symptons[i] = self.dict_symptoms[k]
            dict_nums_keys[i] = k
            i = i + 1

        return dict_nums_symptons, dict_nums_keys
