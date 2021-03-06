"""disney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
    borrar esto
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from . import views
from recetas import views as recetasviews
from django.contrib.auth.views import login,logout


urlpatterns = [



    url(r'^index/$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ayuda/$', views.ayuda, name='ayuda'),
    url(r'^documentacion/$',views.documentacion, name='documentacion'),
    url(r'^login/$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^logout/$', logout, {'template_name': 'login.html', }, name="logout"),
    url(r'^usuario/$', views.usuario,name="usuario" ),



    url(r'^signup/$', views.signup, name='signup'),
    url(r'^usuariosAdmin/$', views.usuariosAdmin, name='usuariosAdmin'),
    url(r'^usuarioEditar/(?P<usuario_id>[0-9]+)/$', views.usuarioEditar, name='usuarioEditar'),
    url(r'^usuarioCambiarClaveAjax/(?P<usuario_id>[0-9]+)/$', views.usuarioCambiarClave, name='usuarioCambiarClaveAjax'),
    url(r'^usuarios/admin/modificar/(?P<usuario_id>[0-9]+)/$',views.usuariosAdminModificar,name='usuariosAdminModificar'),
    url(r'^usuarios/admin/baja/(?P<usuario_id>[0-9]+)/$',views.usuariosAdminBaja,name='usuariosAdminBaja'),
    url(r'^usuarios/admin/modificar/quitar/grupo/(?P<usuario_id>[0-9]+)/(?P<grupo_usuario_id>[0-9]+)/$',views.usuariosAdminModificarQuitarGrupo,name='usuariosAdminModificarQuitarGrupo'),
    url(r'^usuarios/admin/modificar/agregar/grupo/(?P<usuario_id>[0-9]+)/(?P<grupo_id>[0-9]+)/$',views.usuariosAdminModificarAgregarGrupo,name='usuariosAdminModificarAgregarGrupo'),
#/(?P<password>[^/]+)   usuarioCambiarClaveMostrar
    url(r'^usuarioCambiarClave/(?P<usuario_id>[0-9]+)/$', views.usuarioCambiarClaveMostrar, name='usuarioCambiarClaveMostrar'),


    url(r'^recetasConsulta/$',views.recetasConsulta,name='recetasConsulta'),


    url(r'^clientesConsulta/$',views.clientesConsulta,name='clientesConsulta'),
    url(r'^clientesModificar/$',views.clientesModificar,name='clientesModificar'),
    url(r'^proveedoresConsulta/$',views.proveedoresConsulta,name='proveedoresConsulta'),
    url(r'^proveedoresModificar/$',views.proveedoresModificar,name='proveedoresModificar'),
    url(r'^producciones/$',views.producciones,name='producciones'),
    url(r'^produccionesAlta/$',views.produccionesAlta,name='produccionesAlta'),
    url(r'^produccionesConsulta/$',views.produccionesConsulta,name='produccionesConsulta'),
    url(r'^produccionesModificar/$',views.produccionesModificar,name='produccionesModificar'),

    url(r'^ciudadesModificar/$',views.ciudadesModificar,name='ciudadesModificar'),

    url(r'^listadoClientesMorosos/$',views.listadoClientesMorosos,name='listadoClientesMorosos'),
    url(r'^listadoClientesMorososFiltros/$',views.listadoClientesMorososFiltros,name='listadoClientesMorososFiltros'),
    url(r'^listadoClientesMorososExcel/$',views.listadoClientesMorososExcel,name='listadoClientesMorososExcel'),

    url(r'^listadoProductosTerminadosDisponibles/$',views.listadoProductosTerminadosDisponibles,name='listadoProductosTerminadosDisponibles'),
    url(r'^listadoProductosTerminadosDisponiblesFiltros/$',views.listadoProductosTerminadosDisponiblesFiltros,name='listadoProductosTerminadosDisponiblesFiltros'),
    url(r'^listadoProductosTerminadosDisponiblesExcel/$',views.listadoProductosTerminadosDisponiblesExcel,name='listadoProductosTerminadosDisponiblesExcel'),

    url(r'^listadoProductosMasVendidos/$',views.listadoProductosMasVendidos,name='listadoProductosMasVendidos'),
    url(r'^listadoProductosMasVendidosFiltros/$',views.listadoProductosMasVendidosFiltros,name='listadoProductosMasVendidosFiltros'),
    url(r'^listadoProductosMasVendidosExcel/$',views.listadoProductosMasVendidosExcel,name='listadoProductosMasVendidosExcel'),
    url(r'^listadoProductosMasVendidosGrafico/$',views.ListadoProductosMasVendidosGrafico,name='ListadoProductosMasVendidosGrafico'),
    url(r'^listadoHojasDeRutaFinalizadas/$',views.listadoHojasDeRutaFinalizadas,name='listadoHojasDeRutaFinalizadas'),

                    # Hechos en forms


    ##############################################################################################
    #                                         PDF

    url(r'^imprimir/HojaRuta/(?P<hoja_id>[0-9]+)/$',recetasviews.HojaDeRutaPdf,name='imprimirHojaRuta'),
    url(r'^imprimir/LotesHojaRuta/(?P<hoja_id>[0-9]+)/$',recetasviews.LotesHojaRutaPdf,name='imprimirLotesHojaRuta'),




    #############################################################################################

    url(r'^choferes/$',recetasviews.choferes,name='choferes'),
    url(r'^choferes/(?P<chofer_id>[0-9]+)/$',recetasviews.choferes,name='choferConsulta'),
    url(r'^choferes/alta/$',recetasviews.choferesAlta,name='choferesAlta'),
    url(r'^choferes/modificar/(?P<chofer_id>[0-9]+)/$',recetasviews.choferesModificar,name='choferModificar'),
    url(r'^choferes/baja/(?P<chofer_id>[0-9]+)/$',recetasviews.choferesBaja,name='choferesBaja'),
    url(r'^choferesAltaAjax/$',recetasviews.choferesAltaAjax,name='choferesAltaAjax'),


    url(r'^recetas/$',recetasviews.recetas,name='recetas'),
    url(r'^recetas/alta/$',recetasviews.recetasAlta,name='recetasAlta'),
    url(r'^recetas/(?P<receta_id>[0-9]+)/$',recetasviews.recetas,name='recetaConsulta'),
    url(r'^recetas/modificar/(?P<receta_id>[0-9]+)/$',recetasviews.recetasModificar,name='recetaModificar'),
    url(r'^recetas/baja/(?P<receta_id>[0-9]+)/$',recetasviews.recetasBaja,name='recetasBaja'),

    url(r'^lotes/$',recetasviews.lotes,name='lotes'),
    url(r'^lotes/alta/$',recetasviews.lotesAlta,name='lotesAlta'),
    url(r'^lotes/(?P<lote_id>[0-9]+)/$',recetasviews.lotes,name='loteConsulta'),
    url(r'^lotes/modificar/(?P<lote_id>[0-9]+)/$',recetasviews.lotesModificar,name='loteModificar'),
    url(r'^lotes/perdidaStock/$',recetasviews.perdidasStockLotes,name='perdidaStock'),


    url(r'^insumos/$',recetasviews.insumos,name='insumos'),
    url(r'^insumos/alta/$',recetasviews.insumosAlta,name='insumosAlta'),
    url(r'^insumos/(?P<insumo_id>[0-9]+)/$',recetasviews.insumos,name='insumoConsulta'),
    url(r'^insumos/modificar/(?P<insumo_id>[0-9]+)/$',recetasviews.insumosModificar,name='insumoModificar'),
    url(r'^insumos/baja/(?P<insumo_id>[0-9]+)/$',recetasviews.insumosBaja,name='insumosBaja'),


    url(r'^insumos/modificarStock/$',recetasviews.insumosModificarStock,name='ModificarStockInsumos'),
    url(r'^datosInsumo/(?P<insumo_id>[0-9]+)/$',recetasviews.datosInsumo,name='datosInsumo'),


    url(r'^zonas/$',recetasviews.zonas,name='zonas'),
    url(r'^zonas/alta/$',recetasviews.zonasAlta,name='zonasAlta'),
    url(r'^zonas/(?P<zona_id>[0-9]+)/$',recetasviews.zonas,name='zonaConsulta'),
    url(r'^zonas/modificar/(?P<zona_id>[0-9]+)/$',recetasviews.zonasModificar,name='zonaModificar'),
    url(r'^zonas/baja/(?P<zona_id>[0-9]+)/$',recetasviews.zonasBaja,name='zonasBaja'),


    url(r'^clientes/$',recetasviews.clientes,name='clientes'),
    url(r'^clientes/alta/$',recetasviews.clientesAlta,name='clientesAlta'),
    url(r'^clientes/(?P<cliente_id>[0-9]+)/$',recetasviews.clientes,name='clienteConsulta'),
    url(r'^clientes/modificar/(?P<cliente_id>[0-9]+)/$',recetasviews.clientesModificar,name='clienteModificar'),
    url(r'^clientes/baja/(?P<cliente_id>[0-9]+)/$',recetasviews.clientesBaja,name='clienteBaja'),

    url(r'^ciudades/$',recetasviews.ciudades,name='ciudades'),
    url(r'^ciudades/alta/$',recetasviews.ciudadesAlta,name='ciudadesAlta'),
    url(r'^ciudades/(?P<ciudad_id>[0-9]+)/$',recetasviews.ciudades,name='ciudadConsulta'),
    url(r'^ciudades/modificar/(?P<ciudad_id>[0-9]+)/$',recetasviews.ciudadesModificar,name='ciudadModificar'),
    url(r'^ciudades/baja/(?P<ciudad_id>[0-9]+)/$',recetasviews.ciudadesBaja,name='ciudadesBaja'),
    #falta producto

    url(r'^productosTerminados/$',recetasviews.productosTerminados,name='productosTerminados'),
    url(r'^productosTerminados/alta/$',recetasviews.productosTerminadosAlta,name='productosTerminadosAlta'),
    url(r'^productosTerminados/(?P<producto_id>[0-9]+)/$',recetasviews.productosTerminados,name='productosTerminadosConsulta'),
    url(r'^productosTerminados/modificar/(?P<producto_id>[0-9]+)/$',recetasviews.productosTerminadosModificar,name='productosTerminadosModificar'),
    url(r'^productosTerminados/baja/(?P<producto_id>[0-9]+)/$',recetasviews.productosTerminadosBaja,name='productosTerminadosBaja'),
    url(r'^productosTerminadosAltaAjax/(?P<producto_id>[0-9]+)/$',recetasviews.productosTerminadosAltaAjax,name='productosTerminadosAltaAjax'),

    url(r'^productosTerminadosActualizarStock/(?P<lote_id>[0-9]+)/$',recetasviews.loteStock,name='productosTerminadosActualizarStock'),

    url(r'^rendicionReparto/(?P<hoja_id>[0-9]+)/$',recetasviews.rendicionReparto,name='rendicionReparto'),
    url(r'^rendicionHojasDeRutas/$',recetasviews.rendicionHojasDeRutas,name='rendicionHojasDeRutas'), #este llama al de arriba "rendicionReparto$"

                # FIN PRIMERA ENTREGA

    url(r'^cobrarCliente/$',recetasviews.cobrarCliente,name='cobrarCliente'),
    url(r'^cobrarCliente/cobrarSaldo/$',recetasviews.cobrarClienteClasificar,name='cobrarClienteClasificar'),
    url(r'^cobrarCliente/facturar/$',recetasviews.cobrarClienteFacturar,name='cobrarClienteFacturar'),
    url(r'^cobrarCliente/Filtrado/(?P<cliente_id>[0-9]+)/$',recetasviews.cobrarClienteFiltrado,name='cobrarClienteFiltrado'),
    url(r'^cobrarCliente/mostrarRecibos/$',recetasviews.cobrarClienteMostrarRecibos,name='cobrarClienteMostrarRecibos'),
    url(r'^cobrarCliente/facturas/$',recetasviews.getFacturas,name='getFacturas'),
    url(r'^cobrarCliente/recibos/$',recetasviews.getRecibos,name='getRecibos'),



                # INICIO SEGUNDA ENTREGA

    url(r'^proveedores/$',recetasviews.proveedores,name='proveedores'),
    url(r'^proveedoresAlta/$',recetasviews.proveedoresAlta,name='proveedoresAlta'),

    url(r'^pedidosProveedor/$',recetasviews.pedidosProveedor,name='pedidosProveedor'),
    url(r'^pedidosProveedor/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosProveedor,name='pedidosProveedorConsulta'),
    url(r'^pedidosProveedor/alta/$',recetasviews.pedidosProveedorAlta,name='pedidosProveedorAlta'),

    url(r'^pedidosProveedor/modificar/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosProveedorModificar,name='pedidosProveedorModificar'),
    url(r'^pedidosProveedor/baja/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosProveedorBaja,name='pedidosProveedorBaja'),
    url(r'^pedidosProveedor/recepcionar/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosProveedorRecepcionar,name='pedidosProveedorRecepcionar'),
    url(r'^pedidosProveedor/cancelar/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosProveedorCancelar,name='pedidosProveedorCancelar'),
                # FIN SEGUNDA ENTREGA
    #url(r'^ciudades/add$',recetasviews.ciudades,name='ciudadesAlta'),
    #url(r'^clientes$',recetasviews.clientes,name='clientes'),
    #url(r'^clientes/add$',recetasviews.clientes,name='clientesAlta'),


     url(r'^hojaDeRuta/$',recetasviews.hojaDeRuta,name='hojaDeRuta'),
     url(r'^hojaDeRuta/generarTotales/$',recetasviews.generarTotales,name='generarTotales'),
     url(r'^hojaDeRuta/alta/$',recetasviews.hojaDeRutaAlta,name='hojaDeRutaAlta'),
     url(r'^hojaDeRuta/mostrarRecibos/(?P<hoja_id>[0-9]+)/$',recetasviews.HojaDeRutaMostrar,name='HojaDeRutaMostrar'),

     url(r'^rendicionDeReparto/mostrar/(?P<hoja_id>[0-9]+)/$',recetasviews.RendicionDeRepartoMostrar,name='rendicionDeRepartoMostrar'),
     url(r'^rendicionDeReparto/mostrar/sinCobrar/$',recetasviews.rendicionHojasDeRutasSinCobrar,name='rendicionHojasDeRutasSinCobrar'),





    url(r'^proveedores/Baja/(?P<proveedor_id>[0-9]+)/$',recetasviews.proveedoresBaja,name='proveedoresBaja'),
    #url(r'^proveedoresBaja/(?P<proveedor_id>[0-9]+)/$',recetasviews.proveedoresBaja,name='proveedoresBaja'),
    url(r'^proveedores/Consulta/(?P<proveedor_id>[0-9]+)/$',recetasviews.proveedores,name='proveedoresConsulta'),
    url(r'^proveedores/Modificar/(?P<proveedor_id>[0-9]+)/$',recetasviews.proveedoresModificar,name='proveedoresModificar'),
    url(r'^proveedores/Alta$',recetasviews.proveedoresAlta,name='proveedoresAlta'),
    url(r'^proveedores/(?P<proveedor_id>[0-9]+)/$',recetasviews.proveedores,name='proveedoresID'),
    url(r'^proveedores/$',recetasviews.proveedores,name='proveedores'),

    url(r'^pedidosCliente/$',recetasviews.pedidosClientes,name='pedidosCliente'),
    url(r'^pedidosCliente/Consulta/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosClientes,name='pedidoClienteConsulta'),
    url(r'^pedidosCliente/Alta/(?P<tipo_pedido_id>[0-9]+)/$',recetasviews.pedidosClientesAlta,name='pedidosClientesAlta'),
    url(r'^pedidosCliente/Baja/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosClienteBaja,name='pedidosClienteBaja'),
    url(r'^pedidosCliente/Modificar/(?P<pedido_id>[0-9]+)/$',recetasviews.pedidosClienteModificar,name='pedidosClienteModificar'),



    url(r'^recetasConsulta$',views.recetasConsulta,name='recetasConsulta'),
    url(r'^clientesConsulta$',views.clientesConsulta,name='clientesConsulta'),
    #url(r'^clientesAlta$',views.clientesAlta,name='clientesAlta'),
    url(r'^clientesModificar$',views.clientesModificar,name='clientesModificar'),
    url(r'^producciones$',views.producciones,name='producciones'),
    url(r'^produccionesAlta$',views.produccionesAlta,name='produccionesAlta'),
    url(r'^produccionesConsulta$',views.produccionesConsulta,name='produccionesConsulta'),
    url(r'^produccionesModificar$',views.produccionesModificar,name='produccionesModificar'),

    url(r'^ciudadesModificar$',views.ciudadesModificar,name='ciudadesModificar'),
    url(r'^insumosConsulta/$',views.insumosConsulta,name='insumosConsulta'),
    url(r'^insumosModificar$',views.insumosModificar,name='insumosModificar'),
    # url(r'^zonas$',views.zonas,name='zonas'),
    #url(r'^zonasAlta$',views.zonasAlta,name='zonasAlta'),
    url(r'^zonasConsulta$',views.zonasConsulta,name='zonasConsulta'),
    url(r'^zonasModificar$',views.zonasModificar,name='zonasMoficar'),
    url(r'^hojaDeRuta/$',views.hojaDeRuta,name='hojaDeRuta'),
    #url(r'^productosTerminadosAlta$',views.productosTerminadosAlta,name='productosTerminadosAlta'),
    url(r'^productosTerminadosModificar$',views.productosTerminadosModificar,name='productosTerminadosModificar'),
    url(r'^productosTerminadosActualizarPrecio$',views.productosTerminadosActualizarPrecio,name='productosTerminadosActualizarPrecio'),
    url(r'^productos_mas_vendidos.png$',recetasviews.productosMasVendidos,name='productosMasVendidos'),



    url(r'^$', login, {'template_name': 'login.html', }, name="login"),

]
