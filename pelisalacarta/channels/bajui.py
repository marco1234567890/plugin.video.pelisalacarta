﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para bajui
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "bajui"
__adult__ = "false"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Bajui"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[bajui.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"                , action="menupeliculas", url="http://www.bajui.com/descargas/categoria/2/peliculas",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="menuseries",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Documentales"             , action="menudocumentales",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

def menupeliculas(item):
    logger.info("[bajui.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - Novedades"        , action="peliculas"   , url=item.url,fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Películas - A-Z"              , action="peliculas"   , url=item.url+"/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    
    #<ul class="submenu2 subcategorias"><li ><a href="/descargas/subcategoria/4/br-scr-dvdscr">BR-Scr / DVDScr</a></li><li ><a href="/descargas/subcategoria/6/dvdr-full">DVDR - Full</a></li><li ><a href="/descargas/subcategoria/1/dvdrip-vhsrip">DVDRip / VHSRip</a></li><li ><a href="/descargas/subcategoria/3/hd">HD</a></li><li ><a href="/descargas/subcategoria/2/hdrip-bdrip">HDRip / BDRip</a></li><li ><a href="/descargas/subcategoria/35/latino">Latino</a></li><li ><a href="/descargas/subcategoria/5/ts-scr-cam">TS-Scr / CAM</a></li><li ><a href="/descargas/subcategoria/7/vos">VOS</a></li></ul>
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="submenu2 subcategorias">(.*?)</ul>')
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, title="Películas en "+title , action="peliculas", url=scrapedurl,fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))

    itemlist.append( Item(channel=__channel__, title="Buscar"                       , action="search"      , url="",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

def menuseries(item):
    logger.info("[bajui.py] menuseries")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series - Novedades"           , action="peliculas"        , url="http://www.bajui.com/descargas/categoria/3/series",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series - A-Z"                 , action="peliculas"        , url="http://www.bajui.com/descargas/categoria/3/series/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series - HD"                  , action="peliculas"        , url="http://www.bajui.com/descargas/subcategoria/11/hd/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                       , action="search"            , url="",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

def menudocumentales(item):
    logger.info("[bajui.py] menudocumentales")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Documentales - Novedades"         , action="peliculas"     , url="http://www.bajui.com/descargas/categoria/7/docus-y-tv",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Documentales - A-Z"               , action="peliculas"     , url="http://www.bajui.com/descargas/categoria/7/docus-y-tv/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                           , action="search"        , url="",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[bajui.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://www.bajui.com/descargas/busqueda/%s"
        item.url = item.url % texto
        itemlist.extend(peliculas(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item,paginacion=True):
    logger.info("[bajui.py] peliculas")
    url = item.url

    # Descarga la página
    data = scrapertools.cache_page(url)
    patron  = '<li id="ficha-\d+" class="ficha2[^<]+'
    patron += '<div class="detalles-ficha"[^<]+'
    patron += '<span class="nombre-det">Ficha\: ([^<]+)</span>[^<]+'
    patron += '<span class="categoria-det">[^<]+</span>[^<]+'
    patron += '<span class="descrip-det">(.*?)</span>[^<]+'
    patron += '</div>.*?<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    
    for title,plot,url,thumbnail in matches:
        scrapedtitle = title
        scrapedplot = clean_plot(plot)
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin("http://www.bajui.com/",thumbnail.replace("_m.jpg","_g.jpg"))
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="enlaces", title=scrapedtitle , fulltitle=title , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5", fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg", viewmode="movie_with_plot") )

    # Extrae el paginador
    patron = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin("http://www.bajui.com/",matches[0])
        pagitem = Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=scrapedurl,fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg")
        if not paginacion:
            itemlist.extend( peliculas(pagitem) )
        else:
            itemlist.append( pagitem )

    return itemlist

def clean_plot(scrapedplot):
    scrapedplot = scrapedplot.replace("\n","").replace("\r","")
    scrapedplot = re.compile("TÍTULO ORIGINAL[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("AÑO[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Año[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("DURACIÓN[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Duración[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("PAIS[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("PAÍS[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Pais[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("País[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("DIRECTOR[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("DIRECCIÓN[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Dirección[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("REPARTO[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Reparto[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Interpretación[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("GUIÓN[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Guión[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("MÚSICA[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Música[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("FOTOGRAFÍA[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Fotografía[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("PRODUCTORA[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Producción[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Montaje[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Vestuario[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("GÉNERO[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("GENERO[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Genero[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Género[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("PREMIOS[^<]+<br />",re.DOTALL).sub("",scrapedplot)
    
    scrapedplot = re.compile("SINOPSIS",re.DOTALL).sub("",scrapedplot)
    scrapedplot = re.compile("Sinopsis",re.DOTALL).sub("",scrapedplot)
    scrapedplot = scrapertools.htmlclean(scrapedplot)
    return scrapedplot

def enlaces(item):
    logger.info("[bajui.py] enlaces")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    
    try:
        item.plot = scrapertools.get_match(data,'<span class="ficha-descrip">(.*?)</span>')
        item.plot = clean_plot(item.plot)
    except:
        pass

    try:
        item.thumbnail = scrapertools.get_match(data,'<div class="ficha-imagen"[^<]+<img src="([^"]+)"')
        item.thumbnail = urlparse.urljoin("http://www.bajui.com/",item.thumbnail)
    except:
        pass

    '''
    <div id="enlaces-34769"><img id="enlaces-cargando-34769" src="/images/cargando.gif" style="display:none;"/></div>
    </li><li id="box-enlace-330690" class="box-enlace">
    <div class="box-enlace-cabecera">
    <div class="datos-usuario"><img class="avatar" src="images/avatars/116305_p.jpg" />Enlaces de: 
    <a class="nombre-usuario" href="/usuario/jerobien">jerobien</a> </div>
    <div class="datos-act">Actualizado: Hace 8 minutos</div>
    <div class="datos-boton-mostrar"><a id="boton-mostrar-330690" class="boton" href="javascript:mostrar_enlaces(330690,'b01de63028139fdd348d');">Mostrar enlaces</a></div>
    <div class="datos-servidores"><div class="datos-servidores-cell"><img src="/images/servidores/ul.to.png" title="uploaded.com" border="0" alt="uploaded.com" /><img src="/images/servidores/bitshare.png" title="bitshare.com" border="0" alt="bitshare.com" /><img src="/images/servidores/freakshare.net.jpg" title="freakshare.com" border="0" alt="freakshare.com" /><img src="/images/servidores/letitbit.png" title="letitbit.net" border="0" alt="letitbit.net" /><img src="/images/servidores/turbobit.png" title="turbobit.net" border="0" alt="turbobit.net" /><img src="/images/servidores/rapidgator.png" title="rapidgator.net" border="0" alt="rapidgator.net" /><img src="/images/servidores/cloudzer.png" title="clz.to" border="0" alt="clz.to" /></div></div>
    </div>
    '''

    patron  = '<div class="box-enlace-cabecera"[^<]+'
    patron += '<div class="datos-usuario"><img class="avatar" src="([^"]+)" />Enlaces[^<]+'
    patron += '<a class="nombre-usuario" href="[^"]+">([^<]+)</a[^<]+</div>[^<]+'
    patron += '<div class="datos-act">Actualizado. ([^<]+)</div>.*?'
    patron += '<div class="datos-boton-mostrar"><a id="boton-mostrar-\d+" class="boton" href="javascript.mostrar_enlaces\((\d+)\,\'([^\']+)\'[^>]+>Mostrar enlaces</a></div>[^<]+'
    patron += '<div class="datos-servidores"><div class="datos-servidores-cell">(.*?)</div></div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    logger.info("matches="+repr(matches))
    
    for thumbnail,usuario,fecha,id,id2,servidores in matches:
        #<img src="/images/servidores/bitshare.png" title="bitshare.com" border="0" alt="bitshare.com" /><img src="/images/servidores/freakshare.net.jpg" title="freakshare.com" border="0" alt="freakshare.com" /><img src="/images/servidores/rapidgator.png" title="rapidgator.net" border="0" alt="rapidgator.net" /><img src="/images/servidores/turbobit.png" title="turbobit.net" border="0" alt="turbobit.net" /><img src="/images/servidores/muchshare.png" title="muchshare.net" border="0" alt="muchshare.net" /><img src="/images/servidores/letitbit.png" title="letitbit.net" border="0" alt="letitbit.net" /><img src="/images/servidores/shareflare.png" title="shareflare.net" border="0" alt="shareflare.net" /><img src="/images/servidores/otros.gif" title="Otros servidores" border="0" alt="Otros" />
        patronservidores = '<img src="[^"]+" title="([^"]+)"'
        matches2 = re.compile(patronservidores,re.DOTALL).findall(servidores)
        lista_servidores = ""
        for servidor in matches2:
            lista_servidores = lista_servidores + servidor + ", "
        lista_servidores = lista_servidores[:-2]

        scrapedthumbnail = item.thumbnail
        #http://www.bajui.com/ajax/mostrar-enlaces.php?id=330582&code=124767d31bfbf14c3861
        scrapedurl = "http://www.bajui.com/ajax/mostrar-enlaces.php?id="+id+"&code="+id2
        scrapedplot = item.plot
        scrapedtitle="Enlaces de "+usuario+" ("+fecha+") ("+lista_servidores+")"

        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , context="4|5",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg",viewmode="movie_with_plot") )

    return itemlist
        
def findvideos(item):
    logger.info("[bajui.py] findvideos")
    
    data = scrapertools.cache_page(item.url)
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.plot = item.plot
        videoitem.thumbnail = item.thumbnail
        videoitem.fulltitle = item.fulltitle
        
        try:
            parsed_url = urlparse.urlparse(videoitem.url)
            fichero = parsed_url.path
            partes = fichero.split("/")
            titulo = partes[ len(partes)-1 ]
            videoitem.title = titulo + " - [" + videoitem.server+"]"
        except:
            videoitem.title = item.title
        
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    import time
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    menupeliculas_items = menupeliculas(mainlist_items[0])
    peliculas_items = peliculas(menupeliculas_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        lista_enlaces = enlaces(item=pelicula_item)
        for un_enlace in lista_enlaces:
            mirrors = findvideos(item=un_enlace)
            if len(mirrors)>0:
                bien = True
                break
        if bien:
            break

    return bien
