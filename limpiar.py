# este script es para limpiar datos para debugg en Mia Pastas #
# borra todos los lotes.#
# stock de prod terminados = 0#
# saldo en clientes = 0#
# borra todas las hoja de ruta #
# borra todas las facturas #
# borra todos los resibos.#

import datetime
from datetime import date,timedelta
from recetas import models

for c in models.Cliente.objects.all():
	c.saldo=0
	c.save()

for p in models.ProductoTerminado.objects.all():
	p.stock=0
	p.save()

for l in models.Lote.objects.all():
	l.delete()

for h in models.HojaDeRuta.objects.all():
	h.delete()

for f in models.Factura.objects.all():
	f.delete()

for f in models.Recibo.objects.all():
	f.delete()


	
for i in range(1,4):
	for l in range(0,3):
		producto = models.ProductoTerminado.objects.all()[l]		
		lote = models.Lote.objects.create(producto_terminado=producto,fecha_produccion= date.today(),fecha_vencimiento= date.today() + timedelta(days=1000),cantidad_producida=100,stock_reservado=0,stock_disponible=100)
		producto.stock +=100
		producto.save()


# Recorre lotes e indica que cantidades estan reservadas y cuales fueron dadas de baja.#
for l in models.Lote.objects.all():
    print "LOTE: ",l.nro_lote
    reservado = 0
    for d in l.productosllevadosdetalle_set.all():
        reservado +=  d.cantidad
    print " - total Reservado: ",reservado
    perdido = 0
    for d in l.perdidastock_set.all():
        perdido += d.cantidad_perdida
    print " - total Perdido : ",perdido
    vendido = 0
    for d in l.productosllevadosdetalle_set.all():
    	vendido = d.cantidad - d.cantidad_sobrante
    print "cantidad vendida ", vendido 
