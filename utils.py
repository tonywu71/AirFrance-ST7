import os
from typing import Generator
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
    
    def __str__(self):
        return f'Passager catégorie {self.categorie} du groupe #{self.idx}, classe {self.classe} et temps de transit de {self.transit_time}'
    
    def __repr__(self):
        return f'passager du groupe #{self.idx}'

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

    def __str__(self):
        return f'Groupe #{self.idx} avec {self.get_nombre_passagers()} passager(s), classe {self.classe} et temps de transit de {self.transit_time}'

    def __repr__(self):
        return f'groupe #{self.idx}'
    
    def iter_passagers(self):
        """Générateur pour la liste des passagers dans le groupe.

        Yields:
            Passager: instance de la classe Passager
        """
        for passager in self.list_passagers:
            yield passager

    def est_seul(self):
        """Renvoie True si le groupe contient au moins un seul
        passager et False sinon.
        """
        return len(self.list_passagers) == 1
    
    def get_nombre_passagers(self):
        """Renvoie le nombre de passagers dans le groupe considéré.
        """
        return len(self.list_passagers)

    def comprend_enfants(self):
        """Renvoie True si le groupe contient au moins un enfant
        en son sein et False sinon.
        """
        return any([passager.categorie == 'enfants' for passager in self.list_passagers])


def read_and_preprocess(date):
    df = pd.read_csv(get_filepath(date))

    # Conversion en TimeStamp
    df['TransitTime'] = pd.to_datetime(df['TransitTime']).dt.time

    return df

def get_list_passagers(df):
    list_groupes = []

    for idx, row in df.iterrows():

        list_groupes.append(Groupe(
            idx=idx,
            nb_femmes=row['Femmes'],
            nb_hommes=row['Hommes'],
            nb_enfants=row['Enfants'],
            nb_WCHR=row['WCHR'],
            classe=row['Classe'],
            transit_time=row['TransitTime']
        ))
    
    return list_groupes