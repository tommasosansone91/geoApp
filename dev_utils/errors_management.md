# errors management

###    from geo.Geoserver.Postgres import Db <br>ModuleNotFoundError: No module named 'geo.Geoserver.Postgres'; 'geo.Geoserver' is not a package

nell'ultima versione di geo non c'è la classe Db.

devo prendere invece


    from pg.pg import Pg

    # initialize the Pg class

    db = Pg(
        dbname=db_params['dbname'], 
        user=db_params['user'], 
        password=db_params['password'], 
        host=db_params['host'], 
        port=db_params['port']
        )

this requires pip installing pymongo and postgres-helper.


### funciotn that genersted the up.oad directory is called only once

Il problema con la funzione generate_uploaded_shp_file_relpath nel tuo modello Django è che viene valutata una sola volta, al momento del caricamento del modulo, e non per ogni istanza di modello. Questo significa che il valore restituito dalla funzione viene utilizzato come valore fisso per l'argomento upload_to di FileField.

Per risolvere questo problema, puoi modificare la tua funzione generate_uploaded_shp_file_relpath in modo che accetti l'istanza del modello come argomento e utilizzi un callable per l'argomento upload_to. Questo garantisce che la funzione venga chiamata ogni volta che un nuovo file viene caricato.

Ecco come puoi modificare il tuo modello per risolvere il problema:

Modifica la funzione generate_uploaded_shp_file_relpath in modo che accetti l'istanza del modello e il nome del file come argomenti.
Passa la funzione generate_uploaded_shp_file_relpath come callable all'argomento upload_to.
Ecco il codice aggiornato:

python
Copia codice
import os
import datetime
from django.core.exceptions import ValidationError
from django.db import models

def generate_current_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def generate_uploaded_shp_file_relpath(instance, filename):
    """
    This function generates the relative path to be passed to the "upload_to" argument of FileField.
    
    The input of this function must be the instance of the model and the filename.
    """
    timestamp = generate_current_timestamp()
    current_file_subfolder = timestamp

    uploaded_shp_files_folder_relpath_from_media_root = 'shp'

    uploaded_shp_file_relpath = os.path.join(
        uploaded_shp_files_folder_relpath_from_media_root,  
        current_file_subfolder,
        filename
    )

    return uploaded_shp_file_relpath

class Shp(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    shp_file = models.FileField(upload_to=generate_uploaded_shp_file_relpath)
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)
    shp_file_folder_path = models.CharField(default='undefined', max_length=1000, blank=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)

    def clean(self):
        super().clean()
        if UPLOADED_SHP_FILES_MUST_BE_ZIPPED:
            print("File validation: UPLOADED_SHP_FILES_MUST_BE_ZIPPED")
            if not self.shp_file.name.endswith('.zip'):
                raise ValidationError('The file must have .zip extension.')
            else:
                print("Validation passed")
                pass
Spiegazione
Funzione generate_current_timestamp:

python
Copia codice
def generate_current_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
Questa funzione genera un timestamp corrente.

Funzione generate_uploaded_shp_file_relpath:

python
Copia codice
def generate_uploaded_shp_file_relpath(instance, filename):
    timestamp = generate_current_timestamp()
    current_file_subfolder = timestamp

    uploaded_shp_files_folder_relpath_from_media_root = 'shp'

    uploaded_shp_file_relpath = os.path.join(
        uploaded_shp_files_folder_relpath_from_media_root,  
        current_file_subfolder,
        filename
    )

    return uploaded_shp_file_relpath
La funzione ora accetta instance e filename come argomenti e genera un percorso relativo unico ogni volta che viene chiamata.

Modello Shp:

python
Copia codice
class Shp(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    shp_file = models.FileField(upload_to=generate_uploaded_shp_file_relpath)
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)
    shp_file_folder_path = models.CharField(default='undefined', max_length=1000, blank=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)

    def clean(self):
        super().clean()
        if UPLOADED_SHP_FILES_MUST_BE_ZIPPED:
            print("File validation: UPLOADED_SHP_FILES_MUST_BE_ZIPPED")
            if not self.shp_file.name.endswith('.zip'):
                raise ValidationError('The file must have .zip extension.')
            else:
                print("Validation passed")
                pass
Note
Il callable generate_uploaded_shp_file_relpath viene passato direttamente all'argomento upload_to di FileField.
La funzione genera un percorso relativo unico basato sul timestamp corrente ogni volta che un nuovo file viene caricato, garantendo così che ogni percorso sia unico.
Salva le modifiche e prova a caricare nuovamente i file. Questa soluzione dovrebbe risolvere il problema e generare percorsi unici per ogni file caricato.