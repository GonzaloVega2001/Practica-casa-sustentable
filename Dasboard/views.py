from django.shortcuts import render
from .models import EstadoSensor
import json
from django.core.serializers.json import DjangoJSONEncoder # Importar el encoder

def index(request):
    # 1. Obtenemos los datos directamente como un QuerySet de diccionarios
    sensores_qs = EstadoSensor.objects.all().values(
        'id_lectura', 
        'id_termocupla', 
        'fecha_hora', 
        'temperatura', 
        'tipo_pared',
        'humedad',
    )
    
    # 2. Convertimos el QuerySet a una lista simple de Python
    sensores_list = list(sensores_qs)
    
    # 3. Serializamos la lista a una cadena JSON
    #    Usamos DjangoJSONEncoder para manejar correctamente los objetos 'datetime'
    #    y convertirlos a formato ISO (que JavaScript entiende)
    sensores_json_string = json.dumps(sensores_list, cls=DjangoJSONEncoder)
    
    # 4. Pasamos la CADENA JSON al template con un nuevo nombre de contexto
    context = {
        'sensores_json': sensores_json_string
    }
    
    return render(request, 'Dashboard.html', context)

