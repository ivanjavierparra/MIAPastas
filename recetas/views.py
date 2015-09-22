from django.shortcuts import render, redirect
from . import models
from . import forms
# Create your views here.

def get_order(get):
    if "o" in get:
        return get["o"]

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
    return mfilter

def insumos(request):
    filters = get_filtros(request.GET, models.Insumo)
    mfilters = dict(filter(lambda v: v[0] in models.Insumo.FILTROS, filters.items()))
    insumos = models.Insumo.objects.filter(**mfilters)
    if request.method == 'POST':
        form = forms.InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insumos')
    else:
        form = forms.InsumoForm()
    return render(request, "recetas/insumos.html",
                  {"insumos": insumos,
                   "filtros": filters,
                   "form": form})



def recetas(request):
    filters = get_filtros(request.GET, models.Receta)
    mfilters = dict(filter(lambda v: v[0] in models.Receta.FILTROS, filters.items()))
    recetas = models.Receta.objects.filter(**mfilters)
    if request.method == "POST":
        form = forms.RecetaForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('recetas')
    else:
        form = forms.RecetaForm()

    #recetas = models.Receta.objects.all()
    i=[]
    for r in recetas:
        z = r.insumos.all()
        for x in z:
            i.append(x)
    return render(request, "recetas/recetas.html",{"recetas": recetas,"insumos":i,"form": form})




def proveedores(request):
    filters = get_filtros(request.GET, models.Proveedor)
    mfilters = dict(filter(lambda v: v[0] in models.Proveedor.FILTROS, filters.items()))
    proveedores = models.Proveedor.objects.filter(**mfilters)
    if request.method == "POST":
        form = forms.ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = forms.ProveedorForm()

    #recetas = models.Receta.objects.all()
    i=[]



    return render(request, "recetas/proveedores.html",{"proveedores": proveedores,"form": form,"filtros":filters})

def productosTerminados(request):
    filters = get_filtros(request.GET, models.ProductoTerminado)
    mfilters = dict(filter(lambda v: v[0] in models.ProductoTerminado.FILTROS, filters.items()))
    productosTerminados = models.ProductoTerminado.objects.filter(**mfilters)
    if request.method == "POST":
        form = forms.ProductoTerminadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productosTerminados')
    else:
        form = forms.ProductoTerminadoForm()
    return render(request, "recetas/productosTerminados.html",{"productosTerminados": productosTerminados,"form": form})



def zonas(request):
    filters = get_filtros(request.GET, models.Zona)
    mfilters = dict(filter(lambda v: v[0] in models.Zona.FILTROS, filters.items()))
    zonas = models.Zona.objects.filter(**mfilters)
    if request.method == 'POST':
        form = forms.ZonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zonas')
    else:
        form = forms.ZonaForm()
    return render(request, "recetas/zonas.html",
                  {"zonas": zonas,
                   "filtros": filters,
                   "form": form})



def ciudades(request):
    filters = get_filtros(request.GET, models.Ciudad)
    mfilters = dict(filter(lambda v: v[0] in models.Ciudad.FILTROS, filters.items()))
    ciudades = models.Ciudad.objects.filter(**mfilters)
    if request.method == 'POST':
        form = forms.CiudadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ciudades')
    else:
        form = forms.CiudadForm()
    return render(request, "recetas/ciudades.html",
                  {"ciudades": ciudades,
                   "filtros": filters,
                   "form": form})



def clientes(request):
    filters = get_filtros(request.GET, models.Cliente)
    mfilters = dict(filter(lambda v: v[0] in models.Cliente.FILTROS, filters.items()))
    clientes = models.Cliente.objects.filter(**mfilters)
    if request.method == 'POST':
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = forms.ClienteForm()
    return render(request, "recetas/clientes.html",
                  {"clientes": clientes,
                   "filtros": filters,
                   "form": form})