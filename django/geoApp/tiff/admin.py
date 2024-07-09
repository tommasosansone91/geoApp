from django.contrib import admin

# make my model accessible from the admin interface
from .models import Tiff


# # Register your models here.
class TiffAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'tiff_file', 'uploaded_date')  # Lista di campi da visualizzare nel form
    readonly_fields = ('tiff_file_folder_path',)

    # La virgola è necessaria perché in Python, 
    # una singola coppia di parentesi tonde con un unico elemento non viene interpretata come una tupla, 
    # ma semplicemente come l'elemento stesso racchiuso tra parentesi. 
    # Aggiungere una virgola dopo l'elemento assicura che 
    # Python lo interpreti correttamente come una tupla.

admin.site.register(Tiff, TiffAdmin)


