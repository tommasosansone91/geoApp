from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tiff

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
    
    
    def test_create_and_delete_tiff_via_admin(self):
        # URL per creare un nuovo oggetto Tiff nell'admin UI
        #  url = reverse('admin:<app_name>_tiff_add')
        url = reverse('admin:tiff_tiff_add')

        self.test_name = 'Test Tiff'
        self.test_description = "This is a test description for test file 'Test tiff'"
        
        self.test_tiff_file_path = os.path.join(BASE_DIR, 'tiff', 'files_for_tests', 'test_tif_file1.tif')

        with open(self.test_tiff_file_path, 'rb') as test_file:
            file_data = test_file.read()

        # Creare l'oggetto SimpleUploadedFile
        self.test_tiff_file = SimpleUploadedFile(
            name='test_tif_file1.tif',
            content=file_data,
            content_type='image/tiff'
        )
        
        
        self.test_uploaded_date = generate_current_date()
        
        # Dati da inviare al form
        data = {
            'name': self.test_name,
            'description': self.test_description,
            'tiff_file': self.test_tiff_file,
            'uploaded_date': self.test_uploaded_date,
        }

        print("\n\nTest the creation of object tiff with data:\n")
        pp.pprint(data)
        print("\n\n")
        
        # Inviare una richiesta POST per creare il nuovo oggetto Tiff
        response = self.client.post(url, data, follow=True)
        
        # Controllare che il nuovo oggetto Tiff sia stato creato
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Tiff.objects.filter(
                name=self.test_name, 
                description=self.test_description,
                uploaded_date=self.test_uploaded_date
                ).exists()
            )
        
        print("\n\nTest the deletion of object tiff with data:\n")
        pp.pprint(data)
        print("\n\n")

        # Recuperare l'oggetto Tiff creato
        tiff_to_delete = Tiff.objects.get(
            name=self.test_name, 
            description=self.test_description,
            uploaded_date=self.test_uploaded_date
            )
        
        # URL per eliminare un oggetto Tiff nell'admin UI
        url_delete = reverse('admin:tiff_tiff_delete', args=[tiff_to_delete.id])
        
        data_delete = {
            'post': 'yes'
        }
        
        # Inviare una richiesta POST per eliminare l'oggetto Tiff
        response_delete = self.client.post(url_delete, data_delete, follow=True)
        
        # Controllare che l'oggetto Tiff sia stato eliminato
        self.assertEqual(response_delete.status_code, 200)
        self.assertFalse(
            Tiff.objects.filter(
                name=self.test_name, 
                description=self.test_description,
                uploaded_date=self.test_uploaded_date
                ).exists()
            )