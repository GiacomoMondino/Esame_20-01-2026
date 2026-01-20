from dataclasses import dataclass
from model.artist import Artist

@dataclass
class Collegamento:
    a1 : Artist
    a2 : Artist
    peso : int = 0



    def __str__(self):
        return (f'Collegamento : {self.a1.id} - {self.a2.id},'
                f'peso : {self.peso}')

    def __repr__(self):
        return (f'Collegamento : {self.a1.id} - {self.a2.id},'
                f'peso : {self.peso}')
