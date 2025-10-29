from django.db import models


class EstadoSensor(models.Model):
    id_lectura = models.AutoField(primary_key=True)
    id_termocupla = models.IntegerField()
    fecha_hora = models.DateTimeField()
    temperatura = models.FloatField()
    tipo_pared = models.CharField(max_length=50)
    humedad = models.FloatField()

    class Meta:
        db_table = 'estado_sensor'  # importante: coincide con tu tabla MySQL
        managed = False  # Django NO modificará esta tabla (ya existe)

