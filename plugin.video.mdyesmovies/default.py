# -*- coding: utf-8 -*-
import sys
l1ll1ll1Fuck_You_Anonymous = sys.version_info [0] == 2
l11ll11Fuck_You_Anonymous = 2048
l1llll1lFuck_You_Anonymous = 7
def l1lllFuck_You_Anonymous (l1l1l1Fuck_You_Anonymous):
    global l11lll1Fuck_You_Anonymous
    l1111llFuck_You_Anonymous = ord (l1l1l1Fuck_You_Anonymous [-1])
    l1ll1lllFuck_You_Anonymous = l1l1l1Fuck_You_Anonymous [:-1]
    l1ll111Fuck_You_Anonymous = l1111llFuck_You_Anonymous % len (l1ll1lllFuck_You_Anonymous)
    l11ll1Fuck_You_Anonymous = l1ll1lllFuck_You_Anonymous [:l1ll111Fuck_You_Anonymous] + l1ll1lllFuck_You_Anonymous [l1ll111Fuck_You_Anonymous:]
    if l1ll1ll1Fuck_You_Anonymous:
        l11l1Fuck_You_Anonymous = unicode () .join ([unichr (ord (char) - l11ll11Fuck_You_Anonymous - (l11lFuck_You_Anonymous + l1111llFuck_You_Anonymous) % l1llll1lFuck_You_Anonymous) for l11lFuck_You_Anonymous, char in enumerate (l11ll1Fuck_You_Anonymous)])
    else:
        l11l1Fuck_You_Anonymous = str () .join ([chr (ord (char) - l11ll11Fuck_You_Anonymous - (l11lFuck_You_Anonymous + l1111llFuck_You_Anonymous) % l1llll1lFuck_You_Anonymous) for l11lFuck_You_Anonymous, char in enumerate (l11ll1Fuck_You_Anonymous)])
    return eval (l11l1Fuck_You_Anonymous)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import os,re,sys,shutil,time
# Yes Movies Add-on Created By Mucky Duck (10/2016)
l111l1lFuck_You_Anonymous = xbmcaddon.Addon().getAddonInfo(l1lllFuck_You_Anonymous (u"ࠫ࡮ࡪࠧࠀ"))
l1ll1Fuck_You_Anonymous = Addon(l111l1lFuck_You_Anonymous, sys.argv)
l1l1lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_name()
l11111lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_path()
md = md(l111l1lFuck_You_Anonymous, sys.argv)
l1l1l1lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l1lllFuck_You_Anonymous (u"ࠬࡧࡵࡵࡱࡳࡰࡦࡿࠧࠁ"))
l111llFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l1lllFuck_You_Anonymous (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥ࡭ࡦࡶࡤࠫࠂ"))
l11l111Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l1lllFuck_You_Anonymous (u"ࠧࡦࡰࡤࡦࡱ࡫࡟ࡴࡪࡲࡻࡸ࠭ࠃ"))
l1llllllFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l1lllFuck_You_Anonymous (u"ࠨࡧࡱࡥࡧࡲࡥࡠ࡯ࡲࡺ࡮࡫ࡳࠨࠄ"))
l1l1l11Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l1lllFuck_You_Anonymous (u"ࠩࡨࡲࡦࡨ࡬ࡦࡡࡩࡥࡻࡹࠧࠅ"))
l1llFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l1lllFuck_You_Anonymous (u"ࠪࡥࡩࡪ࡟ࡴࡧࡷࠫࠆ"))
l1l1l11lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_setting(l1lllFuck_You_Anonymous (u"ࠫࡪࡴࡡࡣ࡮ࡨࡣࡲ࡫ࡴࡢࡡࡶࡩࡹ࠭ࠇ"))
l1l111Fuck_You_Anonymous = md.get_art()
l1ll111lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_icon()
l1l111lFuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_fanart()
l11l1l1Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡹࡦࡵࡰࡳࡻ࡯ࡥࡴ࠰ࡷࡳࠬࠈ")
reload(sys)
sys.setdefaultencoding(l1lllFuck_You_Anonymous (u"ࠨࡵࡵࡨ࠰࠼ࠧࠉ"))
l1111Fuck_You_Anonymous = [l1lllFuck_You_Anonymous (u"ࠧࡳࡣࡷ࡭ࡳ࡭ࠧࠊ"),l1lllFuck_You_Anonymous (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨࠋ"),l1lllFuck_You_Anonymous (u"ࠩࡹ࡭ࡪࡽࠧࠌ"),l1lllFuck_You_Anonymous (u"ࠪࡪࡦࡼ࡯ࡳ࡫ࡷࡩࠬࠍ"),l1lllFuck_You_Anonymous (u"ࠫ࡮ࡳࡤࡣࡡࡰࡥࡷࡱࠧࠎ")]
sort = [l1lllFuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤ࡮ࡴࡤࡪࡣࡱࡶࡪࡪ࡝ࡎࡱࡶࡸࠥࡘࡡࡵࡧࡧ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ࠏ"), l1lllFuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞ࡔࡨࡧࡪࡴࡴ࡭ࡻࠣࡅࡩࡪࡥࡥ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫࠐ"),
	l1lllFuck_You_Anonymous (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡩ࡯ࡦ࡬ࡥࡳࡸࡥࡥ࡟ࡐࡳࡸࡺࠠࡗ࡫ࡨࡻࡪࡪ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࠑ"), l1lllFuck_You_Anonymous (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡴࡹࡴࠡࡈࡤࡺࡴࡻࡲࡪࡶࡨࡨࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࠒ"),
	l1lllFuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࡎࡓࡄࡃࠢࡕࡥࡹ࡯࡮ࡨ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫࠓ")]
def l1l1llFuck_You_Anonymous():
	if l1llllllFuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠪࡸࡷࡻࡥࠨࠔ"):
		md.addDir({l1lllFuck_You_Anonymous (u"ࠫࡲࡵࡤࡦࠩࠕ"): l1lllFuck_You_Anonymous (u"ࠬ࠷ࠧࠖ"), l1lllFuck_You_Anonymous (u"࠭࡮ࡢ࡯ࡨࠫࠗ"):l1lllFuck_You_Anonymous (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠ࡟ࡇࡣࡍࡐࡘࡌࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫ࠘"), l1lllFuck_You_Anonymous (u"ࠨࡷࡵࡰࠬ࠙"):l1lllFuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ࠚ"), l1lllFuck_You_Anonymous (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࠛ"):l1lllFuck_You_Anonymous (u"ࠫࡲࡵࡶࡪࡧࡶࠫࠜ")})
	if l11l111Fuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠬࡺࡲࡶࡧࠪࠝ"):
		md.addDir({l1lllFuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫࠞ"): l1lllFuck_You_Anonymous (u"ࠧ࠲ࠩࠟ"), l1lllFuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ࠠ"):l1lllFuck_You_Anonymous (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢ࡬ࡲࡩ࡯ࡡ࡯ࡴࡨࡨࡢࡡࡂ࡞ࡖ࡙ࠤࡘࡎࡏࡘࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨࠡ"), l1lllFuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࠢ"):l1lllFuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࠣ"), l1lllFuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࠤ"):l1lllFuck_You_Anonymous (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹࠧࠥ")})
	if l1l1l11Fuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠧࡵࡴࡸࡩࠬࠦ"):
		md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࠧ"): l1lllFuck_You_Anonymous (u"ࠩࡩࡩࡹࡩࡨࡠࡨࡤࡺࡸ࠭ࠨ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࠩ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡮ࡴࡤࡪࡣࡱࡶࡪࡪ࡝࡜ࡄࡠࡑ࡞ࠦࡆࡂࡘࡒ࡙ࡗࡏࡔࡆࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨࠪ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࠫ"):l1lllFuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪࠬ")})
	if l111llFuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠧࡵࡴࡸࡩࠬ࠭"):
		if l1l1l11lFuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠨࡶࡵࡹࡪ࠭࠮"):
			md.addDir({l1lllFuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧ࠯"):l1lllFuck_You_Anonymous (u"ࠪࡱࡪࡺࡡࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ࠰"), l1lllFuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩ࠱"):l1lllFuck_You_Anonymous (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞࡝ࡅࡡࡒࡋࡔࡂࠢࡖࡉ࡙࡚ࡉࡏࡉࡖ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ࠲"), l1lllFuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪ࠳"):l1lllFuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ࠴")}, is_folder=False, is_playable=False)
	if l1llFuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠨࡶࡵࡹࡪ࠭࠵"):
		md.addDir({l1lllFuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫ࠧ࠶"):l1lllFuck_You_Anonymous (u"ࠪࡥࡩࡪ࡯࡯ࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ࠷"), l1lllFuck_You_Anonymous (u"ࠫࡳࡧ࡭ࡦࠩ࠸"):l1lllFuck_You_Anonymous (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞࡝ࡅࡡࡆࡊࡄࡐࡐࠣࡗࡊ࡚ࡔࡊࡐࡊࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ࠹"), l1lllFuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪ࠺"):l1lllFuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫ࠻")}, is_folder=False, is_playable=False)
	l1lllll1Fuck_You_Anonymous()
        l1ll11Fuck_You_Anonymous()
	setView(l111l1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠨࡨ࡬ࡰࡪࡹࠧ࠼"), l1lllFuck_You_Anonymous (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬ࠽"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1l1l1llFuck_You_Anonymous(content):
	if l1l1l11Fuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠪࡸࡷࡻࡥࠨ࠾"):
		md.addDir({l1lllFuck_You_Anonymous (u"ࠫࡲࡵࡤࡦࠩ࠿"): l1lllFuck_You_Anonymous (u"ࠬ࡬ࡥࡵࡥ࡫ࡣ࡫ࡧࡶࡴࠩࡀ"), l1lllFuck_You_Anonymous (u"࠭࡮ࡢ࡯ࡨࠫࡁ"):l1lllFuck_You_Anonymous (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠ࡟ࡇࡣࡍ࡚ࠢࡄࡈࡉ࠳ࡏࡏࠢࡉࡅ࡛ࡕࡕࡓࡋࡗࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡂ"), l1lllFuck_You_Anonymous (u"ࠨࡷࡵࡰࠬࡃ"):l1lllFuck_You_Anonymous (u"ࠩࡸࡶࡱ࠭ࡄ")})
	if content == l1lllFuck_You_Anonymous (u"ࠪࡱࡴࡼࡩࡦࡵࠪࡅ"):
		l111111Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠫࡲࡵࡶࡪࡧࠪࡆ")
	elif content == l1lllFuck_You_Anonymous (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࡇ"):
		l111111Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"࠭ࡳࡦࡴ࡬ࡩࡸ࠭ࡈ")
	l1l1111Fuck_You_Anonymous = l11l1l1Fuck_You_Anonymous+l1lllFuck_You_Anonymous (u"ࠧ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࠦࡵ࠲ࠩࡸ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࡣ࡯ࡰࠬࡉ")
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࡊ"): l1lllFuck_You_Anonymous (u"ࠩ࠵ࠫࡋ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࡌ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡔࡈࡇࡊࡔࡔࡍ࡛ࠣࡅࡉࡊࡅࡅ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࡍ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡎ"):l1l1111Fuck_You_Anonymous %(l111111Fuck_You_Anonymous,l1lllFuck_You_Anonymous (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ࡏ")), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡐ"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࡑ"): l1lllFuck_You_Anonymous (u"ࠩ࠵ࠫࡒ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࡓ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡈࡄ࡚ࡔ࡛ࡒࡊࡖࡈࡈࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࡔ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡕ"):l1l1111Fuck_You_Anonymous %(l111111Fuck_You_Anonymous,l1lllFuck_You_Anonymous (u"࠭ࡦࡢࡸࡲࡶ࡮ࡺࡥࠨࡖ")), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡗ"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࡘ"): l1lllFuck_You_Anonymous (u"ࠩ࠵࡙ࠫ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨ࡚"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡔࡄࡘࡎࡔࡇࡔ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣ࡛ࠧ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩ࡜"):l1l1111Fuck_You_Anonymous %(l111111Fuck_You_Anonymous,l1lllFuck_You_Anonymous (u"࠭ࡲࡢࡶ࡬ࡲ࡬࠭࡝")), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࡞"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭࡟"): l1lllFuck_You_Anonymous (u"ࠩ࠵ࠫࡠ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࡡ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡘࡌࡉ࡜ࡋࡄ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࡢ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡣ"):l1l1111Fuck_You_Anonymous %(l111111Fuck_You_Anonymous,l1lllFuck_You_Anonymous (u"࠭ࡶࡪࡧࡺࠫࡤ")), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡥ"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࡦ"): l1lllFuck_You_Anonymous (u"ࠩ࠵ࠫࡧ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࡨ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡘࡔࡖࠠࡊࡏࡇࡆࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࡩ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡪ"):l1l1111Fuck_You_Anonymous %(l111111Fuck_You_Anonymous,l1lllFuck_You_Anonymous (u"࠭ࡩ࡮ࡦࡥࡣࡲࡧࡲ࡬ࠩ࡫")), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࡬"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭࡭"): l1lllFuck_You_Anonymous (u"ࠩ࠹ࠫ࡮"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨ࡯"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡇࡔ࡛ࡎࡕࡔ࡜࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩࡰ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡱ"):l11l1l1Fuck_You_Anonymous+l1lllFuck_You_Anonymous (u"࠭࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠭ࡲ"), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡳ"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࡴ"): l1lllFuck_You_Anonymous (u"ࠩࡶࡩࡦࡸࡣࡩࠩࡵ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࡶ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡗࡊࡇࡒࡄࡊ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨࡷ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡸ"):l1lllFuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪࡹ"), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡺ"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࡻ"): l1lllFuck_You_Anonymous (u"ࠩ࠷ࠫࡼ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࡽ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡋࡊࡔࡒࡆ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࡾ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࡿ"):l11l1l1Fuck_You_Anonymous+l1lllFuck_You_Anonymous (u"࠭࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠭ࢀ"), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࢁ"):content})
	md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࢂ"): l1lllFuck_You_Anonymous (u"ࠩ࠸ࠫࢃ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࢄ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠ࡝ࡊࡇࡒ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࢅ"), l1lllFuck_You_Anonymous (u"ࠬࡻࡲ࡭ࠩࢆ"):l11l1l1Fuck_You_Anonymous+l1lllFuck_You_Anonymous (u"࠭࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠭ࢇ"), l1lllFuck_You_Anonymous (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࢈"):content})
	setView(l111l1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠨࡨ࡬ࡰࡪࡹࠧࢉ"), l1lllFuck_You_Anonymous (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬࢊ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1l11lFuck_You_Anonymous(url,content):
	link = open_url(url,verify=False).content
	l1l11Fuck_You_Anonymous = md.regex_get_all(link, l1lllFuck_You_Anonymous (u"ࠪࡧࡱࡧࡳࡴ࠿ࠥࡱࡱ࠳ࡩࡵࡧࡰࠦࡃ࠭ࢋ"), l1lllFuck_You_Anonymous (u"ࠫࡁ࠵ࡤࡪࡸࡁࠫࢌ"))
	items = len(l1l11Fuck_You_Anonymous)
	for a in l1l11Fuck_You_Anonymous:
		name = md.regex_from_to(a, l1lllFuck_You_Anonymous (u"ࠬࡺࡩࡵ࡮ࡨࡁࠧ࠭ࢍ"), l1lllFuck_You_Anonymous (u"࠭ࠢࠨࢎ"))
		name = l1ll1Fuck_You_Anonymous.unescape(name).replace(l1lllFuck_You_Anonymous (u"ࠢ࡝࡞ࠪࠦ࢏"),l1lllFuck_You_Anonymous (u"ࠣࠩࠥ࢐"))
		url = md.regex_from_to(a, l1lllFuck_You_Anonymous (u"ࠩ࡫ࡶࡪ࡬࠽ࠣࠩ࢑"), l1lllFuck_You_Anonymous (u"ࠪࠦࠬ࢒")).replace(l1lllFuck_You_Anonymous (u"ࠫ࠳࡮ࡴ࡮࡮ࠪ࢓"),l1lllFuck_You_Anonymous (u"ࠬ࠵ࡷࡢࡶࡦ࡬࡮ࡴࡧ࠯ࡪࡷࡱࡱ࠭࢔"))
		l1l1Fuck_You_Anonymous = md.regex_from_to(a, l1lllFuck_You_Anonymous (u"࠭ࡤࡢࡶࡤ࠱ࡴࡸࡩࡨ࡫ࡱࡥࡱࡃࠧ࢕"), l1lllFuck_You_Anonymous (u"ࠧࠣࠩ࢖"))
		l11l11lFuck_You_Anonymous = md.regex_from_to(a, l1lllFuck_You_Anonymous (u"ࠨ࡯࡯࡭࠲ࡷࡵࡢ࡮࡬ࡸࡾࠨ࠾ࠨࢗ"), l1lllFuck_You_Anonymous (u"ࠩ࠿ࠫ࢘"))
		l1l1ll1lFuck_You_Anonymous = md.regex_from_to(a, l1lllFuck_You_Anonymous (u"ࠪࠦࡲࡲࡩ࠮ࡧࡳࡷࠧࡄ࢙ࠧ"), l1lllFuck_You_Anonymous (u"ࠫࡁ࠵࢚ࠧ"))
		l1l1ll1lFuck_You_Anonymous = l1l1ll1lFuck_You_Anonymous.replace(l1lllFuck_You_Anonymous (u"ࠬࡂࡳࡱࡣࡱࡂ࢛ࠬ"),l1lllFuck_You_Anonymous (u"࠭ࠠࠨ࢜")).replace(l1lllFuck_You_Anonymous (u"ࠧ࠽࡫ࡁࠫ࢝"),l1lllFuck_You_Anonymous (u"ࠨࠢࠪ࢞"))
		if content == l1lllFuck_You_Anonymous (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩ࢟"):
			if l11l11lFuck_You_Anonymous:
				md.addDir({l1lllFuck_You_Anonymous (u"ࠪࡱࡴࡪࡥࠨࢠ"): l1lllFuck_You_Anonymous (u"ࠫ࠼࠭ࢡ"), l1lllFuck_You_Anonymous (u"ࠬࡴࡡ࡮ࡧࠪࢢ"):l1lllFuck_You_Anonymous (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࠬࠪࡹࠩ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࢣ") %(name,l11l11lFuck_You_Anonymous),
					   l1lllFuck_You_Anonymous (u"ࠧࡶࡴ࡯ࠫࢤ"):url, l1lllFuck_You_Anonymous (u"ࠨ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠫࢥ"):l1l1Fuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࢦ"):content}, {l1lllFuck_You_Anonymous (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪ࠭ࢧ"):name},
					  fan_art={l1lllFuck_You_Anonymous (u"ࠫ࡮ࡩ࡯࡯ࠩࢨ"):l1l1Fuck_You_Anonymous}, is_folder=False, item_count=items)
		elif content == l1lllFuck_You_Anonymous (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࢩ"):
			if l1l1ll1lFuck_You_Anonymous:
				data = name.split(l1lllFuck_You_Anonymous (u"࠭࠭ࠡࡕࡨࡥࡸࡵ࡮ࠨࢪ"))
				l1111l1Fuck_You_Anonymous = data[0].strip()
				try:
					l11l1llFuck_You_Anonymous = data[1].strip()
				except:
					l11l1llFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠧࠨࢫ")
				md.addDir({l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡨࡪ࠭ࢬ"): l1lllFuck_You_Anonymous (u"ࠩ࠶ࠫࢭ"), l1lllFuck_You_Anonymous (u"ࠪࡲࡦࡳࡥࠨࢮ"):l1lllFuck_You_Anonymous (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠣ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡩ࡯ࡦ࡬ࡥࡳࡸࡥࡥ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࢯ") %(name,l1l1ll1lFuck_You_Anonymous),
					   l1lllFuck_You_Anonymous (u"ࠬࡺࡩࡵ࡮ࡨࠫࢰ"):l1111l1Fuck_You_Anonymous, l1lllFuck_You_Anonymous (u"࠭ࡵࡳ࡮ࠪࢱ"):url, l1lllFuck_You_Anonymous (u"ࠧࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࠪࢲ"):l1l1Fuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࢳ"):content, l1lllFuck_You_Anonymous (u"ࠩࡶࡩࡦࡹ࡯࡯ࠩࢴ"):l11l1llFuck_You_Anonymous},
					  {l1lllFuck_You_Anonymous (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪ࠭ࢵ"):l1111l1Fuck_You_Anonymous}, fan_art={l1lllFuck_You_Anonymous (u"ࠫ࡮ࡩ࡯࡯ࠩࢶ"):l1l1Fuck_You_Anonymous}, item_count=items)
	try:
		l111Fuck_You_Anonymous = re.compile(l1lllFuck_You_Anonymous (u"ࠬࡂ࡬ࡪࠢࡦࡰࡦࡹࡳ࠾ࠤࡱࡩࡽࡺࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠰࠿ࠪࠤࠣࡨࡦࡺࡡ࠮ࡥ࡬࠱ࡵࡧࡧࡪࡰࡤࡸ࡮ࡵ࡮࠮ࡲࡤ࡫ࡪࡃࠢ࠯ࠬࡂࠦࠥࡸࡥ࡭࠿ࠥࡲࡪࡾࡴࠣࡀࠪࢷ")).findall(link)[0]
		md.addDir({l1lllFuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫࢸ"): l1lllFuck_You_Anonymous (u"ࠧ࠳ࠩࢹ"), l1lllFuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ࢺ"):l1lllFuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࢻ"), l1lllFuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࢼ"):l111Fuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࢽ"):content})
	except: pass
	if content == l1lllFuck_You_Anonymous (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࢾ"):
		setView(l111l1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࢿ"), l1lllFuck_You_Anonymous (u"ࠧ࡮ࡱࡹ࡭ࡪ࠳ࡶࡪࡧࡺࠫࣀ"))
	elif content == l1lllFuck_You_Anonymous (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࣁ"):
		setView(l111l1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࣂ"), l1lllFuck_You_Anonymous (u"ࠪࡷ࡭ࡵࡷ࠮ࡸ࡬ࡩࡼ࠭ࣃ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l111l11Fuck_You_Anonymous(title, url, l111l1Fuck_You_Anonymous, content, l11l1llFuck_You_Anonymous):
	link = open_url(url,verify=False).content
	l111lllFuck_You_Anonymous = url
	l11ll1lFuck_You_Anonymous = re.compile(l1lllFuck_You_Anonymous (u"ࠫ࡮ࡪ࠺ࠡࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠫࣄ")).findall(link)[0]
	request_url = l1lllFuck_You_Anonymous (u"ࠬࠫࡳ࠰ࡣ࡭ࡥࡽ࠵ࡶ࠵ࡡࡰࡳࡻ࡯ࡥࡠࡧࡳ࡭ࡸࡵࡤࡦࡵ࠲ࠩࡸ࠭ࣅ") %(l11l1l1Fuck_You_Anonymous,l11ll1lFuck_You_Anonymous)
	headers = {l1lllFuck_You_Anonymous (u"࠭ࡁࡤࡥࡨࡴࡹ࠳ࡅ࡯ࡥࡲࡨ࡮ࡴࡧࠨࣆ"):l1lllFuck_You_Anonymous (u"ࠧࡨࡼ࡬ࡴ࠱ࠦࡤࡦࡨ࡯ࡥࡹ࡫ࠬࠡࡵࡧࡧ࡭࠲ࠠࡣࡴࠪࣇ"), l1lllFuck_You_Anonymous (u"ࠨࡔࡨࡪࡪࡸࡥࡳࠩࣈ"):l111lllFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭ࣉ"):md.User_Agent()}
	l1ll1l1lFuck_You_Anonymous = open_url(request_url, headers=headers, verify=False).json()
	l11llllFuck_You_Anonymous = md.regex_get_all(l1ll1l1lFuck_You_Anonymous[l1lllFuck_You_Anonymous (u"ࠪ࡬ࡹࡳ࡬ࠨ࣊")], l1lllFuck_You_Anonymous (u"ࠫࠧ࡫ࡰࡪࡵࡲࡨࡪࡹ࠭ࡴࡸ࠰࠵࠵ࠨࠧ࣋"), l1lllFuck_You_Anonymous (u"ࠬࡂ࠯ࡶ࡮ࡁࠫ࣌"))
	l1l11Fuck_You_Anonymous = md.regex_get_all(str(l11llllFuck_You_Anonymous), l1lllFuck_You_Anonymous (u"࠭࠼࡭࡫ࠪ࣍"), l1lllFuck_You_Anonymous (u"ࠧ࠽࠱࡯࡭ࡃ࠭࣎"))
	items = len(l1l11Fuck_You_Anonymous)
	for a in l1l11Fuck_You_Anonymous:
		name = md.regex_from_to(a, l1lllFuck_You_Anonymous (u"ࠨࡶ࡬ࡸࡱ࡫࠽࣏ࠣࠩ"), l1lllFuck_You_Anonymous (u"࣐ࠩࠥࠫ"))
		name = name.replace(l1lllFuck_You_Anonymous (u"ࠪࡉࡵ࡯ࡳࡰࡦࡨ࣑ࠫ"),l1lllFuck_You_Anonymous (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡮ࡴࡤࡪࡣࡱࡶࡪࡪ࡝ࡆࡲ࡬ࡷࡴࡪࡥ࡜࠱ࡆࡓࡑࡕࡒ࡞࣒ࠩ"))
                name = l1ll1Fuck_You_Anonymous.unescape(name).replace(l1lllFuck_You_Anonymous (u"ࠧࡢ࡜ࠨࠤ࣓"),l1lllFuck_You_Anonymous (u"ࠨࠧࠣࣔ"))
		l1ll11llFuck_You_Anonymous = md.regex_from_to(a, l1lllFuck_You_Anonymous (u"ࠧࡥࡣࡷࡥ࠲࡯ࡤ࠾ࠤࠪࣕ"), l1lllFuck_You_Anonymous (u"ࠨࠤࠪࣖ"))
		headers = l111lllFuck_You_Anonymous + l1lllFuck_You_Anonymous (u"ࠩࡿࠫࣗ") + l1ll11llFuck_You_Anonymous + l1lllFuck_You_Anonymous (u"ࠪࢀࠬࣘ") + l11ll1lFuck_You_Anonymous
		url =  l1lllFuck_You_Anonymous (u"ࠫࠪࡹ࠯ࡢ࡬ࡤࡼ࠴ࡳ࡯ࡷ࡫ࡨࡣࡸࡵࡵࡳࡥࡨࡷ࠴ࠫࡳࠨࣙ") %(l11l1l1Fuck_You_Anonymous,l1ll11llFuck_You_Anonymous)
		try:
			l1ll1111Fuck_You_Anonymous = name.split(l1lllFuck_You_Anonymous (u"ࠬࡋࡰࡪࡵࡲࡨࡪ࠭ࣚ"))[1].strip()[:2]
		except:pass
		fan_art = {l1lllFuck_You_Anonymous (u"࠭ࡩࡤࡱࡱࠫࣛ"):l111l1Fuck_You_Anonymous}
		md.addDir({l1lllFuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬࣜ"): l1lllFuck_You_Anonymous (u"ࠨ࠹ࠪࣝ"), l1lllFuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧࣞ"):l1lllFuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࣟ") %name,
			   l1lllFuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨ࣠"):url, l1lllFuck_You_Anonymous (u"ࠬ࡯ࡣࡰࡰ࡬ࡱࡦ࡭ࡥࠨ࣡"):l111l1Fuck_You_Anonymous, l1lllFuck_You_Anonymous (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧ࣢"):l1lllFuck_You_Anonymous (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࣣࠩ"), l1lllFuck_You_Anonymous (u"ࠨࡳࡸࡩࡷࡿࠧࣤ"):headers},
			  {l1lllFuck_You_Anonymous (u"ࠩࡶࡳࡷࡺࡴࡪࡶ࡯ࡩࠬࣥ"):title, l1lllFuck_You_Anonymous (u"ࠪࡷࡪࡧࡳࡰࡰࣦࠪ"):l11l1llFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠫࡪࡶࡩࡴࡱࡧࡩࠬࣧ"):l1ll1111Fuck_You_Anonymous},
			  fan_art, is_folder=False, item_count=items)
	setView(l111l1lFuck_You_Anonymous,l1lllFuck_You_Anonymous (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࠧࣨ"), l1lllFuck_You_Anonymous (u"࠭ࡥࡱ࡫࠰ࡺ࡮࡫ࡷࠨࣩ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1l1l1l1Fuck_You_Anonymous(url, content):
	l1111lFuck_You_Anonymous = md.dialog_select(l1lllFuck_You_Anonymous (u"ࠧࡔࡧ࡯ࡩࡨࡺࠠࡔࡱࡵࡸࠥࡓࡥࡵࡪࡲࡨࠬ࣪"),sort)
	l111ll1Fuck_You_Anonymous = l1111Fuck_You_Anonymous[l1111lFuck_You_Anonymous]
	link = open_url(url,verify=False).content
	match = re.compile(l1lllFuck_You_Anonymous (u"ࠨ࠾࡬ࡲࡵࡻࡴࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡩࡨࡲࡷ࡫࠭ࡪࡦࡶࠦࠥࡼࡡ࡭ࡷࡨࡁࠧ࠮࠮ࠫࡁࠬࠦࠥࡴࡡ࡮ࡧࡀࠦ࠳࠰࠿ࠣ࡞ࡱ࠲࠯ࡅࡴࡺࡲࡨࡁࠧࡩࡨࡦࡥ࡮ࡦࡴࡾࠢࠡࡀࠫ࠲࠯ࡅࠩ࠽࠱࡯ࡥࡧ࡫࡬࠿ࠩ࣫")).findall(link)
	for l1llll1Fuck_You_Anonymous,name in match:
		name = name.replace(l1lllFuck_You_Anonymous (u"ࠩࠣࠫ࣬"),l1lllFuck_You_Anonymous (u"࣭ࠪࠫ"))
		if content == l1lllFuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷ࣮ࠬ"):
			url = l1lllFuck_You_Anonymous (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࡴࡧࡵ࡭ࡪࡹ࠯ࠦࡵ࠲ࠩࡸ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨ࣯") %(l11l1l1Fuck_You_Anonymous,l111ll1Fuck_You_Anonymous,l1llll1Fuck_You_Anonymous)
			md.addDir({l1lllFuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࣰࠫ"): l1lllFuck_You_Anonymous (u"ࠧ࠳ࣱࠩ"), l1lllFuck_You_Anonymous (u"ࠨࡰࡤࡱࡪࣲ࠭"):l1lllFuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࣳ") %name, l1lllFuck_You_Anonymous (u"ࠪࡹࡷࡲࠧࣴ"):url, l1lllFuck_You_Anonymous (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࣵ"):content})
		elif content == l1lllFuck_You_Anonymous (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࣶࠬ"):
			url = l1lllFuck_You_Anonymous (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰࡯ࡲࡺ࡮࡫࠯ࠦࡵ࠲ࠩࡸ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨࣷ") %(l11l1l1Fuck_You_Anonymous,l111ll1Fuck_You_Anonymous,l1llll1Fuck_You_Anonymous)
			md.addDir({l1lllFuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬࣸ"): l1lllFuck_You_Anonymous (u"ࠨ࠴ࣹࠪ"), l1lllFuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࣺࠧ"):l1lllFuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢ࡬ࡲࡩ࡯ࡡ࡯ࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࣻ") %name, l1lllFuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨࣼ"):url, l1lllFuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࣽ"):content})
	setView(l111l1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"࠭ࡦࡪ࡮ࡨࡷࠬࣾ"), l1lllFuck_You_Anonymous (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪࣿ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1llllFuck_You_Anonymous(url, content):
	l1111lFuck_You_Anonymous = md.dialog_select(l1lllFuck_You_Anonymous (u"ࠨࡕࡨࡰࡪࡩࡴࠡࡕࡲࡶࡹࠦࡍࡦࡶ࡫ࡳࡩ࠭ऀ"),sort)
	l111ll1Fuck_You_Anonymous = l1111Fuck_You_Anonymous[l1111lFuck_You_Anonymous]
	l11l1lFuck_You_Anonymous = md.numeric_select(l1lllFuck_You_Anonymous (u"ࠩࡈࡲࡹ࡫ࡲ࡛ࠡࡨࡥࡷ࠭ँ"), l1lllFuck_You_Anonymous (u"ࠪ࠶࠵࠷࠷ࠨं"))
	if content == l1lllFuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬः"):
		l1l11lFuck_You_Anonymous(l1lllFuck_You_Anonymous (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࡴࡧࡵ࡭ࡪࡹ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨऄ") %(l11l1l1Fuck_You_Anonymous,l111ll1Fuck_You_Anonymous,l11l1lFuck_You_Anonymous), content)
	elif content == l1lllFuck_You_Anonymous (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭अ"):
		l1l11lFuck_You_Anonymous(l1lllFuck_You_Anonymous (u"ࠧࠦࡵ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳ࠱ࡰࡳࡻ࡯ࡥ࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࠫࡳ࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࠩआ") %(l11l1l1Fuck_You_Anonymous,l111ll1Fuck_You_Anonymous,l11l1lFuck_You_Anonymous), content)
	setView(l111l1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠨࡨ࡬ࡰࡪࡹࠧइ"), l1lllFuck_You_Anonymous (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬई"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1ll11Fuck_You_Anonymous():
	link = open_url(l1lllFuck_You_Anonymous (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡵࡧࡳࡵࡧࡥ࡭ࡳ࠴ࡣࡰ࡯࠲ࡶࡦࡽ࠯ࡄࡨ࠷ࡇ࠸ࡻࡈ࠲ࠩउ")).content
	version = re.findall(l1lllFuck_You_Anonymous (u"ࡶࠬࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠡࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠫऊ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l1lllFuck_You_Anonymous (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࡳࡤࡴ࡬ࡴࡹ࠴࡭ࡰࡦࡸࡰࡪ࠴࡭ࡶࡥ࡮ࡽࡸ࠴ࡣࡰ࡯ࡰࡳࡳ࠵ࡡࡥࡦࡲࡲ࠳ࡾ࡭࡭ࠩऋ")), l1lllFuck_You_Anonymous (u"࠭ࡲࠬࠩऌ")) as f:
		l11111Fuck_You_Anonymous = f.read()
		if re.search(l1lllFuck_You_Anonymous (u"ࡲࠨࡸࡨࡶࡸ࡯࡯࡯࠿ࠥࠩࡸࠨࠧऍ") %version, l11111Fuck_You_Anonymous):
			l1ll1Fuck_You_Anonymous.log(l1lllFuck_You_Anonymous (u"ࠨࡘࡨࡶࡸ࡯࡯࡯ࠢࡆ࡬ࡪࡩ࡫ࠡࡑࡎࠫऎ"))
		else:
			l11Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠤ࡚ࡶࡴࡴࡧࠡࡘࡨࡶࡸ࡯࡯࡯ࠢࡒࡪࠥࡓࡵࡤ࡭ࡼࡷࠥࡉ࡯࡮࡯ࡲࡲࠥࡓ࡯ࡥࡷ࡯ࡩࠧए")
			l1lll11lFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠥࡔࡱ࡫ࡡࡴࡧࠣࡍࡳࡹࡴࡢ࡮࡯ࠤࡈࡵࡲࡳࡧࡦࡸࠥ࡜ࡥࡳࡵ࡬ࡳࡳࠦࡆࡳࡱࡰࠤ࡙࡮ࡥࠡࡔࡨࡴࡴࠨऐ")
			l1lll1l1Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠦࡅࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞ࡪࡷࡸࡵࡀ࠯࠰࡯ࡸࡧࡰࡿࡳ࠯࡯ࡨࡨ࡮ࡧࡰࡰࡴࡷࡥࡱ࠺࡫ࡰࡦ࡬࠲ࡲࡲ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣऑ")
			l1ll1Fuck_You_Anonymous.show_ok_dialog([l11Fuck_You_Anonymous, l1lll11lFuck_You_Anonymous, l1lll1l1Fuck_You_Anonymous], l1l1lFuck_You_Anonymous)
			xbmc.executebuiltin(l1lllFuck_You_Anonymous (u"ࠧ࡞ࡂࡎࡅ࠱ࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡕࡱࡦࡤࡸࡪ࠮ࡰࡢࡶ࡫࠰ࡷ࡫ࡰ࡭ࡣࡦࡩ࠮ࠨऒ"))
			xbmc.executebuiltin(l1lllFuck_You_Anonymous (u"ࠨࡘࡃࡏࡆ࠲ࡆࡩࡴࡪࡸࡤࡸࡪ࡝ࡩ࡯ࡦࡲࡻ࠭ࡎ࡯࡮ࡧࠬࠦओ"))
def l11lllFuck_You_Anonymous(url, content):
	l1111lFuck_You_Anonymous = md.dialog_select(l1lllFuck_You_Anonymous (u"ࠧࡔࡧ࡯ࡩࡨࡺࠠࡔࡱࡵࡸࠥࡓࡥࡵࡪࡲࡨࠬऔ"),sort)
	l111ll1Fuck_You_Anonymous = l1111Fuck_You_Anonymous[l1111lFuck_You_Anonymous]
	link = open_url(url,verify=False).content
	match=re.compile(l1lllFuck_You_Anonymous (u"ࠨ࠾࡬ࡲࡵࡻࡴࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡥࡲࡹࡳࡺࡲࡺ࠯࡬ࡨࡸࠨࠠࡷࡣ࡯ࡹࡪࡃࠢࠩ࠰࠭ࡃ࠮ࠨࠠ࡯ࡣࡰࡩࡂࠨ࠮ࠫࡁࠥࡠࡳ࠴ࠪࡀࡶࡼࡴࡪࡃࠢࡤࡪࡨࡧࡰࡨ࡯ࡹࠤࠣࡂ࠭࠴ࠪࡀࠫ࠿࠳ࡱࡧࡢࡦ࡮ࡁࠫक")).findall(link)
	for l1lll11Fuck_You_Anonymous,name in match:
		name = name.replace(l1lllFuck_You_Anonymous (u"ࠩࠣࠫख"),l1lllFuck_You_Anonymous (u"ࠪࠫग"))
		if content == l1lllFuck_You_Anonymous (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬघ"):
			url = l1lllFuck_You_Anonymous (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࡴࡧࡵ࡭ࡪࡹ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨङ") %(l11l1l1Fuck_You_Anonymous,l111ll1Fuck_You_Anonymous,l1lll11Fuck_You_Anonymous)
			md.addDir({l1lllFuck_You_Anonymous (u"࠭࡭ࡰࡦࡨࠫच"): l1lllFuck_You_Anonymous (u"ࠧ࠳ࠩछ"), l1lllFuck_You_Anonymous (u"ࠨࡰࡤࡱࡪ࠭ज"):l1lllFuck_You_Anonymous (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩझ") %name, l1lllFuck_You_Anonymous (u"ࠪࡹࡷࡲࠧञ"):url, l1lllFuck_You_Anonymous (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬट"):content})
		elif content == l1lllFuck_You_Anonymous (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬठ"):
			url = l1lllFuck_You_Anonymous (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰࡯ࡲࡺ࡮࡫࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨड") %(l11l1l1Fuck_You_Anonymous,l111ll1Fuck_You_Anonymous,l1lll11Fuck_You_Anonymous)
			md.addDir({l1lllFuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬढ"): l1lllFuck_You_Anonymous (u"ࠨ࠴ࠪण"), l1lllFuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧत"):l1lllFuck_You_Anonymous (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢ࡬ࡲࡩ࡯ࡡ࡯ࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪथ") %name, l1lllFuck_You_Anonymous (u"ࠫࡺࡸ࡬ࠨद"):url, l1lllFuck_You_Anonymous (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ध"):content})
	setView(l111l1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"࠭ࡦࡪ࡮ࡨࡷࠬन"), l1lllFuck_You_Anonymous (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪऩ"))
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l11l11Fuck_You_Anonymous(content, query):
	try:
		if query:
			search = query.replace(l1lllFuck_You_Anonymous (u"ࠨࠢࠪप"),l1lllFuck_You_Anonymous (u"ࠩ࠮ࠫफ"))
		else:
			search = md.search()
			if search == l1lllFuck_You_Anonymous (u"ࠪࠫब"):
				md.notification(l1lllFuck_You_Anonymous (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟࡞ࡆࡢࡋࡍࡑࡖ࡜ࠤࡖ࡛ࡅࡓ࡛࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝࠭ࡃࡥࡳࡷࡺࡩ࡯ࡩࠣࡷࡪࡧࡲࡤࡪࠪभ"),l1ll111lFuck_You_Anonymous)
				return
			else:
				pass
		url = l1lllFuck_You_Anonymous (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡴࡧࡤࡶࡨ࡮࠯ࠦࡵࠪम") %(l11l1l1Fuck_You_Anonymous,search)
		l1l11lFuck_You_Anonymous(url,content)
	except:
		md.notification(l1lllFuck_You_Anonymous (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࡠࡈ࡝ࡔࡱࡵࡶࡾࠦࡎࡰࠢࡕࡩࡸࡻ࡬ࡵࡵ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨय"),l1ll111lFuck_You_Anonymous)
def llFuck_You_Anonymous(data):
        l1l1lllFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠧࠨर")
        l1l1ll1Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠨࠩऱ")
        try:
            data = l1lllFuck_You_Anonymous (u"ࠩࠫࠫल") + data.split(l1lllFuck_You_Anonymous (u"ࠥࠬࡤࠪࠤࠪࠫࠣࠬࠬࡥࠧࠪ࠽ࠥळ"))[0].split(l1lllFuck_You_Anonymous (u"ࠦ࠴࠰ࠠࡡࠦࠧࡤࠥ࠰࠯ࠣऴ"))[-1].strip()
            data = data.replace(l1lllFuck_You_Anonymous (u"ࠬ࠮࡟ࡠࠦࠬ࡟ࠩࠪࠤ࡞ࠩव"), l1lllFuck_You_Anonymous (u"࠭࡜ࠨࠤ࡟ࠫࠬश"))
            data = data.replace(l1lllFuck_You_Anonymous (u"ࠧࠩࡡࡢࠨ࠮ࡡ࡟ࠥ࡟ࠪष"), l1lllFuck_You_Anonymous (u"ࠨࠤ࡟ࡠࡡࡢࠢࠨस"))
            data = data.replace(l1lllFuck_You_Anonymous (u"ࠩࠫࡳࡣࡥ࡞ࡰࠫࠪह"), l1lllFuck_You_Anonymous (u"ࠪ࠷ࠬऺ"))
            data = data.replace(l1lllFuck_You_Anonymous (u"ࠫ࠭ࡩ࡞ࡠࡠࡲ࠭ࠬऻ"), l1lllFuck_You_Anonymous (u"ࠬ࠶़ࠧ"))
            data = data.replace(l1lllFuck_You_Anonymous (u"࠭ࠨࡠࠦࠧ࠭ࠬऽ"), l1lllFuck_You_Anonymous (u"ࠧ࠲ࠩा"))
            data = data.replace(l1lllFuck_You_Anonymous (u"ࠨࠪࠧࠨࡤ࠯ࠧि"), l1lllFuck_You_Anonymous (u"ࠩ࠷ࠫी"))
            code = l1lllFuck_You_Anonymous (u"ࠪࠫࠬࡪࡥࡧࠢࡵࡩࡹࡇࠨࠪ࠼ࠍࠤࠥࠦࠠࡤ࡮ࡤࡷࡸࠦࡉ࡯ࡨ࡬ࡼ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡤࡥࡩ࡯࡫ࡷࡣࡤ࠮ࡳࡦ࡮ࡩ࠰ࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡴࡧ࡯ࡪ࠳࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠ࠾ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡥࡧࠢࡢࡣࡷࡵࡲࡠࡡࠫࡷࡪࡲࡦ࠭ࠢࡲࡸ࡭࡫ࡲࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡋࡱࡪ࡮ࡾࠨ࡭ࡣࡰࡦࡩࡧࠠࡹ࠮ࠣࡷࡪࡲࡦ࠾ࡵࡨࡰ࡫࠲ࠠࡰࡶ࡫ࡩࡷࡃ࡯ࡵࡪࡨࡶ࠿ࠦࡳࡦ࡮ࡩ࠲࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮࡯ࡵࡪࡨࡶ࠱ࠦࡸࠪࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡࡡࡢࡳࡷࡥ࡟ࠩࡵࡨࡰ࡫࠲ࠠࡰࡶ࡫ࡩࡷ࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡳࡦ࡮ࡩ࠲࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮࡯ࡵࡪࡨࡶ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡤࡥࡲ࡭ࡵ࡫࡭࡫ࡺ࡟ࡠࠪࡶࡩࡱ࡬ࠬࠡࡱࡷ࡬ࡪࡸࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠࡊࡰࡩ࡭ࡽ࠮࡬ࡢ࡯ࡥࡨࡦࠦࡸ࠭ࠢࡶࡩࡱ࡬࠽ࡴࡧ࡯ࡪ࠱ࠦ࡯ࡵࡪࡨࡶࡂࡵࡴࡩࡧࡵ࠾ࠥࡹࡥ࡭ࡨ࠱ࡪࡺࡴࡣࡵ࡫ࡲࡲ࠭ࡵࡴࡩࡧࡵ࠰ࠥࡾࠩࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠࡠࡡࡵࡷ࡭࡯ࡦࡵࡡࡢࠬࡸ࡫࡬ࡧ࠮ࠣࡳࡹ࡮ࡥࡳࠫ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡶࡩࡱ࡬࠮ࡧࡷࡱࡧࡹ࡯࡯࡯ࠪࡲࡸ࡭࡫ࡲࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠࡠࡡࡦࡥࡱࡲ࡟ࡠࠪࡶࡩࡱ࡬ࠬࠡࡸࡤࡰࡺ࡫࠱࠭ࠢࡹࡥࡱࡻࡥ࠳ࠫ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡶࡩࡱ࡬࠮ࡧࡷࡱࡧࡹ࡯࡯࡯ࠪࡹࡥࡱࡻࡥ࠲࠮ࠣࡺࡦࡲࡵࡦ࠴ࠬࠎࠥࠦࠠࠡࡦࡨࡪࠥࡳࡹࡠࡣࡧࡨ࠭ࡾࠬࠡࡻࠬ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠤࡷ࡫ࡴࡶࡴࡱࠤࡽࠦࠫࠡࡻࠍࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡴࡨࡸࡺࡸ࡮ࠡࡵࡷࡶ࠭ࡾࠩࠡ࠭ࠣࡷࡹࡸࠨࡺࠫࠍࠤࠥࠦࠠࡹࠢࡀࠤࡎࡴࡦࡪࡺࠫࡱࡾࡥࡡࡥࡦࠬࠎࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࠧࡶࠎࡵࡧࡲࡢ࡯ࠣࡁࠥࡸࡥࡵࡃࠫ࠭ࠬ࠭ࠧु")
            l1l1llllFuck_You_Anonymous = {l1lllFuck_You_Anonymous (u"ࠦࡤࡥࡢࡶ࡫࡯ࡸ࡮ࡴࡳࡠࡡࠥू"): None, l1lllFuck_You_Anonymous (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧृ"):__name__, l1lllFuck_You_Anonymous (u"࠭ࡳࡵࡴࠪॄ"):str, l1lllFuck_You_Anonymous (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠪॅ"):Exception}
            l1l11l1Fuck_You_Anonymous = { l1lllFuck_You_Anonymous (u"ࠨࡲࡤࡶࡦࡳࠧॆ"): None }
            exec( code % data.replace(l1lllFuck_You_Anonymous (u"ࠩ࠮ࠫे"),l1lllFuck_You_Anonymous (u"ࠪࢀࡽࢂࠧै")), l1l1llllFuck_You_Anonymous, l1l11l1Fuck_You_Anonymous)
            data = l1l11l1Fuck_You_Anonymous[l1lllFuck_You_Anonymous (u"ࠫࡵࡧࡲࡢ࡯ࠪॉ")].decode(l1lllFuck_You_Anonymous (u"ࠬࡹࡴࡳ࡫ࡱ࡫ࡤ࡫ࡳࡤࡣࡳࡩࠬॊ"))
            data = re.compile(l1lllFuck_You_Anonymous (u"࠭ࠧࠨ࠿࡞ࠫࠧࡣࠨ࡜ࡠࠥࡢࠬࡣࠫࡀࠫ࡞ࠫࠧࡣࠧࠨࠩो")).findall(data)
            l1l1lllFuck_You_Anonymous = data[0]
            l1l1ll1Fuck_You_Anonymous = data[1]
        except Exception:
            l1ll1Fuck_You_Anonymous.log(l1lllFuck_You_Anonymous (u"ࠧࡔࡱࡵࡶࡾࠦࡃࡰࡷ࡯ࡨࡳࡢࠧࡵࠢࡇࡩࡨࡵࡤࡦࠩौ"))
        return l1l1lllFuck_You_Anonymous, l1l1ll1Fuck_You_Anonymous
def l1ll1lFuck_You_Anonymous(url,name,l111l1Fuck_You_Anonymous,content,l1lll1Fuck_You_Anonymous,query):
	if content == l1lllFuck_You_Anonymous (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨ्"):
		link = open_url(url,verify=False).content
		l111lllFuck_You_Anonymous = url
		headers = {l1lllFuck_You_Anonymous (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭ॎ"):md.User_Agent()}
		link = open_url(url, headers=headers).content
		l11ll1lFuck_You_Anonymous = re.compile(l1lllFuck_You_Anonymous (u"ࠪ࡭ࡩࡀࠠࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪॏ")).findall(link)[0]
		request_url = l1lllFuck_You_Anonymous (u"ࠫࠪࡹ࠯ࡢ࡬ࡤࡼ࠴ࡼ࠴ࡠ࡯ࡲࡺ࡮࡫࡟ࡦࡲ࡬ࡷࡴࡪࡥࡴ࠱ࠨࡷࠬॐ") %(l11l1l1Fuck_You_Anonymous,l11ll1lFuck_You_Anonymous)
		headers = {l1lllFuck_You_Anonymous (u"ࠬࡇࡣࡤࡧࡳࡸ࠲ࡋ࡮ࡤࡱࡧ࡭ࡳ࡭ࠧ॑"):l1lllFuck_You_Anonymous (u"࠭ࡧࡻ࡫ࡳ࠰ࠥࡪࡥࡧ࡮ࡤࡸࡪ࠲ࠠࡴࡦࡦ࡬࠱ࠦࡢࡳ॒ࠩ"), l1lllFuck_You_Anonymous (u"ࠧࡓࡧࡩࡩࡷ࡫ࡲࠨ॓"):l111lllFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬ॔"):md.User_Agent()}
		l1ll1l1lFuck_You_Anonymous = open_url(request_url, headers=headers, verify=False).json()
		l1ll11llFuck_You_Anonymous = re.compile(l1lllFuck_You_Anonymous (u"ࠩࡧࡥࡹࡧ࠭ࡴࡧࡵࡺࡪࡸ࠽ࠣ࠳࠳ࠦࠥࡪࡡࡵࡣ࠰࡭ࡩࡃࠢࠩ࡝ࡡࠦࡢ࠱ࠩࠣࠩॕ")).findall(l1ll1l1lFuck_You_Anonymous[l1lllFuck_You_Anonymous (u"ࠪ࡬ࡹࡳ࡬ࠨॖ")])[0]
	else:
		l111lllFuck_You_Anonymous = query.split(l1lllFuck_You_Anonymous (u"ࠫࢁ࠭ॗ"))[0]
		l1ll11llFuck_You_Anonymous = query.split(l1lllFuck_You_Anonymous (u"ࠬࢂࠧक़"))[1]
		l11ll1lFuck_You_Anonymous = query.split(l1lllFuck_You_Anonymous (u"࠭ࡼࠨख़"))[2]
	l1lll111Fuck_You_Anonymous = int(time.time() * 10000)
        l1lll1lFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠧࠦࡵ࠲ࡥ࡯ࡧࡸ࠰࡯ࡲࡺ࡮࡫࡟ࡵࡱ࡮ࡩࡳ࠭ग़") %l11l1l1Fuck_You_Anonymous
        params = {l1lllFuck_You_Anonymous (u"ࠨࡧ࡬ࡨࠬज़"):l1ll11llFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠩࡰ࡭ࡩ࠭ड़"):l11ll1lFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠪࡣࠬढ़"):l1lll111Fuck_You_Anonymous}
        headers = {l1lllFuck_You_Anonymous (u"ࠫࡆࡩࡣࡦࡲࡷࠫफ़"):l1lllFuck_You_Anonymous (u"ࠬࡺࡥࡹࡶ࠲࡮ࡦࡼࡡࡴࡥࡵ࡭ࡵࡺࠬࠡࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡢࡸࡤࡷࡨࡸࡩࡱࡶ࠯ࠤࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡨࡧࡲࡧࡳࡤࡴ࡬ࡴࡹ࠲ࠠࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡦࡥࡰࡥࡸࡩࡲࡪࡲࡷ࠰ࠥ࠰࠯ࠫ࠽ࠣࡵࡂ࠶࠮࠱࠳ࠪय़"),
                   l1lllFuck_You_Anonymous (u"࠭ࡁࡤࡥࡨࡴࡹ࠳ࡅ࡯ࡥࡲࡨ࡮ࡴࡧࠨॠ"):l1lllFuck_You_Anonymous (u"ࠧࡨࡼ࡬ࡴ࠱ࠦࡤࡦࡨ࡯ࡥࡹ࡫ࠬࠡࡵࡧࡧ࡭࠲ࠠࡣࡴࠪॡ"), l1lllFuck_You_Anonymous (u"ࠨࡃࡦࡧࡪࡶࡴ࠮ࡎࡤࡲ࡬ࡻࡡࡨࡧࠪॢ"):l1lllFuck_You_Anonymous (u"ࠩࡨࡲ࠲࡛ࡓ࠭ࡧࡱ࠿ࡶࡃ࠰࠯࠺ࠪॣ"),
                   l1lllFuck_You_Anonymous (u"ࠪࡖࡪ࡬ࡥࡳࡧࡵࠫ।"):l111lllFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨ॥"):md.User_Agent(), l1lllFuck_You_Anonymous (u"ࠬ࡞࠭ࡓࡧࡴࡹࡪࡹࡴࡦࡦ࠰࡛࡮ࡺࡨࠨ०"):l1lllFuck_You_Anonymous (u"࠭ࡘࡎࡎࡋࡸࡹࡶࡒࡦࡳࡸࡩࡸࡺࠧ१")}
        data = l1lllFuck_You_Anonymous (u"ࠧࠨ२")
        l1ll11l1Fuck_You_Anonymous = 0
        while l1ll11l1Fuck_You_Anonymous < 10:
            l1ll11l1Fuck_You_Anonymous += 1
            data = open_url(l1lll1lFuck_You_Anonymous, params=params, headers=headers).content
            if not data:
                data = l1lllFuck_You_Anonymous (u"ࠨࠩ३")
                continue
            if l1lllFuck_You_Anonymous (u"ࠩ࡞ࡡࠬ४") not in data:
                time.sleep(1)
                break
        l1l1lllFuck_You_Anonymous, l1l1ll1Fuck_You_Anonymous = llFuck_You_Anonymous(data)
        l1ll11lFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡲࡵࡶࡪࡧࡢࡷࡴࡻࡲࡤࡧࡶ࠳ࠪࡹࠧ५") %(l11l1l1Fuck_You_Anonymous,l1ll11llFuck_You_Anonymous)
	l1lFuck_You_Anonymous = {l1lllFuck_You_Anonymous (u"ࠫࡽ࠭६"):l1l1lllFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"ࠬࡿࠧ७"):l1l1ll1Fuck_You_Anonymous}
	headers = {l1lllFuck_You_Anonymous (u"࠭ࡁࡤࡥࡨࡴࡹ࠭८"):l1lllFuck_You_Anonymous (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰ࠯ࠤࡹ࡫ࡸࡵ࠱࡭ࡥࡻࡧࡳࡤࡴ࡬ࡴࡹ࠲ࠠࠫ࠱࠭࠿ࠥࡷ࠽࠱࠰࠳࠵ࠬ९"),
		   l1lllFuck_You_Anonymous (u"ࠨࡃࡦࡧࡪࡶࡴ࠮ࡇࡱࡧࡴࡪࡩ࡯ࡩࠪ॰"):l1lllFuck_You_Anonymous (u"ࠩࡪࡾ࡮ࡶࠬࠡࡦࡨࡪࡱࡧࡴࡦ࠮ࠣࡷࡩࡩࡨ࠭ࠢࡥࡶࠬॱ"), l1lllFuck_You_Anonymous (u"ࠪࡅࡨࡩࡥࡱࡶ࠰ࡐࡦࡴࡧࡶࡣࡪࡩࠬॲ"):l1lllFuck_You_Anonymous (u"ࠫࡪࡴ࠭ࡖࡕ࠯ࡩࡳࡁࡱ࠾࠲࠱࠼ࠬॳ"),
		   l1lllFuck_You_Anonymous (u"ࠬࡘࡥࡧࡧࡵࡩࡷ࠭ॴ"):l111lllFuck_You_Anonymous, l1lllFuck_You_Anonymous (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪॵ"):md.User_Agent(), l1lllFuck_You_Anonymous (u"࡙ࠧ࠯ࡕࡩࡶࡻࡥࡴࡶࡨࡨ࠲࡝ࡩࡵࡪࠪॶ"):l1lllFuck_You_Anonymous (u"ࠨ࡚ࡐࡐࡍࡺࡴࡱࡔࡨࡵࡺ࡫ࡳࡵࠩॷ")}
	final = open_url(l1ll11lFuck_You_Anonymous, params=l1lFuck_You_Anonymous, headers=headers, verify=False).json()
	l1lllllFuck_You_Anonymous = []
	l1ll1llFuck_You_Anonymous = []
	l1l11llFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠩࠪॸ")
	if l1l1l1lFuck_You_Anonymous == l1lllFuck_You_Anonymous (u"ࠪࡸࡷࡻࡥࠨॹ"):
		url = max(final[l1lllFuck_You_Anonymous (u"ࠫࡵࡲࡡࡺ࡮࡬ࡷࡹ࠭ॺ")][0][l1lllFuck_You_Anonymous (u"ࠬࡹ࡯ࡶࡴࡦࡩࡸ࠭ॻ")], key=lambda l1ll1l11Fuck_You_Anonymous: int(re.sub(l1lllFuck_You_Anonymous (u"࠭࡜ࡅࠩॼ"), l1lllFuck_You_Anonymous (u"ࠧࠨॽ"), l1ll1l11Fuck_You_Anonymous[l1lllFuck_You_Anonymous (u"ࠨ࡮ࡤࡦࡪࡲࠧॾ")])))
		url = url[l1lllFuck_You_Anonymous (u"ࠩࡩ࡭ࡱ࡫ࠧॿ")]
	else:
		match = final[l1lllFuck_You_Anonymous (u"ࠪࡴࡱࡧࡹ࡭࡫ࡶࡸࠬঀ")][0][l1lllFuck_You_Anonymous (u"ࠫࡸࡵࡵࡳࡥࡨࡷࠬঁ")]
		for a in match:
			l1l11llFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤ࡮ࡴࡤࡪࡣࡱࡶࡪࡪ࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬং") %a[l1lllFuck_You_Anonymous (u"࠭࡬ࡢࡤࡨࡰࠬঃ")]
			l1lllllFuck_You_Anonymous.append(l1l11llFuck_You_Anonymous)
			l1ll1llFuck_You_Anonymous.append(a[l1lllFuck_You_Anonymous (u"ࠧࡧ࡫࡯ࡩࠬ঄")])
		if len(match) >1:
			l1111lFuck_You_Anonymous = md.dialog_select(l1lllFuck_You_Anonymous (u"ࠨࡕࡨࡰࡪࡩࡴࠡࡕࡷࡶࡪࡧ࡭ࠡࡓࡸࡥࡱ࡯ࡴࡺࠩঅ"),l1lllllFuck_You_Anonymous)
			if l1111lFuck_You_Anonymous == -1:
				return
			elif l1111lFuck_You_Anonymous > -1:
				url = l1ll1llFuck_You_Anonymous[l1111lFuck_You_Anonymous]
		else:
			url = final[l1lllFuck_You_Anonymous (u"ࠩࡳࡰࡦࡿ࡬ࡪࡵࡷࠫআ")][0][l1lllFuck_You_Anonymous (u"ࠪࡷࡴࡻࡲࡤࡧࡶࠫই")][0][l1lllFuck_You_Anonymous (u"ࠫ࡫࡯࡬ࡦࠩঈ")]
	md.resolved(url, name, fan_art, l1lll1Fuck_You_Anonymous)
	l1ll1Fuck_You_Anonymous.end_of_directory()
def l1lllll1Fuck_You_Anonymous():
        l111lFuck_You_Anonymous = xbmc.translatePath(l1lllFuck_You_Anonymous (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࡲࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻ࠱ࡱࡦ࡬ࠧউ"))
        l11llFuck_You_Anonymous = xbmc.translatePath(l1lllFuck_You_Anonymous (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹ࠯ࡱ࡮ࡸ࡫࡮ࡴ࠮ࡱࡴࡲ࡫ࡷࡧ࡭࠯ࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡰࡥ࡫ࡽࡩࡻࡣࡵࡨࠬঊ"))
        l1l1ll11Fuck_You_Anonymous = xbmc.translatePath(l1lllFuck_You_Anonymous (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡸ࡬ࡨࡪࡵ࠮࡬ࡴࡤࡸࡴࡹࠧঋ"))
        if os.path.exists(l111lFuck_You_Anonymous):
                l11Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠨ࡛ࡲࡹࠥࡎࡡࡷࡧࠣࡍࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡆࡳࡱࡰࠤࡆࡴࠧঌ")
                l1lll11lFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠩࡘࡲࡴ࡬ࡦࡪࡥ࡬ࡥࡱࠦࡓࡰࡷࡵࡧࡪ࡙ࠦࠦࠡ࡬ࡰࡱࠦࡎࡰࡹࠣࡈࡪࡲࡥࡵࡧࠣࡔࡱ࡫ࡡࡴࡧࠪ঍")
                l1lll1l1Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠪࡍࡳࡹࡴࡢ࡮࡯ࠤࡅࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞ࡪࡷࡸࡵࡀ࠯࠰࡯ࡸࡧࡰࡿࡳ࠯࡯ࡨࡨ࡮ࡧࡰࡰࡴࡷࡥࡱ࠺࡫ࡰࡦ࡬࠲ࡲࡲ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ঎")
                l1lll1llFuck_You_Anonymous = l1lllFuck_You_Anonymous (u"ࠫࡗ࡫࡭ࡰࡸࡨࡨࠥࡇ࡮ࡰࡰࡼࡱࡴࡻࡳࠡࡔࡨࡴࡴࠦࡁ࡯ࡦࠣࡅࡩࡪ࡯࡯ࡵࠪএ")
                l1llll11Fuck_You_Anonymous = l1lllFuck_You_Anonymous (u"࡙ࠬࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡕࡲࡥࡢࡵࡨࠤࡉࡵ࡮ࡵࠢࡖࡹࡵࡶ࡯ࡳࡶࠣࡍࡩ࡯࡯ࡵࡵࠪঐ")
                l1ll1Fuck_You_Anonymous.show_ok_dialog([l11Fuck_You_Anonymous, l1lll11lFuck_You_Anonymous, l1lll1l1Fuck_You_Anonymous], l1l1lFuck_You_Anonymous)
                l1Fuck_You_Anonymous = l1ll1Fuck_You_Anonymous.get_path()
                shutil.rmtree(l1Fuck_You_Anonymous, ignore_errors=True)
                shutil.rmtree(l111lFuck_You_Anonymous, ignore_errors=True)
                shutil.rmtree(l11llFuck_You_Anonymous, ignore_errors=True)
                shutil.rmtree(l1l1ll11Fuck_You_Anonymous, ignore_errors=True)
                l1ll1Fuck_You_Anonymous.log(l1lllFuck_You_Anonymous (u"࠭࠽࠾࠿ࡇࡉࡑࡋࡔࡊࡐࡊࡁࡂࡃࡁࡏࡑࡑ࡝ࡒࡕࡕࡔ࠿ࡀࡁࡆࡊࡄࡐࡐࡖࡁࡂࡃࠫ࠾࠿ࡀࡖࡊࡖࡏ࠾࠿ࡀࠫ঑"))
                l1ll1Fuck_You_Anonymous.show_ok_dialog([l1lll1llFuck_You_Anonymous, l1llll11Fuck_You_Anonymous], l1l1lFuck_You_Anonymous)
                time.sleep(2)
                os._exit(0)
md.check_source()
mode = md.args[l1lllFuck_You_Anonymous (u"ࠧ࡮ࡱࡧࡩࠬ঒")]
url = md.args.get(l1lllFuck_You_Anonymous (u"ࠨࡷࡵࡰࠬও"), None)
name = md.args.get(l1lllFuck_You_Anonymous (u"ࠩࡱࡥࡲ࡫ࠧঔ"), None)
query = md.args.get(l1lllFuck_You_Anonymous (u"ࠪࡵࡺ࡫ࡲࡺࠩক"), None)
title = md.args.get(l1lllFuck_You_Anonymous (u"ࠫࡹ࡯ࡴ࡭ࡧࠪখ"), None)
l11l1llFuck_You_Anonymous = md.args.get(l1lllFuck_You_Anonymous (u"ࠬࡹࡥࡢࡵࡲࡲࠬগ"), None)
l1ll1111Fuck_You_Anonymous = md.args.get(l1lllFuck_You_Anonymous (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࠧঘ") ,None)
l1lll1Fuck_You_Anonymous = md.args.get(l1lllFuck_You_Anonymous (u"ࠧࡪࡰࡩࡳࡱࡧࡢࡦ࡮ࡶࠫঙ"), None)
content = md.args.get(l1lllFuck_You_Anonymous (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩচ"), None)
l1ll1l1Fuck_You_Anonymous = md.args.get(l1lllFuck_You_Anonymous (u"ࠩࡰࡳࡩ࡫࡟ࡪࡦࠪছ"), None)
l111l1Fuck_You_Anonymous = md.args.get(l1lllFuck_You_Anonymous (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭জ"), None)
fan_art = md.args.get(l1lllFuck_You_Anonymous (u"ࠫ࡫ࡧ࡮ࡠࡣࡵࡸࠬঝ"), None)
is_folder = md.args.get(l1lllFuck_You_Anonymous (u"ࠬ࡯ࡳࡠࡨࡲࡰࡩ࡫ࡲࠨঞ"), True)
if mode is None or url is None or len(url)<1:
	l1l1llFuck_You_Anonymous()
elif mode == l1lllFuck_You_Anonymous (u"࠭࠱ࠨট"):
	l1l1l1llFuck_You_Anonymous(content)
elif mode == l1lllFuck_You_Anonymous (u"ࠧ࠳ࠩঠ"):
	l1l11lFuck_You_Anonymous(url,content)
elif mode == l1lllFuck_You_Anonymous (u"ࠨ࠵ࠪড"):
	l111l11Fuck_You_Anonymous(title, url, l111l1Fuck_You_Anonymous, content, l11l1llFuck_You_Anonymous)
elif mode == l1lllFuck_You_Anonymous (u"ࠩ࠷ࠫঢ"):
	l1l1l1l1Fuck_You_Anonymous(url, content)
elif mode == l1lllFuck_You_Anonymous (u"ࠪ࠹ࠬণ"):
	l1llllFuck_You_Anonymous(url, content)
elif mode == l1lllFuck_You_Anonymous (u"ࠫ࠻࠭ত"):
	l11lllFuck_You_Anonymous(url, content)
elif mode == l1lllFuck_You_Anonymous (u"ࠬ࠽ࠧথ"):
	l1ll1lFuck_You_Anonymous(url,name,l111l1Fuck_You_Anonymous,content,l1lll1Fuck_You_Anonymous,query)
elif mode == l1lllFuck_You_Anonymous (u"࠭ࡳࡦࡣࡵࡧ࡭࠭দ"):
	l11l11Fuck_You_Anonymous(content,query)
elif mode == l1lllFuck_You_Anonymous (u"ࠧࡢࡦࡧࡳࡳࡥࡳࡦࡣࡵࡧ࡭࠭ধ"):
	md.addon_search(content,query,fan_art,l1lll1Fuck_You_Anonymous)
elif mode == l1lllFuck_You_Anonymous (u"ࠨࡩࡨࡸࡤࡶࡲࡰࡺࡼࠫন"):
	l1l1lll1Fuck_You_Anonymous(url)
elif mode == l1lllFuck_You_Anonymous (u"ࠩࡤࡨࡩࡥࡲࡦ࡯ࡲࡺࡪࡥࡦࡢࡸࠪ঩"):
	md.add_remove_fav(name, url, l1lll1Fuck_You_Anonymous, fan_art,
			  content, l1ll1l1Fuck_You_Anonymous, is_folder)
elif mode == l1lllFuck_You_Anonymous (u"ࠪࡪࡪࡺࡣࡩࡡࡩࡥࡻࡹࠧপ"):
	md.fetch_favs(l11l1l1Fuck_You_Anonymous)
elif mode == l1lllFuck_You_Anonymous (u"ࠫࡦࡪࡤࡰࡰࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬফ"):
	l1ll1Fuck_You_Anonymous.show_settings()
elif mode == l1lllFuck_You_Anonymous (u"ࠬࡳࡥࡵࡣࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬব"):
	import metahandler
	metahandler.display_settings()