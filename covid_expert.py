from experta import *
from laboratory_csp import laboratory_csp
from covid_ontology import covid_ontology


def valid_response(response: str):
    valid = False
    response = response.lower()

    if response == "si" or response == "no":
        valid = True

    return valid


def valid_response2(response2: str):
    valid = False
    response2 = response2.lower()

    if response2 == "positivo" or response2 == "negativo":
        valid = True

    return valid


class covid_expert(KnowledgeEngine):
    @DefFacts()
    def initial_action(self):
        yield Fact(start="si")
        self.number_prints=0
        self.no_sympton=0

        self.lab_covid_analysis = laboratory_csp("Laboratorio per il tampone")
        self.lab_covid_analysis.addConstraint(lambda day, hours: hours>=8 and hours<=13 if day == "lunedi" else
                    hours >=15 and hours<=20 if day == "mercoledi" else None, ["day", "hours"])

    def prototype_lab_booking(self, ask_text: str, lab_selected: laboratory_csp):
        print("Hai avuto la prescrizione per %s, vuoi prenotare il controllo? [si/no]" %ask_text)
        response = str(input())

        while valid_response(response) == False:
            print("Hai avuto la prescrizione per %s, vuoi prenotare il controllo? [si/no]" % ask_text)
            response = str(input())

        if response == "si":
            first, last = lab_selected.get_availability()

            print("Inserisci un numero per selezionare il turno: ")
            turn = int(input())

            while turn < first and turn > last:
                print("Inserisci un numero per selezionare il turno: ")
                turn = int(input())

            lab_selected.print_single_availability(turn)

    def prototype_ask_sympton(self, ask_text: str, fact_declared: Fact):
        print(ask_text)
        response = str(input())

        while valid_response(response) == False:
            print(ask_text)
            response = str(input())

        if response == "si":
            self.declare(fact_declared)

        return response

    @Rule(Fact(start="si"))
    def rule(self):
        print("\nInizio diagnosi!\n")
        self.declare(Fact(ask_sympton="si"))

    @Rule(Fact(chiedi_tampone="si"))
    def rule_2(self):
        print("Hai effettuato già un tampone? ")
        response = str(input())

        while valid_response(response) == False:
            print("\nHai effettuato già un tampone? ")
            response = str(input())

        if response == "si":
            self.declare(Fact(tampone_fatto="si"))
        else:
            self.declare(Fact(fare_tampone="si"))

    @Rule(Fact(tampone_fatto="si"))
    def rule_3(self):
        print("\nIl risultato del tampone effettuato è: ")
        response = str(input())

        while valid_response2(response) == False:
            print("\nIl risultato del tampone effettuato è: ")
            response = str(input())

        if response == "positivo":
            print("Hai il covid!\n")
        else:
            print("Non hai il covid!\n")

    @Rule(Fact(fare_tampone="si"))
    def rule_4(self):
        print("Dovresti fare il tampone!")
        self.prototype_lab_booking("gli esami per il tampone", self.lab_covid_analysis)

    @Rule(Fact(ask_sympton="si"))
    def sympotns(self):
        s1 = self.prototype_ask_sympton("Hai la febbre? [si/no]", Fact(febbre="si"))
        s2 = self.prototype_ask_sympton("Hai dei sintomi di stanchezza? [si/no]", Fact(stanchezza="si"))
        s3 = self.prototype_ask_sympton("Hai la tosse secca? [si/no]", Fact(tosse_secca="si"))
        s4 = self.prototype_ask_sympton("Hai difficolta nel respirare? [si/no]", Fact(difficolta_respiro="si"))
        s5 = self.prototype_ask_sympton("Ti senti irritato in gola? [si/no]", Fact(gola="si"))
        s6 = self.prototype_ask_sympton("Accussi dolori fisici senza un'apparente motivazione? [si/no]",
                                        Fact(dolore="si"))
        s7 = self.prototype_ask_sympton("Percepisci una senzazione di ostruzione nel naso? [si/no]",
                                        Fact(congestione_nasale="si"))
        s8 = self.prototype_ask_sympton("Hai il naso che ti cola? [si/no]", Fact(rinorrea="si"))
        s9 = self.prototype_ask_sympton("Le tue feci sono di una consistenza liquida? [si/no]", Fact(diarrea="si"))

        if s1 == "no" and s2 == "no" and s3 == "no" and s4 == "no" and s5 == "no" and s6 == "no" and s7 == "no" and s8 == "no" and s9 == "no":
            self.no_sympton = 1

    @Rule(AND(Fact(febbre="si"), Fact(stanchezza="si"), Fact(tosse_secca="si"), Fact(difficolta_respiro="si"), Fact(gola="si"),
              Fact(dolore="si"), Fact(congestione_nasale="si"), Fact(rinorrea="si"), Fact(diarrea="si")))
    def all_symptons(self):
        print("\nPossiedi tutti i sintomi del covid!\n")
        self.declare(Fact(tutti_sintomi="si"))
        self.declare(Fact(chiedi_tampone="si"))

    @Rule(NOT(AND(Fact(febbre="si"), Fact(stanchezza="si"), Fact(tosse_secca="si"), Fact(difficolta_respiro="si"),
                Fact(gola="si"), Fact(dolore="si"), Fact(comgestione_nasale="si"), Fact(rinorrea="si"), Fact(diarrea="si"))))
    def no_symptons(self):
        if self.number_prints == 0 and self.no_sympton == 1:
            print("\nNon hai nessun sintomo riconducibile al covid!\n")
            self.declare(Fact(no_sintomi="si"))
            self.number_prints = self.number_prints+1

    @Rule(AND(Fact(febbre="si"), Fact(stanchezza="si"), Fact(tosse_secca="si"), NOT(Fact(difficolta_respiro="si")),
              Fact(gola="si"), NOT(Fact(dolore="si")), NOT(Fact(congestione_nasale="si")), NOT(Fact(rinorrea="si")),
              NOT(Fact(diarrea="si"))))
    def some_symptons(self):
        print("\nPossiedi solo alcuni sintomi riconducibili al covid, si consiglia comunque di fare il tampone!")
        self.declare(Fact(alcuni_sintomi="si"))
        self.declare(Fact(chiedi_tampone="si"))

    @Rule(AND(Fact(febbre="si"), NOT(Fact(stanchezza="si")), NOT(Fact(tosse_secca="si")), NOT(Fact(difficolta_respiro="si")),
            Fact(gola="si"), NOT(Fact(dolore="si")), NOT(Fact(congestione_nasale="si")), NOT(Fact(rinorrea="si")),
              NOT(Fact(diarrea="si"))))
    def cold_symptons(self):
        print("\nPotresti essere semplicemente raffreddato, aspetti una settimana e ripeti il test, nel frattempo"
              " rimanga in isolamento precauzionale\n")
        self.declare(Fact(raffreddore="si"))


def main_agent():
    expert_agent = covid_expert()
    expert_agent.reset()
    expert_agent.run()


def main_ontology():
    do = covid_ontology()

    do.get_symptoms_descriptions()
    sympton, keys_sympton = do.print_symptoms()

    print("\nInserisci il numero del sintomo di cui vuoi conoscere la descrizione: ")
    numsintomo = int(input())

    print("Sintomo: %s \nDescrizione: %s"%(keys_sympton[numsintomo], " ".join(sympton[numsintomo])))


def main():

    exit_program = False

    print("Sistema di diagnosi avviato")
    while exit_program == False:

        print("-----*MENU*------\n[1]Mostra i vari sintomi del covid\n[2]Calcola diagnosi\n[3]Esci")
        scelta = None

        try:
            scelta = int(input())

        except ValueError:
            exit_program = True

        if scelta == 1:
            main_ontology()

        elif scelta == 2:
            main_agent()

        else:
            print("Chiusura del programma...")
            exit_program = True


main()
