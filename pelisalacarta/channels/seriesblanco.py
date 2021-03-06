# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriesblanco"
__category__ = "F"
__type__ = "generic"
__title__ = "Series Blanco"
__language__ = "ES"
__thumbnail__ = "http://seriesblanco.com/imags_estilos/logofb.jpg"
__adult__ = "false"

host = "http://seriesblanco.com/"
idiomas = {'es':'Español','la':'Latino','vos':'VOS','vo':'VO','japovose':'Japones'}
logo =  "http://seriesblanco.com/imags_estilos/logofb.jpg"
fondo= "http://data.hdwallpapers.im/white_blue_background.jpg"
DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.seriesblanco mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series", action="listado", url="http://seriesblanco.com/lista_series/", thumbnail = logo , fanart= fondo))
    itemlist.append( Item( channel=__channel__, title="Novedades", action="series", url="http://seriesblanco.com/" , thumbnail = logo , fanart= fondo) )
    itemlist.append( Item( channel=__channel__, title="Series mas vistas", action="vistas", url="http://seriesblanco.com/",  thumbnail = logo , fanart= fondo ) )
    itemlist.append( Item( channel=__channel__, title="Buscar...", action="search", url=host, thumbnail = logo , fanart= fondo) )

    return itemlist

def search(item,texto):
    logger.info("[pelisalacarta.seriesblanco search texto="+texto)

    itemlist = []

    item.url = urlparse.urljoin(host,"/search.php?q1=%s" % (texto))
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)

    #<div style='float:left;width: 620px;'><div style='float:left;width: 33%;text-align:center;'><a href='/serie/20/against-the-wall.html' '><img class='ict' src='http://4.bp.blogspot.com/-LBERI18Cq-g/UTendDO7iNI/AAAAAAAAPrk/QGqjmfdDreQ/s320/Against_the_Wall_Seriesdanko.jpg' alt='Capitulos de: Against The Wall' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='/serie/20/against-the-wall.html' style='font-size: 11px;'> Against The Wall</a></div><br><br>

    patron = "<img class='ict' src='([^']+)'.*?<div style='text-align:center;line-height:20px;height:20px;'><a href='([^']+)' style='font-size: 11px;'>([^<]+)</a>"

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        
        
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=urlparse.urljoin(host,scrapedurl), action="episodios", thumbnail=scrapedthumbnail, fanart ="http://portfolio.vernier.se/files/2014/03/light-grey-wood-photography-hd-wallpaper-1920x1200-46471.jpg", show=scrapedtitle) )

    try:
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
def vistas(item):
    logger.info("pelisalacarta.seriesblanco series")
    
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)

    patron = "<div class='item-thumbnail-only'><div class='item-thumbnail'>"
    patron += "<a href='([^']+)'>.*?"
    patron += "src='([^']+)'.*?"
    patron += "title='([^<]+)' width='72'/>"

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=urlparse.urljoin(host,scrapedurl), thumbnail= scrapedthumbnail, fanart="http://portfolio.vernier.se/files/2014/03/light-grey-wood-photography-hd-wallpaper-1920x1200-46471.jpg", action="episodios", show=scrapedtitle) )

    return itemlist

def listado(item):
    logger.info("pelisalacarta.seriesblanco series")
    
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)
    
    patron = "<li><a href='([^']+)' title='([^']+)'>[^<]+</a></li>"
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl, scrapedtitle in matches:
        scrapedthumbnail = scrapertools.get_match(data,'<div id=\'fondo-cajas-seriesblanco\'>.*?<img src="..([^"]+)"')
        scrapedthumbnail=urlparse.urljoin(host,scrapedthumbnail)
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=urlparse.urljoin(host,scrapedurl), action="episodios", fanart ="http://portfolio.vernier.se/files/2014/03/light-grey-wood-photography-hd-wallpaper-1920x1200-46471.jpg", thumbnail =scrapedthumbnail, show=scrapedtitle) )
    
    return itemlist



def series(item):
    logger.info("pelisalacarta.seriesblanco series")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)
    
    patron = '<h6.*?<img src=\'([^\']+)\' width=\'25\'>'
    patron += '([^<]+).*?'
    patron += 'href="([^"]+)".*?'
    patron += 'src=\'([^\']+)\'.*?'

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedidioma, scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=urlparse.urljoin(host,scrapedurl), thumbnail= scrapedthumbnail, fanart="http://portfolio.vernier.se/files/2014/03/light-grey-wood-photography-hd-wallpaper-1920x1200-46471.jpg", action="findvideos", show=scrapedtitle ,extra = scrapedidioma) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.seriesblanco episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    

    #<a href='/serie/534/temporada-1/capitulo-00/the-big-bang-theory.html'>1x00 - Capitulo 00 </a></td><td> <img src=/banderas/vo.png border='0' height='15' width='25' /> <img src=/banderas/vos.png border='0' height='15' width='25' /></td></tr>
    patronseries = "</script></center>(.*?)</td></tbody></table><div style='clear: both;'></div>"
    matchesseries = re.compile(patronseries,re.DOTALL).findall(data)
    
    for bloque_series in matchesseries:
        if (DEBUG): logger.info("bloque_series="+bloque_series)
    # Extrae las series

        patron = "<tr><td>.*?<a href='([^']+)'>([^<]+)</a></td><td>.*?<img src=/([^']+) "

        matches = re.compile(patron,re.DOTALL).findall(bloque_series)
        scrapertools.printMatches(matches)

        for scrapedurl, scrapedtitle, scrapedidioma in matches:
            scrapedfanart = scrapertools.get_match(data,"<img id='port' src='([^']+)'")
            title = item.title + " - " + scrapedtitle
            itemlist.append( Item(channel=__channel__, title =title , url=urlparse.urljoin(host,scrapedurl), action="findvideos", thumbnail=item.thumbnail, extra =scrapedidioma, fanart=scrapedfanart, show=item.show) )

        if len(itemlist) == 0 and "<title>404 Not Found</title>" in data:
            itemlist.append( Item(channel=__channel__, title ="la url '"++"' parece no estar disponible en la web. Iténtalo más tarde." , url=item.url, action="series") )

    ## Opción "Añadir esta serie a la biblioteca de XBMC"
    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.seriesblanco findvideos")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)
    data = re.sub(r"<td class='tam12'></td></tr>","<td class='tam12'>SD</td></tr>",data)
    data = re.sub(r"<center>|</center>","",data)

    #<tr><td class='tam12'><img src='/banderas/es.png' width='30' height='20' /></td><td class='tam12'>2014-10-04</td><td class='tam12'><center><a href='/enlace/534/1/01/1445121/' rel='nofollow' target='_blank' alt=''><img src='/servidores/allmyvideos.jpg' width='80' height='25' /></a></center></td><td class='tam12'><center>Darkgames</center></td><td class='tam12'></td></tr>
    

    #<tr><td class='tam12'><img src='/banderas/es.png' width='30' height='20' /></td><td class='tam12'>2014-10-04</td><td class='tam12'><a href='/enlace/534/1/01/1444719/' rel='nofollow' target='_blank' alt=''><img src='/servidores/uploaded.jpg' width='80' height='25' /></a></td><td class='tam12'><center>Darkgames</center></td><td class='tam12'>SD</td></tr>

    patron = "<td class='tam12'><img src='/banderas/([^\.]+)\.[^']+'[^>]+></td>"
    patron+= "<td class='tam12'>([^<]+)</td>"
    patron+= "<td class='tam12'><a href='([^']+)'[^>]+>"
    patron+= "<img src='/servidores/([^\.]+)\.[^']+'[^>]+></a></td>"
    patron+= "<td class='tam12'>[^<]+</td>"
    patron+= "<td class='tam12'>([^<]+)</td>"
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedidioma, scrapedfecha, scrapedurl, scrapedservidor, scrapedcalidad in matches:
        title = "Ver en " + scrapedservidor + " [" + idiomas[scrapedidioma] + "] [" + scrapedcalidad + "] (" + scrapedfecha + ")"
        itemlist.append( Item(channel=__channel__, title =title , url=urlparse.urljoin(host,scrapedurl), action="play", thumbnail=urlparse.urljoin(host,item.extra), fanart=item.fanart, show=item.show) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.seriesblanco play url="+item.url)

    data = scrapertools.cache_page(item.url)

    patron = "<input type='button' value='Ver o Descargar' onclick='window.open\(\"([^\"]+)\"\);'/>"
    url = scrapertools.find_single_match(data,patron)

    itemlist = servertools.find_video_items(data=url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.channel = __channel__

    return itemlist    
