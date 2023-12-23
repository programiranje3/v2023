Resenje ovog zadatka je dato u dva oblika:

1) Resenje u okviru modula "solution_option_1",
u kome je kompletan kod dat u okviru jedne python skripte.

2) Resenje u okviru modula "solution_option_2",
u kome je kompletan kod podeljen u dve python skripte,
jedna (jun2021.py) u kojoj su definisane klase i
funkcije koje je trebalo implementirati i druga (test.py)
u kojoj je dat kod za proveru napisanih klasa i funkcija.

Razlog za ova dva oblika resenja je da se proveri da li ce
load f. iz json_tricks modula raditi kako treba i kada se
definicije klasa ciji se objekti (de-)serijalizuju ne nalaze
u istom modulu u kojima je poziv funkcija za (de-)serijalizaciju.
Povod za ovu proveru je upozorenje koje json_tricks prijavljuje
u verziji "solution_option_1". Ispostavilo se da sve funkcionise
kako treba i bez setovanja argumenta 'cls_lookup_map' na globals()
kako je upozorenje sugerisalo. Ovaj argument je ipak u nekim
slucajevim potrebno setovati o cemu se moze procitati u sekciji
"Class instances" json_tricks dokumentacije:
https://json-tricks.readthedocs.io/en/latest/

Za potrebe ispita bilo koje od ova dva oblika resenja je dobro
i nema potrebe za bilo kakvim dodatnim argumentima u dump i load
funkcija iz json_tricks paketa.