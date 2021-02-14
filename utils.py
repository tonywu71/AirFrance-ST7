import os
import pandas as pd



def get_filepath(date, data_source='data'):
    """Renvoie le filepath d'un fichier donné 

    Args:
        date (string): string contenant la date sous
            le format {jour}{Mois abbrégé}
            -> exemple : 7Nov

    Returns:
        string
    """
    return os.path.join(data_source, f'data_seating_{date}.csv')



class Passager:
    def __init__(self, idx, categorie, classe, transit_time=0):
        self.idx = idx
        self.categorie = categorie
        self.classe = classe
        self.transit_time = transit_time



class Groupe:
    """Une classe représentant un groupe de passagers ayant réservé
    leur places d'avion ensemble. Un groupe correspond donc à une ligne
    dans le fichier Excel de départ.
    """

    def __init__(self, idx, nb_femmes, nb_hommes, nb_enfants, nb_WCHR, classe, transit_time=0):
        """Constructeur pour la classe Groupe.

        Args:
            idx (int): Indice du groupe dans le fichier Excel
            nb_femmes (int): Nombre de femmes dans le groupe
            nb_hommes (int): Nombre d'hommes dans le groupe
            nb_enfants (int): Nombre d'enfants dans le groupe
            nb_WCHR (int): Nombre de personnes handicapés dans le groupe
            classe (string): Lettre donnant la classe du groupe
            transit_time (string, optional): String au format %H:%M:%S donnat le
                temps de transit pour le groupe. Defaults to 0.
        """
        self.idx = idx
        self.composition = {
            'femmes': nb_femmes,
            'hommes': nb_hommes,
            'enfants': nb_enfants,
            'WHCR': nb_WCHR
        }
        self.classe = classe
        self.transit_time = transit_time

        self.list_passagers = []

        for categorie, nombre in self.composition.items():
            self.list_passagers.append(Passager(
                self.idx,
                categorie,
                self.classe,
                self.transit_time))

        return

    def est_seul(self):
        """Renvoie True si le groupe contient au moins un seul
        passager et False sinon.
        """
        return len(self.list_passagers) == 1
    
    def comprend_enfants(self):
        """Renvoie True si le groupe contient au moins un enfant
        en son sein et False sinon.
        """
        return any([passager.categorie == 'enfants' for passager in self.list_passagers])

