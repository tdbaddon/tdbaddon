# -*- coding: utf-8 -*-
import sys
l11l1l1Created_By_Mucky_Duck = sys.version_info [0] == 2
l1111llCreated_By_Mucky_Duck = 2048
l1111Created_By_Mucky_Duck = 7
def l11l11Created_By_Mucky_Duck (llCreated_By_Mucky_Duck):
    global l11lCreated_By_Mucky_Duck
    l111lllCreated_By_Mucky_Duck = ord (llCreated_By_Mucky_Duck [-1])
    l1lllllCreated_By_Mucky_Duck = llCreated_By_Mucky_Duck [:-1]
    l111Created_By_Mucky_Duck = l111lllCreated_By_Mucky_Duck % len (l1lllllCreated_By_Mucky_Duck)
    l1lllCreated_By_Mucky_Duck = l1lllllCreated_By_Mucky_Duck [:l111Created_By_Mucky_Duck] + l1lllllCreated_By_Mucky_Duck [l111Created_By_Mucky_Duck:]
    if l11l1l1Created_By_Mucky_Duck:
        l1l1ll1Created_By_Mucky_Duck = unicode () .join ([unichr (ord (char) - l1111llCreated_By_Mucky_Duck - (l11l1lCreated_By_Mucky_Duck + l111lllCreated_By_Mucky_Duck) % l1111Created_By_Mucky_Duck) for l11l1lCreated_By_Mucky_Duck, char in enumerate (l1lllCreated_By_Mucky_Duck)])
    else:
        l1l1ll1Created_By_Mucky_Duck = str () .join ([chr (ord (char) - l1111llCreated_By_Mucky_Duck - (l11l1lCreated_By_Mucky_Duck + l111lllCreated_By_Mucky_Duck) % l1111Created_By_Mucky_Duck) for l11l1lCreated_By_Mucky_Duck, char in enumerate (l1lllCreated_By_Mucky_Duck)])
    return eval (l1l1ll1Created_By_Mucky_Duck)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import os,re,shutil,sys,urllib
# M4U Add-on Created By Mucky Duck (3/2016)
l11ll11Created_By_Mucky_Duck = xbmcaddon.Addon().getAddonInfo(l11l11Created_By_Mucky_Duck (u"ࠫ࡮ࡪࠧࠀ"))
l11ll1lCreated_By_Mucky_Duck = Addon(l11ll11Created_By_Mucky_Duck, sys.argv)
l1lll1lCreated_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_name()
l1l1111Created_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_path()
md = md(l11ll11Created_By_Mucky_Duck, sys.argv)
l1ll1lCreated_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_setting(l11l11Created_By_Mucky_Duck (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࠪࠁ"))
l1l11l1Created_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_setting(l11l11Created_By_Mucky_Duck (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥࡳࡩࡱࡺࡷࠬࠂ"))
l1l1lCreated_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_setting(l11l11Created_By_Mucky_Duck (u"ࠧࡦࡰࡤࡦࡱ࡫࡟࡮ࡱࡹ࡭ࡪࡹࠧࠃ"))
l1ll1Created_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_setting(l11l11Created_By_Mucky_Duck (u"ࠨࡧࡱࡥࡧࡲࡥࡠࡨࡤࡺࡸ࠭ࠄ"))
l11llCreated_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_setting(l11l11Created_By_Mucky_Duck (u"ࠩࡤࡨࡩࡥࡳࡦࡶࠪࠅ"))
l1llllllCreated_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_setting(l11l11Created_By_Mucky_Duck (u"ࠪࡩࡳࡧࡢ࡭ࡧࡢࡱࡪࡺࡡࡠࡵࡨࡸࠬࠆ"))
l11Created_By_Mucky_Duck = md.get_art()
l1111lCreated_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_icon()
l1ll11Created_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_fanart()
l1llCreated_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_setting(l11l11Created_By_Mucky_Duck (u"ࠫࡧࡧࡳࡦࡡࡸࡶࡱ࠭ࠇ"))
reload(sys)
sys.setdefaultencoding(l11l11Created_By_Mucky_Duck (u"ࠧࡻࡴࡧ࠯࠻ࠦࠈ"))
def l111111Created_By_Mucky_Duck():
	if l1l11l1Created_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠉ"):
		md.addDir({l11l11Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࠊ"): l11l11Created_By_Mucky_Duck (u"ࠨ࠴ࠪࠋ"), l11l11Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠌ"):l11l11Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢ࡚ࡖ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࠍ"), l11l11Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠎ"):l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠏ")})
	if l1l1lCreated_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠐ"):
		md.addDir({l11l11Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࠑ"): l11l11Created_By_Mucky_Duck (u"ࠨ࠳ࠪࠒ"), l11l11Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠓ"):l11l11Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡓࡏࡗࡋࡈࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࠔ"), l11l11Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠕ"):l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠖ")})
	if l1ll1Created_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠗ"):
		md.addDir({l11l11Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬ࠘"): l11l11Created_By_Mucky_Duck (u"ࠨࡨࡨࡸࡨ࡮࡟ࡧࡣࡹࡷࠬ࠙"), l11l11Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠚ"):l11l11Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡓ࡙ࠡࡈࡄ࡚ࡔ࡛ࡒࡊࡖࡈࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࠛ"), l11l11Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠜ"):l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠝ")})
	if l1ll1lCreated_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠞ"):
		if l1llllllCreated_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬࠟ"):
			md.addDir({l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠠ"):l11l11Created_By_Mucky_Duck (u"ࠩࡰࡩࡹࡧ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠩࠡ"), l11l11Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠢ"):l11l11Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡍࡆࡖࡄࠤࡘࡋࡔࡕࡋࡑࡋࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࠣ"), l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠤ"):l11l11Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠥ")}, is_folder=False, is_playable=False)
	if l11llCreated_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬࠦ"):
		md.addDir({l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠧ"):l11l11Created_By_Mucky_Duck (u"ࠩࡤࡨࡩࡵ࡮ࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠪࠨ"), l11l11Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠩ"):l11l11Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡁࡅࡆࡒࡒ࡙ࠥࡅࡕࡖࡌࡒࡌ࡙࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࠪ"), l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠫ"):l11l11Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠬ")}, is_folder=False, is_playable=False)
	l111lCreated_By_Mucky_Duck()
	l111ll1Created_By_Mucky_Duck()
	setView(l11ll11Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭࠭"), l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫ࠮"))
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
def l111l1lCreated_By_Mucky_Duck():
	if l1ll1Created_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"ࠩࡷࡶࡺ࡫ࠧ࠯"):
		md.addDir({l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ࠰"): l11l11Created_By_Mucky_Duck (u"ࠫ࡫࡫ࡴࡤࡪࡢࡪࡦࡼࡳࠨ࠱"), l11l11Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ࠲"):l11l11Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡏ࡜ࠤࡋࡇࡖࡐࡗࡕࡍ࡙ࡋࡓ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭࠳"), l11l11Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࠴"):l11l11Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࠵")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ࠶"): l11l11Created_By_Mucky_Duck (u"ࠪ࠷ࠬ࠷"), l11l11Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ࠸"):l11l11Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡍࡃࡗࡉࡘ࡚ࠠࡂࡆࡇࡉࡉࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫ࠹"), l11l11Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࠺"):l1llCreated_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠧ࠰ࡰࡨࡻࡦࡪࡤࠨ࠻"), l11l11Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ࠼"):l11l11Created_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩ࠽")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ࠾"): l11l11Created_By_Mucky_Duck (u"ࠫ࠸࠭࠿"), l11l11Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࡀ"):l11l11Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡏࡒࡗ࡙ࠦࡖࡊࡇ࡚ࡉࡉࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡁ"), l11l11Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࡂ"):l1llCreated_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠨ࠱ࡷࡳࡵ࠳ࡶࡪࡧࡺࠫࡃ"), l11l11Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࡄ"):l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪࡅ")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡆ"): l11l11Created_By_Mucky_Duck (u"ࠬ࠹ࠧࡇ"), l11l11Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡈ"):l11l11Created_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣ࡛ࡃ࡟ࡋࡓ࡙ࠦࡍࡐࡘࡌࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡉ"), l11l11Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡊ"):l1llCreated_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠩ࠲࡬ࡴࡺ࠭࡮ࡱࡹ࡭ࡪ࠳࠱࠯ࡪࡷࡱࡱ࠭ࡋ"), l11l11Created_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࡌ"):l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶࠫࡍ")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪࡎ"): l11l11Created_By_Mucky_Duck (u"࠭ࡳࡦࡣࡵࡧ࡭࠭ࡏ"), l11l11Created_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬࡐ"):l11l11Created_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝࡜ࡄࡠࡗࡊࡇࡒࡄࡊ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨࡑ"), l11l11Created_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ࡒ"):l11l11Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࡓ"), l11l11Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࡔ"):l11l11Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࡕ")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࡖ"): l11l11Created_By_Mucky_Duck (u"ࠧ࠵ࠩࡗ"), l11l11Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࡘ"):l11l11Created_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞࡝ࡅࡡࡌࡋࡎࡓࡇ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࡙"), l11l11Created_By_Mucky_Duck (u"ࠪࡹࡷࡲ࡚ࠧ"):l1llCreated_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸ࡛ࠬ"):l11l11Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬ࡜")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫ࡝"): l11l11Created_By_Mucky_Duck (u"ࠧ࠶ࠩ࡞"), l11l11Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭࡟"):l11l11Created_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞࡝ࡅࡡ࡞ࡋࡁࡓ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧࡠ"), l11l11Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࡡ"):l1llCreated_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࡢ"):l11l11Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࡣ")})
	setView(l11ll11Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࡷࠬࡤ"), l11l11Created_By_Mucky_Duck (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪࡥ"))
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
def l111l11Created_By_Mucky_Duck():
	if l1ll1Created_By_Mucky_Duck == l11l11Created_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭ࡦ"):
		md.addDir({l11l11Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࡧ"): l11l11Created_By_Mucky_Duck (u"ࠪࡪࡪࡺࡣࡩࡡࡩࡥࡻࡹࠧࡨ"), l11l11Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࡩ"):l11l11Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡎ࡛ࠣࡊࡆ࡜ࡏࡖࡔࡌࡘࡊ࡙࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࡪ"), l11l11Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࡫"):l11l11Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࡬")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭࡭"): l11l11Created_By_Mucky_Duck (u"ࠩ࠶ࠫ࡮"), l11l11Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ࡯"):l11l11Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡌࡂࡖࡈࡗ࡙ࠦࡁࡅࡆࡈࡈࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࡰ"), l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡱ"):l1llCreated_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"࠭࠯࡭ࡣࡷࡩࡸࡺ࠭ࡵࡸࡶ࡬ࡴࡽࠧࡲ"), l11l11Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡳ"):l11l11Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࡴ")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࡵ"): l11l11Created_By_Mucky_Duck (u"ࠪ࠷ࠬࡶ"), l11l11Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࡷ"):l11l11Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡎࡑࡖࡘࠥ࡜ࡉࡆ࡙ࡈࡈࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࡸ"), l11l11Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࡹ"):l1llCreated_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠧ࠰ࡶࡲࡴ࠲ࡼࡩࡦࡹ࠰ࡸࡻࡹࡨࡰࡹࠪࡺ"), l11l11Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࡻ"):l11l11Created_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࡼ")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࡽ"): l11l11Created_By_Mucky_Duck (u"ࠫࡸ࡫ࡡࡳࡥ࡫ࠫࡾ"), l11l11Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࡿ"):l11l11Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡕࡈࡅࡗࡉࡈ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࢀ"), l11l11Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࢁ"):l1llCreated_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࢂ"):l11l11Created_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࢃ")})
	md.addDir({l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࢄ"): l11l11Created_By_Mucky_Duck (u"ࠫ࠸࠭ࢅ"), l11l11Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࢆ"):l11l11Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡃࡏࡐࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࢇ"), l11l11Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࢈"):l1llCreated_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠨ࠱ࡷࡺࡸ࡮࡯ࡸࠩࢉ"), l11l11Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࢊ"):l11l11Created_By_Mucky_Duck (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫࢋ")})
	setView(l11ll11Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪࢌ"), l11l11Created_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨࢍ"))
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
def l1Created_By_Mucky_Duck(url,content):
	link = open_url(url).text
	l1ll1l1Created_By_Mucky_Duck = md.regex_get_all(link, l11l11Created_By_Mucky_Duck (u"࠭ࠢࡪࡶࡨࡱࠧ࠭ࢎ"), l11l11Created_By_Mucky_Duck (u"ࠧࡤ࡮ࡨࡥࡷࡀࡢࡰࡶ࡫ࠫ࢏"))
	items = len(l1ll1l1Created_By_Mucky_Duck)
	for a in l1ll1l1Created_By_Mucky_Duck:
		if content == l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨ࢐"):
			name = md.regex_from_to(a, l11l11Created_By_Mucky_Duck (u"ࠩࡦ࡭ࡹ࡫࠾ࠨ࢑"), l11l11Created_By_Mucky_Duck (u"ࠪࡀࠬ࢒"))
		elif content == l11l11Created_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬ࢓"):
			name = md.regex_from_to(a, l11l11Created_By_Mucky_Duck (u"ࠬ࡮ࡲࡦࡨࡀ࠲࠯ࡅ࠾ࠨ࢔"), l11l11Created_By_Mucky_Duck (u"࠭࠼ࠨ࢕"))
		name = l11ll1lCreated_By_Mucky_Duck.unescape(name)
		name = name.encode(l11l11Created_By_Mucky_Duck (u"ࠧࡢࡵࡦ࡭࡮࠭࢖"), l11l11Created_By_Mucky_Duck (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨࢗ")).decode(l11l11Created_By_Mucky_Duck (u"ࠩࡤࡷࡨ࡯ࡩࠨ࢘"))
		l1l1l11Created_By_Mucky_Duck = md.regex_from_to(a, l11l11Created_By_Mucky_Duck (u"ࠪࡧࡱࡧࡳࡴ࠿ࠥ࡬࠸࠳ࡱࡶࡣ࡯࡭ࡹࡿࠢ࠯ࠬࡂࡂ࢙ࠬ"), l11l11Created_By_Mucky_Duck (u"ࠫࡁ࢚࠭"))
		url = md.regex_from_to(a, l11l11Created_By_Mucky_Duck (u"ࠬ࡮ࡲࡦࡨࡀ࢛ࠦࠬ"), l11l11Created_By_Mucky_Duck (u"࠭ࠢࠨ࢜"))
		l1lll1Created_By_Mucky_Duck = md.regex_from_to(a, l11l11Created_By_Mucky_Duck (u"ࠧࡴࡴࡦࡁࠬ࢝"), l11l11Created_By_Mucky_Duck (u"ࠨࡣ࡯ࡸࡂ࠭࢞")).replace(l11l11Created_By_Mucky_Duck (u"ࠩࠣࠫ࢟"),l11l11Created_By_Mucky_Duck (u"ࠪࠫࢠ"))
		l1111l1Created_By_Mucky_Duck = md.regex_from_to(a, l11l11Created_By_Mucky_Duck (u"ࠫࠧ࡮࠴࠮ࡥࡤࡸࠧ࠴ࠪࡀࡀࠪࢡ"), l11l11Created_By_Mucky_Duck (u"ࠬࡂࠧࢢ"))
		if l11l11Created_By_Mucky_Duck (u"࠭࠼ࡢࠢࡷ࡭ࡹࡲࡥࠨࢣ") in l1111l1Created_By_Mucky_Duck:
			l1111l1Created_By_Mucky_Duck = md.regex_from_to(a, l11l11Created_By_Mucky_Duck (u"ࠧࠣࡪ࠷࠱ࡨࡧࡴࠣ࠰࠭ࡃࡃ࠴ࠪࡀ࠾࠱࠮ࡄࡄࠧࢤ"), l11l11Created_By_Mucky_Duck (u"ࠨ࠾ࠪࢥ"))
		fan_art = {l11l11Created_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࠧࢦ"):l1lll1Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪࢧ"):l11Created_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠫࡲ࠺ࡵ࠯࡬ࡳ࡫ࠬࢨ")}
		title = name
		md.remove_punctuation(title)
		if content == l11l11Created_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࢩ"):
			if l11l11Created_By_Mucky_Duck (u"࠭࠭ࡵࡸࡶ࡬ࡴࡽ࠭ࠨࢪ") in url:
				md.addDir({l11l11Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࢫ"): l11l11Created_By_Mucky_Duck (u"ࠨ࠸ࠪࢬ"), l11l11Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࢭ"):l11l11Created_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤࡩࡵࡤࡨࡧࡵࡦࡱࡻࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ࢮ") %(name,l1111l1Created_By_Mucky_Duck), l11l11Created_By_Mucky_Duck (u"ࠫࡹ࡯ࡴ࡭ࡧࠪࢯ"):title,
					   l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࢰ"):url, l11l11Created_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱ࡭ࡲࡧࡧࡦࠩࢱ"):l1lll1Created_By_Mucky_Duck ,l11l11Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࢲ"):l11l11Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࢳ")}, {l11l11Created_By_Mucky_Duck (u"ࠩࡶࡳࡷࡺࡴࡪࡶ࡯ࡩࠬࢴ"):title}, fan_art, item_count=items)
		else:
			if l11l11Created_By_Mucky_Duck (u"ࠪ࠱ࡹࡼࡳࡩࡱࡺ࠱ࠬࢵ") not in url:
				md.addDir({l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࢶ"): l11l11Created_By_Mucky_Duck (u"ࠬ࠽ࠧࢷ"), l11l11Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࢸ"):l11l11Created_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡦࡲࡨ࡬࡫ࡲࡣ࡮ࡸࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࢹ") %(name,l1l1l11Created_By_Mucky_Duck),
					   l11l11Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࢺ"):url, l11l11Created_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠬࢻ"):l1lll1Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࢼ"):l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶࠫࢽ")}, {l11l11Created_By_Mucky_Duck (u"ࠬࡹ࡯ࡳࡶࡷ࡭ࡹࡲࡥࠨࢾ"):title}, fan_art, is_folder=False, item_count=items)
	try:
		l1llll1Created_By_Mucky_Duck = {l11l11Created_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫࢿ"):l11Created_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠧ࡯ࡧࡻࡸ࠳ࡶ࡮ࡨࠩࣀ"), l11l11Created_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨࣁ"):l11Created_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠩࡰ࠸ࡺ࠴ࡪࡱࡩࠪࣂ")}
		l111l1Created_By_Mucky_Duck = re.compile(l11l11Created_By_Mucky_Duck (u"ࠥࡀࡦࠦࡩࡥ࠿ࠪࡶ࡮࡭ࡨࡵࠩࠣ࡬ࡷ࡫ࡦ࠾ࠩࠫ࠲࠯ࡅࠩࠨࡀࠣࡀ࡮ࡳࡧࠡࡵࡵࡧࡂ࠭࡮ࡦࡺࡷࡠ࠳ࡶ࡮ࡨࠩࠣࡥࡱࡺ࠽ࠨ࠰࠭ࡃࠬࠦࡷࡪࡦࡷ࡬ࡂ࠭࠵࠱ࠩࡁࡀ࠴ࡧ࠾ࠣࣃ")).findall(link)[0]
		md.addDir({l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࣄ"): l11l11Created_By_Mucky_Duck (u"ࠬ࠹ࠧࣅ"), l11l11Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࣆ"):l11l11Created_By_Mucky_Duck (u"ࠧ࡜ࡋࡠ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡤࡰࡦࡪࡩࡷࡨ࡬ࡶࡧࡠࡋࡴࠦࡔࡰࠢࡑࡩࡽࡺࠠࡑࡣࡪࡩࡃࡄ࠾࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࡡ࠯ࡊ࡟ࠪࣇ"),
			   l11l11Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࣈ"):l111l1Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࣉ"):content}, fan_art=l1llll1Created_By_Mucky_Duck)
	except:pass
	try:
		l111l1Created_By_Mucky_Duck = re.compile(l11l11Created_By_Mucky_Duck (u"ࠪࡀࡦࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡵࡰࡳ࡫ࠥࡨࡴ࡯ࡲࡪ࠱ࡦࡲࡴࠡࡤࡷࡲࡵ࡭࠭ࡧ࡮ࡤࡸࠥࡽࡡࡷࡧࡶ࠱ࡧࡻࡴࡵࡱࡱࠤࡼࡧࡶࡦࡵ࠰ࡩ࡫࡬ࡥࡤࡶࠥࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠰࠿ࠪࠤࡁࠬ࠳࠰࠿ࠪ࠾࠲ࡥࡃ࠴ࠪࡀࠩ࣊")).findall(link)
		for url, name in l111l1Created_By_Mucky_Duck:
			md.addDir({l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩ࣋"): l11l11Created_By_Mucky_Duck (u"ࠬ࠹ࠧ࣌"), l11l11Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ࣍"):l11l11Created_By_Mucky_Duck (u"ࠧ࡜ࡋࡠ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡤࡰࡦࡪࡩࡷࡨ࡬ࡶࡧࡠࡔࡦ࡭ࡥࠡࠧࡶࠤࡃࡄ࠾࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࡡ࠯ࡊ࡟ࠪ࣎") %name,
				   l11l11Created_By_Mucky_Duck (u"ࠨࡷࡵࡰ࣏ࠬ"):url, l11l11Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶ࣐ࠪ"):content}, l1llll1Created_By_Mucky_Duck)
	except:pass
	if content == l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵ࣑ࠪ"):
		setView(l11ll11Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶ࣒ࠫ"), l11l11Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨ࠱ࡻ࡯ࡥࡸ࣓ࠩ"))
	elif content == l11l11Created_By_Mucky_Duck (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹࠧࣔ"):
		setView(l11ll11Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠧࡵࡸࡶ࡬ࡴࡽࡳࠨࣕ"), l11l11Created_By_Mucky_Duck (u"ࠨࡵ࡫ࡳࡼ࠳ࡶࡪࡧࡺࠫࣖ"))
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
def l111ll1Created_By_Mucky_Duck():
	link = open_url(l11l11Created_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡴࡦࡹࡴࡦࡤ࡬ࡲ࠳ࡩ࡯࡮࠱ࡵࡥࡼ࠵ࡃࡧ࠶ࡆ࠷ࡺࡎ࠱ࠨࣗ")).content
	version = re.findall(l11l11Created_By_Mucky_Duck (u"ࡵࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠠࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪࣘ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l11l11Created_By_Mucky_Duck (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷ࠴ࡹࡣࡳ࡫ࡳࡸ࠳ࡳ࡯ࡥࡷ࡯ࡩ࠳ࡳࡵࡤ࡭ࡼࡷ࠳ࡩ࡯࡮࡯ࡲࡲ࠴ࡧࡤࡥࡱࡱ࠲ࡽࡳ࡬ࠨࣙ")), l11l11Created_By_Mucky_Duck (u"ࠬࡸࠫࠨࣚ")) as f:
		l1ll111Created_By_Mucky_Duck = f.read()
		if re.search(l11l11Created_By_Mucky_Duck (u"ࡸࠧࡷࡧࡵࡷ࡮ࡵ࡮࠾ࠤࠨࡷࠧ࠭ࣛ") %version, l1ll111Created_By_Mucky_Duck):
			l11ll1lCreated_By_Mucky_Duck.log(l11l11Created_By_Mucky_Duck (u"ࠧࡗࡧࡵࡷ࡮ࡵ࡮ࠡࡅ࡫ࡩࡨࡱࠠࡐࡍࠪࣜ"))
		else:
			l11lllCreated_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"࡙ࠣࡵࡳࡳ࡭ࠠࡗࡧࡵࡷ࡮ࡵ࡮ࠡࡑࡩࠤࡒࡻࡣ࡬ࡻࡶࠤࡈࡵ࡭࡮ࡱࡱࠤࡒࡵࡤࡶ࡮ࡨࠦࣝ")
			l1l111Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"ࠤࡓࡰࡪࡧࡳࡦࠢࡌࡲࡸࡺࡡ࡭࡮ࠣࡇࡴࡸࡲࡦࡥࡷࠤ࡛࡫ࡲࡴ࡫ࡲࡲࠥࡌࡲࡰ࡯ࠣࡘ࡭࡫ࠠࡓࡧࡳࡳࠧࣞ")
			l1l11lCreated_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"ࠥࡄࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟࡫ࡸࡹࡶ࠺࠰࠱ࡰࡹࡨࡱࡹࡴ࠰ࡰࡩࡩ࡯ࡡࡱࡱࡵࡸࡦࡲ࠴࡬ࡱࡧ࡭࠳ࡳ࡬࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤࣟ")
			l11ll1lCreated_By_Mucky_Duck.show_ok_dialog([l11lllCreated_By_Mucky_Duck, l1l111Created_By_Mucky_Duck, l1l11lCreated_By_Mucky_Duck], l1lll1lCreated_By_Mucky_Duck)
			xbmc.executebuiltin(l11l11Created_By_Mucky_Duck (u"ࠦ࡝ࡈࡍࡄ࠰ࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡛ࡰࡥࡣࡷࡩ࠭ࡶࡡࡵࡪ࠯ࡶࡪࡶ࡬ࡢࡥࡨ࠭ࠧ࣠"))
			xbmc.executebuiltin(l11l11Created_By_Mucky_Duck (u"ࠧ࡞ࡂࡎࡅ࠱ࡅࡨࡺࡩࡷࡣࡷࡩ࡜࡯࡮ࡥࡱࡺࠬࡍࡵ࡭ࡦࠫࠥ࣡"))
def l11l11lCreated_By_Mucky_Duck(title,url,l1l1l1Created_By_Mucky_Duck,content):
	if l1l1l1Created_By_Mucky_Duck == None:
		l1l1l1Created_By_Mucky_Duck = l1111lCreated_By_Mucky_Duck
	link = open_url(url).content
	match=re.compile(l11l11Created_By_Mucky_Duck (u"࠭ࡨࡳࡧࡩࡁࠧ࠮࡛࡟ࠤࡠ࠮࠮ࠨ࠾࠽࠰࠭ࡃࡨࡲࡡࡴࡵࡀࠦࡪࡶࡩࡴࡱࡧࡩࠧ࠴ࠪࡀࡀࠫ࡟ࡣࡂ࠾࡞ࠬࠬࡀ࠴࠭࣢")).findall(link)
	items = len(match)
	for url,name in match:
		data = name.split(l11l11Created_By_Mucky_Duck (u"ࠧ࠮ࣣࠩ"))
		l111llCreated_By_Mucky_Duck = data[0].replace(l11l11Created_By_Mucky_Duck (u"ࠨࡕࠪࣤ"),l11l11Created_By_Mucky_Duck (u"ࠩࠪࣥ")).replace(l11l11Created_By_Mucky_Duck (u"ࠪࡷࣦࠬ"),l11l11Created_By_Mucky_Duck (u"ࠫࠬࣧ"))
		l11lll1Created_By_Mucky_Duck = data[1].replace(l11l11Created_By_Mucky_Duck (u"ࠬࡋࠧࣨ"),l11l11Created_By_Mucky_Duck (u"ࣩ࠭ࠧ")).replace(l11l11Created_By_Mucky_Duck (u"ࠧࡦࠩ࣪"),l11l11Created_By_Mucky_Duck (u"ࠨࠩ࣫"))
		try:
			l11lll1Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.split(l11l11Created_By_Mucky_Duck (u"ࠩ࠯ࠫ࣬"))[0]
		except:
			pass
		fan_art = {l11l11Created_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨ࣭"):l1l1l1Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷ࣮ࠫ"):l11Created_By_Mucky_Duck+l11l11Created_By_Mucky_Duck (u"ࠬࡳ࠴ࡶ࠰࡭ࡴ࡬࣯࠭")}
		md.addDir({l11l11Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࣰࠫ"): l11l11Created_By_Mucky_Duck (u"ࠧ࠸ࣱࠩ"), l11l11Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪࣲ࠭"):l11l11Created_By_Mucky_Duck (u"ࠩ࡞ࡍࡢࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡦࡲࡨ࡬࡫ࡲࡣ࡮ࡸࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࡡ࠯ࡊ࡟ࠪࣳ") %name,
			   l11l11Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࣴ"):url, l11l11Created_By_Mucky_Duck (u"ࠫ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫ࠧࣵ"):l1l1l1Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹࣶ࠭"):l11l11Created_By_Mucky_Duck (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࡳࠨࣷ")},
			  {l11l11Created_By_Mucky_Duck (u"ࠧࡴࡱࡵࡸࡹ࡯ࡴ࡭ࡧࠪࣸ"):title, l11l11Created_By_Mucky_Duck (u"ࠨࡵࡨࡥࡸࡵ࡮ࠨࣹ"):l111llCreated_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࣺࠪ"):l11lll1Created_By_Mucky_Duck},
			  fan_art, is_folder=False, item_count=items)
	setView(l11ll11Created_By_Mucky_Duck,l11l11Created_By_Mucky_Duck (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࡷࠬࣻ"), l11l11Created_By_Mucky_Duck (u"ࠫࡪࡶࡩ࠮ࡸ࡬ࡩࡼ࠭ࣼ"))
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
def l11111lCreated_By_Mucky_Duck(url,content):
	link = open_url(url).text
	if content == l11l11Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࣽ"):
		match=re.compile(l11l11Created_By_Mucky_Duck (u"࠭࠼࡭࡫ࡁࠤࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯ࠬࡂ࠭ࠧࠦࡴࡪࡶ࡯ࡩࡂࠨࡁ࡭࡮ࠣࡱࡴࡼࡩࡦࡵ࠱࠮ࡄࠨ࠾ࠩ࠰࠭ࡃ࠮ࡂ࠯ࡢࡀ࠿࠳ࡱ࡯࠾ࠨࣾ")).findall(link)
		for url,name in match:
			if l11l11Created_By_Mucky_Duck (u"ࠧ࠰࡯ࡲࡺ࡮࡫࠭ࠨࣿ") in url:
				md.addDir({l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ऀ"): l11l11Created_By_Mucky_Duck (u"ࠩ࠶ࠫँ"), l11l11Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨं"):l11l11Created_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧः") %name, l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩऄ"):url,
					   l11l11Created_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧअ"):l11l11Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧआ")})
	elif content == l11l11Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩइ"):
		match=re.compile(l11l11Created_By_Mucky_Duck (u"ࠩ࠿ࡰ࡮ࡄࠠ࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࠫ࠲࠯ࡅࠩࠣࠢࡷ࡭ࡹࡲࡥ࠾ࠤࡄࡰࡱࠦࡔࡗࡵ࡫ࡳࡼ࠴ࠪࡀࠤࡁࠬ࠳࠰࠿ࠪ࠾࠲ࡥࡃࡂ࠯࡭࡫ࡁࠫई")).findall(link)
		for url,name in match:
			if l11l11Created_By_Mucky_Duck (u"ࠪ࠳ࡹࡼࡳࡩࡱࡺ࠱ࠬउ") in url:
				md.addDir({l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩऊ"): l11l11Created_By_Mucky_Duck (u"ࠬ࠹ࠧऋ"), l11l11Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫऌ"):l11l11Created_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪऍ") %name, l11l11Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬऎ"):url,
					   l11l11Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪए"):l11l11Created_By_Mucky_Duck (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫऐ")})
	setView(l11ll11Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪऑ"), l11l11Created_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨऒ"))
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
def l111lCreated_By_Mucky_Duck():
	l1l1l1lCreated_By_Mucky_Duck = xbmc.translatePath(l11l11Created_By_Mucky_Duck (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹ࠯ࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼ࠲ࡲࡧࡦࠨओ"))
	l1l1lllCreated_By_Mucky_Duck = xbmc.translatePath(l11l11Created_By_Mucky_Duck (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡳࡰࡺ࡭ࡩ࡯࠰ࡳࡶࡴ࡭ࡲࡢ࡯࠱ࡱࡦ࡬ࡷࡪࡼࡤࡶࡩ࠭औ"))
	l11l111Created_By_Mucky_Duck = xbmc.translatePath(l11l11Created_By_Mucky_Duck (u"ࠨࡵࡳࡩࡨ࡯ࡡ࡭࠼࠲࠳࡭ࡵ࡭ࡦ࠱ࡤࡨࡩࡵ࡮ࡴ࠱ࡳࡰࡺ࡭ࡩ࡯࠰ࡹ࡭ࡩ࡫࡯࠯࡭ࡵࡥࡹࡵࡳࠨक"))
	if os.path.exists(l1l1l1lCreated_By_Mucky_Duck):
		l11lllCreated_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"ࠩ࡜ࡳࡺࠦࡈࡢࡸࡨࠤࡎࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡇࡴࡲࡱࠥࡇ࡮ࠨख")
		l1l111Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"࡙ࠪࡳࡵࡦࡧ࡫ࡦ࡭ࡦࡲࠠࡔࡱࡸࡶࡨ࡫࡚ࠠࠧࠢ࡭ࡱࡲࠠࡏࡱࡺࠤࡉ࡫࡬ࡦࡶࡨࠤࡕࡲࡥࡢࡵࡨࠫग")
		l1l11lCreated_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"ࠫࡎࡴࡳࡵࡣ࡯ࡰࠥࡆ࡛ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡ࡭ࡺࡴࡱ࠼࠲࠳ࡲࡻࡣ࡬ࡻࡶ࠲ࡲ࡫ࡤࡪࡣࡳࡳࡷࡺࡡ࡭࠶࡮ࡳࡩ࡯࠮࡮࡮࡞࠳ࡈࡕࡌࡐࡔࡠࠫघ")
		l1lCreated_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"ࠬࡘࡥ࡮ࡱࡹࡩࡩࠦࡁ࡯ࡱࡱࡽࡲࡵࡵࡴࠢࡕࡩࡵࡵࠠࡂࡰࡧࠤࡆࡪࡤࡰࡰࡶࠫङ")
		l1l1llCreated_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡖ࡬ࡦࡣࡶࡩࠥࡊ࡯࡯ࡶࠣࡗࡺࡶࡰࡰࡴࡷࠤࡎࡪࡩࡰࡶࡶࠫच")
		l11ll1lCreated_By_Mucky_Duck.show_ok_dialog([l11lllCreated_By_Mucky_Duck, l1l111Created_By_Mucky_Duck, l1l11lCreated_By_Mucky_Duck], l1lll1lCreated_By_Mucky_Duck)
		l1l1Created_By_Mucky_Duck = l11ll1lCreated_By_Mucky_Duck.get_path()
		shutil.rmtree(l1l1Created_By_Mucky_Duck, ignore_errors=True)
		shutil.rmtree(l1l1l1lCreated_By_Mucky_Duck, ignore_errors=True)
		shutil.rmtree(l1l1lllCreated_By_Mucky_Duck, ignore_errors=True)
		shutil.rmtree(l11l111Created_By_Mucky_Duck, ignore_errors=True)
		l11ll1lCreated_By_Mucky_Duck.log(l11l11Created_By_Mucky_Duck (u"ࠧ࠾࠿ࡀࡈࡊࡒࡅࡕࡋࡑࡋࡂࡃ࠽ࡂࡐࡒࡒ࡞ࡓࡏࡖࡕࡀࡁࡂࡇࡄࡅࡑࡑࡗࡂࡃ࠽ࠬ࠿ࡀࡁࡗࡋࡐࡐ࠿ࡀࡁࠬछ"))
		l11ll1lCreated_By_Mucky_Duck.show_ok_dialog([l1lCreated_By_Mucky_Duck, l1l1llCreated_By_Mucky_Duck], l1lll1lCreated_By_Mucky_Duck)
		time.sleep(2)
		os._exit(0)
def l11llllCreated_By_Mucky_Duck(url,content):
	link = open_url(url).text
	match=re.compile(l11l11Created_By_Mucky_Duck (u"ࠨ࠾࡯࡭ࡃࠦ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠮ࡄ࠯ࠢࠡࡶ࡬ࡸࡱ࡫࠽ࠣࡃ࡯ࡰࠥࡳ࡯ࡷ࡫ࡨࡷ࠳࠰࠿ࠣࡀࠫ࠲࠯ࡅࠩ࠽࠱ࡤࡂࡁ࠵࡬ࡪࡀࠪज")).findall(link)
	for url,name in match:
		if l11l11Created_By_Mucky_Duck (u"ࠩ࠲ࡽࡪࡧࡲ࠮ࠩझ") in url:
			md.addDir({l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨञ"): l11l11Created_By_Mucky_Duck (u"ࠫ࠸࠭ट"), l11l11Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪठ"):l11l11Created_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩड") %name, l11l11Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫढ"):url,
					   l11l11Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩण"):l11l11Created_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩत")})
	setView(l11ll11Created_By_Mucky_Duck, l11l11Created_By_Mucky_Duck (u"ࠪࡪ࡮ࡲࡥࡴࠩथ"), l11l11Created_By_Mucky_Duck (u"ࠫࡲ࡫࡮ࡶ࠯ࡹ࡭ࡪࡽࠧद"))
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
def l1llllCreated_By_Mucky_Duck(content, query):
	try:
		if query:
			search = query.replace(l11l11Created_By_Mucky_Duck (u"ࠬࠦࠧध"),l11l11Created_By_Mucky_Duck (u"࠭࠭ࠨन"))
		else:
			search = md.search(l11l11Created_By_Mucky_Duck (u"ࠧ࠮ࠩऩ"))
			if search == l11l11Created_By_Mucky_Duck (u"ࠨࠩप"):
				md.notification(l11l11Created_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝࡜ࡄࡠࡉࡒࡖࡔ࡚ࠢࡔ࡙ࡊࡘ࡙࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠲ࡁࡣࡱࡵࡸ࡮ࡴࡧࠡࡵࡨࡥࡷࡩࡨࠨफ"),l1111lCreated_By_Mucky_Duck)
				return
			else:
				pass
		if content == l11l11Created_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪब"):
			url = l11l11Created_By_Mucky_Duck (u"ࠫࠪࡹ࠯ࡵࡣࡪ࠳ࠪࡹࠧभ") %(l1llCreated_By_Mucky_Duck,search)
		elif content == l11l11Created_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭म"):
			url = l11l11Created_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡷࡥ࡬ࡺࡶࡴ࠱ࠨࡷࠬय") %(l1llCreated_By_Mucky_Duck,search)
		l1Created_By_Mucky_Duck(url,content)
	except:
		md.notification(l11l11Created_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡡࡂ࡞ࡕࡲࡶࡷࡿࠠࡏࡱࠣࡖࡪࡹࡵ࡭ࡶࡶ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩर"),l1111lCreated_By_Mucky_Duck)
def l1lll11Created_By_Mucky_Duck(url,name,content,fan_art,l11l1llCreated_By_Mucky_Duck):
	link = open_url(url).content
	if content == l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨऱ"):
		request_url = re.findall(l11l11Created_By_Mucky_Duck (u"ࡴࠪ࡬ࡷ࡫ࡦ࠾ࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࡂ࡜ࡧࡴࡤࡪࠪल"), str(link), re.I|re.DOTALL)[0]
		link = open_url(request_url).content
		l1l111lCreated_By_Mucky_Duck = request_url
	else:
		l1l111lCreated_By_Mucky_Duck = url
	value = []
	l11l1Created_By_Mucky_Duck = []
	l11111Created_By_Mucky_Duck= l11l11Created_By_Mucky_Duck (u"ࠪࠫळ")
	match = re.findall(l11l11Created_By_Mucky_Duck (u"ࡶࠬࠨࡦࡪ࡮ࡨࠦ࠿ࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢ࠯ࠬࡂࠦࡱࡧࡢࡦ࡮ࠥ࠾ࠧ࠮࡛࡟ࠤࡠ࠯࠮ࠨࠧऴ"), str(link), re.I|re.DOTALL)
	for url,l11ll1Created_By_Mucky_Duck in match:
		value.append(int(re.sub(l11l11Created_By_Mucky_Duck (u"ࠬࡢࡄࠨव"), l11l11Created_By_Mucky_Duck (u"࠭ࠧश"), l11ll1Created_By_Mucky_Duck)))
		l11l1Created_By_Mucky_Duck.append(url)
	try:
		l11111Created_By_Mucky_Duck =  l11l1Created_By_Mucky_Duck[md.get_max_value_index(value)[0]]
	except:
		pass
	if not l11111Created_By_Mucky_Duck:
                l1l11llCreated_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡥ࡯ࡧࡸ࠮ࡶࡲ࡯ࡪࡴ࠮ࡱࡪࡳࠫष") %l1llCreated_By_Mucky_Duck
		link = link.replace(l11l11Created_By_Mucky_Duck (u"ࠨࠢࠪस"),l11l11Created_By_Mucky_Duck (u"ࠩࠪह"))
		try:
			params = {l11l11Created_By_Mucky_Duck (u"ࠪࡸࡰ࠭ऺ"):l11l11Created_By_Mucky_Duck (u"ࠫࡲ࠺ࡵࡧࡴࡨࡩ࡮ࡹࡴࡩࡧࡥࡩࡸࡺࠧऻ"), l11l11Created_By_Mucky_Duck (u"ࠬࡼ़ࠧ"):re.findall(l11l11Created_By_Mucky_Duck (u"ࡸࠧ࡭࡫ࡱ࡯ࡂࠨࠨ࡜ࡠࠥࡡ࠯࠯ࠢ࠿ࡕࡨࡶࡻ࡫ࡲ࠱࠾࠲ࡷࡵࡧ࡮࠿ࠩऽ"), str(link), re.I|re.DOTALL)[0]}
			l1ll11lCreated_By_Mucky_Duck = open_url(l1l11llCreated_By_Mucky_Duck, params=params).content
			l1ll11lCreated_By_Mucky_Duck = l1ll11lCreated_By_Mucky_Duck.replace(l11l11Created_By_Mucky_Duck (u"ࠧࠡࠩा"),l11l11Created_By_Mucky_Duck (u"ࠨࠩि"))
			try:
				data = re.findall(l11l11Created_By_Mucky_Duck (u"ࡴࠪࡷࡴࡻࡲࡤࡧࡶ࠾ࡡࡡࠨ࠯ࠬࡂ࠭ࡡࡣࠧी"), str(l1ll11lCreated_By_Mucky_Duck), re.I|re.DOTALL)[0]
				match = re.findall(l11l11Created_By_Mucky_Duck (u"ࡵࠫ࡫࡯࡬ࡦ࠰࠭ࡃ࠿ࠨࠨ࡜ࡠࠥࡡ࠯࠯ࠢࠨु"), str(data), re.I|re.DOTALL)
				l1ll1llCreated_By_Mucky_Duck = re.findall(l11l11Created_By_Mucky_Duck (u"ࡶࠬࡲࡡࡣࡧ࡯ࠦ࠿࠮࠮ࠫࡁࠬ࠰ࠬू"), str(data), re.I|re.DOTALL)
				for url in match:
					l11l1Created_By_Mucky_Duck.append(url)
				for l11ll1Created_By_Mucky_Duck in l1ll1llCreated_By_Mucky_Duck:
					value.append(int(re.sub(l11l11Created_By_Mucky_Duck (u"ࠬࡢࡄࠨृ"), l11l11Created_By_Mucky_Duck (u"࠭ࠧॄ"), l11ll1Created_By_Mucky_Duck)))
				try:
					l11111Created_By_Mucky_Duck =  l11l1Created_By_Mucky_Duck[md.get_max_value_index(value)[0]]
				except:
					try:
						l11111Created_By_Mucky_Duck = match[-1]
					except:
						l11111Created_By_Mucky_Duck = match[0]
			except:
				l11111Created_By_Mucky_Duck = re.findall(l11l11Created_By_Mucky_Duck (u"ࡲࠨࡵࡲࡹࡷࡩࡥ࠯ࠬࡂࡷࡷࡩ࠽ࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪॅ"), str(l1ll11lCreated_By_Mucky_Duck), re.I|re.DOTALL)[0]
		except:
			params = {l11l11Created_By_Mucky_Duck (u"ࠨࡶ࡮ࠫॆ"):l11l11Created_By_Mucky_Duck (u"ࠩࡰ࠸ࡺ࡬ࡲࡦࡧ࡬ࡷࡹ࡮ࡥࡣࡧࡶࡸࠬे"), l11l11Created_By_Mucky_Duck (u"ࠪࡺࠬै"):re.findall(l11l11Created_By_Mucky_Duck (u"ࡶࠬࡲࡩ࡯࡭ࡀࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧࡄࡓࡦࡴࡹࡩࡷ࠷࠼࠰ࡵࡳࡥࡳࡄࠧॉ"), str(link), re.I|re.DOTALL)[0]}
			l1ll11lCreated_By_Mucky_Duck = open_url(l1l11llCreated_By_Mucky_Duck, params=params).content
			l1ll11lCreated_By_Mucky_Duck = l1ll11lCreated_By_Mucky_Duck.replace(l11l11Created_By_Mucky_Duck (u"ࠬࠦࠧॊ"),l11l11Created_By_Mucky_Duck (u"࠭ࠧो"))
			try:
				data = re.findall(l11l11Created_By_Mucky_Duck (u"ࡲࠨࡵࡲࡹࡷࡩࡥࡴ࠼࡟࡟࠭࠴ࠪࡀࠫ࡟ࡡࠬौ"), str(l1ll11lCreated_By_Mucky_Duck), re.I|re.DOTALL)[0].replace(l11l11Created_By_Mucky_Duck (u"ࠨ्ࠢࠪ"),l11l11Created_By_Mucky_Duck (u"ࠩࠪॎ"))
				match = re.findall(l11l11Created_By_Mucky_Duck (u"ࡵࠫ࡫࡯࡬ࡦࠤ࠽ࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧ࠭ॏ"), str(data), re.I|re.DOTALL)
				l1ll1llCreated_By_Mucky_Duck = re.findall(l11l11Created_By_Mucky_Duck (u"ࡶࠬࡲࡡࡣࡧ࡯ࠦ࠿࠮࠮ࠫࡁࠬ࠰ࠬॐ"), str(data), re.I|re.DOTALL)
				for url in match:
					l11l1Created_By_Mucky_Duck.append(url)
				for l11ll1Created_By_Mucky_Duck in l1ll1llCreated_By_Mucky_Duck:
					value.append(int(re.sub(l11l11Created_By_Mucky_Duck (u"ࠬࡢࡄࠨ॑"), l11l11Created_By_Mucky_Duck (u"॒࠭ࠧ"), l11ll1Created_By_Mucky_Duck)))
				try:
					l11111Created_By_Mucky_Duck =  l11l1Created_By_Mucky_Duck[md.get_max_value_index(value)[0]]
				except:
					try:
						l11111Created_By_Mucky_Duck = match[-1]
					except:
						l11111Created_By_Mucky_Duck = match[0]
			except:
				l11111Created_By_Mucky_Duck = re.findall(l11l11Created_By_Mucky_Duck (u"ࡲࠨࡵࡲࡹࡷࡩࡥ࠯ࠬࡂࡷࡷࡩ࠽ࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪ॓"), str(l1ll11lCreated_By_Mucky_Duck), re.I|re.DOTALL)[0]
	if l11l11Created_By_Mucky_Duck (u"ࠨࡩࡲࡳ࡬ࡲࡥࠨ॔") in l11111Created_By_Mucky_Duck or l11l11Created_By_Mucky_Duck (u"ࠩࡸࡷࡪࡸࡣࡥࡰࠪॕ") in l11111Created_By_Mucky_Duck:
		l11111Created_By_Mucky_Duck = l11111Created_By_Mucky_Duck
	else:
		if l1llCreated_By_Mucky_Duck not in l11111Created_By_Mucky_Duck:
			l11111Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࠥࡴࠩॖ") %(l1llCreated_By_Mucky_Duck,l11111Created_By_Mucky_Duck)
	md.resolved(l11111Created_By_Mucky_Duck, name, fan_art, l11l1llCreated_By_Mucky_Duck)
	l11ll1lCreated_By_Mucky_Duck.end_of_directory()
md.check_source()
mode = md.args[l11l11Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩॗ")]
url = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩक़"), None)
name = md.args.get(l11l11Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫख़"), None)
query = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠧࡲࡷࡨࡶࡾ࠭ग़"), None)
title = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠨࡶ࡬ࡸࡱ࡫ࠧज़"), None)
l111llCreated_By_Mucky_Duck = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠩࡶࡩࡦࡹ࡯࡯ࠩड़"), None)
l11lll1Created_By_Mucky_Duck = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࠫढ़") ,None)
l11l1llCreated_By_Mucky_Duck = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠫ࡮ࡴࡦࡰ࡮ࡤࡦࡪࡲࠧफ़"), None)
content = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭य़"), None)
l1l11Created_By_Mucky_Duck = md.args.get(l11l11Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࡣ࡮ࡪࠧॠ"), None)
l1l1l1Created_By_Mucky_Duck = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࠪॡ"), None)
fan_art = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠨࡨࡤࡲࡤࡧࡲࡵࠩॢ"), None)
is_folder = md.args.get(l11l11Created_By_Mucky_Duck (u"ࠩ࡬ࡷࡤ࡬࡯࡭ࡦࡨࡶࠬॣ"), True)
if mode is None or url is None or len(url)<1:
	l111111Created_By_Mucky_Duck()
elif mode == l11l11Created_By_Mucky_Duck (u"ࠪ࠵ࠬ।"):
	l111l1lCreated_By_Mucky_Duck()
elif mode == l11l11Created_By_Mucky_Duck (u"ࠫ࠷࠭॥"):
	l111l11Created_By_Mucky_Duck()
elif mode == l11l11Created_By_Mucky_Duck (u"ࠬ࠹ࠧ०"):
	l1Created_By_Mucky_Duck(url,content)
elif mode == l11l11Created_By_Mucky_Duck (u"࠭࠴ࠨ१"):
	l11111lCreated_By_Mucky_Duck(url,content)
elif mode == l11l11Created_By_Mucky_Duck (u"ࠧ࠶ࠩ२"):
	l11llllCreated_By_Mucky_Duck(url,content)
elif mode == l11l11Created_By_Mucky_Duck (u"ࠨ࠸ࠪ३"):
	l11l11lCreated_By_Mucky_Duck(title,url,l1l1l1Created_By_Mucky_Duck,content)
elif mode == l11l11Created_By_Mucky_Duck (u"ࠩ࠺ࠫ४"):
	l1lll11Created_By_Mucky_Duck(url,name,content,fan_art,l11l1llCreated_By_Mucky_Duck)
elif mode == l11l11Created_By_Mucky_Duck (u"ࠪࡷࡪࡧࡲࡤࡪࠪ५"):
	l1llllCreated_By_Mucky_Duck(content,query)
elif mode == l11l11Created_By_Mucky_Duck (u"ࠫࡦࡪࡤࡰࡰࡢࡷࡪࡧࡲࡤࡪࠪ६"):
	md.addon_search(content,query,fan_art,l11l1llCreated_By_Mucky_Duck)
elif mode == l11l11Created_By_Mucky_Duck (u"ࠬࡧࡤࡥࡡࡵࡩࡲࡵࡶࡦࡡࡩࡥࡻ࠭७"):
	md.add_remove_fav(name, url, l11l1llCreated_By_Mucky_Duck, fan_art,
			  content, l1l11Created_By_Mucky_Duck, is_folder)
elif mode == l11l11Created_By_Mucky_Duck (u"࠭ࡦࡦࡶࡦ࡬ࡤ࡬ࡡࡷࡵࠪ८"):
	md.fetch_favs(l1llCreated_By_Mucky_Duck)
elif mode == l11l11Created_By_Mucky_Duck (u"ࠧࡢࡦࡧࡳࡳࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ९"):
	l11ll1lCreated_By_Mucky_Duck.show_settings()
elif mode == l11l11Created_By_Mucky_Duck (u"ࠨ࡯ࡨࡸࡦࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ॰"):
	import metahandler
	metahandler.display_settings()
l11ll1lCreated_By_Mucky_Duck.end_of_directory()