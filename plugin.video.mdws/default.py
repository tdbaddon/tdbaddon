# -*- coding: utf-8 -*-
import sys
l1ll1l1Fuck_You_Anonymous = sys.version_info [0] == 2
l111l11Fuck_You_Anonymous = 2048
l1llllFuck_You_Anonymous = 7
def l11l11Fuck_You_Anonymous (llFuck_You_Anonymous):
    global l111lFuck_You_Anonymous
    l111lllFuck_You_Anonymous = ord (llFuck_You_Anonymous [-1])
    l1llll1Fuck_You_Anonymous = llFuck_You_Anonymous [:-1]
    l1lllFuck_You_Anonymous = l111lllFuck_You_Anonymous % len (l1llll1Fuck_You_Anonymous)
    l1ll1Fuck_You_Anonymous = l1llll1Fuck_You_Anonymous [:l1lllFuck_You_Anonymous] + l1llll1Fuck_You_Anonymous [l1lllFuck_You_Anonymous:]
    if l1ll1l1Fuck_You_Anonymous:
        l1l1l1lFuck_You_Anonymous = unicode () .join ([unichr (ord (char) - l111l11Fuck_You_Anonymous - (l11l1lFuck_You_Anonymous + l111lllFuck_You_Anonymous) % l1llllFuck_You_Anonymous) for l11l1lFuck_You_Anonymous, char in enumerate (l1ll1Fuck_You_Anonymous)])
    else:
        l1l1l1lFuck_You_Anonymous = str () .join ([chr (ord (char) - l111l11Fuck_You_Anonymous - (l11l1lFuck_You_Anonymous + l111lllFuck_You_Anonymous) % l1llllFuck_You_Anonymous) for l11l1lFuck_You_Anonymous, char in enumerate (l1ll1Fuck_You_Anonymous)])
    return eval (l1l1l1lFuck_You_Anonymous)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,itertools,re,sys,shutil,urlresolver
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
# Watchseries - By Mucky Duck (03/2015)
l11ll1lFuck_You_Anonymous = xbmcaddon.Addon().getAddonInfo(l11l11Fuck_You_Anonymous (u"ࠫ࡮ࡪࠧࠀ"))
l11lll1Fuck_You_Anonymous = Addon(l11ll1lFuck_You_Anonymous, sys.argv)
l1lll11Fuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_name()
l11llllFuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_path()
md = md(l11ll1lFuck_You_Anonymous, sys.argv)
l1ll11Fuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_setting(l11l11Fuck_You_Anonymous (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࠪࠁ"))
l1l1lFuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_setting(l11l11Fuck_You_Anonymous (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥࡦࡢࡸࡶࠫࠂ"))
l11llFuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_setting(l11l11Fuck_You_Anonymous (u"ࠧࡢࡦࡧࡣࡸ࡫ࡴࠨࠃ"))
l11111lFuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_setting(l11l11Fuck_You_Anonymous (u"ࠨࡧࡱࡥࡧࡲࡥࡠ࡯ࡨࡸࡦࡥࡳࡦࡶࠪࠄ"))
l111l1Fuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_setting(l11l11Fuck_You_Anonymous (u"ࠩࡨࡲࡦࡨ࡬ࡦࡡࡵࡩࡸࡵ࡬ࡷࡧࡵࡣࡸ࡫ࡴࠨࠅ"))
l11Fuck_You_Anonymous = md.get_art()
l1111lFuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_icon()
l1l1llFuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_fanart()
l1l1Fuck_You_Anonymous =  l11lll1Fuck_You_Anonymous.get_setting(l11l11Fuck_You_Anonymous (u"ࠪࡦࡦࡹࡥࡠࡷࡵࡰࠬࠆ"))
reload(sys)
sys.setdefaultencoding(l11l11Fuck_You_Anonymous (u"ࠦࡺࡺࡦ࠮࠺ࠥࠇ"))
def l1111l1Fuck_You_Anonymous():
	md.addDir({l11l11Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࠪࠈ"):l11l11Fuck_You_Anonymous (u"࠭࠴ࠨࠉ"), l11l11Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬࠊ"):l11l11Fuck_You_Anonymous (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡾ࡫࡬࡭ࡱࡺࡡࡆ࠳࡚࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࠋ"), l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ࠌ"):l1l1Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠪ࠳ࡱ࡫ࡴࡵࡧࡵࡷ࠴ࡇࠧࠍ")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠫ࡮ࡩ࡯࡯ࠩࠎ"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠬࡳࡤࡸࡵ࠱ࡴࡳ࡭ࠧࠏ")})
	md.addDir({l11l11Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫࠐ"):l11l11Fuck_You_Anonymous (u"ࠧࡴࡧࡤࡶࡨ࡮ࠧࠑ"), l11l11Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ࠒ"):l11l11Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡿࡥ࡭࡮ࡲࡻࡢ࡙ࡥࡢࡴࡦ࡬ࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࠓ"), l11l11Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࠔ"):l11l11Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࠕ")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠬ࡯ࡣࡰࡰࠪࠖ"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"࠭࡭ࡥࡹࡶ࠲ࡵࡴࡧࠨࠗ")})
	md.addDir({l11l11Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬ࠘"):l11l11Fuck_You_Anonymous (u"ࠨ࠸ࠪ࠙"), l11l11Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࠚ"):l11l11Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡹࡦ࡮࡯ࡳࡼࡣࡔࡗࠢࡖࡧ࡭࡫ࡤࡶ࡮ࡨ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩࠛ"), l11l11Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࠜ"):l1l1Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠬ࠵ࡴࡷࡵࡦ࡬ࡪࡪࡵ࡭ࡧࠪࠝ")}, fan_art={l11l11Fuck_You_Anonymous (u"࠭ࡩࡤࡱࡱࠫࠞ"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠧ࡮ࡦࡺࡷ࠳ࡶ࡮ࡨࠩࠟ")})
	if l1l1lFuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"ࠨࡶࡵࡹࡪ࠭ࠠ"):
		md.addDir({l11l11Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧࠡ"): l11l11Fuck_You_Anonymous (u"ࠪࡪࡪࡺࡣࡩࡡࡩࡥࡻࡹࠧࠢ"), l11l11Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩࠣ"):l11l11Fuck_You_Anonymous (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡿࡥ࡭࡮ࡲࡻࡢࡡࡂ࡞ࡏࡼࠤࡋࡧࡶࡰࡷࡵ࡭ࡹ࡫ࡳ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࠤ"), l11l11Fuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪࠥ"):l11l11Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫࠦ")})
	md.addDir({l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࠧ"):l11l11Fuck_You_Anonymous (u"ࠩ࠺ࠫࠨ"), l11l11Fuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࠩ"):l11l11Fuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡺࡧ࡯ࡰࡴࡽ࡝ࡕࡘࠣࡗ࡭ࡵࡷࡴࠢ࡜ࡩࡦࡸࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࠪ"), l11l11Fuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࠫ"):l1l1Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"࠭࠯ࡺࡧࡤࡶࡸ࠵࠲࠱࠳࠺ࠫࠬ")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠧࡪࡥࡲࡲࠬ࠭"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡧࡻࡸ࠴ࡰ࡯ࡩࠪ࠮")})
	md.addDir({l11l11Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧ࠯"):l11l11Fuck_You_Anonymous (u"ࠪ࠹ࠬ࠰"), l11l11Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩ࠱"):l11l11Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡻࡨࡰࡱࡵࡷ࡞ࡖ࡙ࠤࡘ࡮࡯ࡸࡵࠣࡋࡪࡴࡲࡦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨ࠲"), l11l11Fuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪ࠳"):l1l1Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠧ࠰ࡩࡨࡲࡷ࡫ࡳ࠰ࡣࡦࡸ࡮ࡵ࡮ࠨ࠴")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠨ࡫ࡦࡳࡳ࠭࠵"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠩࡰࡨࡼࡹ࠮ࡱࡰࡪࠫ࠶")})
	md.addDir({l11l11Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨ࠷"):l11l11Fuck_You_Anonymous (u"ࠫ࠶࠭࠸"), l11l11Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪ࠹"):l11l11Fuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡼࡩࡱࡲ࡯ࡸ࡟ࡑࡩࡼ࡫ࡳࡵࠢࡈࡴ࡮ࡹ࡯ࡥࡧࡶࠤࡆࡪࡤࡦࡦ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨ࠺"), l11l11Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ࠻"):l1l1Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠨ࠱࡯ࡥࡹ࡫ࡳࡵࠩ࠼"), l11l11Fuck_You_Anonymous (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪ࠽"):l11l11Fuck_You_Anonymous (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࡷࠬ࠾")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠫ࡮ࡩ࡯࡯ࠩ࠿"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠬࡳࡤࡸࡵ࠱ࡴࡳ࡭ࠧࡀ")})
	md.addDir({l11l11Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫࡁ"):l11l11Fuck_You_Anonymous (u"ࠧ࠲ࠩࡂ"), l11l11Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ࡃ"):l11l11Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡿࡥ࡭࡮ࡲࡻࡢ࡚ࡨࡪࡵ࡛ࠣࡪ࡫࡫࡝ࠩࡶࠤࡕࡵࡰࡶ࡮ࡤࡶࠥࡋࡰࡪࡵࡲࡨࡪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬࡄ"), l11l11Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࡅ"):l1l1Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠫ࠴ࡴࡥࡸࠩࡆ"), l11l11Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࡇ"):l11l11Fuck_You_Anonymous (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࡳࠨࡈ")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠧࡪࡥࡲࡲࠬࡉ"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡧࡻࡸ࠴ࡰ࡯ࡩࠪࡊ")})
	if l111l1Fuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"ࠩࡷࡶࡺ࡫ࠧࡋ"):
		md.addDir({l11l11Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨࡌ"):l11l11Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࡳࡧࡶࡳࡱࡼࡥࡳࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠫࡍ"), l11l11Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪࡎ"):l11l11Fuck_You_Anonymous (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡹࡦ࡮࡯ࡳࡼࡣ࡛ࡃ࡟ࡘࡶࡱࡘࡥࡴࡱ࡯ࡺࡪࡸࠠࡔࡧࡷࡸ࡮ࡴࡧࡴ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧࡏ"), l11l11Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫࡐ"):l11l11Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬࡑ")}, is_folder=False, is_playable=False)
        if l11llFuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"ࠩࡷࡶࡺ࡫ࠧࡒ"):
		md.addDir({l11l11Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨࡓ"):l11l11Fuck_You_Anonymous (u"ࠫࡦࡪࡤࡰࡰࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬࡔ"), l11l11Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪࡕ"):l11l11Fuck_You_Anonymous (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡹࡦ࡮࡯ࡳࡼࡣ࡛ࡃ࡟ࡄࡨࡩ࠳࡯࡯ࠢࡖࡩࡹࡺࡩ࡯ࡩࡶ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩࡖ"), l11l11Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫࡗ"):l11l11Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬࡘ")}, is_folder=False, is_playable=False)
	if l1ll11Fuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"ࠩࡷࡶࡺ࡫࡙ࠧ"):
		if l11111lFuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"ࠪࡸࡷࡻࡥࠨ࡚"):
			md.addDir({l11l11Fuck_You_Anonymous (u"ࠫࡲࡵࡤࡦ࡛ࠩ"):l11l11Fuck_You_Anonymous (u"ࠬࡳࡥࡵࡣࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬ࡜"), l11l11Fuck_You_Anonymous (u"࠭࡮ࡢ࡯ࡨࠫ࡝"):l11l11Fuck_You_Anonymous (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡺࡧ࡯ࡰࡴࡽ࡝࡜ࡄࡠࡑࡪࡺࡡࠡࡕࡨࡸࡹ࡯࡮ࡨࡵ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࡞"), l11l11Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬ࡟"):l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ࡠ")}, is_folder=False, is_playable=False)
        l1111Fuck_You_Anonymous()
        l111ll1Fuck_You_Anonymous()
	setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠪࡪ࡮ࡲࡥࡴࠩࡡ"), l11l11Fuck_You_Anonymous (u"ࠫࡲ࡫࡮ࡶ࠯ࡹ࡭ࡪࡽࠧࡢ"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l1Fuck_You_Anonymous(url,title,l1l11Fuck_You_Anonymous,content):
	link = open_url(url).content
	if l1l11Fuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"ࠬ࠼ࠧࡣ"):
		link = md.regex_get_all(link, title, l11l11Fuck_You_Anonymous (u"࠭࠼ࡶ࡮ࠣࡧࡱࡧࡳࡴ࠿ࠥࡸࡦࡨࡳࠣࡀࠪࡤ"))
	l1lllllFuck_You_Anonymous = md.regex_get_all(str(link), l11l11Fuck_You_Anonymous (u"ࠧࠣ࡮࡬ࡷࡹ࡯࡮ࡨࡵࠥࡂࠬࡥ"), l11l11Fuck_You_Anonymous (u"ࠨ࠾࠲ࡹࡱࡄࠧࡦ"))
	l1ll11lFuck_You_Anonymous = md.regex_get_all(str(l1lllllFuck_You_Anonymous), l11l11Fuck_You_Anonymous (u"ࠩ࠿ࡰ࡮࠭ࡧ"), l11l11Fuck_You_Anonymous (u"ࠪࡀ࠴ࡲࡩࠨࡨ"))
	items = len(l1ll11lFuck_You_Anonymous)
	for a in l1ll11lFuck_You_Anonymous:
		name = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠫࡹ࡯ࡴ࡭ࡧࡀࠦࠬࡩ"), l11l11Fuck_You_Anonymous (u"ࠬࠨࠧࡪ")).replace(l11l11Fuck_You_Anonymous (u"ࠨ࡜࡝ࠩࠥ࡫"),l11l11Fuck_You_Anonymous (u"ࠢࠨࠤ࡬"))
		name = l11lll1Fuck_You_Anonymous.unescape(name)
		url = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠨࡪࡵࡩ࡫ࡃࠢࠨ࡭"), l11l11Fuck_You_Anonymous (u"ࠩࠥࠫ࡮"))
		if l11l11Fuck_You_Anonymous (u"ࠪ࡮ࡦࡼࡡࡴࡥࡵ࡭ࡵࡺ࠺ࠨ࡯") in url:
                        url = md.regex_get_all(a, l11l11Fuck_You_Anonymous (u"ࠫ࡭ࡸࡥࡧ࠿ࠥࠫࡰ"), l11l11Fuck_You_Anonymous (u"ࠬࠨࠧࡱ"), True)[1]
                if l11l11Fuck_You_Anonymous (u"࠭ࡪࡢࡸࡤࡷࡨࡸࡩࡱࡶ࠽ࠫࡲ") in url:
                        url = md.regex_get_all(a, l11l11Fuck_You_Anonymous (u"ࠧࡩࡴࡨࡪࡂࠨࠧࡳ"), l11l11Fuck_You_Anonymous (u"ࠨࠤࠪࡴ"), True)[2]
		l1ll1lFuck_You_Anonymous = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠩࡶࡶࡨࡃࠢࠨࡵ"), l11l11Fuck_You_Anonymous (u"ࠪࠦࠬࡶ"))
                if not l1ll1lFuck_You_Anonymous:
                        l1ll1lFuck_You_Anonymous = l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠫࡲࡪࡷࡴ࠰ࡳࡲ࡬࠭ࡷ")
		if l1l1Fuck_You_Anonymous not in url:
			url = l1l1Fuck_You_Anonymous + url
		if content == l11l11Fuck_You_Anonymous (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࠧࡸ"):
			info = name.split(l11l11Fuck_You_Anonymous (u"࠭࠭ࠡࡕࡨࡥࡸࡵ࡮ࠨࡹ"))
			title = info[0].strip()
			try:
                                sep = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠧ࠽ࡤࡵ࠳ࡃ࠭ࡺ"), l11l11Fuck_You_Anonymous (u"ࠨ࠾ࡥࡶ࠴ࡄࠧࡻ"))
                                l11l1llFuck_You_Anonymous = sep.split(l11l11Fuck_You_Anonymous (u"ࠩࡈࡴ࡮ࡹ࡯ࡥࡧࠪࡼ"))[1]
                                l11l111Fuck_You_Anonymous = sep.split(l11l11Fuck_You_Anonymous (u"ࠪࡉࡵ࡯ࡳࡰࡦࡨࠫࡽ"))[0]
                        except:
                                l11l111Fuck_You_Anonymous = info[1].split(l11l11Fuck_You_Anonymous (u"ࠫࡊࡶࡩࡴࡱࡧࡩࠬࡾ"))[0]
                                l11l1llFuck_You_Anonymous = info[1].split(l11l11Fuck_You_Anonymous (u"ࠬࡋࡰࡪࡵࡲࡨࡪ࠭ࡿ"))[1].split(l11l11Fuck_You_Anonymous (u"࠭࠭ࠨࢀ"))[0]
                        md.remove_punctuation(title)
                        md.addDir({l11l11Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬࢁ"):l11l11Fuck_You_Anonymous (u"ࠨ࠺ࠪࢂ"),l11l11Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࢃ"):l11l11Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝ࡆࡓࡑࡕࡒࠡࡻࡨࡰࡱࡵࡷ࡞࡝ࡌࡡࠥ࠳ࠠࡔࡧࡤࡷࡴࡴࠠࠦࡵ࡞࠳ࡎࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬࢄ") %(title,info[1]),
				   l11l11Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࢅ"):url, l11l11Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࢆ"):content, l11l11Fuck_You_Anonymous (u"࠭ࡴࡪࡶ࡯ࡩࠬࢇ"):title, l11l11Fuck_You_Anonymous (u"ࠧࡴࡧࡤࡷࡴࡴࠧ࢈"):l11l111Fuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠨ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠫࢉ"):l1ll1lFuck_You_Anonymous,
                                   l11l11Fuck_You_Anonymous (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࠪࢊ"):l11l1llFuck_You_Anonymous}, {l11l11Fuck_You_Anonymous (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪ࠭ࢋ"):title, l11l11Fuck_You_Anonymous (u"ࠫࡸ࡫ࡡࡴࡱࡱࠫࢌ"):l11l111Fuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪ࠭ࢍ"):l11l1llFuck_You_Anonymous},
                                  fan_art={l11l11Fuck_You_Anonymous (u"࠭ࡩࡤࡱࡱࠫࢎ"):l1ll1lFuck_You_Anonymous}, item_count=items)
		else:
			if l1l11Fuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"ࠧ࠵ࠩ࢏"):
				l11ll11Fuck_You_Anonymous = {}
			else:
				l11ll11Fuck_You_Anonymous = {l11l11Fuck_You_Anonymous (u"ࠨࡵࡲࡶࡹࡺࡩࡵ࡮ࡨࠫ࢐"):name}
			md.remove_punctuation(name)
			md.addDir({l11l11Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧ࢑"):l11l11Fuck_You_Anonymous (u"ࠪ࠶ࠬ࢒"), l11l11Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩ࢓"):l11l11Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨ࢔") %name, l11l11Fuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪ࢕"):url,
				   l11l11Fuck_You_Anonymous (u"ࠧࡵ࡫ࡷࡰࡪ࠭࢖"):title, l11l11Fuck_You_Anonymous (u"ࠨ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠫࢗ"):l1ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪ࢘"):content},
				  l11ll11Fuck_You_Anonymous, fan_art={l11l11Fuck_You_Anonymous (u"ࠪ࡭ࡨࡵ࡮ࠨ࢙"):l1ll1lFuck_You_Anonymous}, item_count=items)
	try:
                l1l11llFuck_You_Anonymous = re.compile(l11l11Fuck_You_Anonymous (u"ࠫࡁࡲࡩࠡࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭ࡡ࡞ࠣ࡟࠮࠭ࠧࡄࡎࡦࡺࡷࠤࡕࡧࡧࡦ࠾࠲ࡥࡃࡂ࠯࡭࡫ࡁ࢚ࠫ")).findall(link)[0]
                md.addDir({l11l11Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧ࢛ࠪ"):l11l11Fuck_You_Anonymous (u"࠭࠱ࠨ࢜"),l11l11Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬ࢝"):l11l11Fuck_You_Anonymous (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡻࡨࡰࡱࡵࡷ࡞࡝ࡅࡡࡠࡏ࡝࠿ࡀࡑࡩࡽࡺࠠࡑࡣࡪࡩࡃࡄ࠾࡜࠱ࡌࡡࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ࢞"), l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭࢟"):l1l11llFuck_You_Anonymous,
			   l11l11Fuck_You_Anonymous (u"ࠪࡸ࡮ࡺ࡬ࡦࠩࢠ"):title, l11l11Fuck_You_Anonymous (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࢡ"):content, l11l11Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࡢ࡭ࡩ࠭ࢢ"):l1l11Fuck_You_Anonymous}, fan_art={l11l11Fuck_You_Anonymous (u"࠭ࡩࡤࡱࡱࠫࢣ"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠧ࡮ࡦࡺࡷ࠳ࡶ࡮ࡨࠩࢤ")})
        except:pass
	if content == l11l11Fuck_You_Anonymous (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࢥ"):
		setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࢦ"), l11l11Fuck_You_Anonymous (u"ࠪࡷ࡭ࡵࡷ࠮ࡸ࡬ࡩࡼ࠭ࢧ"))
	elif content == l11l11Fuck_You_Anonymous (u"ࠫࡪࡶࡩࡴࡱࡧࡩࡸ࠭ࢨ"):
		setView(l11ll1lFuck_You_Anonymous,l11l11Fuck_You_Anonymous (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࠧࢩ"), l11l11Fuck_You_Anonymous (u"࠭ࡥࡱ࡫࠰ࡺ࡮࡫ࡷࠨࢪ"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l1111llFuck_You_Anonymous(url,title):
	link = open_url(url).content
	match = re.compile(l11l11Fuck_You_Anonymous (u"ࠧ࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠤ࡮ࡺࡥ࡮ࡲࡵࡳࡵࡃࠢࡶࡴ࡯ࠦࡃࡂࡳࡱࡣࡱࠤ࡮ࡺࡥ࡮ࡲࡵࡳࡵࡃࠢ࡯ࡣࡰࡩࠧࡄࠨ࡜ࡠ࠿ࡂࡢ࠰ࠩ࠽࠱ࡶࡴࡦࡴ࠾ࠨࢫ")).findall(link)
	items = len(match)
	try:
		l1ll1lFuck_You_Anonymous = re.compile(l11l11Fuck_You_Anonymous (u"ࠨ࠾ࡰࡩࡹࡧࠠࡱࡴࡲࡴࡪࡸࡴࡺ࠿ࠥࡳ࡬ࡀࡩ࡮ࡣࡪࡩࠧࠦࡣࡰࡰࡷࡩࡳࡺ࠽ࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠣ࠳ࡃ࠭ࢬ")).findall(link)[0]
	except:
		l1ll1lFuck_You_Anonymous = l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠩࡰࡨࡼࡹ࠮ࡱࡰࡪࠫࢭ")
	try:
		year = re.compile(l11l11Fuck_You_Anonymous (u"ࠪ࡬ࡷ࡫ࡦ࠾࠰࠭ࡃ࠴ࡿࡥࡢࡴࡶ࠳࠳࠰࠿࠿ࠪ࡞ࡢࡁࡄ࡝ࠫࠫ࠿࠳ࡦࡄ࠼࠰ࡵࡳࡥࡳࡄࠧࢮ")).findall(link)[0]
	except:
		year = l11l11Fuck_You_Anonymous (u"ࠫࠬࢯ")
	md.remove_punctuation(title)
	for url,name in match:
		md.addDir({l11l11Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࠪࢰ"):l11l11Fuck_You_Anonymous (u"࠭࠳ࠨࢱ"),l11l11Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬࢲ"):l11l11Fuck_You_Anonymous (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡻࡨࡰࡱࡵࡷ࡞࡝ࡅࡡࡠࡏ࡝ࠦࡵ࡞࠳ࡎࡣ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࢳ") %name, l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ࢴ"):url,
			   l11l11Fuck_You_Anonymous (u"ࠪࡸ࡮ࡺ࡬ࡦࠩࢵ"):title, l11l11Fuck_You_Anonymous (u"ࠫ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫ࠧࢶ"):l1ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࢷ"):l11l11Fuck_You_Anonymous (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹࠧࢸ"), l11l11Fuck_You_Anonymous (u"ࠧࡴࡧࡤࡷࡴࡴࠧࢹ"):name},
			  {l11l11Fuck_You_Anonymous (u"ࠨࡵࡲࡶࡹࡺࡩࡵ࡮ࡨࠫࢺ"):title, l11l11Fuck_You_Anonymous (u"ࠩࡼࡩࡦࡸࠧࢻ"):year}, fan_art={l11l11Fuck_You_Anonymous (u"ࠪ࡭ࡨࡵ࡮ࠨࢼ"):l1ll1lFuck_You_Anonymous}, item_count=items)
	setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬࢽ"), l11l11Fuck_You_Anonymous (u"ࠬࡹࡨࡰࡹ࠰ࡺ࡮࡫ࡷࠨࢾ"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l111ll1Fuck_You_Anonymous():
	link = open_url(l11l11Fuck_You_Anonymous (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡱࡣࡶࡸࡪࡨࡩ࡯࠰ࡦࡳࡲ࠵ࡲࡢࡹ࠲ࡇ࡫࠺ࡃ࠴ࡷࡋ࠵ࠬࢿ")).content
	version = re.findall(l11l11Fuck_You_Anonymous (u"ࡲࠨࡸࡨࡶࡸ࡯࡯࡯ࠢࡀࠤࠧ࠮࡛࡟ࠤࡠ࠯࠮ࠨࠧࣀ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l11l11Fuck_You_Anonymous (u"ࠨࡵࡳࡩࡨ࡯ࡡ࡭࠼࠲࠳࡭ࡵ࡭ࡦ࠱ࡤࡨࡩࡵ࡮ࡴ࠱ࡶࡧࡷ࡯ࡰࡵ࠰ࡰࡳࡩࡻ࡬ࡦ࠰ࡰࡹࡨࡱࡹࡴ࠰ࡦࡳࡲࡳ࡯࡯࠱ࡤࡨࡩࡵ࡮࠯ࡺࡰࡰࠬࣁ")), l11l11Fuck_You_Anonymous (u"ࠩࡵ࠯ࠬࣂ")) as f:
		l1l1lllFuck_You_Anonymous = f.read()
		if re.search(l11l11Fuck_You_Anonymous (u"ࡵࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡂࠨࠥࡴࠤࠪࣃ") %version, l1l1lllFuck_You_Anonymous):
			l11lll1Fuck_You_Anonymous.log(l11l11Fuck_You_Anonymous (u"࡛ࠫ࡫ࡲࡴ࡫ࡲࡲࠥࡉࡨࡦࡥ࡮ࠤࡔࡑࠧࣄ"))
		else:
			l11ll1Fuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"ࠧ࡝ࡲࡰࡰࡪࠤ࡛࡫ࡲࡴ࡫ࡲࡲࠥࡕࡦࠡࡏࡸࡧࡰࡿࡳࠡࡅࡲࡱࡲࡵ࡮ࠡࡏࡲࡨࡺࡲࡥࠣࣅ")
			l11lllFuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"ࠨࡐ࡭ࡧࡤࡷࡪࠦࡉ࡯ࡵࡷࡥࡱࡲࠠࡄࡱࡵࡶࡪࡩࡴࠡࡘࡨࡶࡸ࡯࡯࡯ࠢࡉࡶࡴࡳࠠࡕࡪࡨࠤࡗ࡫ࡰࡰࠤࣆ")
			l1l111Fuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"ࠢࡁ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢ࡮ࡴࡵࡲ࠽࠳࠴ࡳࡵࡤ࡭ࡼࡷ࠳ࡳࡥࡥ࡫ࡤࡴࡴࡸࡴࡢ࡮࠷࡯ࡴࡪࡩ࠯࡯࡯࡟࠴ࡉࡏࡍࡑࡕࡡࠧࣇ")
			l11lll1Fuck_You_Anonymous.show_ok_dialog([l11ll1Fuck_You_Anonymous, l11lllFuck_You_Anonymous, l1l111Fuck_You_Anonymous], l1lll11Fuck_You_Anonymous)
			xbmc.executebuiltin(l11l11Fuck_You_Anonymous (u"࡚ࠣࡅࡑࡈ࠴ࡃࡰࡰࡷࡥ࡮ࡴࡥࡳ࠰ࡘࡴࡩࡧࡴࡦࠪࡳࡥࡹ࡮ࠬࡳࡧࡳࡰࡦࡩࡥࠪࠤࣈ"))
			xbmc.executebuiltin(l11l11Fuck_You_Anonymous (u"ࠤ࡛ࡆࡒࡉ࠮ࡂࡥࡷ࡭ࡻࡧࡴࡦ࡙࡬ࡲࡩࡵࡷࠩࡊࡲࡱࡪ࠯ࠢࣉ"))
def l1l11l1Fuck_You_Anonymous(url,l1l11lFuck_You_Anonymous,title,l11l111Fuck_You_Anonymous,l11ll11Fuck_You_Anonymous):
	if l1l11lFuck_You_Anonymous is None:
		fan_art = {l11l11Fuck_You_Anonymous (u"ࠪ࡭ࡨࡵ࡮ࠨ࣊"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠫࡲࡪࡷࡴ࠰ࡳࡲ࡬࠭࣋")}
	else:
		fan_art = {l11l11Fuck_You_Anonymous (u"ࠬ࡯ࡣࡰࡰࠪ࣌"):l1l11lFuck_You_Anonymous}
	try:
		code = re.compile(l11l11Fuck_You_Anonymous (u"ࠨࠧࡪ࡯ࡧࡦࡤ࡯ࡤࠨ࠼ࠣࡹࠬ࠮࡛࡟ࠩࡠ࠯࠮࠭ࠢ࣍")).findall(l11ll11Fuck_You_Anonymous)[0]
	except:
		code = l11l11Fuck_You_Anonymous (u"ࠧࠨ࣎")
	link = open_url(url).content
	l1ll11lFuck_You_Anonymous = md.regex_get_all(link, l11l11Fuck_You_Anonymous (u"ࠨ࠾࡯࡭ࠥ࡯ࡤ࠾ࠤࡨࡴ࡮ࡹ࡯ࡥࡧࡢ࣏ࠫ"), l11l11Fuck_You_Anonymous (u"ࠩ࠿࠳ࡱ࡯࠾ࠨ࣐"))
	items = len(l1ll11lFuck_You_Anonymous)
	for a in l1ll11lFuck_You_Anonymous:
		name = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠪࠦࡳࡧ࡭ࡦࠤࡁ࣑ࠫ"), l11l11Fuck_You_Anonymous (u"ࠫࡁ࣒࠭"))
		name = l11lll1Fuck_You_Anonymous.unescape(name)
		date = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠬࠨࡤࡢࡶࡨࡴࡺࡨ࡬ࡪࡵ࡫ࡩࡩࠨ࠾ࠨ࣓"), l11l11Fuck_You_Anonymous (u"࠭࠼ࠨࣔ"))
		links = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠧ࠽ࡤࡁࠫࣕ"), l11l11Fuck_You_Anonymous (u"ࠨ࠾ࠪࣖ"))
		url = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠩ࡫ࡶࡪ࡬࠽ࠣࠩࣗ"), l11l11Fuck_You_Anonymous (u"ࠪࠦࠬࣘ"))
		l11l1llFuck_You_Anonymous = name.split(l11l11Fuck_You_Anonymous (u"ࠫࠫ࠭ࣙ"))[0]
		name = name.replace(l11l11Fuck_You_Anonymous (u"ࠧࠬࡡ࡮ࡲ࠾ࠦࣚ"),l11l11Fuck_You_Anonymous (u"ࠨࠦࠣࣛ")).replace(l11l11Fuck_You_Anonymous (u"ࠧࠧࡰࡥࡷࡵࡁࠧࣜ"),l11l11Fuck_You_Anonymous (u"ࠨࠢࠪࣝ"))
		md.addDir({l11l11Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧࣞ"):l11l11Fuck_You_Anonymous (u"ࠪ࠼ࠬࣟ"), l11l11Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩ࣠"):l11l11Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡹࡦ࡮࡯ࡳࡼࡣࠥࡴࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭࣡") %(name,links,date),
			   l11l11Fuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪ࣢"):url, l11l11Fuck_You_Anonymous (u"ࠧࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࣣࠪ"):l1l11lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࣤ"):l11l11Fuck_You_Anonymous (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࡶࠫࣥ")},
			  {l11l11Fuck_You_Anonymous (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪࣦ࠭"):title, l11l11Fuck_You_Anonymous (u"ࠫࡨࡵࡤࡦࠩࣧ"):code, l11l11Fuck_You_Anonymous (u"ࠬࡹࡥࡢࡵࡲࡲࠬࣨ"):l11l111Fuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࣩࠧ"):l11l1llFuck_You_Anonymous},
			  fan_art, item_count=items)
	setView(l11ll1lFuck_You_Anonymous,l11l11Fuck_You_Anonymous (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࠩ࣪"), l11l11Fuck_You_Anonymous (u"ࠨࡧࡳ࡭࠲ࡼࡩࡦࡹࠪ࣫"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l1lll1lFuck_You_Anonymous(url):
	link = open_url(url).content
	l1lllllFuck_You_Anonymous = md.regex_get_all(link, l11l11Fuck_You_Anonymous (u"ࠩࠥࡴࡦ࡭ࡩ࡯ࡣࡷ࡭ࡴࡴࠢ࠿ࠩ࣬"), l11l11Fuck_You_Anonymous (u"ࠪࡀ࠴ࡻ࡬࠿࣭ࠩ"))
	l1ll11lFuck_You_Anonymous = md.regex_get_all(str(l1lllllFuck_You_Anonymous), l11l11Fuck_You_Anonymous (u"ࠫࡁࡲࡩࠨ࣮"), l11l11Fuck_You_Anonymous (u"ࠬࡂ࠯࡭࡫࣯ࠪ"))
	items = len(l1ll11lFuck_You_Anonymous)
	for a in l1ll11lFuck_You_Anonymous:
		name = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"࠭ࡨࡳࡧࡩࡁ࠳࠰࠿࠿ࣰࠩ"), l11l11Fuck_You_Anonymous (u"ࠧ࠽ࣱࠩ"))
		url = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠨࡪࡵࡩ࡫ࡃࠢࠨࣲ"), l11l11Fuck_You_Anonymous (u"ࠩࠥࠫࣳ"))
		if l1l1Fuck_You_Anonymous not in url:
			url = l1l1Fuck_You_Anonymous + url
		if l11l11Fuck_You_Anonymous (u"ࠪࡒࡊ࡝ࠧࣴ") not in name:
			md.addDir({l11l11Fuck_You_Anonymous (u"ࠫࡲࡵࡤࡦࠩࣵ"):l11l11Fuck_You_Anonymous (u"ࠬ࠷ࣶࠧ"),l11l11Fuck_You_Anonymous (u"࠭࡮ࡢ࡯ࡨࠫࣷ"):l11l11Fuck_You_Anonymous (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡺࡧ࡯ࡰࡴࡽ࡝࡜ࡄࡠ࡟ࡎࡣࠥࡴ࡝࠲ࡍࡢࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࣸ") %name,
				   l11l11Fuck_You_Anonymous (u"ࠨࡷࡵࡰࣹࠬ"):url, l11l11Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫࡟ࡪࡦࣺࠪ"):l11l11Fuck_You_Anonymous (u"ࠪ࠸ࠬࣻ"), l11l11Fuck_You_Anonymous (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࣼ"):l11l11Fuck_You_Anonymous (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࣽ")},
				  fan_art={l11l11Fuck_You_Anonymous (u"࠭ࡩࡤࡱࡱࠫࣾ"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠧ࡮ࡦࡺࡷ࠳ࡶ࡮ࡨࠩࣿ")}, item_count=items)
	setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠨࡨ࡬ࡰࡪࡹࠧऀ"), l11l11Fuck_You_Anonymous (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬँ"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l111Fuck_You_Anonymous(url):
	link = open_url(url).content
	l1lllllFuck_You_Anonymous = md.regex_get_all(link, l11l11Fuck_You_Anonymous (u"ࠪࠦࡵࡧࡧࡪࡰࡤࡸ࡮ࡵ࡮ࠣࠢࡶࡸࡾࡲࡥࠨं"), l11l11Fuck_You_Anonymous (u"ࠫࡁ࠵ࡵ࡭ࡀࠪः"))
	l1ll11lFuck_You_Anonymous = md.regex_get_all(str(l1lllllFuck_You_Anonymous), l11l11Fuck_You_Anonymous (u"ࠬࡂ࡬ࡪࠩऄ"), l11l11Fuck_You_Anonymous (u"࠭࠼࠰࡮࡬ࠫअ"))
	items = len(l1ll11lFuck_You_Anonymous)
	for a in l1ll11lFuck_You_Anonymous:
		name = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠧࡩࡴࡨࡪࡂ࠴ࠪࡀࡀࠪआ"), l11l11Fuck_You_Anonymous (u"ࠨ࠾ࠪइ"))
		url = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠩ࡫ࡶࡪ࡬࠽ࠣࠩई"), l11l11Fuck_You_Anonymous (u"ࠪࠦࠬउ"))
		url = url + l11l11Fuck_You_Anonymous (u"ࠫ࠴࠷࠯࠱࠱࠳ࠫऊ")
		if l1l1Fuck_You_Anonymous not in url:
			url = l1l1Fuck_You_Anonymous + url
		md.addDir({l11l11Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࠪऋ"):l11l11Fuck_You_Anonymous (u"࠭࠱ࠨऌ"),l11l11Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬऍ"):l11l11Fuck_You_Anonymous (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡻࡨࡰࡱࡵࡷ࡞࡝ࡅࡡࡠࡏ࡝ࠦࡵ࡞࠳ࡎࡣ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬऎ") %name,
                           l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ए"):url, l11l11Fuck_You_Anonymous (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫऐ"):l11l11Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬऑ")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠬ࡯ࡣࡰࡰࠪऒ"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"࠭࡭ࡥࡹࡶ࠲ࡵࡴࡧࠨओ")}, item_count=items)
	setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠧࡧ࡫࡯ࡩࡸ࠭औ"), l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫक"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l11l1Fuck_You_Anonymous(url):
        year = []
        l11l11lFuck_You_Anonymous = []
        link = open_url(url).content
	l1lllllFuck_You_Anonymous = md.regex_get_all(link, l11l11Fuck_You_Anonymous (u"ࠩࠥࡴࡦ࡭ࡩ࡯ࡣࡷ࡭ࡴࡴࠢࠡࡵࡷࡽࡱ࡫ࠧख"), l11l11Fuck_You_Anonymous (u"ࠪࡀ࠴ࡻ࡬࠿ࠩग"))
	l1ll11lFuck_You_Anonymous = md.regex_get_all(str(l1lllllFuck_You_Anonymous), l11l11Fuck_You_Anonymous (u"ࠫࡁࡲࡩࠨघ"), l11l11Fuck_You_Anonymous (u"ࠬࡂ࠯࡭࡫ࠪङ"))
	for a in l1ll11lFuck_You_Anonymous:
		name = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"࠭ࡨࡳࡧࡩࡁ࠳࠰࠿࠿ࠩच"), l11l11Fuck_You_Anonymous (u"ࠧ࠽ࠩछ"))
		url = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠨࡪࡵࡩ࡫ࡃࠢࠨज"), l11l11Fuck_You_Anonymous (u"ࠩࠥࠫझ"))
		if l1l1Fuck_You_Anonymous not in url:
			url = l1l1Fuck_You_Anonymous + url
		year.append(name)
		l11l11lFuck_You_Anonymous.append(url)
	match = re.compile(l11l11Fuck_You_Anonymous (u"ࠪࡺࡦࡲࡵࡦ࠿ࠥࠬࡠࡤࠢ࡞࠭ࠬࠦ࠳࠰࠿࠿ࠪ࡞ࡢࡁࡄ࡝ࠫࠫ࠿࠳ࡴࡶࡴࡪࡱࡱࡂࠬञ")).findall(link)
	for l111llFuck_You_Anonymous,l1l1111Fuck_You_Anonymous in match:
                if l11l11Fuck_You_Anonymous (u"ࠫ࠴ࡿࡥࡢࡴࡶ࠳ࠬट") in l111llFuck_You_Anonymous:
                        year.append(l1l1111Fuck_You_Anonymous)
                        l11l11lFuck_You_Anonymous.append(l111llFuck_You_Anonymous)
        items = len(year)
        for l111l1lFuck_You_Anonymous,l1l111lFuck_You_Anonymous in itertools.izip_longest(year,l11l11lFuck_You_Anonymous):
                md.addDir({l11l11Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࠪठ"):l11l11Fuck_You_Anonymous (u"࠭࠱ࠨड"),l11l11Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬढ"):l11l11Fuck_You_Anonymous (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡻࡨࡰࡱࡵࡷ࡞࡝ࡅࡡࡠࡏ࡝ࠦࡵ࡞࠳ࡎࡣ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬण") %l111l1lFuck_You_Anonymous,
                           l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭त"):l1l111lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫथ"):l11l11Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬद")}, fan_art={l11l11Fuck_You_Anonymous (u"ࠬ࡯ࡣࡰࡰࠪध"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"࠭࡭ࡥࡹࡶ࠲ࡵࡴࡧࠨन")}, item_count=items)
	setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠧࡧ࡫࡯ࡩࡸ࠭ऩ"), l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫप"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l1ll111Fuck_You_Anonymous(url):
	link = open_url(url).content
	match = re.compile(l11l11Fuck_You_Anonymous (u"ࠩ࠿ࡨ࡮ࡼࠠࡴࡶࡼࡰࡪࡃࠢࡸ࡫ࡧࡸ࡭ࡀࠠ࠲࠷࠶ࡴࡽࡁࠢ࠿ࠪ࡞ࡢࡁࡄ࡝ࠫࠫ࠿ࠫफ")).findall(link)
	items = len(match)
	for name in match:
		md.addDir({l11l11Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨब"):l11l11Fuck_You_Anonymous (u"ࠫ࠶࠭भ"),l11l11Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪम"):l11l11Fuck_You_Anonymous (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡹࡦ࡮࡯ࡳࡼࡣ࡛ࡃ࡟࡞ࡍࡢࠫࡳ࡜࠱ࡌࡡࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪय") %name,
			   l11l11Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫर"):url, l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪࡥࡩࡥࠩऱ"):l11l11Fuck_You_Anonymous (u"ࠩ࠹ࠫल"), l11l11Fuck_You_Anonymous (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫळ"):l11l11Fuck_You_Anonymous (u"ࠫࡪࡶࡩࡴࡱࡧࡩࡸ࠭ऴ"), l11l11Fuck_You_Anonymous (u"ࠬࡺࡩࡵ࡮ࡨࠫव"):name},
			  fan_art={l11l11Fuck_You_Anonymous (u"࠭ࡩࡤࡱࡱࠫश"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠧ࡮ࡦࡺࡷ࠳ࡶ࡮ࡨࠩष")}, item_count=items)
	setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠨࡨ࡬ࡰࡪࡹࠧस"), l11l11Fuck_You_Anonymous (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬह"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l1lll1Fuck_You_Anonymous(content, query):
        if content is None:
                content = l11l11Fuck_You_Anonymous (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫऺ")
	try:
		if query:
			search = query.replace(l11l11Fuck_You_Anonymous (u"ࠫࠥ࠭ऻ"), l11l11Fuck_You_Anonymous (u"ࠬࠫ࠲࠱़ࠩ"))
		else:
			search = md.search(l11l11Fuck_You_Anonymous (u"࠭ࠥ࠳࠲ࠪऽ"))
			if search == l11l11Fuck_You_Anonymous (u"ࠧࠨा"):
				md.notification(l11l11Fuck_You_Anonymous (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣ࡛ࡃ࡟ࡈࡑࡕ࡚࡙ࠡࡓࡘࡉࡗ࡟࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡ࠱ࡇࡢࡰࡴࡷ࡭ࡳ࡭ࠠࡴࡧࡤࡶࡨ࡮ࠧि"),l1111lFuck_You_Anonymous)
				return
			else:
				pass
		url = l11l11Fuck_You_Anonymous (u"ࠩࠨࡷ࠴ࡹࡥࡢࡴࡦ࡬࠴ࠫࡳࠨी") %(l1l1Fuck_You_Anonymous,search)
                link = open_url(url).content
                l1ll11lFuck_You_Anonymous = md.regex_get_all(link, l11l11Fuck_You_Anonymous (u"ࠪ࡭࡭࠳ࡩࡵࡧࡰࠫु"), l11l11Fuck_You_Anonymous (u"ࠫࡆࡪࡤࠡࡎ࡬ࡲࡰ࠭ू"))
                items = len(l1ll11lFuck_You_Anonymous)
                for a in l1ll11lFuck_You_Anonymous:
                        name = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠬࡂࡳࡵࡴࡲࡲ࡬ࡄࠧृ"), l11l11Fuck_You_Anonymous (u"࠭࠼࠰ࠩॄ")).replace(l11l11Fuck_You_Anonymous (u"ࠢ࡝࡞ࠪࠦॅ"),l11l11Fuck_You_Anonymous (u"ࠣࠩࠥॆ"))
                        name = l11lll1Fuck_You_Anonymous.unescape(name)
                        url = md.regex_get_all(a, l11l11Fuck_You_Anonymous (u"ࠩ࡫ࡶࡪ࡬࠽ࠣࠩे"), l11l11Fuck_You_Anonymous (u"ࠪࠦࠬै"), l11l1l1Fuck_You_Anonymous=True)[2]
                        l1ll1lFuck_You_Anonymous = md.regex_from_to(a, l11l11Fuck_You_Anonymous (u"ࠫࡸࡸࡣ࠾ࠤࠪॉ"), l11l11Fuck_You_Anonymous (u"ࠬࠨࠧॊ"))
                        if not l1ll1lFuck_You_Anonymous:
                                l1ll1lFuck_You_Anonymous = l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"࠭࡭ࡥࡹࡶ࠲ࡵࡴࡧࠨो")
                        if l1l1Fuck_You_Anonymous not in url:
                                url = l1l1Fuck_You_Anonymous + url
                        md.remove_punctuation(name)
                        md.addDir({l11l11Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬौ"):l11l11Fuck_You_Anonymous (u"ࠨ࠴्ࠪ"), l11l11Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧॎ"):l11l11Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ॏ") %name, l11l11Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨॐ"):url,
                                   l11l11Fuck_You_Anonymous (u"ࠬࡺࡩࡵ࡮ࡨࠫ॑"):name, l11l11Fuck_You_Anonymous (u"࠭ࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ॒ࠩ"):l1ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ॓"):content},
                                  {l11l11Fuck_You_Anonymous (u"ࠨࡵࡲࡶࡹࡺࡩࡵ࡮ࡨࠫ॔"):name}, fan_art={l11l11Fuck_You_Anonymous (u"ࠩ࡬ࡧࡴࡴࠧॕ"):l1ll1lFuck_You_Anonymous}, item_count=items)
                setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫॖ"), l11l11Fuck_You_Anonymous (u"ࠫࡸ࡮࡯ࡸ࠯ࡹ࡭ࡪࡽࠧॗ"))
                l11lll1Fuck_You_Anonymous.end_of_directory()
        except:
		md.notification(l11l11Fuck_You_Anonymous (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠ࡟ࡇࡣࡓࡰࡴࡵࡽࠥࡔ࡯ࠡࡔࡨࡷࡺࡲࡴࡴ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧक़"),l1111lFuck_You_Anonymous)
def l11111Fuck_You_Anonymous(url,l1l11lFuck_You_Anonymous,title,l11l111Fuck_You_Anonymous,l11l1llFuck_You_Anonymous,l11ll11Fuck_You_Anonymous):
	if l1l11lFuck_You_Anonymous is None or l1l11lFuck_You_Anonymous == l11l11Fuck_You_Anonymous (u"࠭ࠧख़"):
		l1l1llFuck_You_Anonymous = {l11l11Fuck_You_Anonymous (u"ࠧࡪࡥࡲࡲࠬग़"):l11Fuck_You_Anonymous+l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡧࡻࡸ࠴ࡰ࡯ࡩࠪज़")}
	else:
		l1l1llFuck_You_Anonymous = {l11l11Fuck_You_Anonymous (u"ࠩ࡬ࡧࡴࡴࠧड़"):l1l11lFuck_You_Anonymous}
	link = open_url(url).content
	match = re.compile(l11l11Fuck_You_Anonymous (u"ࠪࡧࡦࡲࡥ࡝࠰࡫ࡸࡲࡲ࡜ࡀࡴࡀࠬ࠳࠰࠿ࠪࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡺࡺࡴࡰࡰ࡯࡭ࡳࡱࠢࠡࡶ࡬ࡸࡱ࡫࠽ࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪढ़")).findall(link)
	items = len(match)
	for url,name in match:
		url = url.decode(l11l11Fuck_You_Anonymous (u"ࠫࡧࡧࡳࡦ࠸࠷ࠫफ़"))
		if urlresolver.HostedMediaFile(url):
			md.addDir({l11l11Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࠪय़"):l11l11Fuck_You_Anonymous (u"࠭࠹ࠨॠ"),l11l11Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬॡ"):l11l11Fuck_You_Anonymous (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡻࡨࡰࡱࡵࡷ࡞࡝ࡅࡡࡠࡏ࡝ࠦࡵ࡞࠳ࡎࡣ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬॢ") %name, l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ॣ"):url},
				  fan_art=l1l1llFuck_You_Anonymous, is_folder=False, item_count=items)
	setView(l11ll1lFuck_You_Anonymous, l11l11Fuck_You_Anonymous (u"ࠪࡪ࡮ࡲࡥࡴࠩ।"), l11l11Fuck_You_Anonymous (u"ࠫࡲ࡫࡮ࡶ࠯ࡹ࡭ࡪࡽࠧ॥"))
	l11lll1Fuck_You_Anonymous.end_of_directory()
def l1ll1llFuck_You_Anonymous(url,name,fan_art,l11ll11Fuck_You_Anonymous):
	try:
		l1l111lFuck_You_Anonymous = urlresolver.resolve(url)
		md.resolved(l1l111lFuck_You_Anonymous, name, fan_art, l11ll11Fuck_You_Anonymous)
	except:
		md.notification(l11l11Fuck_You_Anonymous (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠ࡟ࡇࡣࡓࡐࡔࡕ࡝ࠥࡒࡉࡏࡍࠣࡈࡔ࡝ࡎࠡࡒࡏࡉࡆ࡙ࡅࠡࡖࡕ࡝ࠥࡇࡎࡐࡖࡋࡉࡗࠦࡏࡏࡇ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ०"), l1111lFuck_You_Anonymous)
	l11lll1Fuck_You_Anonymous.end_of_directory()
md.check_source()
mode = md.args[l11l11Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫ१")]
url = md.args.get(l11l11Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ२"), None)
name = md.args.get(l11l11Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭३"), None)
query = md.args.get(l11l11Fuck_You_Anonymous (u"ࠩࡴࡹࡪࡸࡹࠨ४"), None)
title = md.args.get(l11l11Fuck_You_Anonymous (u"ࠪࡸ࡮ࡺ࡬ࡦࠩ५"), None)
year = md.args.get(l11l11Fuck_You_Anonymous (u"ࠫࡾ࡫ࡡࡳࠩ६"), None)
l11l111Fuck_You_Anonymous = md.args.get(l11l11Fuck_You_Anonymous (u"ࠬࡹࡥࡢࡵࡲࡲࠬ७"), None)
l11l1llFuck_You_Anonymous = md.args.get(l11l11Fuck_You_Anonymous (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࠧ८") ,None)
l11ll11Fuck_You_Anonymous = md.args.get(l11l11Fuck_You_Anonymous (u"ࠧࡪࡰࡩࡳࡱࡧࡢࡦ࡮ࡶࠫ९"), None)
content = md.args.get(l11l11Fuck_You_Anonymous (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ॰"), None)
l1l11Fuck_You_Anonymous = md.args.get(l11l11Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫࡟ࡪࡦࠪॱ"), None)
l1l11lFuck_You_Anonymous = md.args.get(l11l11Fuck_You_Anonymous (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭ॲ"), None)
fan_art = md.args.get(l11l11Fuck_You_Anonymous (u"ࠫ࡫ࡧ࡮ࡠࡣࡵࡸࠬॳ"), None)
is_folder = md.args.get(l11l11Fuck_You_Anonymous (u"ࠬ࡯ࡳࡠࡨࡲࡰࡩ࡫ࡲࠨॴ"), True)
def l1111Fuck_You_Anonymous():
        l1l1l11Fuck_You_Anonymous = xbmc.translatePath(l11l11Fuck_You_Anonymous (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹ࠯ࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼ࠲ࡲࡧࡦࠨॵ"))
        l1l1ll1Fuck_You_Anonymous = xbmc.translatePath(l11l11Fuck_You_Anonymous (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡳࡰࡺ࡭ࡩ࡯࠰ࡳࡶࡴ࡭ࡲࡢ࡯࠱ࡱࡦ࡬ࡷࡪࡼࡤࡶࡩ࠭ॶ"))
        l1llFuck_You_Anonymous = xbmc.translatePath(l11l11Fuck_You_Anonymous (u"ࠨࡵࡳࡩࡨ࡯ࡡ࡭࠼࠲࠳࡭ࡵ࡭ࡦ࠱ࡤࡨࡩࡵ࡮ࡴ࠱ࡳࡰࡺ࡭ࡩ࡯࠰ࡹ࡭ࡩ࡫࡯࠯࡭ࡵࡥࡹࡵࡳࠨॷ"))
        if os.path.exists(l1l1l11Fuck_You_Anonymous):
                l11ll1Fuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"ࠩ࡜ࡳࡺࠦࡈࡢࡸࡨࠤࡎࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡇࡴࡲࡱࠥࡇ࡮ࠨॸ")
                l11lllFuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"࡙ࠪࡳࡵࡦࡧ࡫ࡦ࡭ࡦࡲࠠࡔࡱࡸࡶࡨ࡫࡚ࠠࠧࠢ࡭ࡱࡲࠠࡏࡱࡺࠤࡉ࡫࡬ࡦࡶࡨࠤࡕࡲࡥࡢࡵࡨࠫॹ")
                l1l111Fuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"ࠫࡎࡴࡳࡵࡣ࡯ࡰࠥࡆ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠ࡬ࡹࡺࡰ࠻࠱࠲ࡱࡺࡩ࡫ࡺࡵ࠱ࡱࡪࡪࡩࡢࡲࡲࡶࡹࡧ࡬࠵࡭ࡲࡨ࡮࠴࡭࡭࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪॺ")
                l1lFuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"ࠬࡘࡥ࡮ࡱࡹࡩࡩࠦࡁ࡯ࡱࡱࡽࡲࡵࡵࡴࠢࡕࡩࡵࡵࠠࡂࡰࡧࠤࡆࡪࡤࡰࡰࡶࠫॻ")
                l1l1l1Fuck_You_Anonymous = l11l11Fuck_You_Anonymous (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡖ࡬ࡦࡣࡶࡩࠥࡊ࡯࡯ࡶࠣࡗࡺࡶࡰࡰࡴࡷࠤࡎࡪࡩࡰࡶࡶࠫॼ")
                l11lll1Fuck_You_Anonymous.show_ok_dialog([l11ll1Fuck_You_Anonymous, l11lllFuck_You_Anonymous, l1l111Fuck_You_Anonymous], l1lll11Fuck_You_Anonymous)
                l11lFuck_You_Anonymous = l11lll1Fuck_You_Anonymous.get_path()
                shutil.rmtree(l11lFuck_You_Anonymous, ignore_errors=True)
                shutil.rmtree(l1l1l11Fuck_You_Anonymous, ignore_errors=True)
                shutil.rmtree(l1l1ll1Fuck_You_Anonymous, ignore_errors=True)
                shutil.rmtree(l1llFuck_You_Anonymous, ignore_errors=True)
                l11lll1Fuck_You_Anonymous.log(l11l11Fuck_You_Anonymous (u"ࠧ࠾࠿ࡀࡈࡊࡒࡅࡕࡋࡑࡋࡂࡃ࠽ࡂࡐࡒࡒ࡞ࡓࡏࡖࡕࡀࡁࡂࡇࡄࡅࡑࡑࡗࡂࡃ࠽ࠬ࠿ࡀࡁࡗࡋࡐࡐ࠿ࡀࡁࠬॽ"))
                l11lll1Fuck_You_Anonymous.show_ok_dialog([l1lFuck_You_Anonymous, l1l1l1Fuck_You_Anonymous], l1lll11Fuck_You_Anonymous)
                time.sleep(2)
                os._exit(0)
if mode is None or url is None or len(url)<1:
	l1111l1Fuck_You_Anonymous()
elif mode == l11l11Fuck_You_Anonymous (u"ࠨ࠳ࠪॾ"):
	l1Fuck_You_Anonymous(url,title,l1l11Fuck_You_Anonymous,content)
elif mode == l11l11Fuck_You_Anonymous (u"ࠩ࠵ࠫॿ"):
	l1111llFuck_You_Anonymous(url,title)
elif mode == l11l11Fuck_You_Anonymous (u"ࠪ࠷ࠬঀ"):
	l1l11l1Fuck_You_Anonymous(url,l1l11lFuck_You_Anonymous,title,l11l111Fuck_You_Anonymous,l11ll11Fuck_You_Anonymous)
elif mode == l11l11Fuck_You_Anonymous (u"ࠫ࠹࠭ঁ"):
	l1lll1lFuck_You_Anonymous(url)
elif mode == l11l11Fuck_You_Anonymous (u"ࠬ࠻ࠧং"):
	l111Fuck_You_Anonymous(url)
elif mode == l11l11Fuck_You_Anonymous (u"࠭࠶ࠨঃ"):
	l1ll111Fuck_You_Anonymous(url)
elif mode == l11l11Fuck_You_Anonymous (u"ࠧ࠸ࠩ঄"):
	l11l1Fuck_You_Anonymous(url)
elif mode == l11l11Fuck_You_Anonymous (u"ࠨ࠺ࠪঅ"):
	l11111Fuck_You_Anonymous(url,l1l11lFuck_You_Anonymous,title,l11l111Fuck_You_Anonymous,l11l1llFuck_You_Anonymous,l11ll11Fuck_You_Anonymous)
elif mode == l11l11Fuck_You_Anonymous (u"ࠩ࠼ࠫআ"):
	l1ll1llFuck_You_Anonymous(url,name,fan_art,l11ll11Fuck_You_Anonymous)
elif mode == l11l11Fuck_You_Anonymous (u"ࠪࡷࡪࡧࡲࡤࡪࠪই"):
	l1lll1Fuck_You_Anonymous(content, query)
elif mode == l11l11Fuck_You_Anonymous (u"ࠫࡦࡪࡤࡰࡰࡢࡷࡪࡧࡲࡤࡪࠪঈ"):
	md.addon_search(content,query,fan_art,l11ll11Fuck_You_Anonymous)
elif mode == l11l11Fuck_You_Anonymous (u"ࠬࡧࡤࡥࡡࡵࡩࡲࡵࡶࡦࡡࡩࡥࡻ࠭উ"):
	md.add_remove_fav(name,url,l11ll11Fuck_You_Anonymous,fan_art,
			  content,l1l11Fuck_You_Anonymous,is_folder)
elif mode == l11l11Fuck_You_Anonymous (u"࠭ࡦࡦࡶࡦ࡬ࡤ࡬ࡡࡷࡵࠪঊ"):
	md.fetch_favs(l1l1Fuck_You_Anonymous)
elif mode == l11l11Fuck_You_Anonymous (u"ࠧࡢࡦࡧࡳࡳࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨঋ"):
	l11lll1Fuck_You_Anonymous.show_settings()
elif mode == l11l11Fuck_You_Anonymous (u"ࠨ࡯ࡨࡸࡦࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨঌ"):
	import metahandler
	metahandler.display_settings()
elif mode == l11l11Fuck_You_Anonymous (u"ࠩࡸࡶࡱࡸࡥࡴࡱ࡯ࡺࡪࡸ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ঍"):
	urlresolver.display_settings()
l11lll1Fuck_You_Anonymous.end_of_directory()