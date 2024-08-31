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

### FutureWarning: Neither gdal.UseExceptions() nor gdal.DontUseExceptions() has been explicitly called. In GDAL 4.0, exceptions will be enabled by default.

(venv) tommaso@tommaso-virtualbox02:~/tommaso03/coding_projects/corsi_udemy/geoApp/dev_utils/dev_lab/geoserver-rest$ python geoserver-rest.py
/home/tommaso/tommaso03/coding_projects/corsi_udemy/geoApp/dev_utils/dev_lab/geoserver-rest/venv/lib/python3.10/site-packages/osgeo/gdal.py:312: FutureWarning: Neither gdal.UseExceptions() nor gdal.DontUseExceptions() has been explicitly called. In GDAL 4.0, exceptions will be enabled by default.
  warnings.warn(

pe4r risolvere chiama uno di questi

from osgeo import gdal
gdal.UseExceptions()    # Enable exceptions
gdal.DontUseExceptions()


### ModuleNotFoundError: No module named 'bson'

Error met as trying to intall postgres-helper.

solve by 

    pip install pymongo


### errors met as trying to intall all the requirements at once

Collecting GDAL==3.6.0
  Using cached GDAL-3.6.0.tar.gz (757 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [21 lines of output]
      Traceback (most recent call last):
        File "/var/www/geoApp/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 353, in <module>
          main()
        File "/var/www/geoApp/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 335, in main
          json_out['return_val'] = hook(**hook_input['kwargs'])
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/var/www/geoApp/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 118, in get_requires_for_build_wheel
          return hook(config_settings)
                 ^^^^^^^^^^^^^^^^^^^^^
        File "/tmp/pip-build-env-n246iepe/overlay/lib/python3.12/site-packages/setuptools/build_meta.py", line 332, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/tmp/pip-build-env-n246iepe/overlay/lib/python3.12/site-packages/setuptools/build_meta.py", line 302, in _get_build_requires
          self.run_setup()
        File "/tmp/pip-build-env-n246iepe/overlay/lib/python3.12/site-packages/setuptools/build_meta.py", line 503, in run_setup
          super().run_setup(setup_script=setup_script)
        File "/tmp/pip-build-env-n246iepe/overlay/lib/python3.12/site-packages/setuptools/build_meta.py", line 318, in run_setup
          exec(code, locals())
        File "<string>", line 145, in <module>
        File "<string>", line 63, in get_numpy_include
      AttributeError: 'dict' object has no attribute '__NUMPY_SETUP__'
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: subprocess-exited-with-error

× Getting requirements to build wheel did not run successfully.
│ exit code: 1
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.



Collecting greenlet==2.0.2
  Using cached greenlet-2.0.2.tar.gz (164 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Building wheels for collected packages: greenlet
  Building wheel for greenlet (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Building wheel for greenlet (pyproject.toml) did not run successfully.
  │ exit code: 1




Collecting numpy==1.24.2
  Using cached numpy-1.24.2.tar.gz (10.9 MB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [33 lines of output]
      Traceback (most recent call last):
        File "/var/www/geoApp/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 353, in <module>
          main()
        File "/var/www/geoApp/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 335, in main
          json_out['return_val'] = hook(**hook_input['kwargs'])
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/var/www/geoApp/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 112, in get_requires_for_build_wheel
          backend = _build_backend()
                    ^^^^^^^^^^^^^^^^
        File "/var/www/geoApp/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 77, in _build_backend
          obj = import_module(mod_path)
                ^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
          return _bootstrap._gcd_import(name[level:], package, level)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
        File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
        File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
        File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
        File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
        File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
        File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
        File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
        File "<frozen importlib._bootstrap_external>", line 995, in exec_module
        File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
        File "/tmp/pip-build-env-81l74_dl/overlay/lib/python3.12/site-packages/setuptools/__init__.py", line 16, in <module>
          import setuptools.version
        File "/tmp/pip-build-env-81l74_dl/overlay/lib/python3.12/site-packages/setuptools/version.py", line 1, in <module>
          import pkg_resources
        File "/tmp/pip-build-env-81l74_dl/overlay/lib/python3.12/site-packages/pkg_resources/__init__.py", line 2172, in <module>
          register_finder(pkgutil.ImpImporter, find_on_path)
                          ^^^^^^^^^^^^^^^^^^^
      AttributeError: module 'pkgutil' has no attribute 'ImpImporter'. Did you mean: 'zipimporter'?
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: subprocess-exited-with-error



pandas takes forever



