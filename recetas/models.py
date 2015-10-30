# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
import datetime
from multiselectfield import MultiSelectField


TIPODIAS = (
        (1, "lunes"),
        (2, "martes"),
        (3, "miercoles"),
        (4,"jueves"),
        (5,"viernes")
      )

# Create your models here.
#********************************************************#
               #     C H O F E R E S    #
#********************************************************#
class Chofer (models.Model):
    FILTROS = ['cuit_icontains', 'nombre_icontains']
    cuit= models.CharField(max_length=20, unique=True)
    nombre= models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    telefono=models.PositiveIntegerField()
    e_mail=models.CharField(max_length=100)

#********************************************************#
               #     I N S U M O     #
#********************************************************#
def stock_litros_kg(cant):
    cant= cant * 1000
    return cant

def stock_unidad(cant):
    return cant

def stock_docena(cant):
    cant = cant * 12
    return cant



class Insumo(models.Model):
    FILTROS = ['nombre__icontains', 'stock__lte']



    NONE = 0
    GRAMO = 1
    CM3 = 2
    UNIDAD = 3
    KG = 4
    LITRO = 5
    DOCENA = 6
    MAPLE = 7
    TUPLAS = [(GRAMO,KG),
              (CM3,LITRO),
              (UNIDAD,DOCENA,MAPLE)]

    UNIDADES_BASICAS = (
        (GRAMO, "g"),
        (CM3, "cm3"),
        (UNIDAD, "unidad")
    )

    UNIDADES_DERIVADAS = (
        (KG, "kg"),
        (LITRO, "litro"),
        (DOCENA, "docena"),
        (MAPLE, "maple")
    )

    UNIDADES = UNIDADES_BASICAS + UNIDADES_DERIVADAS

    CONVERT = {
        NONE: lambda cantidad: cantidad,
        GRAMO: lambda cantidad: cantidad,
        CM3: lambda cantidad: cantidad,
        UNIDAD: lambda cantidad: cantidad,
        KG: lambda cantidad: cantidad * 1000,
        LITRO: lambda cantidad: cantidad * 1000,
        DOCENA: lambda cantidad: cantidad * 12,
        MAPLE: lambda cantidad: cantidad * 30
    }

    FORMAT = {
        GRAMO: lambda cantidad: "%s.%s kg" % (cantidad // 1000, cantidad % 1000),
        CM3: lambda cantidad: "%s.%s litros" % (cantidad // 1000, cantidad % 1000),
        UNIDAD: lambda cantidad: "%s docenas y %s unidades" % (cantidad // 12, cantidad % 12)
    }

    nombre = models.CharField(max_length=100, unique=True, help_text="El nombre del insumo")
    descripcion = models.TextField("Descripcón")
    stock = models.IntegerField(blank=True, null=True, default=0)
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES_BASICAS)

    # Control de stock
    def incrementar(self, cantidad, unidad=NONE):
        self.stock += self.CONVERT[unidad](cantidad)

    def decrementar(self, cantidad, unidad=NONE):
        print "voy a decrementar del insumo ",self.nombre, "la cantidad: ",cantidad, "unidad medida: ",unidad
        self.stock -= self.CONVERT[unidad](cantidad)

    modificar_stock = incrementar

    def get_stock_humano(self):
        return self.FORMAT[self.unidad_medida](self.stock)

    def __str__(self):
        return "%s (%s)" % (self.nombre, self.get_unidad_medida_display())


#********************************************************#
            #     P R O D U C T O S     #
#********************************************************#

class ProductoTerminado(models.Model):
    UNIDADES = {
        (1, "Bolsines"),
    }
    FILTROS = ['nombre__icontains','stock__lte']
    nombre = models.CharField(max_length=100,unique=True,help_text="El nombre del producto")
    stock = models.PositiveIntegerField(default = 0)
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES)
    precio= models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])
    #http://blog.p3infotech.in/2013/enforcing-minimum-and-maximum-values-in-django-model-fields/


    def __str__(self):
        return "%s"% self.nombre



#********************************************************#
               #     R E C E T A S    #
#********************************************************#


class Receta(models.Model):
    UNIDADES = (

        (1, "Bolsines"),
    )
    FILTROS = ['nombre__icontains','producto_terminado']
    fecha_creacion = models.DateField(auto_now_add = True)
    nombre = models.CharField(max_length=100, unique=True,help_text="El nombre de la receta")
    unidad_medida =  models.PositiveSmallIntegerField(choices=UNIDADES)
    descripcion = models.TextField()
    cant_prod_terminado= models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)
    insumos = models.ManyToManyField(Insumo, through="RecetaDetalle")


    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.cant_prod_terminado, self.get_unidad_medida_display())


class RecetaDetalle(models.Model):
    cantidad_insumo = models.PositiveIntegerField()
    insumo = models.ForeignKey(Insumo)
    receta = models.ForeignKey(Receta)


#********************************************************#
            #     P R O V E E D O R E S    #
#********************************************************#

class Proveedor(models.Model):

    FILTROS = ['cuit__icontains','razon_social__icontains','localidad__icontains']
    razon_social = models.CharField(max_length=100, unique=True)
    nombre_dueno = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=30, unique=True, blank=True,null=True) #blank=True indica que puede estar el campo vacio
    localidad = models.CharField(max_length=50, unique=True)
    numero_cuenta= models.PositiveIntegerField(unique=True)
    provincia = models.CharField(max_length=50, unique=True)
    telefono= models.PositiveIntegerField()
    cuit= models.PositiveIntegerField(unique=True)
    insumos= models.ManyToManyField(Insumo,related_name='proveedores')#con related_name='proveedores' los objetos insumos puede llamar a sus proveedores por "proveedores"
#RELACION UNO A MUCHOS CON pedidosProveedor

    def __str__(self):
        return "%s (%d %s)" % (self.razon_social, self.telefono, self.cuit)


#********************************************************#
               #     Z O N A S    #
#********************************************************#

class Zona(models.Model):

    FILTROS = ['nombre__icontains']
    nombre = models.CharField(max_length=100, unique=True)
    #el campo "activo" es para las bajas logicas
    #activo = models.BooleanField(default=True);

    def __str__(self):
        return (self.nombre)



#********************************************************#
               #     C I U D A D E S    #
#********************************************************#
class Ciudad(models.Model):

    FILTROS = ['nombre__icontains','codigo_postal__icontains','zona']
    nombre = models.CharField(max_length=100, unique=True)
    codigo_postal = models.PositiveIntegerField(unique=True)
    zona = models.ForeignKey(Zona,related_name="ciudades")

    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.codigo_postal, self.zona)





#********************************************************#
               #     C L I E N T E S    #
#********************************************************#
class Cliente(models.Model):

    FILTROS = ['cuit_cuil__icontains','razon_social__icontains','ciudad','es_moroso']#'zona_icontains'
    cuit_cuil = models.PositiveIntegerField(unique=True)
    razon_social = models.CharField(max_length=100, unique=True)
    nombre_dueno = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad)#----> problema para filtrar
    direccion = models.CharField(max_length=100, unique=True)
    telefono= models.PositiveIntegerField()
    email = models.CharField(max_length=30, unique=True, blank=True,null=True) #blank=True indica que puede estar el campo vacio
    es_moroso = models.BooleanField(default=False)


    def __str__(self):
        return "%s (%s)" % (self.cuit_cuil, self.razon_social)


#************************************************************************#
               #     P E D I D O S  D E  C L I E N T E S    #
#************************************************************************#

'''
class PedidoCliente(models.Model):
    FILTROS = ['fecha_creacion__gte','tipo_pedido','cliente' ] #,'tipo_pedido__' como hacer para filtrar
    fecha_creacion = models.DateField(auto_now_add = True)
    productos = models.ManyToManyField(ProductoTerminado, through="PedidoClienteDetalle")
    cliente = models.ForeignKey(Cliente)
    TIPOS = {}


    def __str__(self):
        return "%s " % (self.cliente)

class PedidoClienteDetalle(models.Model):
    cantidad_producto = models.FloatField()
    producto_terminado = models.ForeignKey(ProductoTerminado)   #como hacer para q a un mismo cliente solo pueda haber un producto el mismo tipo
    pedido_cliente = models.ForeignKey(PedidoCliente)

class PedidoFijo(PedidoCliente):
    fecha_inicio = models.DateField(default=date.today())
    fecha_cancelacion = models.DateField(blank=True,null=True)
    dias = MultiSelectField(choices=TIPODIAS)
    NOMBRE = "Pedido Fijo"
    TIPO = 1

    def esParaHoy(self):
        d = date.today()
        if d.day in self.dias:
            return True
        else:
            return False
PedidoCliente.TIPOS[PedidoFijo.TIPO] = PedidoFijo

class PedidoCambio(PedidoCliente):
    fecha_entrega = models.DateField()
    TIPO = 3
    def esParaHoy(self):
        d = date.today()
        if d in self.fecha_entrega:
            return True
        else:
            return False
PedidoCliente.TIPOS[PedidoCambio.TIPO] = PedidoCambio

class PedidoOcacional(PedidoCliente):
    fecha_entrega = models.DateField()
    TIPO = 2
    def esParaHoy(self):
        d = date.today()
        if d in self.fecha_entrega:
            return True
        else:
            return False
PedidoCliente.TIPOS[PedidoOcacional.TIPO] = PedidoOcacional

'''


class PedidoCliente(models.Model):
    FILTROS = ['fecha_creacion__gte','tipo_pedido','cliente' ] #,'tipo_pedido__' como hacer para filtrar
    TIPOPEDIDO = (
        (1, "Pedido Fijo"),
        (2, "Pedido Ocasional"),
        (3,"Pedido de Cambio")
    )
    fecha_creacion = models.DateField(auto_now_add = True)
    tipo_pedido = models.PositiveSmallIntegerField(choices=TIPOPEDIDO)
    productos = models.ManyToManyField(ProductoTerminado, through="PedidoClienteDetalle")
    cliente = models.ForeignKey(Cliente)
    def esParaHoy(self):
        pass

    def esParaHoy(self):
        pass
    
    def __str__(self):
        return "%s ( %s)" % (self.cliente, self.get_tipo_pedido_display())

class PedidoClienteDetalle(models.Model):
    cantidad_producto = models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)   #como hacer para q a un mismo cliente solo pueda haber un producto el mismo tipo

    pedido_cliente = models.ForeignKey(PedidoCliente)


class PedidoFijo(PedidoCliente):
    fecha_inicio = models.DateField(default=date.today())
    fecha_cancelacion = models.DateField(blank=True,null=True)
    dias = MultiSelectField(choices=TIPODIAS)

    def esParaHoy(self):
        d = date.today()
        if d.day in self.dias:
            return True
        else:
            return False

class PedidoCambio(PedidoCliente):
    fecha_entrega = models.DateField()

    def esParaHoy(self):
        d = date.today()
        if d in self.fecha_entrega:
            return True
        else:
            return False


class PedidoOcacional(PedidoCliente):
    fecha_entrega = models.DateField()

    def esParaHoy(self):
        d = date.today()
        if d in self.fecha_entrega:
            return True
        else:
            return False

#********************************************************#
         #   P E D I D O S   A  P R O V E E D O R   #
#********************************************************#
class PedidoProveedor(models.Model):

    FILTROS = ['fecha_desde','fecha_hasta','proveedor','estado_pedido']
    FILTROS_MAPPER = {
        'fecha_desde': 'fecha_realizacion__gte',
        'fecha_hasta': 'fecha_realizacion__lte'
    }
    ESTADO = (
        (1, "Pendiente"),
        (2, "Recibido"),
        (3, "Cancelado"),
    )
    fecha_realizacion = models.DateField()
    fecha_de_entrega = models.DateField(blank=True,null=True)
    proveedor = models.ForeignKey(Proveedor)
    estado_pedido = models.PositiveSmallIntegerField(choices=ESTADO,default="1")
    insumos = models.ManyToManyField(Insumo, through="DetallePedidoProveedor")
    descripcion = models.TextField()
    #fecha_desde =  models.DateField()
    #fecha_hasta =  models.DateField()
    #fecha_cancelacion =  models.DateField()

    #relacion con proveedor
    #relacion con
    #https://jqueryui.com/datepicker/
    #fecha_realizacion__gte

    #detalle de pedido


    #detalle de pedido
    #auto_now_add = True


class DetallePedidoProveedor(models.Model):
    cantidad_insumo = models.PositiveIntegerField()
    insumo = models.ForeignKey(Insumo)
    pedido_proveedor = models.ForeignKey(PedidoProveedor)


#********************************************************#
         #   L O T E S   P R O D U C C I O N #
#********************************************************#
class Lote(models.Model):
    FILTROS = ['producto_terminado']

    nro_lote = models.AutoField(primary_key=True) # Field name made lowercase.
    fecha_produccion = models.DateField()
    fecha_vencimiento=models.DateField()
    cantidad_producida = models.PositiveIntegerField()
    stock_disponible= models.PositiveIntegerField()
    stock_reservado= models.PositiveIntegerField(default=0)
    producto_terminado=models.ForeignKey(ProductoTerminado)

#********************************************************#
         #    HOJA DE RUTA   #
#********************************************************#

'''
class HojaDeRuta(models.Model):
    fecha_creacion = models.DateField(auto_now_add = True)
    chofer = models.ForeignKey(Chofer)
    lote_extra = models.ManyToManyField(Lote, through="LotesExtraDetalle")


class LotesExtraDetalle(models.Model):
    cantidad = models.FloatField()
    lote = models.ForeignKey(Lote)
    hoja_de_ruta = models.ForeignKey(HojaDeRuta)



#********************************************************#
         #    ENTREGA PEDIDO   #
#********************************************************#


class EntregaPedido(models.Model):
    fecha_entrega = models.DateField(auto_now_add = True)
    pedido = models.ForeignKey(PedidoCliente)
    lotes = models.ManyToManyField(Lote, through="EntregaPedidoDetalle")
    hoja_de_ruta = models.ForeignKey(HojaDeRuta)
    #falta recibo, factura
    def __str__(self):
        return "%s ( %s)" % (self.cliente, self.get_tipo_pedido_display())

class EntregaPedidoDetalle(models.Model):
    cantidad_entregada = models.FloatField()    #poner integer
    cantidad_enviada = models.FloatField()
    precio = models.FloatField()
    detalle_pedido = models.ForeignKey(PedidoClienteDetalle)    #porque
    lote = models.ManyToManyField(Lote)
    entrega_pedido = models.ForeignKey(EntregaPedido)


'''
