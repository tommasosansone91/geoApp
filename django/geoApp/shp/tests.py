from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth.models import User
from .models import Shp

# Import necessario per gestire file upload fittizi durante i test
from django.core.files.uploadedfile import SimpleUploadedFile

from geoApp.utils import generate_current_date
from geoApp.geo_system_check import check_geoserver_status

import os
from geoApp.settings import BASE_DIR

import pprint 

pp = pprint.PrettyPrinter(indent=4)

# ensure geoserver is active, otherwise, do not allow the app to start
check_geoserver_status()
# here the error raised by check_geoserver_status() is not managed.
# so if it occurs, it crashes the app.

class AdminTestCase(TestCase):
    def setUp(self):
        # Verificare se esiste già un superuser con il nome utente specificato
        self.admin_username = 'test_admin'
        self.admin_password = 'test_admin_password'
        self.admin_email = 'test_admin@example.com'
        
        if not User.objects.filter(username=self.admin_username).exists():
            # Creare un utente superuser se non esiste
            self.admin_user = User.objects.create_superuser(
                username=self.admin_username,
                password=self.admin_password,
                email=self.admin_email
            )
        else:
            self.admin_user = User.objects.get(username=self.admin_username)
        
        self.client.login(username=self.admin_username, password=self.admin_password)
    
    
    def test_create_and_delete_shp_via_admin(self):
        # URL per creare un nuovo oggetto Shp nell'admin UI
        #  url = reverse('admin:<app_name>_shp_add')
        url = reverse('admin:shp_shp_add')

        self.test_name = 'Test Shp'
        self.test_description = "This is a test description for test file 'Test shp'"
        
        self.test_shp_file_path = os.path.join(BASE_DIR, 'shp', 'files_for_tests', 'C_Jamoat.zip')

        with open(self.test_shp_file_path, 'rb') as test_file:
            file_data = test_file.read()

        # Creare l'oggetto SimpleUploadedFile
        self.test_shp_file = SimpleUploadedFile(
            name='C_Jamoat.zip',
            content=file_data,
            content_type='application/zip'
        )
        
        
        self.test_uploaded_date = generate_current_date()
        
        # Dati da inviare al form
        data = {
            'name': self.test_name,
            'description': self.test_description,
            'shp_file': self.test_shp_file,
            'uploaded_date': self.test_uploaded_date,
        }

        print("\n\nTest the creation of object shp with data:\n")
        pp.pprint(data)
        print("\n\n")        

        # Inviare una richiesta POST per creare il nuovo oggetto Shp
        response = self.client.post(url, data, follow=True)
        
        # Controllare che il nuovo oggetto Shp sia stato creato
        self.assertEqual(response.status_code, 200)

        self.assertTrue(Shp.objects.filter(name=self.test_name).exists())

        self.assertTrue(
            Shp.objects.filter(
                name=self.test_name, 
                description=self.test_description,
                uploaded_date=self.test_uploaded_date
                ).exists()
            )
        
        # this cannot be fully tested as conn_str pints to real db and not the test use-and-destroy db

        print("\n\nTest the deletion of object shp with data:\n")
        pp.pprint(data)
        print("\n\n")

        # Recuperare l'oggetto Shp creato
        shp_to_delete = Shp.objects.get(
            name=self.test_name, 
            description=self.test_description,
            uploaded_date=self.test_uploaded_date
            )
        
        # URL per eliminare un oggetto Shp nell'admin UI
        url_delete = reverse('admin:shp_shp_delete', args=[shp_to_delete.id])
        
        data_delete = {
            'post': 'yes'
        }
        
        # Inviare una richiesta POST per eliminare l'oggetto Shp
        response_delete = self.client.post(url_delete, data_delete, follow=True)
        
        # Controllare che l'oggetto Shp sia stato eliminato
        self.assertEqual(response_delete.status_code, 200)
        self.assertFalse(
            Shp.objects.filter(
                name=self.test_name, 
                description=self.test_description,
                uploaded_date=self.test_uploaded_date
                ).exists()
            )