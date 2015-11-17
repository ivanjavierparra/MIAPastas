from django import template

register = template.Library()

@register.simple_tag
def producto_id(detalle):
    if detalle.producto_terminado is not None:
        return detalle.producto_terminado.pk
    else:
        return detalle.pedido_cliente_detalle.producto_terminado.pk

@register.simple_tag
def producto_nombre(detalle):
    if detalle.producto_terminado is not None:
        return detalle.producto_terminado.nombre
    else:
        return detalle.pedido_cliente_detalle.producto_terminado.nombre

@register.simple_tag
def producto_cantidad(detalle):
    if detalle.producto_terminado is not None:
        return 0
    else:
        return detalle.pedido_cliente_detalle.cantidad_producto

@register.simple_tag
def devolver_cantidad_pedida(entrega,prod):
    for d in entrega.pedido.pedidoclientedetalle_set.all():
    	if d.producto_terminado == prod:
    		return d.cantidad_producto
    return 0

@register.simple_tag
def devolver_detalle(entrega,prod):
	for d in entrega.pedido.pedidoclientedetalle_set.all():
		if d.producto_terminado == prod:
			return d.id
	return None

@register.simple_tag
def devolver_producto(entrega,prod):
	for d in entrega.pedido.pedidoclientedetalle_set.all():
		if d.producto_terminado == prod:
			return None
	return prod.id