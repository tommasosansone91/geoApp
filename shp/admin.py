from django.contrib import admin

# make my model accessible from the admin interface
from .models import Shp


# Register your models here.
class ShpAdmin(admin.ModelAdmin):
    fields = ('shp_file', 'name', 'description', 'uploaded_date')  # Lista di campi da visualizzare nel form
    readonly_fields = ('shp_file_folder_path',)

    # La virgola è necessaria perché in Python, 
    # una singola coppia di parentesi tonde con un unico elemento non viene interpretata come una tupla, 
    # ma semplicemente come l'elemento stesso racchiuso tra parentesi. 
    # Aggiungere una virgola dopo l'elemento assicura che 
    # Python lo interpreti correttamente come una tupla.

admin.site.register(Shp, ShpAdmin)