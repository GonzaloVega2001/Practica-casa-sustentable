from django.shortcuts import render
from .models import EstadoSensor
import json
from django.core.serializers.json import DjangoJSONEncoder # Importar el encoder
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import traceback

def dashboard(request):
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

    return render(request, 'dashboard.html', context)

def index(request):
    # Obtener la lista única de sensores para poblar el menú lateral
    try:
        sensores_qs = EstadoSensor.objects.all().values_list('id_termocupla', flat=True).order_by('id_termocupla')
        # convertir a lista y eliminar posibles None
        sensor_keys = [s for s in list(dict.fromkeys(sensores_qs)) if s is not None]
    except Exception:
        sensor_keys = []
    return render(request, 'index.html', {'sensor_keys': sensor_keys})

def dashboard_partial(request):
    """Devuelve solo el HTML parcial de las tarjetas por sensor (sin datos concretos).
    El cliente insertará este HTML y luego solicitará los datos JSON para rellenar valores y crear los charts.
    """
    try:
        # Si se pasa ?sensor=<id> devolvemos solo la tarjeta de ese sensor para evitar
        # renderizar todas y luego ocultarlas desde el cliente (evita parpadeo)
        sensor_param = request.GET.get('sensor')
        if sensor_param and sensor_param != 'all':
            # intentar convertir a número si aplica (pero mantener como string si no)
            try:
                sensor_key = int(sensor_param)
            except Exception:
                sensor_key = sensor_param
            # comprobamos existencia rápida en BD
            exists = EstadoSensor.objects.filter(id_termocupla=sensor_key).exists()
            if exists:
                return render(request, '_cards_partial.html', {'sensor_keys': [sensor_key]})
            else:
                # si no existe, devolvemos empty para que el cliente muestre mensaje apropiado
                return render(request, '_cards_partial.html', {'sensor_keys': []})

        sensores_qs = EstadoSensor.objects.all().values(
            'id_termocupla',
        )
        sensores_list = list(sensores_qs)
        # obtener lista única y ordenada de sensores
        sensor_keys = []
        for s in sensores_list:
            k = s.get('id_termocupla')
            if k not in sensor_keys:
                sensor_keys.append(k)
        return render(request, '_cards_partial.html', {'sensor_keys': sensor_keys})
    except Exception as e:
        tb = traceback.format_exc()
        print('\n--- EXCEPCIÓN EN dashboard_partial ---')
        print(tb)
        print('--- FIN EXCEPCIÓN ---\n')
        # devolver un fragmento mínimo para no romper el cliente
        return render(request, '_cards_partial.html', {'sensor_keys': []})


def dashboard_data(request):
    """Devuelve los datos de sensores en JSON (lista de lecturas).
    Se usa por el cliente para rellenar las tarjetas y dibujar los charts.
    Retorna JsonResponse con DjangoJSONEncoder para serializar datetimes.
    En caso de error devuelve un payload JSON con el mensaje y status 500.
    """
    try:
        sensores_qs = EstadoSensor.objects.all().values(
            'id_lectura',
            'id_termocupla',
            'fecha_hora',
            'temperatura',
            'tipo_pared',
            'humedad',
        )
        sensores_list = list(sensores_qs)
        # devolver lista como JSON (safe=False permite serializar listas)
        return JsonResponse(sensores_list, safe=False, encoder=DjangoJSONEncoder)
    except Exception:
        tb = traceback.format_exc()
        print('\n--- EXCEPCIÓN EN dashboard_data ---')
        print(tb)
        print('--- FIN EXCEPCIÓN ---\n')
        return JsonResponse({'error': 'Error al obtener datos de sensores. Revisa la consola del servidor.'}, status=500)
    

def dashboard_general(request):
    # Obtener lecturas y pasarlas al template como JSON para que el cliente las procese
    try:
        sensores_qs = EstadoSensor.objects.all().values(
            'id_lectura',
            'id_termocupla',
            'fecha_hora',
            'temperatura',
            'tipo_pared',
            'humedad',
        )
        sensores_list = list(sensores_qs)
        sensores_json_string = json.dumps(sensores_list, cls=DjangoJSONEncoder)
    except Exception:
        sensores_json_string = '[]'
    # If requested as a partial, return only the inner fragment for insertion
    if request.GET.get('partial'):
        try:
            html = render_to_string('_db_general_partial.html', {'sensores_json': sensores_json_string}, request=request)
            return HttpResponse(html)
        except Exception:
            return HttpResponse(status=500, content='Error rendering partial')

    return render(request, 'db_general.html', {'sensores_json': sensores_json_string})