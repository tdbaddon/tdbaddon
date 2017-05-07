# -*- coding: utf-8 -*-
import sys
l1l1l1l1Fuck_You_Anonymous = sys.version_info [0] == 2
l1111l1Fuck_You_Anonymous = 2048
l1ll111lFuck_You_Anonymous = 7
def l111Fuck_You_Anonymous (l11lllFuck_You_Anonymous):
    global l1111llFuck_You_Anonymous
    l1lll111Fuck_You_Anonymous = ord (l11lllFuck_You_Anonymous [-1])
    l1l1l1llFuck_You_Anonymous = l11lllFuck_You_Anonymous [:-1]
    l11llllFuck_You_Anonymous = l1lll111Fuck_You_Anonymous % len (l1l1l1llFuck_You_Anonymous)
    l111llFuck_You_Anonymous = l1l1l1llFuck_You_Anonymous [:l11llllFuck_You_Anonymous] + l1l1l1llFuck_You_Anonymous [l11llllFuck_You_Anonymous:]
    if l1l1l1l1Fuck_You_Anonymous:
        l111lFuck_You_Anonymous = unicode () .join ([unichr (ord (char) - l1111l1Fuck_You_Anonymous - (l11lFuck_You_Anonymous + l1lll111Fuck_You_Anonymous) % l1ll111lFuck_You_Anonymous) for l11lFuck_You_Anonymous, char in enumerate (l111llFuck_You_Anonymous)])
    else:
        l111lFuck_You_Anonymous = str () .join ([chr (ord (char) - l1111l1Fuck_You_Anonymous - (l11lFuck_You_Anonymous + l1lll111Fuck_You_Anonymous) % l1ll111lFuck_You_Anonymous) for l11lFuck_You_Anonymous, char in enumerate (l111llFuck_You_Anonymous)])
    return eval (l111lFuck_You_Anonymous)
import hashlib,os,random,re,shutil,string,sys,time
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
# C Movies HD Add-on Created By Mucky Duck (10/2016)
l1lll1llFuck_You_Anonymous = xbmcaddon.Addon().getAddonInfo(l111Fuck_You_Anonymous (u"ࠫ࡮ࡪࠧࠀ"))
l1ll1Fuck_You_Anonymous = Addon(l1lll1llFuck_You_Anonymous, sys.argv)
l1l11Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_name()
l1ll1l1lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_path()
md = md(l1lll1llFuck_You_Anonymous, sys.argv)
l11ll11Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"ࠬࡧࡵࡵࡱࡳࡰࡦࡿࠧࠁ"))
l1111lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥ࡭ࡦࡶࡤࠫࠂ"))
l1lllll1Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"ࠧࡦࡰࡤࡦࡱ࡫࡟ࡴࡪࡲࡻࡸ࠭ࠃ"))
l1ll11llFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"ࠨࡧࡱࡥࡧࡲࡥࡠ࡯ࡲࡺ࡮࡫ࡳࠨࠄ"))
l11l1llFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"ࠩࡨࡲࡦࡨ࡬ࡦࡡࡩࡥࡻࡹࠧࠅ"))
l1ll11Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"ࠪࡩࡳࡧࡢ࡭ࡧࡢࡴࡷࡵࡸࡺࠩࠆ"))
l1llFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"ࠫࡦࡪࡤࡠࡵࡨࡸࠬࠇ"))
l11llll1Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l111Fuck_You_Anonymous (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࡢࡷࡪࡺࠧࠈ"))
l11l1lFuck_You_Anonymous = md.get_art()
l1l11l11Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_icon()
l11l11lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_fanart()
l111111Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡣ࡮ࡱࡹ࡭ࡪࡹࡨࡥ࠰ࡦࡳࡲ࠭ࠉ")
reload(sys)
sys.setdefaultencoding(l111Fuck_You_Anonymous (u"ࠢࡶࡶࡩ࠱࠽ࠨࠊ"))
l1llllFuck_You_Anonymous = [l111Fuck_You_Anonymous (u"ࠨࡴࡤࡸ࡮ࡴࡧࠨࠋ"),l111Fuck_You_Anonymous (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩࠌ"),l111Fuck_You_Anonymous (u"ࠪࡺ࡮࡫ࡷࠨࠍ"),l111Fuck_You_Anonymous (u"ࠫ࡫ࡧࡶࡰࡴ࡬ࡸࡪ࠭ࠎ"),l111Fuck_You_Anonymous (u"ࠬ࡯࡭ࡥࡤࠪࠏ")]
sort = [l111Fuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥࡹࡴࡦࡧ࡯ࡦࡱࡻࡥ࡞ࡏࡲࡷࡹࠦࡒࡢࡶࡨࡨࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࠐ"), l111Fuck_You_Anonymous (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡳࡵࡧࡨࡰࡧࡲࡵࡦ࡟ࡕࡩࡨ࡫࡮ࡵ࡮ࡼࠤࡆࡪࡤࡦࡦ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬࠑ"),
	l111Fuck_You_Anonymous (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡴࡶࡨࡩࡱࡨ࡬ࡶࡧࡠࡑࡴࡹࡴࠡࡘ࡬ࡩࡼ࡫ࡤ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࠒ"), l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࡒࡵࡳࡵࠢࡉࡥࡻࡵࡲࡪࡶࡨࡨࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࠓ"),
	l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢࡏࡍࡅࡄࠣࡖࡦࡺࡩ࡯ࡩ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬࠔ")]
def l1l1ll1Fuck_You_Anonymous():
	if l1ll11llFuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠫࡹࡸࡵࡦࠩࠕ"):
		md.addDir({l111Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࠪࠖ"): l111Fuck_You_Anonymous (u"࠭࠱ࠨࠗ"), l111Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬ࠘"):l111Fuck_You_Anonymous (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡴࡶࡨࡩࡱࡨ࡬ࡶࡧࡠࡑࡔ࡜ࡉࡆࡕ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬ࠙"), l111Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ࠚ"):l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࠛ"), l111Fuck_You_Anonymous (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࠜ"):l111Fuck_You_Anonymous (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࠝ")})
	if l1lllll1Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"࠭ࡴࡳࡷࡨࠫࠞ"):
		md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬࠟ"): l111Fuck_You_Anonymous (u"ࠨ࠳ࠪࠠ"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࠡ"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢ࡚ࡖࠡࡕࡋࡓ࡜࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࠢ"), l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࠣ"):l111Fuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࠤ"), l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࠥ"):l111Fuck_You_Anonymous (u"ࠧࡵࡸࡶ࡬ࡴࡽࡳࠨࠦ")})
	if l11l1llFuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠨࡶࡵࡹࡪ࠭ࠧ"):
		md.addDir({l111Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧࠨ"): l111Fuck_You_Anonymous (u"ࠪࡪࡪࡺࡣࡩࡡࡩࡥࡻࡹࠧࠩ"), l111Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩࠪ"):l111Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤࡸࡺࡥࡦ࡮ࡥࡰࡺ࡫࡝ࡎ࡛ࠣࡊࡆ࡜ࡏࡖࡔࡌࡘࡊ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࠫ"), l111Fuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪࠬ"):l111Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ࠭")})
	if l1111lFuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠨࡶࡵࡹࡪ࠭࠮"):
		if l11llll1Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠩࡷࡶࡺ࡫ࠧ࠯"):
			md.addDir({l111Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨ࠰"):l111Fuck_You_Anonymous (u"ࠫࡲ࡫ࡴࡢࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ࠱"), l111Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪ࠲"):l111Fuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥࡹࡴࡦࡧ࡯ࡦࡱࡻࡥ࡞ࡏࡈࡘࡆࠦࡓࡆࡖࡗࡍࡓࡍࡓ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪ࠳"), l111Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ࠴"):l111Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬ࠵")}, is_folder=False, is_playable=False)
	if l1llFuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠩࡷࡶࡺ࡫ࠧ࠶"):
		md.addDir({l111Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨ࠷"):l111Fuck_You_Anonymous (u"ࠫࡦࡪࡤࡰࡰࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬ࠸"), l111Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪ࠹"):l111Fuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥࡹࡴࡦࡧ࡯ࡦࡱࡻࡥ࡞ࡃࡇࡈࡔࡔࠠࡔࡇࡗࡘࡎࡔࡇࡔ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫ࠺"), l111Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ࠻"):l111Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬ࠼")}, is_folder=False, is_playable=False)
	l1ll11l1Fuck_You_Anonymous()
	l1l11lFuck_You_Anonymous()
	setView(l1lll1llFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠩࡩ࡭ࡱ࡫ࡳࠨ࠽"), l111Fuck_You_Anonymous (u"ࠪࡱࡪࡴࡵ࠮ࡸ࡬ࡩࡼ࠭࠾"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1l11111Fuck_You_Anonymous(content):
	if l11l1llFuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠫࡹࡸࡵࡦࠩ࠿"):
		md.addDir({l111Fuck_You_Anonymous (u"ࠬࡳ࡯ࡥࡧࠪࡀ"): l111Fuck_You_Anonymous (u"࠭ࡦࡦࡶࡦ࡬ࡤ࡬ࡡࡷࡵࠪࡁ"), l111Fuck_You_Anonymous (u"ࠧ࡯ࡣࡰࡩࠬࡂ"):l111Fuck_You_Anonymous (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡴࡶࡨࡩࡱࡨ࡬ࡶࡧࡠࡑࡾࠦࡁࡥࡦ࠰ࡓࡳࠦࡆࡢࡸࡲࡹࡷ࡯ࡴࡦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬࡃ"), l111Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ࡄ"):l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࡅ")})
	if content == l111Fuck_You_Anonymous (u"ࠫࡲࡵࡶࡪࡧࡶࠫࡆ"):
		l1ll1l11Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠬࡳ࡯ࡷ࡫ࡨࠫࡇ")
		l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"࠭ࡦࡢࡰࡤࡶࡹ࠭ࡈ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡹ࡭ࡪࡹ࠮࡫ࡲࡪࠫࡉ")}
	elif content == l111Fuck_You_Anonymous (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࡊ"):
		l1ll1l11Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠩࡶࡩࡷ࡯ࡥࡴࠩࡋ")
		l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠪࡪࡦࡴࡡࡳࡶࠪࡌ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷ࠳ࡰࡰࡨࠩࡍ")}
	l111lllFuck_You_Anonymous = l111111Fuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠬ࠵ࡦࡪ࡮ࡷࡩࡷ࠵࠿ࡴࡱࡵࡸࡂࠫࡳࠧࡶࡼࡴࡪࡃࠥࡴࠨࡴࡹࡦࡲࡩࡵࡻࡀࡥࡱࡲࠦࡺࡧࡤࡶࡂࡧ࡬࡭ࠩࡎ")
	md.addDir({l111Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫࡏ"): l111Fuck_You_Anonymous (u"ࠧ࠳ࠩࡐ"), l111Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ࡑ"):l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࡒࡵࡳࡵࠢࡕࡩࡨ࡫࡮ࡵ࡮ࡼࠤࡆࡪࡤࡦࡦ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬࡒ"), l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࡓ"):l111lllFuck_You_Anonymous %(l111Fuck_You_Anonymous (u"ࠫࡱࡧࡴࡦࡵࡷࠫࡔ"),l1ll1l11Fuck_You_Anonymous), l111Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࡕ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫࡖ"): l111Fuck_You_Anonymous (u"ࠧ࠳ࠩࡗ"), l111Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ࡘ"):l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࡒࡵࡳࡵࠢࡉࡥࡻࡵࡲࡪࡶࡨࡨࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣ࡙ࠧ"), l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲ࡚ࠧ"):l111lllFuck_You_Anonymous %(l111Fuck_You_Anonymous (u"ࠫ࡫ࡧࡶࡰࡴ࡬ࡸࡪ࡛࠭"),l1ll1l11Fuck_You_Anonymous), l111Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭࡜"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫ࡝"): l111Fuck_You_Anonymous (u"ࠧ࠳ࠩ࡞"), l111Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭࡟"):l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࡒࡵࡳࡵ࡙ࠢ࡭ࡪࡽࡥࡥ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫࡠ"), l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࡡ"):l111lllFuck_You_Anonymous %(l111Fuck_You_Anonymous (u"ࠫࡻ࡯ࡥࡸࠩࡢ"),l1ll1l11Fuck_You_Anonymous), l111Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࡣ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫࡤ"): l111Fuck_You_Anonymous (u"ࠧ࠳ࠩࡥ"), l111Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ࡦ"):l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࡒࡵࡳࡵࠢࡕࡥࡹ࡫ࡤ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࡧ"), l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࡨ"):l111lllFuck_You_Anonymous %(l111Fuck_You_Anonymous (u"ࠫࡷࡧࡴࡪࡰࡪࠫࡩ"),l1ll1l11Fuck_You_Anonymous), l111Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࡪ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫ࡫"): l111Fuck_You_Anonymous (u"ࠧ࠷ࠩ࡬"), l111Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭࡭"):l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࡈࡵࡵ࡯ࡶࡵࡽࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧ࡮"), l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧ࡯"):l111111Fuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠫ࠴࡬ࡩ࡭ࡶࡨࡶ࠴࠭ࡰ"), l111Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࡱ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	if content == l111Fuck_You_Anonymous (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࡲ"):
		md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬࡳ"): l111Fuck_You_Anonymous (u"ࠨ࠴ࠪࡴ"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࡵ"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢࡉࡩ࡯ࡧࡰࡥࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࡶ"),l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࡷ"):l111111Fuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠬ࠵ࡣࡪࡰࡨࡱࡦ࠵ࠧࡸ"), l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࡹ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬࡺ"): l111Fuck_You_Anonymous (u"ࠨࡵࡨࡥࡷࡩࡨࠨࡻ"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࡼ"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢ࡙ࡥࡢࡴࡦ࡬ࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࡽ"), l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࡾ"):l111Fuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡿ"), l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࢀ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬࢁ"): l111Fuck_You_Anonymous (u"ࠨ࠶ࠪࢂ"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࢃ"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢࡍࡥ࡯ࡴࡨ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ࢄ"), l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࢅ"):l111111Fuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠬ࠵ࡦࡪ࡮ࡷࡩࡷ࠵ࠧࢆ"), l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࢇ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬ࢈"): l111Fuck_You_Anonymous (u"ࠨ࠴ࠪࢉ"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࢊ"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢࡏࡍࡅࡄ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬࢋ"), l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࢌ"):l111lllFuck_You_Anonymous %(l111Fuck_You_Anonymous (u"ࠬ࡯࡭ࡥࡤࠪࢍ"),l1ll1l11Fuck_You_Anonymous), l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࢎ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬ࢏"): l111Fuck_You_Anonymous (u"ࠨ࠷ࠪ࢐"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧ࢑"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢ࡟ࡥࡢࡴ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬ࢒"), l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨ࢓"):l111111Fuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠬ࠵ࡦࡪ࡮ࡷࡩࡷ࠵ࠧ࢔"), l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧ࢕"):content}, fan_art=l11l11lFuck_You_Anonymous)
	setView(l1lll1llFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠧࡧ࡫࡯ࡩࡸ࠭࢖"), l111Fuck_You_Anonymous (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫࢗ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l11ll1Fuck_You_Anonymous(url,content):
	if l111111Fuck_You_Anonymous not in url:
		url = l111111Fuck_You_Anonymous + url
	link = open_url(url,verify=False).content
	l11llFuck_You_Anonymous = md.regex_get_all(link, l111Fuck_You_Anonymous (u"ࠩࡦࡰࡦࡹࡳ࠾ࠤࡰࡰ࠲࡯ࡴࡦ࡯ࠥࡂࠬ࢘"), l111Fuck_You_Anonymous (u"ࠪࡀ࠴ࡪࡩࡷࡀ࢙ࠪ"))
	items = len(l11llFuck_You_Anonymous)
	for a in l11llFuck_You_Anonymous:
		name = md.regex_from_to(a, l111Fuck_You_Anonymous (u"ࠫࡹ࡯ࡴ࡭ࡧࡀ࢚ࠦࠬ"), l111Fuck_You_Anonymous (u"ࠬࠨ࢛ࠧ")).replace(l111Fuck_You_Anonymous (u"ࠨ࡜࡝ࠩࠥ࢜"),l111Fuck_You_Anonymous (u"ࠢࠨࠤ࢝"))
		name = l1ll1Fuck_You_Anonymous.unescape(name)
		url = md.regex_from_to(a, l111Fuck_You_Anonymous (u"ࠨࡪࡵࡩ࡫ࡃࠢࠨ࢞"), l111Fuck_You_Anonymous (u"ࠩࠥࠫ࢟"))
		l1l1Fuck_You_Anonymous = md.regex_from_to(a, l111Fuck_You_Anonymous (u"ࠪࡨࡦࡺࡡ࠮ࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡀࠦࠬࢠ"), l111Fuck_You_Anonymous (u"ࠫࠧ࠭ࢡ"))
		l1llllllFuck_You_Anonymous = md.regex_from_to(a, l111Fuck_You_Anonymous (u"ࠬࡷࡵࡢ࡮࡬ࡸࡾࡢࠧ࠿ࠩࢢ"), l111Fuck_You_Anonymous (u"࠭࠼ࠨࢣ"))
		l1l111l1Fuck_You_Anonymous = md.regex_from_to(a, l111Fuck_You_Anonymous (u"ࠧࡦࡲࡶࡠࠬࡄࠧࢤ"), l111Fuck_You_Anonymous (u"ࠨ࠾࠲ࠫࢥ"))
		l1l111l1Fuck_You_Anonymous = l1l111l1Fuck_You_Anonymous.replace(l111Fuck_You_Anonymous (u"ࠩ࠿ࡷࡵࡧ࡮࠿ࠩࢦ"),l111Fuck_You_Anonymous (u"ࠪࠤࠬࢧ")).replace(l111Fuck_You_Anonymous (u"ࠫࡁ࡯࠾ࠨࢨ"),l111Fuck_You_Anonymous (u"ࠬࠦࠧࢩ"))
		if content == l111Fuck_You_Anonymous (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࢪ"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠧࡧࡣࡱࡥࡷࡺࠧࢫ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡺ࡮࡫ࡳ࠯࡬ࡳ࡫ࠬࢬ")}
			if l1llllllFuck_You_Anonymous:
				title = name
				md.remove_punctuation(title)
				md.addDir({l111Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧࢭ"): l111Fuck_You_Anonymous (u"ࠪ࠻ࠬࢮ"), l111Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩࢯ"):l111Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡳࡵࡧࡨࡰࡧࡲࡵࡦ࡟ࠫࠩࡸ࠯࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࢰ") %(name,l1llllllFuck_You_Anonymous),
					   l111Fuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪࢱ"):url+l111Fuck_You_Anonymous (u"ࠧࡸࡣࡷࡧ࡭࠭ࢲ"), l111Fuck_You_Anonymous (u"ࠨ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠫࢳ"):l1l1Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࢴ"):content}, {l111Fuck_You_Anonymous (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪ࠭ࢵ"):title},
					  fan_art=l11l11lFuck_You_Anonymous, is_folder=False, item_count=items)
		elif content == l111Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬࢶ"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬࢷ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹ࠮࡫ࡲࡪࠫࢸ")}
			if l1l111l1Fuck_You_Anonymous:
				data = name.split(l111Fuck_You_Anonymous (u"ࠧ࠮ࠢࡖࡩࡦࡹ࡯࡯ࠩࢹ"))
				l1ll1lllFuck_You_Anonymous = data[0].strip()
				md.remove_punctuation(l1ll1lllFuck_You_Anonymous)
				try:
					l11111lFuck_You_Anonymous = data[1].strip()
				except:
					l11111lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠨࠩࢺ")
				md.addDir({l111Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧࢻ"): l111Fuck_You_Anonymous (u"ࠪ࠷ࠬࢼ"), l111Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩࢽ"):l111Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠࠤࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡴࡶࡨࡩࡱࡨ࡬ࡶࡧࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨࢾ") %(name,l1l111l1Fuck_You_Anonymous),
					   l111Fuck_You_Anonymous (u"࠭ࡴࡪࡶ࡯ࡩࠬࢿ"):l1ll1lllFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫࣀ"):url+l111Fuck_You_Anonymous (u"ࠨࡹࡤࡸࡨ࡮ࠧࣁ"), l111Fuck_You_Anonymous (u"ࠩ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠬࣂ"):l1l1Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࣃ"):content, l111Fuck_You_Anonymous (u"ࠫࡸ࡫ࡡࡴࡱࡱࠫࣄ"):l11111lFuck_You_Anonymous},
					  {l111Fuck_You_Anonymous (u"ࠬࡹ࡯ࡳࡶࡷ࡭ࡹࡲࡥࠨࣅ"):l1ll1lllFuck_You_Anonymous}, l11l11lFuck_You_Anonymous, item_count=items)
	try:
		l111ll1Fuck_You_Anonymous = re.findall(l111Fuck_You_Anonymous (u"ࡸࠧ࠽࡮࡬ࠤࡨࡲࡡࡴࡵࡀࠦ࠳࠰࠿ࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࠪࡹࠨ࠯ࠬࡂ࠭ࠧࠦࡤࡢࡶࡤ࠱ࡨ࡯࠭ࡱࡣࡪ࡭ࡳࡧࡴࡪࡱࡱ࠱ࡵࡧࡧࡦ࠿ࠥ࠲࠯ࡅࠢࠡࡴࡨࡰࡂࠨࠨ࠯ࠬࡂ࠭ࠧࡄ࠮ࠫࡁ࠿࠳ࡦࡄ࠼࠰࡮࡬ࡂࠬࣆ") %l111111Fuck_You_Anonymous, str(link), re.I|re.DOTALL)
		for url,name in l111ll1Fuck_You_Anonymous:
			url = url.replace(l111Fuck_You_Anonymous (u"ࠧࠧࡣࡰࡴࡀ࠭ࣇ"),l111Fuck_You_Anonymous (u"ࠨࠨࠪࣈ"))
			l1lll1l1Fuck_You_Anonymous = [l111Fuck_You_Anonymous (u"ࠩࡳࡶࡪࡼࠧࣉ"), l111Fuck_You_Anonymous (u"ࠪࡲࡪࡾࡴࠨ࣊")]
			if name in l1lll1l1Fuck_You_Anonymous:
				name = name.replace(l111Fuck_You_Anonymous (u"ࠫࡳ࡫ࡸࡵࠩ࣋"),l111Fuck_You_Anonymous (u"ࠬࡄ࠾ࡏࡧࡻࡸࠥࡖࡡࡨࡧࡁࡂࡃ࠭࣌"))
				name = name.replace(l111Fuck_You_Anonymous (u"࠭ࡰࡳࡧࡹࠫ࣍"),l111Fuck_You_Anonymous (u"ࠧ࠽࠾࠿ࡔࡷ࡫ࡶࡪࡱࡸࡷࠥࡖࡡࡨࡧ࠿ࡀࠬ࣎"))
				md.addDir({l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࣏࠭"): l111Fuck_You_Anonymous (u"ࠩ࠵࣐ࠫ"), l111Fuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨ࣑"):l111Fuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡋࡠ࡟ࡈࡕࡌࡐࡔࠣࡷࡹ࡫ࡥ࡭ࡤ࡯ࡹࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠ࣒ࠫ") %name, l111Fuck_You_Anonymous (u"ࠬࡻࡲ࡭࣓ࠩ"):url, l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࣔ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	except: pass
	if content == l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧࣕ"):
		setView(l1lll1llFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨࣖ"), l111Fuck_You_Anonymous (u"ࠩࡰࡳࡻ࡯ࡥ࠮ࡸ࡬ࡩࡼ࠭ࣗ"))
	elif content == l111Fuck_You_Anonymous (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫࣘ"):
		setView(l1lll1llFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬࣙ"), l111Fuck_You_Anonymous (u"ࠬࡹࡨࡰࡹ࠰ࡺ࡮࡫ࡷࠨࣚ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1lll11lFuck_You_Anonymous(title, url, l11111Fuck_You_Anonymous, content, l11111lFuck_You_Anonymous):
	if l111111Fuck_You_Anonymous not in url:
		url = l111111Fuck_You_Anonymous + url
	if l11111Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"࠭ࠧࣛ") or l11111Fuck_You_Anonymous == None:
		fan_art = {l111Fuck_You_Anonymous (u"ࠧࡪࡥࡲࡲࠬࣜ"):l1l11l11Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠨࡨࡤࡲࡦࡸࡴࠨࣝ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵ࠱࡮ࡵ࡭ࠧࣞ")}
	else:
		fan_art = {l111Fuck_You_Anonymous (u"ࠪ࡭ࡨࡵ࡮ࠨࣟ"):l11111Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫ࣠"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠴ࡪࡱࡩࠪ࣡")}
	link = open_url(url,verify=False).content
	if not l11ll11Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"࠭ࡴࡳࡷࡨࠫ࣢"):
		l11l111Fuck_You_Anonymous = re.findall(l111Fuck_You_Anonymous (u"ࡲࠨ࠾࡬ࠤࡨࡲࡡࡴࡵࡀࠦ࡫ࡧࠠࡧࡣ࠰ࡷࡪࡸࡶࡦࡴࠣࡱࡷ࠻ࠢ࠿࠾࠲࡭ࡃࡂࡳࡵࡴࡲࡲ࡬ࡄࠨ࡜ࡠ࠿ࡂࡢ࠰ࠩ࠽࠱ࡶࡸࡷࡵ࡮ࡨࡀࣣࠪ"), str(link), re.I|re.DOTALL)
		l111l11Fuck_You_Anonymous = []
		l1l1lllFuck_You_Anonymous = []
		l1ll1lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠨࠩࣤ")
		for l1lll1lFuck_You_Anonymous in l11l111Fuck_You_Anonymous:
			if l111Fuck_You_Anonymous (u"ࠩࡖࡉࡗ࡜ࡅࡓࠩࣥ") in l1lll1lFuck_You_Anonymous:
				l1ll1lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࣦࠪ") %l1lll1lFuck_You_Anonymous
				l111l11Fuck_You_Anonymous.append(l1ll1lFuck_You_Anonymous)
				l1l1lllFuck_You_Anonymous.append(l1lll1lFuck_You_Anonymous)
		if len(l111l11Fuck_You_Anonymous) > 1:
			l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"ࠫࡕࡲࡥࡢࡵࡨࠤࡈ࡮࡯ࡰࡵࡨࠤࡆࠦࡓࡦࡴࡹࡩࡷ࠭ࣧ"),l111l11Fuck_You_Anonymous)
			if l1llll1Fuck_You_Anonymous == -1:
				return
			elif l1llll1Fuck_You_Anonymous > -1:
				l111l1lFuck_You_Anonymous = md.regex_get_all(link, l111Fuck_You_Anonymous (u"ࠬࡂࡳࡵࡴࡲࡲ࡬ࡄࠥࡴ࠾࠲ࡷࡹࡸ࡯࡯ࡩࡁࠫࣨ") %l1l1lllFuck_You_Anonymous[l1llll1Fuck_You_Anonymous], l111Fuck_You_Anonymous (u"࠭ࠢࡤ࡮ࡨࡥࡷ࡬ࡩࡹࠤࣩࠪ"))
		else:
			l111l1lFuck_You_Anonymous = md.regex_get_all(link, l111Fuck_You_Anonymous (u"ࠧࡪࡦࡀࠦࡱ࡯ࡳࡵ࠯ࡨࡴࡸࠨࠧ࣪"), l111Fuck_You_Anonymous (u"ࠨࠤࡦࡰࡪࡧࡲࡧ࡫ࡻࠦࠬ࣫"))
	else:
		l111l1lFuck_You_Anonymous = md.regex_get_all(link, l111Fuck_You_Anonymous (u"ࠩ࡬ࡨࡂࠨ࡬ࡪࡵࡷ࠱ࡪࡶࡳࠣࠩ࣬"), l111Fuck_You_Anonymous (u"ࠪࠦࡨࡲࡥࡢࡴࡩ࡭ࡽࠨ࣭ࠧ"))
	l11llFuck_You_Anonymous = md.regex_get_all(str(l111l1lFuck_You_Anonymous), l111Fuck_You_Anonymous (u"ࠫࡁࡧ࣮ࠧ"), l111Fuck_You_Anonymous (u"ࠬࡧ࠾ࠨ࣯"))
	items = len(l11llFuck_You_Anonymous)
	for a in l11llFuck_You_Anonymous:
		name = md.regex_from_to(a, l111Fuck_You_Anonymous (u"࠭ࡢࡵࡰ࠰ࡩࡵࡹࠠࡧ࡫ࡵࡷࡹ࠳ࡥࡱࠢ࠱࠮ࡄࠨ࠾ࠨࣰ"), l111Fuck_You_Anonymous (u"ࠧ࠽࠱ࣱࠪ")).replace(l111Fuck_You_Anonymous (u"ࠣ࡞࡟ࣲࠫࠧ"),l111Fuck_You_Anonymous (u"ࠤࠪࠦࣳ"))
		name = name.replace(l111Fuck_You_Anonymous (u"ࠪࡉࡵ࡯ࡳࡰࡦࡨࠫࣴ"),l111Fuck_You_Anonymous (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡸࡺࡥࡦ࡮ࡥࡰࡺ࡫࡝ࡆࡲ࡬ࡷࡴࡪࡥ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩࣵ")).replace(l111Fuck_You_Anonymous (u"ࠧࡢ࡜ࡵࠤࣶ"),l111Fuck_You_Anonymous (u"ࠨࠢࣷ"))
		name = l1ll1Fuck_You_Anonymous.unescape(name)
		url = md.regex_from_to(a, l111Fuck_You_Anonymous (u"ࠧࡩࡴࡨࡪࡂࠨࠧࣸ"), l111Fuck_You_Anonymous (u"ࠨࠤࣹࠪ"))
		if l111Fuck_You_Anonymous (u"ࠩ࠲ࡷࡪࡸࡶࡦࡴ࠰ࣺࠫ") in url:
			try:
				l1l111llFuck_You_Anonymous = name.split(l111Fuck_You_Anonymous (u"ࠪ࠾ࠬࣻ"))[0].strip()
			except:pass
			md.remove_punctuation(title)
			md.addDir({l111Fuck_You_Anonymous (u"ࠫࡲࡵࡤࡦࠩࣼ"): l111Fuck_You_Anonymous (u"ࠬ࠽ࠧࣽ"), l111Fuck_You_Anonymous (u"࠭࡮ࡢ࡯ࡨࠫࣾ"):l111Fuck_You_Anonymous (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࣿ") %name,
				   l111Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬऀ"):url, l111Fuck_You_Anonymous (u"ࠩ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠬँ"):l11111Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫं"):l111Fuck_You_Anonymous (u"ࠫࡪࡶࡩࡴࡱࡧࡩࡸ࠭ः")},
				  {l111Fuck_You_Anonymous (u"ࠬࡹ࡯ࡳࡶࡷ࡭ࡹࡲࡥࠨऄ"):title, l111Fuck_You_Anonymous (u"࠭ࡳࡦࡣࡶࡳࡳ࠭अ"):l11111lFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࠨआ"):l1l111llFuck_You_Anonymous},
				  fan_art, is_folder=False, item_count=items)
	setView(l1lll1llFuck_You_Anonymous,l111Fuck_You_Anonymous (u"ࠨࡧࡳ࡭ࡸࡵࡤࡦࡵࠪइ"), l111Fuck_You_Anonymous (u"ࠩࡨࡴ࡮࠳ࡶࡪࡧࡺࠫई"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1l11lFuck_You_Anonymous():
	link = open_url(l111Fuck_You_Anonymous (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡵࡧࡳࡵࡧࡥ࡭ࡳ࠴ࡣࡰ࡯࠲ࡶࡦࡽ࠯ࡄࡨ࠷ࡇ࠸ࡻࡈ࠲ࠩउ")).content
	version = re.findall(l111Fuck_You_Anonymous (u"ࡶࠬࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠡࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠫऊ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l111Fuck_You_Anonymous (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࡳࡤࡴ࡬ࡴࡹ࠴࡭ࡰࡦࡸࡰࡪ࠴࡭ࡶࡥ࡮ࡽࡸ࠴ࡣࡰ࡯ࡰࡳࡳ࠵ࡡࡥࡦࡲࡲ࠳ࡾ࡭࡭ࠩऋ")), l111Fuck_You_Anonymous (u"࠭ࡲࠬࠩऌ")) as f:
		l1lll11Fuck_You_Anonymous = f.read()
		if re.search(l111Fuck_You_Anonymous (u"ࡲࠨࡸࡨࡶࡸ࡯࡯࡯࠿ࠥࠩࡸࠨࠧऍ") %version, l1lll11Fuck_You_Anonymous):
			l1ll1Fuck_You_Anonymous.log(l111Fuck_You_Anonymous (u"ࠨࡘࡨࡶࡸ࡯࡯࡯ࠢࡆ࡬ࡪࡩ࡫ࠡࡑࡎࠫऎ"))
		else:
			l11Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠤ࡚ࡶࡴࡴࡧࠡࡘࡨࡶࡸ࡯࡯࡯ࠢࡒࡪࠥࡓࡵࡤ࡭ࡼࡷࠥࡉ࡯࡮࡯ࡲࡲࠥࡓ࡯ࡥࡷ࡯ࡩࠧए")
			l1l1ll1lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠥࡔࡱ࡫ࡡࡴࡧࠣࡍࡳࡹࡴࡢ࡮࡯ࠤࡈࡵࡲࡳࡧࡦࡸࠥ࡜ࡥࡳࡵ࡬ࡳࡳࠦࡆࡳࡱࡰࠤ࡙࡮ࡥࠡࡔࡨࡴࡴࠨऐ")
			l1l1lll1Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠦࡅࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟࡫ࡸࡹࡶ࠺࠰࠱ࡰࡹࡨࡱࡹࡴ࠰ࡰࡩࡩ࡯ࡡࡱࡱࡵࡸࡦࡲ࠴࡬ࡱࡧ࡭࠳ࡳ࡬࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤऑ")
			l1ll1Fuck_You_Anonymous.show_ok_dialog([l11Fuck_You_Anonymous, l1l1ll1lFuck_You_Anonymous, l1l1lll1Fuck_You_Anonymous], l1l11Fuck_You_Anonymous)
			xbmc.executebuiltin(l111Fuck_You_Anonymous (u"ࠧ࡞ࡂࡎࡅ࠱ࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡕࡱࡦࡤࡸࡪ࠮ࡰࡢࡶ࡫࠰ࡷ࡫ࡰ࡭ࡣࡦࡩ࠮ࠨऒ"))
			xbmc.executebuiltin(l111Fuck_You_Anonymous (u"ࠨࡘࡃࡏࡆ࠲ࡆࡩࡴࡪࡸࡤࡸࡪ࡝ࡩ࡯ࡦࡲࡻ࠭ࡎ࡯࡮ࡧࠬࠦओ"))
def l11lllllFuck_You_Anonymous(url, content):
	l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"ࠧࡔࡧ࡯ࡩࡨࡺࠠࡔࡱࡵࡸࠥࡓࡥࡵࡪࡲࡨࠬऔ"),sort)
	l1llll11Fuck_You_Anonymous = l1llllFuck_You_Anonymous[l1llll1Fuck_You_Anonymous]
	link = open_url(url,verify=False).content
	match = re.findall(l111Fuck_You_Anonymous (u"ࡳࠩ࠿ࡰ࡮ࡄ࠼࡭ࡣࡥࡩࡱࡄ࠼ࡪࡰࡳࡹࡹࠦࡣ࡭ࡣࡶࡷࡂࠨࡧࡦࡰࡵࡩ࠲࡯ࡤࡴࠤࠣࡺࡦࡲࡵࡦ࠿ࠥࠬࡠࡤࠢ࡞࠭ࠬࠦࠥࡴࡡ࡮ࡧࡀࠦ࠳࠰࠿ࠣࠢࡷࡽࡵ࡫࠽ࠣࡥ࡫ࡩࡨࡱࡢࡰࡺࠥࠤࠥࡄࠨ࡜ࡠ࠿ࡂࡢ࠰ࠩ࠽࠱࡯ࡥࡧ࡫࡬࠿࠾࠲ࡰ࡮ࡄࠧक"), str(link), re.I|re.DOTALL)
	for l1ll1l1Fuck_You_Anonymous,name in match:
		name = name.replace(l111Fuck_You_Anonymous (u"ࠩࠣࠫख"),l111Fuck_You_Anonymous (u"ࠪࠫग"))
		if content == l111Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬघ"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬङ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹ࠮࡫ࡲࡪࠫच")}
			url = l111Fuck_You_Anonymous (u"ࠧࠦࡵ࠲ࡪ࡮ࡲࡴࡦࡴ࠲ࡃࡸࡵࡲࡵ࠿ࠨࡷࠫࡺࡹࡱࡧࡀࡷࡪࡸࡩࡦࡵࠩࡵࡺࡧ࡬ࡪࡶࡼࡁࡦࡲ࡬ࠧࡩࡨࡲࡷ࡫ࡳࠦࠧ࠸ࡆࠪࠫ࠵ࡅ࠿ࠨࡷࠫࡿࡥࡢࡴࡀࡥࡱࡲࠧछ") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous,l1ll1l1Fuck_You_Anonymous)
			md.addDir({l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ज"): l111Fuck_You_Anonymous (u"ࠩ࠵ࠫझ"), l111Fuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨञ"):l111Fuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡋࡠ࡟ࡈࡕࡌࡐࡔࠣࡷࡹ࡫ࡥ࡭ࡤ࡯ࡹࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫट") %name, l111Fuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩठ"):url, l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧड"):content}, fan_art=l11l11lFuck_You_Anonymous)
		elif content == l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧढ"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠨࡨࡤࡲࡦࡸࡴࠨण"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠩࡰࡳࡻ࡯ࡥࡴ࠰࡭ࡴ࡬࠭त")}
			url = l111Fuck_You_Anonymous (u"ࠪࠩࡸ࠵ࡦࡪ࡮ࡷࡩࡷ࠵࠿ࡴࡱࡵࡸࡂࠫࡳࠧࡶࡼࡴࡪࡃ࡭ࡰࡸ࡬ࡩࠫࡷࡵࡢ࡮࡬ࡸࡾࡃࡡ࡭࡮ࠩ࡫ࡪࡴࡲࡦࡵࠨࠩ࠺ࡈࠥࠦ࠷ࡇࡁࠪࡹࠦࡺࡧࡤࡶࡂࡧ࡬࡭ࠩथ") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous,l1ll1l1Fuck_You_Anonymous)
			md.addDir({l111Fuck_You_Anonymous (u"ࠫࡲࡵࡤࡦࠩद"): l111Fuck_You_Anonymous (u"ࠬ࠸ࠧध"), l111Fuck_You_Anonymous (u"࠭࡮ࡢ࡯ࡨࠫन"):l111Fuck_You_Anonymous (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡳࡵࡧࡨࡰࡧࡲࡵࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧऩ") %name, l111Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬप"):url, l111Fuck_You_Anonymous (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪफ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	setView(l1lll1llFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠪࡪ࡮ࡲࡥࡴࠩब"), l111Fuck_You_Anonymous (u"ࠫࡲ࡫࡮ࡶ࠯ࡹ࡭ࡪࡽࠧभ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l11l11Fuck_You_Anonymous(url, content):
	l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"࡙ࠬࡥ࡭ࡧࡦࡸ࡙ࠥ࡯ࡳࡶࠣࡑࡪࡺࡨࡰࡦࠪम"),sort)
	l1llll11Fuck_You_Anonymous = l1llllFuck_You_Anonymous[l1llll1Fuck_You_Anonymous]
	link = open_url(url,verify=False).content
	match = re.findall(l111Fuck_You_Anonymous (u"ࡸࠧ࠽࡮࡬ࡂࡁࡲࡡࡣࡧ࡯ࡂࡁ࡯࡮ࡱࡷࡷࠤࡨࡲࡡࡴࡵࡀࠦࡨࡵࡵ࡯ࡶࡵࡽ࠲࡯ࡤࡴࠤࠣࡺࡦࡲࡵࡦ࠿ࠥࠬࡠࡤࠢ࡞࠭ࠬࠦࠥࡴࡡ࡮ࡧࡀࠦ࠳࠰࠿ࠣࠢࡷࡽࡵ࡫࠽ࠣࡥ࡫ࡩࡨࡱࡢࡰࡺࠥࠤࠥࡄࠨ࡜ࡠ࠿ࡂࡢ࠰ࠩ࠽࠱࡯ࡥࡧ࡫࡬࠿࠾࠲ࡰ࡮ࡄࠧय"), str(link), re.I|re.DOTALL)
	for l1l1l1lFuck_You_Anonymous,name in match:
		name = name.replace(l111Fuck_You_Anonymous (u"ࠧࠡࠩर"),l111Fuck_You_Anonymous (u"ࠨࠩऱ"))
		if content == l111Fuck_You_Anonymous (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪल"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠪࡪࡦࡴࡡࡳࡶࠪळ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷ࠳ࡰࡰࡨࠩऴ")}
			url = l111Fuck_You_Anonymous (u"ࠬࠫࡳ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰ࡁࡶࡳࡷࡺ࠽ࠦࡵࠩࡸࡾࡶࡥ࠾ࡵࡨࡶ࡮࡫ࡳࠧࡳࡸࡥࡱ࡯ࡴࡺ࠿ࡤࡰࡱࠬࡣࡰࡷࡱࡸࡷ࡯ࡥࡴࠧࠨ࠹ࡇࠫࠥ࠶ࡆࡀࠩࡸࠬࡹࡦࡣࡵࡁࡦࡲ࡬ࠨव") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous,l1l1l1lFuck_You_Anonymous)
			md.addDir({l111Fuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫश"): l111Fuck_You_Anonymous (u"ࠧ࠳ࠩष"), l111Fuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭स"):l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩह") %name, l111Fuck_You_Anonymous (u"ࠪࡹࡷࡲࠧऺ"):url, l111Fuck_You_Anonymous (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬऻ"):content}, fan_art=l11l11lFuck_You_Anonymous)
		elif content == l111Fuck_You_Anonymous (u"ࠬࡳ࡯ࡷ࡫ࡨࡷ़ࠬ"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"࠭ࡦࡢࡰࡤࡶࡹ࠭ऽ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡹ࡭ࡪࡹ࠮࡫ࡲࡪࠫा")}
			url = l111Fuck_You_Anonymous (u"ࠨࠧࡶ࠳࡫࡯࡬ࡵࡧࡵ࠳ࡄࡹ࡯ࡳࡶࡀࠩࡸࠬࡴࡺࡲࡨࡁࡲࡵࡶࡪࡧࠩࡵࡺࡧ࡬ࡪࡶࡼࡁࡦࡲ࡬ࠧࡥࡲࡹࡳࡺࡲࡪࡧࡶࠩࠪ࠻ࡂࠦࠧ࠸ࡈࡂࠫࡳࠧࡻࡨࡥࡷࡃࡡ࡭࡮ࠪि") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous,l1l1l1lFuck_You_Anonymous)
			md.addDir({l111Fuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧी"): l111Fuck_You_Anonymous (u"ࠪ࠶ࠬु"), l111Fuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩू"):l111Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤࡸࡺࡥࡦ࡮ࡥࡰࡺ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬृ") %name, l111Fuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪॄ"):url, l111Fuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨॅ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	setView(l1lll1llFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠨࡨ࡬ࡰࡪࡹࠧॆ"), l111Fuck_You_Anonymous (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬे"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1lll1Fuck_You_Anonymous(url, content):
	if content == l111Fuck_You_Anonymous (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫै"):
		l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫॉ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠴ࡪࡱࡩࠪॊ")}
		url = l111Fuck_You_Anonymous (u"࠭ࠥࡴ࠱ࡩ࡭ࡱࡺࡥࡳ࠱ࡂࡷࡴࡸࡴ࠾ࠧࡶࠪࡹࡿࡰࡦ࠿ࡶࡩࡷ࡯ࡥࡴࠨࡴࡹࡦࡲࡩࡵࡻࡀࡥࡱࡲࠦࡺࡧࡤࡶࡂ࠸࠰࠲࠹ࠪो") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous)
		md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬौ"): l111Fuck_You_Anonymous (u"ࠨ࠴्ࠪ"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧॎ"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢ࠸࠰࠲࠹࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬॏ"), l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨॐ"):url, l111Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭॑"):content}, fan_art=l11l11lFuck_You_Anonymous)
	elif content == l111Fuck_You_Anonymous (u"࠭࡭ࡰࡸ࡬ࡩࡸ॒࠭"):
		l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠧࡧࡣࡱࡥࡷࡺࠧ॓"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡺ࡮࡫ࡳ࠯࡬ࡳ࡫ࠬ॔")}
		url = l111Fuck_You_Anonymous (u"ࠩࠨࡷ࠴࡬ࡩ࡭ࡶࡨࡶ࠴ࡅࡳࡰࡴࡷࡁࠪࡹࠦࡵࡻࡳࡩࡂࡳ࡯ࡷ࡫ࡨࠪࡶࡻࡡ࡭࡫ࡷࡽࡂࡧ࡬࡭ࠨࡼࡩࡦࡸ࠽࠳࠲࠴࠻ࠬॕ") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous)
		md.addDir({l111Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨॖ"): l111Fuck_You_Anonymous (u"ࠫ࠷࠭ॗ"), l111Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪक़"):l111Fuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥࡹࡴࡦࡧ࡯ࡦࡱࡻࡥ࡞࠴࠳࠵࠼ࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨख़"), l111Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫग़"):url, l111Fuck_You_Anonymous (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩज़"):content}, fan_art=l11l11lFuck_You_Anonymous)
	l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"ࠩࡖࡩࡱ࡫ࡣࡵࠢࡖࡳࡷࡺࠠࡎࡧࡷ࡬ࡴࡪࠧड़"),sort)
	l1llll11Fuck_You_Anonymous = l1llllFuck_You_Anonymous[l1llll1Fuck_You_Anonymous]
	link = open_url(url,verify=False).content
	match = re.findall(l111Fuck_You_Anonymous (u"ࡵࠫࡁ࡯࡮ࡱࡷࡷࠤࡳࡧ࡭ࡦ࠿ࠥࡽࡪࡧࡲࠣࠢࡹࡥࡱࡻࡥ࠾ࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠤࡹࡿࡰࡦ࠿ࠥࡶࡦࡪࡩࡰࠤࠣࠤࡃ࠮࡛࡟࠾ࡁࡡ࠯࠯࠼࠰࡮ࡤࡦࡪࡲ࠾ࠨढ़"), str(link), re.I|re.DOTALL)
	for name,year in match:
		if content == l111Fuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬफ़"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬय़"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹ࠮࡫ࡲࡪࠫॠ")}
			url = l111Fuck_You_Anonymous (u"ࠧࠦࡵ࠲ࡪ࡮ࡲࡴࡦࡴ࠲ࡃࡸࡵࡲࡵ࠿ࠨࡷࠫࡺࡹࡱࡧࡀࡷࡪࡸࡩࡦࡵࠩࡵࡺࡧ࡬ࡪࡶࡼࡁࡦࡲ࡬ࠧࡻࡨࡥࡷࡃࠥࡴࠩॡ") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous,year)
			md.addDir({l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ॢ"): l111Fuck_You_Anonymous (u"ࠩ࠵ࠫॣ"), l111Fuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨ।"):l111Fuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡋࡠ࡟ࡈࡕࡌࡐࡔࠣࡷࡹ࡫ࡥ࡭ࡤ࡯ࡹࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫ॥") %name, l111Fuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩ०"):url, l111Fuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧ१"):content}, fan_art=l11l11lFuck_You_Anonymous)
		elif content == l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧ२"):
			l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠨࡨࡤࡲࡦࡸࡴࠨ३"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠩࡰࡳࡻ࡯ࡥࡴ࠰࡭ࡴ࡬࠭४")}
			url = l111Fuck_You_Anonymous (u"ࠪࠩࡸ࠵ࡦࡪ࡮ࡷࡩࡷ࠵࠿ࡴࡱࡵࡸࡂࠫࡳࠧࡶࡼࡴࡪࡃ࡭ࡰࡸ࡬ࡩࠫࡷࡵࡢ࡮࡬ࡸࡾࡃࡡ࡭࡮ࠩࡽࡪࡧࡲ࠾ࠧࡶࠫ५") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous,year)
			md.addDir({l111Fuck_You_Anonymous (u"ࠫࡲࡵࡤࡦࠩ६"): l111Fuck_You_Anonymous (u"ࠬ࠸ࠧ७"), l111Fuck_You_Anonymous (u"࠭࡮ࡢ࡯ࡨࠫ८"):l111Fuck_You_Anonymous (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡳࡵࡧࡨࡰࡧࡲࡵࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧ९") %name, l111Fuck_You_Anonymous (u"ࠨࡷࡵࡰࠬ॰"):url, l111Fuck_You_Anonymous (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪॱ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	if content == l111Fuck_You_Anonymous (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫॲ"):
		l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫॳ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠴ࡪࡱࡩࠪॴ")}
		url = l111Fuck_You_Anonymous (u"࠭ࠥࡴ࠱ࡩ࡭ࡱࡺࡥࡳ࠱ࡂࡷࡴࡸࡴ࠾ࠧࡶࠪࡹࡿࡰࡦ࠿ࡶࡩࡷ࡯ࡥࡴࠨࡴࡹࡦࡲࡩࡵࡻࡀࡥࡱࡲࠦࡺࡧࡤࡶࡂࡵ࡬ࡥࡧࡵࠫॵ") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous)
		md.addDir({l111Fuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬॶ"): l111Fuck_You_Anonymous (u"ࠨ࠴ࠪॷ"), l111Fuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧॸ"):l111Fuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡶࡸࡪ࡫࡬ࡣ࡮ࡸࡩࡢࡕ࡬ࡥࡧࡵ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ॹ"), l111Fuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨॺ"):url, l111Fuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ॻ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	elif content == l111Fuck_You_Anonymous (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ॼ"):
		l11l11lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"ࠧࡧࡣࡱࡥࡷࡺࠧॽ"):l11l1lFuck_You_Anonymous+l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡺ࡮࡫ࡳ࠯࡬ࡳ࡫ࠬॾ")}
		url = l111Fuck_You_Anonymous (u"ࠩࠨࡷ࠴࡬ࡩ࡭ࡶࡨࡶ࠴ࡅࡳࡰࡴࡷࡁࠪࡹࠦࡵࡻࡳࡩࡂࡳ࡯ࡷ࡫ࡨࠪࡶࡻࡡ࡭࡫ࡷࡽࡂࡧ࡬࡭ࠨࡼࡩࡦࡸ࠽ࡰ࡮ࡧࡩࡷ࠭ॿ") %(l111111Fuck_You_Anonymous,l1llll11Fuck_You_Anonymous)
		md.addDir({l111Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨঀ"): l111Fuck_You_Anonymous (u"ࠫ࠷࠭ঁ"), l111Fuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪং"):l111Fuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥࡹࡴࡦࡧ࡯ࡦࡱࡻࡥ࡞ࡑ࡯ࡨࡪࡸ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩঃ"), l111Fuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ঄"):url, l111Fuck_You_Anonymous (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩঅ"):content}, fan_art=l11l11lFuck_You_Anonymous)
	setView(l1lll1llFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠩࡩ࡭ࡱ࡫ࡳࠨআ"), l111Fuck_You_Anonymous (u"ࠪࡱࡪࡴࡵ࠮ࡸ࡬ࡩࡼ࠭ই"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l111l1Fuck_You_Anonymous(content, query):
	try:
		if query:
			search = query.replace(l111Fuck_You_Anonymous (u"ࠫࠥ࠭ঈ"),l111Fuck_You_Anonymous (u"ࠬ࠱ࠧউ"))
		else:
			search = md.search()
			if search == l111Fuck_You_Anonymous (u"࠭ࠧঊ"):
				md.notification(l111Fuck_You_Anonymous (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡡࡂ࡞ࡇࡐࡔ࡙࡟ࠠࡒࡗࡈࡖ࡞ࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠ࠰ࡆࡨ࡯ࡳࡶ࡬ࡲ࡬ࠦࡳࡦࡣࡵࡧ࡭࠭ঋ"),l1l11l11Fuck_You_Anonymous)
				return
			else:
				pass
		url = l111Fuck_You_Anonymous (u"ࠨࠧࡶ࠳ࡸ࡫ࡡࡳࡥ࡫࠳ࡄࡷ࠽ࠦࡵࠪঌ") %(l111111Fuck_You_Anonymous,search)
		l11ll1Fuck_You_Anonymous(url,content)
	except:
		md.notification(l111Fuck_You_Anonymous (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝࡜ࡄࡠࡗࡴࡸࡲࡺࠢࡑࡳࠥࡘࡥࡴࡷ࡯ࡸࡸࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫ঍"),l1l11l11Fuck_You_Anonymous)
key = l111Fuck_You_Anonymous (u"ࠪࡍ࡚ࡇࡪࡋࡅ࡙ࡩࡏ࡯࡯ࡰࠩ঎")
def l1l1l1Fuck_You_Anonymous(url,name,l11111Fuck_You_Anonymous,content,l1l1llFuck_You_Anonymous,query):
        l1ll1llFuck_You_Anonymous = []
	l1l1l11Fuck_You_Anonymous = []
	l11l1l1Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠫࠬএ")
	if content == l111Fuck_You_Anonymous (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬঐ"):
                link = open_url(url,verify=False).content
		l11l111Fuck_You_Anonymous = re.findall(l111Fuck_You_Anonymous (u"ࡸࠧ࠽࡫ࠣࡧࡱࡧࡳࡴ࠿ࠥࡪࡦࠦࡦࡢ࠯ࡶࡩࡷࡼࡥࡳࠢࡰࡶ࠺ࠨ࠾࠽࠱࡬ࡂࡁࡹࡴࡳࡱࡱ࡫ࡃ࠮࠮ࠫࡁࠬࡀ࠴ࡹࡴࡳࡱࡱ࡫ࡃ࠴ࠪࡀ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠰࠿ࠪࠤࠣ࠲࠯ࡅ࠾ࠨ঑"), str(link), re.I|re.DOTALL)
		l111l11Fuck_You_Anonymous = []
		l1l11ll1Fuck_You_Anonymous = []
		l1ll1lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠧࠨ঒")
		for l1lll1lFuck_You_Anonymous, l1l1l111Fuck_You_Anonymous in l11l111Fuck_You_Anonymous:
			if l111Fuck_You_Anonymous (u"ࠨࡕࡈࡖ࡛ࡋࡒࠨও") in l1lll1lFuck_You_Anonymous:
				l1ll1lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡵࡷࡩࡪࡲࡢ࡭ࡷࡨࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩঔ") %l1lll1lFuck_You_Anonymous
				l111l11Fuck_You_Anonymous.append(l1ll1lFuck_You_Anonymous)
				l1l11ll1Fuck_You_Anonymous.append(l1l1l111Fuck_You_Anonymous)
		if l11ll11Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠪࡸࡷࡻࡥࠨক"):
			request_url = l1l11ll1Fuck_You_Anonymous[0]
		else:
			if len(l11l111Fuck_You_Anonymous) > 1:
				l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"ࠫࡕࡲࡥࡢࡵࡨࠤࡈ࡮࡯ࡰࡵࡨࠤࡆࠦࡓࡦࡴࡹࡩࡷ࠭খ"),l111l11Fuck_You_Anonymous)
				if l1llll1Fuck_You_Anonymous == -1:
					return
				elif l1llll1Fuck_You_Anonymous > -1:
					request_url = l1l11ll1Fuck_You_Anonymous[l1llll1Fuck_You_Anonymous]
			else:
				request_url = l1l11ll1Fuck_You_Anonymous[0]
	else:
		request_url = url
	l1l1l11lFuck_You_Anonymous = open_url(request_url,verify=False).content
	l1ll11lFuck_You_Anonymous = re.findall(l111Fuck_You_Anonymous (u"ࡷ࠭ࡥࡱ࡫ࡶࡳࡩ࡫࠺ࠡࠤࠫ࠲࠯ࡅࠩࠣࠩগ"), str(l1l1l11lFuck_You_Anonymous), re.I|re.DOTALL)[2]
	l1l11l1lFuck_You_Anonymous = l111111Fuck_You_Anonymous.replace(l111Fuck_You_Anonymous (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࠧঘ"),l111Fuck_You_Anonymous (u"ࠧࠨঙ")).replace(l111Fuck_You_Anonymous (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪচ"),l111Fuck_You_Anonymous (u"ࠩࠪছ"))
	try:
		l1lllFuck_You_Anonymous = llFuck_You_Anonymous()
		l1l1lFuck_You_Anonymous = re.findall(l111Fuck_You_Anonymous (u"ࡵࠫ࡭ࡧࡳࡩ࠼ࠣࠦ࠭࠴ࠪࡀࠫࠥࠫজ"), str(l1l1l11lFuck_You_Anonymous), re.I|re.DOTALL)[0]
		cookie = l111Fuck_You_Anonymous (u"ࠫࠪࡹ࠽ࠦࡵࠪঝ") %(hashlib.md5(key.decode(l111Fuck_You_Anonymous (u"ࠬࡨࡡࡴࡧ࠹࠸ࠬঞ"))[::1] + l1ll11lFuck_You_Anonymous + l1lllFuck_You_Anonymous).hexdigest(),
				   hashlib.md5(l1lllFuck_You_Anonymous + request_url + l1ll11lFuck_You_Anonymous).hexdigest())
		l1l1111Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡰ࡭ࡣࡼ࠲ࠪࡹ࠯ࡨࡴࡤࡦࡧ࡫ࡲ࠮ࡣࡳ࡭࠴࡫ࡰࡪࡵࡲࡨࡪ࠵ࠥࡴࡁࡷࡳࡰ࡫࡮࠾ࠧࡶࠫট") %(l1l11l1lFuck_You_Anonymous,l1ll11lFuck_You_Anonymous,l1lllFuck_You_Anonymous)
		headers = {l111Fuck_You_Anonymous (u"ࠧࡂࡥࡦࡩࡵࡺ࠭ࡆࡰࡦࡳࡩ࡯࡮ࡨࠩঠ"):l111Fuck_You_Anonymous (u"ࠨࡩࡽ࡭ࡵ࠲ࠠࡥࡧࡩࡰࡦࡺࡥ࠭ࠢࡶࡨࡨ࡮ࠧড"), l111Fuck_You_Anonymous (u"ࠩࡆࡳࡴࡱࡩࡦࠩঢ"): cookie, l111Fuck_You_Anonymous (u"ࠪࡖࡪ࡬ࡥࡳࡧࡵࠫণ"): request_url,
			   l111Fuck_You_Anonymous (u"ࠫࡔࡸࡩࡨ࡫ࡱࠫত"):l111111Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩথ"):md.User_Agent()}
		final = open_url(l1l1111Fuck_You_Anonymous, headers=headers, verify=False).json()
		if l11ll11Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"࠭ࡴࡳࡷࡨࠫদ"):
			url = max(final[l111Fuck_You_Anonymous (u"ࠧࡱ࡮ࡤࡽࡱ࡯ࡳࡵࠩধ")][0][l111Fuck_You_Anonymous (u"ࠨࡵࡲࡹࡷࡩࡥࡴࠩন")], key=lambda l1l11lllFuck_You_Anonymous: int(re.sub(l111Fuck_You_Anonymous (u"ࠩ࡟ࡈࠬ঩"), l111Fuck_You_Anonymous (u"ࠪࠫপ"), l1l11lllFuck_You_Anonymous[l111Fuck_You_Anonymous (u"ࠫࡱࡧࡢࡦ࡮ࠪফ")])))
			url = url[l111Fuck_You_Anonymous (u"ࠬ࡬ࡩ࡭ࡧࠪব")]
		else:
			match = final[l111Fuck_You_Anonymous (u"࠭ࡰ࡭ࡣࡼࡰ࡮ࡹࡴࠨভ")][0][l111Fuck_You_Anonymous (u"ࠧࡴࡱࡸࡶࡨ࡫ࡳࠨম")]
			for a in match:
				l11l1l1Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡴࡶࡨࡩࡱࡨ࡬ࡶࡧࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨয") %a[l111Fuck_You_Anonymous (u"ࠩ࡯ࡥࡧ࡫࡬ࠨর")]
				l1ll1llFuck_You_Anonymous.append(l11l1l1Fuck_You_Anonymous)
				l1l1l11Fuck_You_Anonymous.append(a[l111Fuck_You_Anonymous (u"ࠪࡪ࡮ࡲࡥࠨ঱")])
			if len(match) >1:
				l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"ࠫࡘ࡫࡬ࡦࡥࡷࠤࡘࡺࡲࡦࡣࡰࠤࡖࡻࡡ࡭࡫ࡷࡽࠬল"),l1ll1llFuck_You_Anonymous)
				if l1llll1Fuck_You_Anonymous == -1:
					return
				elif l1llll1Fuck_You_Anonymous > -1:
					url = l1l1l11Fuck_You_Anonymous[l1llll1Fuck_You_Anonymous]
			else:
				url = max(final[l111Fuck_You_Anonymous (u"ࠬࡶ࡬ࡢࡻ࡯࡭ࡸࡺࠧ঳")][0][l111Fuck_You_Anonymous (u"࠭ࡳࡰࡷࡵࡧࡪࡹࠧ঴")], key=lambda l1l11lllFuck_You_Anonymous: int(re.sub(l111Fuck_You_Anonymous (u"ࠧ࡝ࡆࠪ঵"), l111Fuck_You_Anonymous (u"ࠨࠩশ"), l1l11lllFuck_You_Anonymous[l111Fuck_You_Anonymous (u"ࠩ࡯ࡥࡧ࡫࡬ࠨষ")])))
				url = url[l111Fuck_You_Anonymous (u"ࠪࡪ࡮ࡲࡥࠨস")]
		if l111111Fuck_You_Anonymous not in url:
			if l111Fuck_You_Anonymous (u"ࠫ࡬ࡵ࡯ࡨ࡮ࡨࠫহ") not in url:
				url = l111111Fuck_You_Anonymous + url
	except:
		l1l1111Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡶ࡬ࡢࡻ࠱ࠩࡸ࠵ࡴࡰ࡭ࡨࡲ࠳ࡶࡨࡱࠩ঺") %l1l11l1lFuck_You_Anonymous
		l1ll1ll1Fuck_You_Anonymous = {l111Fuck_You_Anonymous (u"࠭ࡩࡥࠩ঻"):l1ll11lFuck_You_Anonymous}
		headers = {l111Fuck_You_Anonymous (u"ࠧࡂࡥࡦࡩࡵࡺ়ࠧ"):l111Fuck_You_Anonymous (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱ࠰ࠥࡺࡥࡹࡶ࠲࡮ࡦࡼࡡࡴࡥࡵ࡭ࡵࡺࠬࠡࠬ࠲࠮ࡀࠦࡱ࠾࠲࠱࠴࠶࠭ঽ"),
			   l111Fuck_You_Anonymous (u"ࠩࡄࡧࡨ࡫ࡰࡵ࠯ࡈࡲࡨࡵࡤࡪࡰࡪࠫা"):l111Fuck_You_Anonymous (u"ࠪ࡫ࡿ࡯ࡰ࠭ࠢࡧࡩ࡫ࡲࡡࡵࡧࠪি"), l111Fuck_You_Anonymous (u"ࠫࡔࡸࡩࡨ࡫ࡱࠫী"):l111111Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠬࡘࡥࡧࡧࡵࡩࡷ࠭ু"):request_url, l111Fuck_You_Anonymous (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪূ"):md.User_Agent()}
		params = open_url(l1l1111Fuck_You_Anonymous, method=l111Fuck_You_Anonymous (u"ࠧࡱࡱࡶࡸࠬৃ"), data=l1ll1ll1Fuck_You_Anonymous, headers=headers, verify=False).json()
		del params[l111Fuck_You_Anonymous (u"ࠨࡵࡷࡥࡹࡻࡳࠨৄ")]
		l1l111lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡳࡰࡦࡿ࠮ࠦࡵ࠲࡫ࡷࡧࡢࡣࡧࡵ࠱ࡦࡶࡩ࠮ࡸ࠵࠳ࡪࡶࡩࡴࡱࡧࡩ࠴ࠫࡳࠨ৅") %(l1l11l1lFuck_You_Anonymous,l1ll11lFuck_You_Anonymous)
		final = open_url(l1l111lFuck_You_Anonymous, params=params, headers=headers, verify=False).json()
		try:
			if l11ll11Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠪࡸࡷࡻࡥࠨ৆"):
				url = max(final[l111Fuck_You_Anonymous (u"ࠫࡵࡲࡡࡺ࡮࡬ࡷࡹ࠭ে")][0][l111Fuck_You_Anonymous (u"ࠬࡹ࡯ࡶࡴࡦࡩࡸ࠭ৈ")], key=lambda l1l11lllFuck_You_Anonymous: int(re.sub(l111Fuck_You_Anonymous (u"࠭࡜ࡅࠩ৉"), l111Fuck_You_Anonymous (u"ࠧࠨ৊"), l1l11lllFuck_You_Anonymous[l111Fuck_You_Anonymous (u"ࠨ࡮ࡤࡦࡪࡲࠧো")])))
				url = url[l111Fuck_You_Anonymous (u"ࠩࡩ࡭ࡱ࡫ࠧৌ")]
			else:
				match = final[l111Fuck_You_Anonymous (u"ࠪࡴࡱࡧࡹ࡭࡫ࡶࡸ্ࠬ")][0][l111Fuck_You_Anonymous (u"ࠫࡸࡵࡵࡳࡥࡨࡷࠬৎ")]
				for a in match:
					l11l1l1Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤࡸࡺࡥࡦ࡮ࡥࡰࡺ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬ৏") %a[l111Fuck_You_Anonymous (u"࠭࡬ࡢࡤࡨࡰࠬ৐")]
					l1ll1llFuck_You_Anonymous.append(l11l1l1Fuck_You_Anonymous)
					l1l1l11Fuck_You_Anonymous.append(a[l111Fuck_You_Anonymous (u"ࠧࡧ࡫࡯ࡩࠬ৑")])
				if len(match) >1:
					l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"ࠨࡕࡨࡰࡪࡩࡴࠡࡕࡷࡶࡪࡧ࡭ࠡࡓࡸࡥࡱ࡯ࡴࡺࠩ৒"),l1ll1llFuck_You_Anonymous)
					if l1llll1Fuck_You_Anonymous == -1:
						return
					elif l1llll1Fuck_You_Anonymous > -1:
						url = l1l1l11Fuck_You_Anonymous[l1llll1Fuck_You_Anonymous]
				else:
					url = max(final[l111Fuck_You_Anonymous (u"ࠩࡳࡰࡦࡿ࡬ࡪࡵࡷࠫ৓")][0][l111Fuck_You_Anonymous (u"ࠪࡷࡴࡻࡲࡤࡧࡶࠫ৔")], key=lambda l1l11lllFuck_You_Anonymous: int(re.sub(l111Fuck_You_Anonymous (u"ࠫࡡࡊࠧ৕"), l111Fuck_You_Anonymous (u"ࠬ࠭৖"), l1l11lllFuck_You_Anonymous[l111Fuck_You_Anonymous (u"࠭࡬ࡢࡤࡨࡰࠬৗ")])))
					url = url[l111Fuck_You_Anonymous (u"ࠧࡧ࡫࡯ࡩࠬ৘")]
		except:
			l1l1ll11Fuck_You_Anonymous = int(time.time() * 1000)
			l1l11l1Fuck_You_Anonymous = final[l111Fuck_You_Anonymous (u"ࠨࡤࡤࡧࡰࡻࡰࠨ৙")]
			l1llll1lFuck_You_Anonymous = l1l11l1Fuck_You_Anonymous
			if l111Fuck_You_Anonymous (u"ࠩ࡫ࡸࡹࡶ࠺ࠨ৚") not in l1llll1lFuck_You_Anonymous:
			    l1llll1lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠪ࡬ࡹࡺࡰ࠻ࠩ৛") + l1llll1lFuck_You_Anonymous
			if l111Fuck_You_Anonymous (u"ࠫ࡭ࡺࡴࡱ࠼ࠪড়") not in l1l11l1Fuck_You_Anonymous:
			    l1l11l1Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠬ࡮ࡴࡵࡲ࠽ࠩࡸࠬ࡟࠾ࠧࡶࠪࡹࡿࡰࡦ࠿ࡷࡳࡰ࡫࡮ࠨঢ়") %(l1l11l1Fuck_You_Anonymous,l1l1ll11Fuck_You_Anonymous)
			headers = {l111Fuck_You_Anonymous (u"࠭ࡁࡤࡥࡨࡴࡹ࠭৞"):l111Fuck_You_Anonymous (u"ࠧࡵࡧࡻࡸ࠴ࡰࡡࡷࡣࡶࡧࡷ࡯ࡰࡵ࠮ࠣࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡤࡺࡦࡹࡣࡳ࡫ࡳࡸ࠱ࠦࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡪࡩ࡭ࡢࡵࡦࡶ࡮ࡶࡴ࠭ࠢࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡨࡧࡲࡧࡳࡤࡴ࡬ࡴࡹ࠲ࠠࠫ࠱࠭࠿ࠥࡷ࠽࠱࠰࠳࠵ࠬয়"),
				   l111Fuck_You_Anonymous (u"ࠨࡃࡦࡧࡪࡶࡴ࠮ࡇࡱࡧࡴࡪࡩ࡯ࡩࠪৠ"):l111Fuck_You_Anonymous (u"ࠩࡪࡾ࡮ࡶࠬࠡࡦࡨࡪࡱࡧࡴࡦ࠮ࠣࡷࡩࡩࡨࠨৡ"), l111Fuck_You_Anonymous (u"ࠪࡅࡨࡩࡥࡱࡶ࠰ࡐࡦࡴࡧࡶࡣࡪࡩࠬৢ"):l111Fuck_You_Anonymous (u"ࠫࡪࡴ࠭ࡖࡕ࠯ࡩࡳࡁࡱ࠾࠲࠱࠼ࠬৣ"),
				   l111Fuck_You_Anonymous (u"ࠬࡘࡥࡧࡧࡵࡩࡷ࠭৤"):l1llll1lFuck_You_Anonymous, l111Fuck_You_Anonymous (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪ৥"):md.User_Agent(), l111Fuck_You_Anonymous (u"࡙ࠧ࠯ࡕࡩࡶࡻࡥࡴࡶࡨࡨ࠲࡝ࡩࡵࡪࠪ০"):l111Fuck_You_Anonymous (u"ࠨ࡚ࡐࡐࡍࡺࡴࡱࡔࡨࡵࡺ࡫ࡳࡵࠩ১")}
			l1ll111Fuck_You_Anonymous = open_url(l1l11l1Fuck_You_Anonymous, headers=headers, verify=False).content
			l1lllllFuck_You_Anonymous = re.compile(l111Fuck_You_Anonymous (u"ࠩࡨ࡭ࡩࡃࠨ࠯ࠬࡂ࠭ࠫ࠭২")).findall(l1l11l1Fuck_You_Anonymous)[0]
			l11lll1Fuck_You_Anonymous = re.compile(l111Fuck_You_Anonymous (u"ࠥࡣࡽࡃࠧࠩ࡝ࡡࠫࡢ࠱ࠩࠨࠤ৩")).findall(l1ll111Fuck_You_Anonymous)[0]
			l11ll1lFuck_You_Anonymous = re.compile(l111Fuck_You_Anonymous (u"ࠦࡤࡿ࠽ࠨࠪ࡞ࡢࠬࡣࠫࠪࠩࠥ৪")).findall(l1ll111Fuck_You_Anonymous)[0]
			l1l111Fuck_You_Anonymous = l1l11l1Fuck_You_Anonymous.split(l111Fuck_You_Anonymous (u"ࠬࡅࠧ৫"))[0]
			l1lFuck_You_Anonymous = {l111Fuck_You_Anonymous (u"࠭ࡴࡺࡲࡨࠫ৬"):l111Fuck_You_Anonymous (u"ࠧࡴࡱࡸࡶࡨ࡫ࡳࠨ৭"), l111Fuck_You_Anonymous (u"ࠨࡧ࡬ࡨࠬ৮"):l1lllllFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠩࡻࠫ৯"):l11lll1Fuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠪࡽࠬৰ"):l11ll1lFuck_You_Anonymous}
			headers = {l111Fuck_You_Anonymous (u"ࠫࡆࡩࡣࡦࡲࡷࠫৱ"):l111Fuck_You_Anonymous (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮࠭ࠢࡷࡩࡽࡺ࠯࡫ࡣࡹࡥࡸࡩࡲࡪࡲࡷ࠰ࠥ࠰࠯ࠫ࠽ࠣࡵࡂ࠶࠮࠱࠳ࠪ৲"), l111Fuck_You_Anonymous (u"࠭ࡁࡤࡥࡨࡴࡹ࠳ࡅ࡯ࡥࡲࡨ࡮ࡴࡧࠨ৳"):l111Fuck_You_Anonymous (u"ࠧࡨࡼ࡬ࡴ࠱ࠦࡤࡦࡨ࡯ࡥࡹ࡫ࠬࠡࡵࡧࡧ࡭࠭৴"),
				   l111Fuck_You_Anonymous (u"ࠨࡔࡨࡪࡪࡸࡥࡳࠩ৵"):l1llll1lFuck_You_Anonymous, l111Fuck_You_Anonymous (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭৶"):md.User_Agent(), l111Fuck_You_Anonymous (u"ࠪ࡜࠲ࡘࡥࡲࡷࡨࡷࡹ࡫ࡤ࠮࡙࡬ࡸ࡭࠭৷"):l111Fuck_You_Anonymous (u"ࠫ࡝ࡓࡌࡉࡶࡷࡴࡗ࡫ࡱࡶࡧࡶࡸࠬ৸")}
			final = open_url(l1l111Fuck_You_Anonymous, params=l1lFuck_You_Anonymous, headers=headers, verify=False).json()
			if l11ll11Fuck_You_Anonymous == l111Fuck_You_Anonymous (u"ࠬࡺࡲࡶࡧࠪ৹"):
				url = max(final[l111Fuck_You_Anonymous (u"࠭ࡰ࡭ࡣࡼࡰ࡮ࡹࡴࠨ৺")][0][l111Fuck_You_Anonymous (u"ࠧࡴࡱࡸࡶࡨ࡫ࡳࠨ৻")], key=lambda l1l11lllFuck_You_Anonymous: int(re.sub(l111Fuck_You_Anonymous (u"ࠨ࡞ࡇࠫৼ"), l111Fuck_You_Anonymous (u"ࠩࠪ৽"), l1l11lllFuck_You_Anonymous[l111Fuck_You_Anonymous (u"ࠪࡰࡦࡨࡥ࡭ࠩ৾")])))
				url = url[l111Fuck_You_Anonymous (u"ࠫ࡫࡯࡬ࡦࠩ৿")]
			else:
				match = final[l111Fuck_You_Anonymous (u"ࠬࡶ࡬ࡢࡻ࡯࡭ࡸࡺࠧ਀")][0][l111Fuck_You_Anonymous (u"࠭ࡳࡰࡷࡵࡧࡪࡹࠧਁ")]
				for a in match:
					l11l1l1Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡳࡵࡧࡨࡰࡧࡲࡵࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧਂ") %a[l111Fuck_You_Anonymous (u"ࠨ࡮ࡤࡦࡪࡲࠧਃ")]
					l1ll1llFuck_You_Anonymous.append(l11l1l1Fuck_You_Anonymous)
					l1l1l11Fuck_You_Anonymous.append(a[l111Fuck_You_Anonymous (u"ࠩࡩ࡭ࡱ࡫ࠧ਄")])
				if len(match) >1:
					l1llll1Fuck_You_Anonymous = md.dialog_select(l111Fuck_You_Anonymous (u"ࠪࡗࡪࡲࡥࡤࡶࠣࡗࡹࡸࡥࡢ࡯ࠣࡕࡺࡧ࡬ࡪࡶࡼࠫਅ"),l1ll1llFuck_You_Anonymous)
					if l1llll1Fuck_You_Anonymous == -1:
						return
					elif l1llll1Fuck_You_Anonymous > -1:
						url = l1l1l11Fuck_You_Anonymous[l1llll1Fuck_You_Anonymous]
				else:
					url = max(final[l111Fuck_You_Anonymous (u"ࠫࡵࡲࡡࡺ࡮࡬ࡷࡹ࠭ਆ")][0][l111Fuck_You_Anonymous (u"ࠬࡹ࡯ࡶࡴࡦࡩࡸ࠭ਇ")], key=lambda l1l11lllFuck_You_Anonymous: int(re.sub(l111Fuck_You_Anonymous (u"࠭࡜ࡅࠩਈ"), l111Fuck_You_Anonymous (u"ࠧࠨਉ"), l1l11lllFuck_You_Anonymous[l111Fuck_You_Anonymous (u"ࠨ࡮ࡤࡦࡪࡲࠧਊ")])))
					url = url[l111Fuck_You_Anonymous (u"ࠩࡩ࡭ࡱ࡫ࠧ਋")]
	url = url.replace(l111Fuck_You_Anonymous (u"ࠪࠪࡦࡳࡰ࠼ࠩ਌"),l111Fuck_You_Anonymous (u"ࠫࠫ࠭਍"))
	md.resolved(url, name, fan_art, l1l1llFuck_You_Anonymous)
	l1ll1Fuck_You_Anonymous.end_of_directory()
def llFuck_You_Anonymous(size=8, chars=string.ascii_letters + string.digits):
    return l111Fuck_You_Anonymous (u"ࠬ࠭਎").join(random.choice(chars) for x in range(size))
def l1ll11l1Fuck_You_Anonymous():
	l1111Fuck_You_Anonymous = xbmc.translatePath(l111Fuck_You_Anonymous (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹ࠯ࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼ࠲ࡲࡧࡦࠨਏ"))
	l11l1Fuck_You_Anonymous = xbmc.translatePath(l111Fuck_You_Anonymous (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡳࡰࡺ࡭ࡩ࡯࠰ࡳࡶࡴ࡭ࡲࡢ࡯࠱ࡱࡦ࡬ࡷࡪࡼࡤࡶࡩ࠭ਐ"))
	l1l1111lFuck_You_Anonymous = xbmc.translatePath(l111Fuck_You_Anonymous (u"ࠨࡵࡳࡩࡨ࡯ࡡ࡭࠼࠲࠳࡭ࡵ࡭ࡦ࠱ࡤࡨࡩࡵ࡮ࡴ࠱ࡳࡰࡺ࡭ࡩ࡯࠰ࡹ࡭ࡩ࡫࡯࠯࡭ࡵࡥࡹࡵࡳࠨ਑"))
	if os.path.exists(l1111Fuck_You_Anonymous):
		l11Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠩ࡜ࡳࡺࠦࡈࡢࡸࡨࠤࡎࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡇࡴࡲࡱࠥࡇ࡮ࠨ਒")
		l1l1ll1lFuck_You_Anonymous = l111Fuck_You_Anonymous (u"࡙ࠪࡳࡵࡦࡧ࡫ࡦ࡭ࡦࡲࠠࡔࡱࡸࡶࡨ࡫࡚ࠠࠧࠢ࡭ࡱࡲࠠࡏࡱࡺࠤࡉ࡫࡬ࡦࡶࡨࠤࡕࡲࡥࡢࡵࡨࠫਓ")
		l1l1lll1Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠫࡎࡴࡳࡵࡣ࡯ࡰࠥࡆ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠ࡬ࡹࡺࡰ࠻࠱࠲ࡱࡺࡩ࡫ࡺࡵ࠱ࡱࡪࡪࡩࡢࡲࡲࡶࡹࡧ࡬࠵࡭ࡲࡨ࡮࠴࡭࡭࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪਔ")
		l1l1llllFuck_You_Anonymous = l111Fuck_You_Anonymous (u"ࠬࡘࡥ࡮ࡱࡹࡩࡩࠦࡁ࡯ࡱࡱࡽࡲࡵࡵࡴࠢࡕࡩࡵࡵࠠࡂࡰࡧࠤࡆࡪࡤࡰࡰࡶࠫਕ")
		l1ll1111Fuck_You_Anonymous = l111Fuck_You_Anonymous (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡖ࡬ࡦࡣࡶࡩࠥࡊ࡯࡯ࡶࠣࡗࡺࡶࡰࡰࡴࡷࠤࡎࡪࡩࡰࡶࡶࠫਖ")
		l1ll1Fuck_You_Anonymous.show_ok_dialog([l11Fuck_You_Anonymous, l1l1ll1lFuck_You_Anonymous, l1l1lll1Fuck_You_Anonymous], l1l11Fuck_You_Anonymous)
		l1Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_path()
		shutil.rmtree(l1Fuck_You_Anonymous, ignore_errors=True)
		shutil.rmtree(l1111Fuck_You_Anonymous, ignore_errors=True)
		shutil.rmtree(l11l1Fuck_You_Anonymous, ignore_errors=True)
		shutil.rmtree(l1l1111lFuck_You_Anonymous, ignore_errors=True)
		l1ll1Fuck_You_Anonymous.log(l111Fuck_You_Anonymous (u"ࠧ࠾࠿ࡀࡈࡊࡒࡅࡕࡋࡑࡋࡂࡃ࠽ࡂࡐࡒࡒ࡞ࡓࡏࡖࡕࡀࡁࡂࡇࡄࡅࡑࡑࡗࡂࡃ࠽ࠬ࠿ࡀࡁࡗࡋࡐࡐ࠿ࡀࡁࠬਗ"))
		l1ll1Fuck_You_Anonymous.show_ok_dialog([l1l1llllFuck_You_Anonymous, l1ll1111Fuck_You_Anonymous], l1l11Fuck_You_Anonymous)
		time.sleep(2)
		os._exit(0)
md.check_source()
mode = md.args[l111Fuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ਘ")]
url = md.args.get(l111Fuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ਙ"), None)
name = md.args.get(l111Fuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨਚ"), None)
query = md.args.get(l111Fuck_You_Anonymous (u"ࠫࡶࡻࡥࡳࡻࠪਛ"), None)
title = md.args.get(l111Fuck_You_Anonymous (u"ࠬࡺࡩࡵ࡮ࡨࠫਜ"), None)
l11111lFuck_You_Anonymous = md.args.get(l111Fuck_You_Anonymous (u"࠭ࡳࡦࡣࡶࡳࡳ࠭ਝ"), None)
l1l111llFuck_You_Anonymous = md.args.get(l111Fuck_You_Anonymous (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࠨਞ") ,None)
l1l1llFuck_You_Anonymous = md.args.get(l111Fuck_You_Anonymous (u"ࠨ࡫ࡱࡪࡴࡲࡡࡣࡧ࡯ࡷࠬਟ"), None)
content = md.args.get(l111Fuck_You_Anonymous (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪਠ"), None)
l1l11llFuck_You_Anonymous = md.args.get(l111Fuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࡠ࡫ࡧࠫਡ"), None)
l11111Fuck_You_Anonymous = md.args.get(l111Fuck_You_Anonymous (u"ࠫ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫ࠧਢ"), None)
fan_art = md.args.get(l111Fuck_You_Anonymous (u"ࠬ࡬ࡡ࡯ࡡࡤࡶࡹ࠭ਣ"), None)
is_folder = md.args.get(l111Fuck_You_Anonymous (u"࠭ࡩࡴࡡࡩࡳࡱࡪࡥࡳࠩਤ"), True)
if mode is None or url is None or len(url)<1:
	l1l1ll1Fuck_You_Anonymous()
elif mode == l111Fuck_You_Anonymous (u"ࠧ࠲ࠩਥ"):
	l1l11111Fuck_You_Anonymous(content)
elif mode == l111Fuck_You_Anonymous (u"ࠨ࠴ࠪਦ"):
	l11ll1Fuck_You_Anonymous(url,content)
elif mode == l111Fuck_You_Anonymous (u"ࠩ࠶ࠫਧ"):
	l1lll11lFuck_You_Anonymous(title, url, l11111Fuck_You_Anonymous, content, l11111lFuck_You_Anonymous)
elif mode == l111Fuck_You_Anonymous (u"ࠪ࠸ࠬਨ"):
	l11lllllFuck_You_Anonymous(url, content)
elif mode == l111Fuck_You_Anonymous (u"ࠫ࠺࠭਩"):
	l1lll1Fuck_You_Anonymous(url, content)
elif mode == l111Fuck_You_Anonymous (u"ࠬ࠼ࠧਪ"):
	l11l11Fuck_You_Anonymous(url, content)
elif mode == l111Fuck_You_Anonymous (u"࠭࠷ࠨਫ"):
	l1l1l1Fuck_You_Anonymous(url,name,l11111Fuck_You_Anonymous,content,l1l1llFuck_You_Anonymous,query)
elif mode == l111Fuck_You_Anonymous (u"ࠧࡴࡧࡤࡶࡨ࡮ࠧਬ"):
	l111l1Fuck_You_Anonymous(content,query)
elif mode == l111Fuck_You_Anonymous (u"ࠨࡣࡧࡨࡴࡴ࡟ࡴࡧࡤࡶࡨ࡮ࠧਭ"):
	md.addon_search(content,query,fan_art,l1l1llFuck_You_Anonymous)
elif mode == l111Fuck_You_Anonymous (u"ࠩࡤࡨࡩࡥࡲࡦ࡯ࡲࡺࡪࡥࡦࡢࡸࠪਮ"):
	md.add_remove_fav(name, url, l1l1llFuck_You_Anonymous, fan_art,
			  content, l1l11llFuck_You_Anonymous, is_folder)
elif mode == l111Fuck_You_Anonymous (u"ࠪࡪࡪࡺࡣࡩࡡࡩࡥࡻࡹࠧਯ"):
	md.fetch_favs(l111111Fuck_You_Anonymous)
elif mode == l111Fuck_You_Anonymous (u"ࠫࡦࡪࡤࡰࡰࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬਰ"):
	l1ll1Fuck_You_Anonymous.show_settings()
elif mode == l111Fuck_You_Anonymous (u"ࠬࡳࡥࡵࡣࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬ਱"):
	import metahandler
	metahandler.display_settings()
l1ll1Fuck_You_Anonymous.end_of_directory()