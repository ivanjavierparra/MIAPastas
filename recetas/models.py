# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
import datetime
from multiselectfield import MultiSelectField
from django.utils import timezone
from django.db.models import Q


#clase para redefinir objects y obtener solo instancias activas
class ManagerBajasLogicas(models.Manager):
    def __init__(self, activo):
        super(ManagerBajasLogicas, self).__init__()
        self.activo = activo

    def get_queryset(self):
        return super(ManagerBajasLogicas, self).get_queryset().filter(activo=self.activo)


'''
class ManagerActivosHojasRutas(models.Manager):
    def get_queryset(self):
        return super(ManagerActivosHojasRutas, self).get_queryset().filter(rendida=False)
'''
TIPODIAS = (
        (1, "lunes"),
        (2, "martes"),
        (3, "miercoles"),
        (4,"jueves"),
        (5,"viernes")
      ) 

CAUSAS_DECREMENTO_STOCK = (
        (1, "Vencimiento"),
        (2, "Rotura"),
        (3,"Otros")
    )


# Create your models here.
               #     C H O F E R E S    #
#********************************************************#
class Chofer(models.Model):
    FILTROS = ['cuit__icontains', 'nombre__icontains']
    cuit= models.CharField(max_length=20, unique=True)
    nombre= models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    telefono=models.PositiveIntegerField()
    e_mail=models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    disponible = models.BooleanField(default=True)

    # Managers de chofer
    objects = ManagerBajasLogicas(activo=True)
    eliminados = ManagerBajasLogicas(activo=False)

    def __str__(self):
        return "%s" % (self.nombre)


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
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nombre']

    # Control de stock
    def incrementar(self, cantidad, unidad=NONE):
        self.stock += self.CONVERT[unidad](cantidad)
        self.save()
    def decrementar(self, cantidad, unidad=NONE):
        print "voy a decrementar del insumo ",self.nombre, "la cantidad: ",cantidad, "unidad medida: ",unidad
        self.stock -= self.CONVERT[unidad](cantidad)
        self.save()

    modificar_stock = incrementar

    def get_stock_humano(self):
        return self.FORMAT[self.unidad_medida](self.stock)

    def __str__(self):
        return "%s (%s)" % (self.nombre, self.get_unidad_medida_display())


#********************************************************#
            #     P R O D U C T O S     #
#********************************************************#

class ProductoTerminado(models.Model):

    FILTROS = ['nombre__icontains','stock__lte']
    nombre = models.CharField(max_length=100,unique=True,help_text="El nombre del producto")
    stock = models.PositiveIntegerField(default = 0)
    precio= models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])
    dias_vigencia = models.PositiveIntegerField(default=01)#esto es la fecha de vencimiento
    #http://blog.p3infotech.in/2013/enforcing-minimum-and-maximum-values-in-django-model-fields/
    activo = models.BooleanField(default=True)


    class Meta:
        permissions = (
            ("ver_productos_terminados_disponibles", "Puede listar los productos disponibles"),
            ("ver_productos_mas_vendidos", "Puede listar los productos mas vendidos"),
        )
        

    def stockDisponibleEnDeposito(self):
        lotes = self.lote_set.all()
        cantidad = 0
        for lote in lotes: #hay que obtener la cantidad disponible en el deposito
            if lote.fecha_vencimiento >= date.today():
                cantidad += lote.stock_disponible - lote.stock_reservado
        return cantidad


    def __str__(self):
        return "%s"% self.nombre



#********************************************************#
               #     R E C E T A S    #
#********************************************************#


class Receta(models.Model):

    FILTROS = ['nombre__icontains','producto_terminado']
    fecha_creacion = models.DateField(auto_now_add = True)
    nombre = models.CharField(max_length=100, unique=True,help_text="El nombre de la receta")
    descripcion = models.TextField()
    cant_prod_terminado= models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)
    insumos = models.ManyToManyField(Insumo, through="RecetaDetalle")
    #activo = models.BooleanField(default=True)
    #objects=ManagerActivos()

    def __str__(self):
        return "%s (%d) Bolsines" % (self.nombre, self.cant_prod_terminado)


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
    nombre_dueno = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    email = models.EmailField(max_length = 50) #blank=True indica que puede estar el campo vacio
    localidad = models.CharField(max_length=50)
    numero_cuenta= models.PositiveIntegerField(unique=True)
    provincia = models.CharField(max_length=50)
    telefono= models.PositiveIntegerField()
    cuit= models.CharField(unique=True,max_length=20)
    insumos= models.ManyToManyField(Insumo,related_name='proveedores')#con related_name='proveedores' los objetos insumos puede llamar a sus proveedores por "proveedores"
#RELACION UNO A MUCHOS CON pedidosProveedor
    #activo = models.BooleanField(default=True)
    #objects=ManagerActivos()

    def __str__(self):
        return "%s (%d %s)" % (self.razon_social, self.telefono, self.cuit)


#********************************************************#
               #     Z O N A S    #
#********************************************************#

class Zona(models.Model):

    FILTROS = ['nombre__icontains']
    nombre = models.CharField(max_length=100, unique=True)
    #el campo "activo" es para las bajas logicas
    #activo = models.BooleanField(default=True)
    #objects=ManagerActivos()

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
    #activo = models.BooleanField(default=True)
    #objects=ManagerActivos()
    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.codigo_postal, self.zona)





#********************************************************#
               #     C L I E N T E S    #
#********************************************************#
class Cliente(models.Model):

    FILTROS = ['cuit__icontains','razon_social__icontains','ciudad','es_moroso','saldo__gt']#'zona_icontains'
    cuit = models.CharField(unique=True,max_length=20)
    razon_social = models.CharField(max_length=100, unique=True)
    nombre_dueno = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad)#----> problema para filtrar
    direccion = models.CharField(max_length=100, unique=True)
    telefono= models.PositiveIntegerField()
    email = models.EmailField(blank=True, null=True) #blank=True indica que puede estar el campo vacio
    es_moroso = models.BooleanField(default=False)
    saldo = models.FloatField(default=0)

    def __str__(self):
        return "%s (%s)" % (self.cuit, self.razon_social)

    class Meta:
        permissions = (
            ("ver_clientes_morosos", "Puede listar los clientes morosos"),
            ("cobrar_a_cliente", "Puede cobrar a los clientes"),

        )

    def aumentar_saldo(self,cantidad):
        self.saldo +=  float(cantidad)
        self.save()

    def decrementar_saldo(self,cantidad):
        self.saldo -=  float(cantidad)
        self.save()


#************************************************************************#
               #     P E D I D O S  D E  C L I E N T E S    #
#************************************************************************#


class PedidoCliente(models.Model):
    ''' Modelo de la clase padre de los pedidos de cliente
    '''
    FILTROS = ['fecha_creacion__gte','tipo_pedido','cliente' ] #,'tipo_pedido__' como hacer para filtrar
    TIPOPEDIDO = (
        (1, "Pedido Fijo"),
        (2, "Pedido Ocasional"),
        (3, "Pedido de Cambio")
    )
    fecha_creacion = models.DateField(auto_now_add = True)
    tipo_pedido = models.PositiveSmallIntegerField(choices=TIPOPEDIDO)
    productos = models.ManyToManyField(ProductoTerminado, through="PedidoClienteDetalle")
    cliente = models.ForeignKey(Cliente)
    activo = models.BooleanField(default=True)
    
    def esParaHoy(self):
        ''' Metodo que los hijos lo redefinen
        '''
        pass

    
    def __str__(self):
        return "%s ( %s)" % (self.cliente, self.get_tipo_pedido_display())

class PedidoClienteDetalle(models.Model):
    ''' 
        Clase que modela los detalles de los pedidos independientemente del tipo (fijo, ocacional o de cambio)
    '''
    cantidad_producto = models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)   #como hacer para q a un mismo cliente solo pueda haber un producto el mismo tipo

    pedido_cliente = models.ForeignKey(PedidoCliente)

class PedidoFijo(PedidoCliente):
    ''' Clase que modela los pedidos fijos, es hija de PedidoCliente
        Un pedido fijo tiene fecha inicio, los dias para entregas los productos, y puede tener fecha de cancelacion
    '''
    FILTROS = ['fecha_hasta','fecha_desde']
    FILTROS_MAPPER = {
        'fecha_desde': 'pedidofijo__fecha_cancelacion__gte',
        'fecha_hasta': 'pedidofijo__fecha_inicio__lte'
    }#SE VERIFICA LA FECHA DE CANCELACCION NO SEA MENOR A LA FECHA DESDE, Y QUE LA FECHA INICIO NO SEA MAYOR A FECHA HASTA 
    fecha_inicio = models.DateField(default=date.today())
    #fecha_inicio = models.DateField(default=timezone.now())
    fecha_cancelacion = models.DateField(blank=True,null=True)
    dias = MultiSelectField(choices=TIPODIAS)

    def esParaHoy(self):
        ''' Metodo que verifica si un pedido tiene como fecha de entrega la fecha actual.
            Se lo utiliza al armar una hoja de ruta.
            Ademas, realiza una "baja logica" si el pedido fijo ya esta vencido (si se paso la fecha de canceacion). 
        '''
        if self.fecha_cancelacion != None and self.fecha_cancelacion<date.today():
            self.activo=False
            self.save()
            print "en es para hoyyyy"
            return False
        num_dia = date.today().weekday()
        if self.dias == None:
            return False
        if str(num_dia + 1) in self.dias:
            return True
        else:
            return False

class PedidoCambio(PedidoCliente):
    ''' Clase que modela los pedidos de Cambio, es hija de PedidoCliente
        Un pedido de cambio tiene fecha de entrega.
    '''
    FILTROS = ['fecha_hasta','fecha_desde']

    FILTROS_MAPPER = {
        'fecha_desde': 'pedidocambio__fecha_entrega__gte',
        'fecha_hasta': 'pedidocambio__fecha_entrega__lte'
    }
    fecha_entrega = models.DateField()

    def esParaHoy(self):
        '''Metodo que verifica si un pedido tiene como fecha de entrega la fecha actual.
        '''
        d = date.today()
        if d == self.fecha_entrega:
            return True
        else:
            return False



class PedidoOcacional(PedidoCliente):
    ''' Clase que modela los pedidos ocacionales, es hija de PedidoCliente
        Un pedido ocacional tiene fecha de entrega.
    '''
    FILTROS = ['fecha_hasta','fecha_desde']

    FILTROS_MAPPER = {
        'fecha_desde': 'pedidoocacional__fecha_entrega__gte',
        'fecha_hasta': 'pedidoocacional__fecha_entrega__lte'
    }

    fecha_entrega = models.DateField()
    def esParaHoy(self):
        '''Metodo que verifica si un pedido tiene como fecha de entrega la fecha actual.
        '''
        d = date.today()
        if d == self.fecha_entrega:
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
    descripcion = models.TextField(null=True)
    fecha_cancelacion =  models.DateField(blank=True,null=True)


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

    def reservar_stock(self,cantidad):
        """ Resibe la cantidad de stock que se necesita reservar.
            Si stock disponible alcanza a cubrirla, se aumenta el stock reservado en esa cantidad
            Si stock disponible no alcanza a cubrirla, se aumenta el stock reservado con stock disponible
            Este metodo retorna la cantidad que LOGRO reservar
        """
        puede_reservar = self.stock_disponible - self.stock_reservado
        if cantidad <= puede_reservar:
            reservar = cantidad
        else:
            reservar = puede_reservar
        self.stock_reservado += reservar
        self.save()
        return reservar

 

    def decrementar_stock_reservado(self,cant):
        self.stock_reservado -= cant
        self.save()

    def decrementar_stock_disponible(self,cant):
        self.stock_disponible -= cant
        self.producto_terminado.stock -=cant
        self.producto_terminado.save()
        self.save()
        



class Factura(models.Model):
    fecha = models.DateField(auto_now_add = True)
    numero = models.PositiveIntegerField(unique=True)  #es el numero de la factura en papel
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,01)])

    #class Meta: digo que la factura debe ser unica, en numero + cliente
        #unique_together = (("numero", "cliente"),)
    def __str__(self):
        return "%s" % ("Factura")

    def to_string(self):
        return "Factura"


class PerdidaStock(models.Model):
    ''' Clase que modela el suceso de decrementar el stock de un lote debido a una perdida (por rotura, vencimiento u otros)
    '''
    FILTROS = ['fecha_desde','fecha_hasta','causas']
    FILTROS_MAPPER = {
        'fecha_desde': 'fecha__gte',
        'fecha_hasta': 'fecha__lte'
    }
    cantidad_perdida = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=200)
    lote = models.ForeignKey(Lote)
    fecha = models.DateField(auto_now_add=True)
    causas = models.PositiveSmallIntegerField(choices=CAUSAS_DECREMENTO_STOCK, default="1")

    class Meta:
        permissions = (
            ("ver_perdida_stock", "Puede listar las perdidas de stock"),
        )


#********************************************************#
         #    HOJA DE RUTA   #
#********************************************************#


class HojaDeRuta(models.Model):
    FILTROS = ['fecha_desde','fecha_hasta']
    FILTROS_MAPPER = {
        'fecha_desde': 'fecha_creacion__gte',
        'fecha_hasta': 'fecha_creacion__lte'
    }
    fecha_creacion = models.DateField(auto_now_add = True)
    chofer = models.ForeignKey(Chofer)
    rendida = models.BooleanField(default=False)
    pagado = models.BooleanField(default=False)

    def balance(self):
        totales=[]
        for p in self.productosllevados_set.all():
            totales.append({"producto_terminado":p.producto_terminado.nombre,
                            "cantidad_enviada":p.cantidad_enviada,
                            "cantidad_pedida":p.cantidad_pedida}) 
        return totales

    def tiene_alguna_entrega(self):
        if len(self.entrega_set.all()) > 0:
            return True
        return False    

    def tiene_algun_producto(self):
        tiene = False
        for p in self.productosllevados_set.all():
            if p.cantidad_enviada > 0:
                tiene = True
                break
        if tiene:
            return True
        return False
                    

    def lleva_producto(self,p):
        lleva = False
        for prod in self.productosllevados_set.all():
            if prod.producto_terminado == p and prod.cantidad_enviada > 0:
                lleva=True
                break
        if lleva:
            return True
        return False

    def limpiar_reserva(self):
        for p in self.productosllevados_set.all():
            p.limpiar_reserva()
    
    def generar_detalles(self):
        for p in self.productosllevados_set.all():
            p.generar_detalles() 

class ProductosLlevados(models.Model):
    cantidad_pedida = models.PositiveIntegerField(default=0)
    cantidad_extra = models.PositiveIntegerField(default=0)
    cantidad_enviada = models.PositiveIntegerField(default=0)
    producto_terminado = models.ForeignKey(ProductoTerminado)
    hoja_de_ruta = models.ForeignKey(HojaDeRuta)
    precio= models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)],default=0)

    def generar_detalles(self):
        """ En base al producto y a la (cantidad pedida + cantidad_extra), sale a buscarlo en los lotes
            Por cada lote que se necesite para cubrir la cantidad pedida se crea un detalle asociado a el
            junto con la cantidad que pudo sacarle a ese lote.
        """
        cantidad_buscada = self.cantidad_pedida + self.cantidad_extra
        for lote in Lote.objects.filter(producto_terminado = self.producto_terminado,
                                        fecha_vencimiento__gte=datetime.date.today(),
                                        stock_disponible__gte = 0):
            cantidad_reservada = lote.reservar_stock(cantidad_buscada)
            if cantidad_reservada == 0:
                continue
            cantidad_buscada -=cantidad_reservada
            ProductosLlevadosDetalle.objects.create(cantidad = cantidad_reservada,
                                                    lote=lote,
                                                    producto_llevado = self)
            if cantidad_buscada == 0:
                break
        if cantidad_buscada > 0:
            print "Faltaron ",cantidad_buscada, "unidades para el producto: ",self.producto_terminado
        self.cantidad_enviada = (self.cantidad_pedida + self.cantidad_extra) - cantidad_buscada
        self.save()

    def limpiar_reserva(self):
        """ se encarga de devolver a cada lote, la cantidad que habia reservado """
        print " EEEEEEEEEEEEEEEN LIMPIAR RESERVAAAA"
        for d in self.productosllevadosdetalle_set.all():
            d.lote.decrementar_stock_reservado(d.cantidad)

class ProductosLlevadosDetalle(models.Model):
    cantidad = models.PositiveIntegerField()
    lote = models.ForeignKey(Lote)
    producto_llevado= models.ForeignKey(ProductosLlevados)
    cantidad_sobrante = models.PositiveIntegerField(null=True)

class Entrega(models.Model):
    FILTROS = ['fecha_desde','fecha_hasta']
    FILTROS_MAPPER = {
        'fecha_desde': 'fecha__gte',
        'fecha_hasta': 'fecha__lte'
    }
    hoja_de_ruta = models.ForeignKey(HojaDeRuta)
    pedido = models.ForeignKey(PedidoCliente)
    fecha = models.DateField(auto_now_add = True)
    factura = models.ForeignKey(Factura,null=True)
    #cliente = getCliente()

    def generar_detalles(self):
        if self.entregadetalle_set.all().exists():
            raise "Ya tengo detalles para el pedido %s" % self.pedido

        for detalle_pedido in self.pedido.pedidoclientedetalle_set.all():
            # creo detalle de entrega asociada al detalle del pedido
            entrega_detalle = EntregaDetalle.objects.create(entrega=self,
                                                                   precio=(detalle_pedido.producto_terminado.precio *detalle_pedido.cantidad_producto),
                                                                   cantidad_entregada = None,
                                                                   pedido_cliente_detalle=detalle_pedido)
    def getCliente(self):
        print ("soy clienteeeee",self.pedido.cliente)
        return self.pedido.cliente


    def monto_ya_abonado(self):
        recibos = self.recibo_set.all()
        total = 0
        for recibo in recibos:
            total += recibo.monto_pagado
        return total

    def monto_total(self):
        detalles = self.entregadetalle_set.all()
        total = 0
        for detalle in detalles:
            total += detalle.precio
        return total

    def monto_restante(self):   # sirve solo para entregas no facturadas, si esta facturada nunca se deberia llamar, no tendria sentido
        return self.monto_total()-self.monto_ya_abonado()

    def cobrar_con_factura(self,monto,numero_factura=None):
        """ recibe monto que debe coincidir con el precio total de la entrega
            si resiba un nro de factura, asocia esa factura a la entrega.
            si no recibe nro de factura, crea nueva factura y la asocia a la entrega  
        """
        factura=Factura.objects.filter(numero=numero_factura)   #devuelve una lista!!!!
        if (len(factura) == 0):
            factura=Factura.objects.create(numero=numero_factura,fecha=date.today(),monto_pagado=monto)
            self.factura=factura
        else:
            self.factura=factura[0]
        self.save()


    def cobrar_con_recibo(self,monto,numero_recibo=None):
        recibo = Recibo.objects.create(entrega=self,fecha=date.today(),numero=numero_recibo,monto_pagado=monto)

    def precio_total(self):
        count = 0
        for d in self.entregadetalle_set.all():
            count += d.precio
        return count
        

class EntregaDetalle(models.Model):
    entrega = models.ForeignKey(Entrega)
    cantidad_enviada = models.PositiveIntegerField(null=True) #no va
    cantidad_entregada = models.PositiveIntegerField(null=True)
    precio= models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])
    pedido_cliente_detalle = models.ForeignKey(PedidoClienteDetalle,null=True,blank=True)
    producto_terminado = models.ForeignKey(ProductoTerminado,null=True,blank=True)

    def get_producto_terminado(self):
        if self.producto_terminado is not None:
            return self.producto_terminado
        return self.pedido_cliente_detalle.producto_terminado

    def set_precio(self):
        print "en set precio"
        self.precio=0
        # si es pedido de cambio no cobra nada
        if self.entrega.pedido.tipo_pedido == 3:
            self.precio=0
        else:
            print "recorriendo prod llevados"
            for p in self.entrega.hoja_de_ruta.productosllevados_set.all():
                print "-------->",p.producto_terminado
                if p.producto_terminado.id == self.get_producto_terminado().id:                
                    self.precio = p.precio * self.cantidad_entregada 
                    break
        self.save()



class Recibo(models.Model):
    entrega = models.ForeignKey(Entrega)
    fecha = models.DateField(auto_now_add = True)
    numero = models.PositiveIntegerField(unique=True)  #es el numero del recibo en papel
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])

    def __str__(self):
        return "%s" % ("Resibo")

    def to_string(self):
        return "Recibo"
