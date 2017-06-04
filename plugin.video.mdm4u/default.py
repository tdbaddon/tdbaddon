# -*- coding: utf-8 -*-
import sys
l111ll1Created_By_Mucky_Duck = sys.version_info [0] == 2
l111111Created_By_Mucky_Duck = 2048
l1llllCreated_By_Mucky_Duck = 7
def l111l1Created_By_Mucky_Duck (llCreated_By_Mucky_Duck):
    global l111Created_By_Mucky_Duck
    l111l11Created_By_Mucky_Duck = ord (llCreated_By_Mucky_Duck [-1])
    l1lll11Created_By_Mucky_Duck = llCreated_By_Mucky_Duck [:-1]
    l1lllCreated_By_Mucky_Duck = l111l11Created_By_Mucky_Duck % len (l1lll11Created_By_Mucky_Duck)
    l1ll1Created_By_Mucky_Duck = l1lll11Created_By_Mucky_Duck [:l1lllCreated_By_Mucky_Duck] + l1lll11Created_By_Mucky_Duck [l1lllCreated_By_Mucky_Duck:]
    if l111ll1Created_By_Mucky_Duck:
        l1l11l1Created_By_Mucky_Duck = unicode () .join ([unichr (ord (char) - l111111Created_By_Mucky_Duck - (l111llCreated_By_Mucky_Duck + l111l11Created_By_Mucky_Duck) % l1llllCreated_By_Mucky_Duck) for l111llCreated_By_Mucky_Duck, char in enumerate (l1ll1Created_By_Mucky_Duck)])
    else:
        l1l11l1Created_By_Mucky_Duck = str () .join ([chr (ord (char) - l111111Created_By_Mucky_Duck - (l111llCreated_By_Mucky_Duck + l111l11Created_By_Mucky_Duck) % l1llllCreated_By_Mucky_Duck) for l111llCreated_By_Mucky_Duck, char in enumerate (l1ll1Created_By_Mucky_Duck)])
    return eval (l1l11l1Created_By_Mucky_Duck)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import os,re,shutil,sys,urllib
# M4U Add-on Created By Mucky Duck (3/2016)
l11l111Created_By_Mucky_Duck = xbmcaddon.Addon().getAddonInfo(l111l1Created_By_Mucky_Duck (u"ࠫ࡮ࡪࠧࠀ"))
l11l11lCreated_By_Mucky_Duck = Addon(l11l111Created_By_Mucky_Duck, sys.argv)
l1ll1l1Created_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_name()
l1llCreated_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_path()
md = md(l11l111Created_By_Mucky_Duck, sys.argv)
l1ll11Created_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࠪࠁ"))
l11ll1lCreated_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥࡳࡩࡱࡺࡷࠬࠂ"))
l1l11Created_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠧࡦࡰࡤࡦࡱ࡫࡟࡮ࡱࡹ࡭ࡪࡹࠧࠃ"))
l1l1lCreated_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠨࡧࡱࡥࡧࡲࡥࡠࡨࡤࡺࡸ࠭ࠄ"))
l11l1Created_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠩࡤࡨࡩࡥࡳࡦࡶࠪࠅ"))
l1lll1llCreated_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠪࡩࡳࡧࡢ࡭ࡧࡢࡱࡪࡺࡡࡠࡵࡨࡸࠬࠆ"))
l11Created_By_Mucky_Duck = md.get_art()
l1llll1Created_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_icon()
l1l1llCreated_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_fanart()
l1l111lCreated_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠫࡧࡧࡳࡦࡡࡸࡶࡱ࠭ࠇ"))
reload(sys)
sys.setdefaultencoding(l111l1Created_By_Mucky_Duck (u"ࠧࡻࡴࡧ࠯࠻ࠦࠈ"))
def l1llll11Created_By_Mucky_Duck():
	if l11ll1lCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠉ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࠊ"): l111l1Created_By_Mucky_Duck (u"ࠨ࠴ࠪࠋ"), l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠌ"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢ࡚ࡖ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࠍ"), l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠎ"):l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠏ")})
	if l1l11Created_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠐ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࠑ"): l111l1Created_By_Mucky_Duck (u"ࠨ࠳ࠪࠒ"), l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠓ"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡓࡏࡗࡋࡈࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࠔ"), l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠕ"):l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠖ")})
	if l1l1lCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠗ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬ࠘"): l111l1Created_By_Mucky_Duck (u"ࠨࡨࡨࡸࡨ࡮࡟ࡧࡣࡹࡷࠬ࠙"), l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠚ"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡓ࡙ࠡࡈࡄ࡚ࡔ࡛ࡒࡊࡖࡈࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࠛ"), l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠜ"):l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠝ")})
	if l1ll11Created_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠞ"):
		if l1lll1llCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬࠟ"):
			md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠠ"):l111l1Created_By_Mucky_Duck (u"ࠩࡰࡩࡹࡧ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠩࠡ"), l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠢ"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡍࡆࡖࡄࠤࡘࡋࡔࡕࡋࡑࡋࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࠣ"), l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠤ"):l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠥ")}, is_folder=False, is_playable=False)
	if l11l1Created_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬࠦ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠧ"):l111l1Created_By_Mucky_Duck (u"ࠩࡤࡨࡩࡵ࡮ࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠪࠨ"), l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠩ"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡁࡅࡆࡒࡒ࡙ࠥࡅࡕࡖࡌࡒࡌ࡙࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࠪ"), l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠫ"):l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠬ")}, is_folder=False, is_playable=False)
	l1111Created_By_Mucky_Duck()
	l1111llCreated_By_Mucky_Duck()
	setView(l11l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭࠭"), l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫ࠮"))
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
def l1111l1Created_By_Mucky_Duck():
	if l1l1lCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠩࡷࡶࡺ࡫ࠧ࠯"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ࠰"): l111l1Created_By_Mucky_Duck (u"ࠫ࡫࡫ࡴࡤࡪࡢࡪࡦࡼࡳࠨ࠱"), l111l1Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ࠲"):l111l1Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡏ࡜ࠤࡋࡇࡖࡐࡗࡕࡍ࡙ࡋࡓ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭࠳"), l111l1Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࠴"):l111l1Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࠵")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ࠶"): l111l1Created_By_Mucky_Duck (u"ࠪ࠷ࠬ࠷"), l111l1Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ࠸"):l111l1Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡍࡃࡗࡉࡘ࡚ࠠࡂࡆࡇࡉࡉࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫ࠹"), l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࠺"):l1l111lCreated_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠧ࠰ࡰࡨࡻࡦࡪࡤࠨ࠻"), l111l1Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ࠼"):l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩ࠽")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ࠾"): l111l1Created_By_Mucky_Duck (u"ࠫ࠸࠭࠿"), l111l1Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࡀ"):l111l1Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡏࡒࡗ࡙ࠦࡖࡊࡇ࡚ࡉࡉࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡁ"), l111l1Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࡂ"):l1l111lCreated_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠨ࠱ࡷࡳࡵ࠳ࡶࡪࡧࡺࠫࡃ"), l111l1Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࡄ"):l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪࡅ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡆ"): l111l1Created_By_Mucky_Duck (u"ࠬ࠹ࠧࡇ"), l111l1Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡈ"):l111l1Created_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣ࡛ࡃ࡟ࡋࡓ࡙ࠦࡍࡐࡘࡌࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡉ"), l111l1Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡊ"):l1l111lCreated_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠩ࠲࡬ࡴࡺ࠭࡮ࡱࡹ࡭ࡪ࠳࠱࠯ࡪࡷࡱࡱ࠭ࡋ"), l111l1Created_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࡌ"):l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶࠫࡍ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪࡎ"): l111l1Created_By_Mucky_Duck (u"࠭ࡳࡦࡣࡵࡧ࡭࠭ࡏ"), l111l1Created_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬࡐ"):l111l1Created_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝࡜ࡄࡠࡗࡊࡇࡒࡄࡊ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨࡑ"), l111l1Created_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ࡒ"):l111l1Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࡓ"), l111l1Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࡔ"):l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࡕ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࡖ"): l111l1Created_By_Mucky_Duck (u"ࠧ࠵ࠩࡗ"), l111l1Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࡘ"):l111l1Created_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞࡝ࡅࡡࡌࡋࡎࡓࡇ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࡙"), l111l1Created_By_Mucky_Duck (u"ࠪࡹࡷࡲ࡚ࠧ"):l1l111lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸ࡛ࠬ"):l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬ࡜")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫ࡝"): l111l1Created_By_Mucky_Duck (u"ࠧ࠶ࠩ࡞"), l111l1Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭࡟"):l111l1Created_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞࡝ࡅࡡ࡞ࡋࡁࡓ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧࡠ"), l111l1Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࡡ"):l1l111lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࡢ"):l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࡣ")})
	setView(l11l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࡷࠬࡤ"), l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪࡥ"))
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
def l11111lCreated_By_Mucky_Duck():
	if l1l1lCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭ࡦ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࡧ"): l111l1Created_By_Mucky_Duck (u"ࠪࡪࡪࡺࡣࡩࡡࡩࡥࡻࡹࠧࡨ"), l111l1Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࡩ"):l111l1Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡎ࡛ࠣࡊࡆ࡜ࡏࡖࡔࡌࡘࡊ࡙࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࡪ"), l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࡫"):l111l1Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࡬")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭࡭"): l111l1Created_By_Mucky_Duck (u"ࠩ࠶ࠫ࡮"), l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ࡯"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡌࡂࡖࡈࡗ࡙ࠦࡁࡅࡆࡈࡈࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࡰ"), l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡱ"):l1l111lCreated_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"࠭࠯࡭ࡣࡷࡩࡸࡺ࠭ࡵࡸࡶ࡬ࡴࡽࠧࡲ"), l111l1Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡳ"):l111l1Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࡴ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࡵ"): l111l1Created_By_Mucky_Duck (u"ࠪ࠷ࠬࡶ"), l111l1Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࡷ"):l111l1Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡎࡑࡖࡘࠥ࡜ࡉࡆ࡙ࡈࡈࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࡸ"), l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࡹ"):l1l111lCreated_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠧ࠰ࡶࡲࡴ࠲ࡼࡩࡦࡹ࠰ࡸࡻࡹࡨࡰࡹࠪࡺ"), l111l1Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࡻ"):l111l1Created_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࡼ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࡽ"): l111l1Created_By_Mucky_Duck (u"ࠫࡸ࡫ࡡࡳࡥ࡫ࠫࡾ"), l111l1Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࡿ"):l111l1Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡕࡈࡅࡗࡉࡈ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࢀ"), l111l1Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࢁ"):l1l111lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࢂ"):l111l1Created_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࢃ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࢄ"): l111l1Created_By_Mucky_Duck (u"ࠫ࠸࠭ࢅ"), l111l1Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࢆ"):l111l1Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡃࡏࡐࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࢇ"), l111l1Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࢈"):l1l111lCreated_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠨ࠱ࡷࡺࡸ࡮࡯ࡸࠩࢉ"), l111l1Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࢊ"):l111l1Created_By_Mucky_Duck (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫࢋ")})
	setView(l11l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪࢌ"), l111l1Created_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨࢍ"))
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
def l1Created_By_Mucky_Duck(url,content):
	link = open_url(url).text
	l1l1lllCreated_By_Mucky_Duck = md.regex_get_all(link, l111l1Created_By_Mucky_Duck (u"࠭ࠢࡪࡶࡨࡱࠧ࠭ࢎ"), l111l1Created_By_Mucky_Duck (u"ࠧࡤ࡮ࡨࡥࡷࡀࡢࡰࡶ࡫ࠫ࢏"))
	items = len(l1l1lllCreated_By_Mucky_Duck)
	for a in l1l1lllCreated_By_Mucky_Duck:
		if content == l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨ࢐"):
			name = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠩࡦ࡭ࡹ࡫࠾ࠨ࢑"), l111l1Created_By_Mucky_Duck (u"ࠪࡀࠬ࢒"))
		elif content == l111l1Created_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬ࢓"):
			name = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠬ࡮ࡲࡦࡨࡀ࠲࠯ࡅ࠾ࠨ࢔"), l111l1Created_By_Mucky_Duck (u"࠭࠼ࠨ࢕"))
		name = l11l11lCreated_By_Mucky_Duck.unescape(name)
		name = name.encode(l111l1Created_By_Mucky_Duck (u"ࠧࡢࡵࡦ࡭࡮࠭࢖"), l111l1Created_By_Mucky_Duck (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨࢗ")).decode(l111l1Created_By_Mucky_Duck (u"ࠩࡤࡷࡨ࡯ࡩࠨ࢘"))
		l11llllCreated_By_Mucky_Duck = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠪࡧࡱࡧࡳࡴ࠿ࠥ࡬࠸࠳ࡱࡶࡣ࡯࡭ࡹࡿࠢ࠯ࠬࡂࡂ࢙ࠬ"), l111l1Created_By_Mucky_Duck (u"ࠫࡁ࢚࠭"))
		url = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠬ࡮ࡲࡦࡨࡀ࢛ࠦࠬ"), l111l1Created_By_Mucky_Duck (u"࠭ࠢࠨ࢜"))
		l1ll1lCreated_By_Mucky_Duck = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠧࡴࡴࡦࡁࠬ࢝"), l111l1Created_By_Mucky_Duck (u"ࠨࡣ࡯ࡸࡂ࠭࢞")).replace(l111l1Created_By_Mucky_Duck (u"ࠩࠣࠫ࢟"),l111l1Created_By_Mucky_Duck (u"ࠪࠫࢠ"))
		l1l1l11Created_By_Mucky_Duck = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠫࠧ࡮࠴࠮ࡥࡤࡸࠧ࠴ࠪࡀࡀࠪࢡ"), l111l1Created_By_Mucky_Duck (u"ࠬࡂࠧࢢ"))
		if l111l1Created_By_Mucky_Duck (u"࠭࠼ࡢࠢࡷ࡭ࡹࡲࡥࠨࢣ") in l1l1l11Created_By_Mucky_Duck:
			l1l1l11Created_By_Mucky_Duck = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠧࠣࡪ࠷࠱ࡨࡧࡴࠣ࠰࠭ࡃࡃ࠴ࠪࡀ࠾࠱࠮ࡄࡄࠧࢤ"), l111l1Created_By_Mucky_Duck (u"ࠨ࠾ࠪࢥ"))
		fan_art = {l111l1Created_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࠧࢦ"):l1ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪࢧ"):l11Created_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠫࡲ࠺ࡵ࠯࡬ࡳ࡫ࠬࢨ")}
		title = name
		md.remove_punctuation(title)
		if content == l111l1Created_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࢩ"):
			if l111l1Created_By_Mucky_Duck (u"࠭࠭ࡵࡸࡶ࡬ࡴࡽ࠭ࠨࢪ") in url:
				md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࢫ"): l111l1Created_By_Mucky_Duck (u"ࠨ࠸ࠪࢬ"), l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࢭ"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤࡩࡵࡤࡨࡧࡵࡦࡱࡻࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ࢮ") %(name,l1l1l11Created_By_Mucky_Duck), l111l1Created_By_Mucky_Duck (u"ࠫࡹ࡯ࡴ࡭ࡧࠪࢯ"):title,
					   l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࢰ"):url, l111l1Created_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱ࡭ࡲࡧࡧࡦࠩࢱ"):l1ll1lCreated_By_Mucky_Duck ,l111l1Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࢲ"):l111l1Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࢳ")}, {l111l1Created_By_Mucky_Duck (u"ࠩࡶࡳࡷࡺࡴࡪࡶ࡯ࡩࠬࢴ"):title}, fan_art, item_count=items)
		else:
			if l111l1Created_By_Mucky_Duck (u"ࠪ࠱ࡹࡼࡳࡩࡱࡺ࠱ࠬࢵ") not in url:
				md.addDir({l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࢶ"): l111l1Created_By_Mucky_Duck (u"ࠬ࠽ࠧࢷ"), l111l1Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࢸ"):l111l1Created_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡦࡲࡨ࡬࡫ࡲࡣ࡮ࡸࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࢹ") %(name,l11llllCreated_By_Mucky_Duck),
					   l111l1Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࢺ"):url, l111l1Created_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠬࢻ"):l1ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࢼ"):l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶࠫࢽ")}, {l111l1Created_By_Mucky_Duck (u"ࠬࡹ࡯ࡳࡶࡷ࡭ࡹࡲࡥࠨࢾ"):title}, fan_art, is_folder=False, item_count=items)
	try:
		l1ll1llCreated_By_Mucky_Duck = {l111l1Created_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫࢿ"):l11Created_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠧ࡯ࡧࡻࡸ࠳ࡶ࡮ࡨࠩࣀ"), l111l1Created_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨࣁ"):l11Created_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠩࡰ࠸ࡺ࠴ࡪࡱࡩࠪࣂ")}
		l1lllllCreated_By_Mucky_Duck = re.compile(l111l1Created_By_Mucky_Duck (u"ࠥࡀࡦࠦࡩࡥ࠿ࠪࡶ࡮࡭ࡨࡵࠩࠣ࡬ࡷ࡫ࡦ࠾ࠩࠫ࠲࠯ࡅࠩࠨࡀࠣࡀ࡮ࡳࡧࠡࡵࡵࡧࡂ࠭࡮ࡦࡺࡷࡠ࠳ࡶ࡮ࡨࠩࠣࡥࡱࡺ࠽ࠨ࠰࠭ࡃࠬࠦࡷࡪࡦࡷ࡬ࡂ࠭࠵࠱ࠩࡁࡀ࠴ࡧ࠾ࠣࣃ")).findall(link)[0]
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࣄ"): l111l1Created_By_Mucky_Duck (u"ࠬ࠹ࠧࣅ"), l111l1Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࣆ"):l111l1Created_By_Mucky_Duck (u"ࠧ࡜ࡋࡠ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡤࡰࡦࡪࡩࡷࡨ࡬ࡶࡧࡠࡋࡴࠦࡔࡰࠢࡑࡩࡽࡺࠠࡑࡣࡪࡩࡃࡄ࠾࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࡡ࠯ࡊ࡟ࠪࣇ"),
			   l111l1Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࣈ"):l1lllllCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࣉ"):content}, fan_art=l1ll1llCreated_By_Mucky_Duck)
	except:pass
	try:
		l1lllllCreated_By_Mucky_Duck = re.compile(l111l1Created_By_Mucky_Duck (u"ࠪࡀࡦࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡵࡰࡳ࡫ࠥࡨࡴ࡯ࡲࡪ࠱ࡦࡲࡴࠡࡤࡷࡲࡵ࡭࠭ࡧ࡮ࡤࡸࠥࡽࡡࡷࡧࡶ࠱ࡧࡻࡴࡵࡱࡱࠤࡼࡧࡶࡦࡵ࠰ࡩ࡫࡬ࡥࡤࡶࠥࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠰࠿ࠪࠤࡁࠬ࠳࠰࠿ࠪ࠾࠲ࡥࡃ࠴ࠪࡀࠩ࣊")).findall(link)
		for url, name in l1lllllCreated_By_Mucky_Duck:
			md.addDir({l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩ࣋"): l111l1Created_By_Mucky_Duck (u"ࠬ࠹ࠧ࣌"), l111l1Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ࣍"):l111l1Created_By_Mucky_Duck (u"ࠧ࡜ࡋࡠ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡤࡰࡦࡪࡩࡷࡨ࡬ࡶࡧࡠࡔࡦ࡭ࡥࠡࠧࡶࠤࡃࡄ࠾࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࡡ࠯ࡊ࡟ࠪ࣎") %name,
				   l111l1Created_By_Mucky_Duck (u"ࠨࡷࡵࡰ࣏ࠬ"):url, l111l1Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶ࣐ࠪ"):content}, l1ll1llCreated_By_Mucky_Duck)
	except:pass
	if content == l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵ࣑ࠪ"):
		setView(l11l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶ࣒ࠫ"), l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨ࠱ࡻ࡯ࡥࡸ࣓ࠩ"))
	elif content == l111l1Created_By_Mucky_Duck (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹࠧࣔ"):
		setView(l11l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠧࡵࡸࡶ࡬ࡴࡽࡳࠨࣕ"), l111l1Created_By_Mucky_Duck (u"ࠨࡵ࡫ࡳࡼ࠳ࡶࡪࡧࡺࠫࣖ"))
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
def l1111llCreated_By_Mucky_Duck():
	link = open_url(l111l1Created_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡴࡦࡹࡴࡦࡤ࡬ࡲ࠳ࡩ࡯࡮࠱ࡵࡥࡼ࠵ࡃࡧ࠶ࡆ࠷ࡺࡎ࠱ࠨࣗ")).content
	version = re.findall(l111l1Created_By_Mucky_Duck (u"ࡵࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠠࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪࣘ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l111l1Created_By_Mucky_Duck (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷ࠴ࡹࡣࡳ࡫ࡳࡸ࠳ࡳ࡯ࡥࡷ࡯ࡩ࠳ࡳࡵࡤ࡭ࡼࡷ࠳ࡩ࡯࡮࡯ࡲࡲ࠴ࡧࡤࡥࡱࡱ࠲ࡽࡳ࡬ࠨࣙ")), l111l1Created_By_Mucky_Duck (u"ࠬࡸࠫࠨࣚ")) as f:
		l1l11llCreated_By_Mucky_Duck = f.read()
		if re.search(l111l1Created_By_Mucky_Duck (u"ࡸࠧࡷࡧࡵࡷ࡮ࡵ࡮࠾ࠤࠨࡷࠧ࠭ࣛ") %version, l1l11llCreated_By_Mucky_Duck):
			l11l11lCreated_By_Mucky_Duck.log(l111l1Created_By_Mucky_Duck (u"ࠧࡗࡧࡵࡷ࡮ࡵ࡮ࠡࡅ࡫ࡩࡨࡱࠠࡐࡍࠪࣜ"))
		else:
			l11l1lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"࡙ࠣࡵࡳࡳ࡭ࠠࡗࡧࡵࡷ࡮ࡵ࡮ࠡࡑࡩࠤࡒࡻࡣ࡬ࡻࡶࠤࡈࡵ࡭࡮ࡱࡱࠤࡒࡵࡤࡶ࡮ࡨࠦࣝ")
			l1l1111Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠤࡓࡰࡪࡧࡳࡦࠢࡌࡲࡸࡺࡡ࡭࡮ࠣࡇࡴࡸࡲࡦࡥࡷࠤ࡛࡫ࡲࡴ࡫ࡲࡲࠥࡌࡲࡰ࡯ࠣࡘ࡭࡫ࠠࡓࡧࡳࡳࠧࣞ")
			l11lllCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠥࡄࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟࡫ࡸࡹࡶ࠺࠰࠱ࡰࡹࡨࡱࡹࡴ࠰ࡰࡩࡩ࡯ࡡࡱࡱࡵࡸࡦࡲ࠴࡬ࡱࡧ࡭࠳ࡳ࡬࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤࣟ")
			l11l11lCreated_By_Mucky_Duck.show_ok_dialog([l11l1lCreated_By_Mucky_Duck, l1l1111Created_By_Mucky_Duck, l11lllCreated_By_Mucky_Duck], l1ll1l1Created_By_Mucky_Duck)
			xbmc.executebuiltin(l111l1Created_By_Mucky_Duck (u"ࠦ࡝ࡈࡍࡄ࠰ࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡛ࡰࡥࡣࡷࡩ࠭ࡶࡡࡵࡪ࠯ࡶࡪࡶ࡬ࡢࡥࡨ࠭ࠧ࣠"))
			xbmc.executebuiltin(l111l1Created_By_Mucky_Duck (u"ࠧ࡞ࡂࡎࡅ࠱ࡅࡨࡺࡩࡷࡣࡷࡩ࡜࡯࡮ࡥࡱࡺࠬࡍࡵ࡭ࡦࠫࠥ࣡"))
def l111l1lCreated_By_Mucky_Duck(title,url,l1l111Created_By_Mucky_Duck,content):
	if l1l111Created_By_Mucky_Duck == None:
		l1l111Created_By_Mucky_Duck = l1llll1Created_By_Mucky_Duck
	link = open_url(url).content
	match=re.compile(l111l1Created_By_Mucky_Duck (u"࠭ࡨࡳࡧࡩࡁࠧ࠮࡛࡟ࠤࡠ࠮࠮ࠨ࠾࠽࠰࠭ࡃࡨࡲࡡࡴࡵࡀࠦࡪࡶࡩࡴࡱࡧࡩࠧ࠴ࠪࡀࡀࠫ࡟ࡣࡂ࠾࡞ࠬࠬࡀ࠴࠭࣢")).findall(link)
	items = len(match)
	for url,name in match:
		data = name.split(l111l1Created_By_Mucky_Duck (u"ࠧ࠮ࣣࠩ"))
		l1l1l1lCreated_By_Mucky_Duck = data[0].replace(l111l1Created_By_Mucky_Duck (u"ࠨࡕࠪࣤ"),l111l1Created_By_Mucky_Duck (u"ࠩࠪࣥ")).replace(l111l1Created_By_Mucky_Duck (u"ࠪࡷࣦࠬ"),l111l1Created_By_Mucky_Duck (u"ࠫࠬࣧ"))
		l11l1l1Created_By_Mucky_Duck = data[1].replace(l111l1Created_By_Mucky_Duck (u"ࠬࡋࠧࣨ"),l111l1Created_By_Mucky_Duck (u"ࣩ࠭ࠧ")).replace(l111l1Created_By_Mucky_Duck (u"ࠧࡦࠩ࣪"),l111l1Created_By_Mucky_Duck (u"ࠨࠩ࣫"))
		try:
			l11l1l1Created_By_Mucky_Duck = l11l1l1Created_By_Mucky_Duck.split(l111l1Created_By_Mucky_Duck (u"ࠩ࠯ࠫ࣬"))[0]
		except:
			pass
		fan_art = {l111l1Created_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨ࣭"):l1l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷ࣮ࠫ"):l11Created_By_Mucky_Duck+l111l1Created_By_Mucky_Duck (u"ࠬࡳ࠴ࡶ࠰࡭ࡴ࡬࣯࠭")}
		md.addDir({l111l1Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࣰࠫ"): l111l1Created_By_Mucky_Duck (u"ࠧ࠸ࣱࠩ"), l111l1Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪࣲ࠭"):l111l1Created_By_Mucky_Duck (u"ࠩ࡞ࡍࡢࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡦࡲࡨ࡬࡫ࡲࡣ࡮ࡸࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࡡ࠯ࡊ࡟ࠪࣳ") %name,
			   l111l1Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࣴ"):url, l111l1Created_By_Mucky_Duck (u"ࠫ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫ࠧࣵ"):l1l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹࣶ࠭"):l111l1Created_By_Mucky_Duck (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࡳࠨࣷ")},
			  {l111l1Created_By_Mucky_Duck (u"ࠧࡴࡱࡵࡸࡹ࡯ࡴ࡭ࡧࠪࣸ"):title, l111l1Created_By_Mucky_Duck (u"ࠨࡵࡨࡥࡸࡵ࡮ࠨࣹ"):l1l1l1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࣺࠪ"):l11l1l1Created_By_Mucky_Duck},
			  fan_art, is_folder=False, item_count=items)
	setView(l11l111Created_By_Mucky_Duck,l111l1Created_By_Mucky_Duck (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࡷࠬࣻ"), l111l1Created_By_Mucky_Duck (u"ࠫࡪࡶࡩ࠮ࡸ࡬ࡩࡼ࠭ࣼ"))
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
def l1llll1lCreated_By_Mucky_Duck(url,content):
	link = open_url(url).text
	if content == l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࣽ"):
		match=re.compile(l111l1Created_By_Mucky_Duck (u"࠭࠼࡭࡫ࡁࠤࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯ࠬࡂ࠭ࠧࠦࡴࡪࡶ࡯ࡩࡂࠨࡁ࡭࡮ࠣࡱࡴࡼࡩࡦࡵ࠱࠮ࡄࠨ࠾ࠩ࠰࠭ࡃ࠮ࡂ࠯ࡢࡀ࠿࠳ࡱ࡯࠾ࠨࣾ")).findall(link)
		for url,name in match:
			if l111l1Created_By_Mucky_Duck (u"ࠧ࠰࡯ࡲࡺ࡮࡫࠭ࠨࣿ") in url:
				md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ऀ"): l111l1Created_By_Mucky_Duck (u"ࠩ࠶ࠫँ"), l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨं"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧः") %name, l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩऄ"):url,
					   l111l1Created_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧअ"):l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧआ")})
	elif content == l111l1Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩइ"):
		match=re.compile(l111l1Created_By_Mucky_Duck (u"ࠩ࠿ࡰ࡮ࡄࠠ࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࠫ࠲࠯ࡅࠩࠣࠢࡷ࡭ࡹࡲࡥ࠾ࠤࡄࡰࡱࠦࡔࡗࡵ࡫ࡳࡼ࠴ࠪࡀࠤࡁࠬ࠳࠰࠿ࠪ࠾࠲ࡥࡃࡂ࠯࡭࡫ࡁࠫई")).findall(link)
		for url,name in match:
			if l111l1Created_By_Mucky_Duck (u"ࠪ࠳ࡹࡼࡳࡩࡱࡺ࠱ࠬउ") in url:
				md.addDir({l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩऊ"): l111l1Created_By_Mucky_Duck (u"ࠬ࠹ࠧऋ"), l111l1Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫऌ"):l111l1Created_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪऍ") %name, l111l1Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬऎ"):url,
					   l111l1Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪए"):l111l1Created_By_Mucky_Duck (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫऐ")})
	setView(l11l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪऑ"), l111l1Created_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨऒ"))
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
def l1111Created_By_Mucky_Duck():
        l11ll1Created_By_Mucky_Duck = [l111l1Created_By_Mucky_Duck (u"࠭ࡲࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻ࠱ࡱࡦ࡬ࠧओ"), l111l1Created_By_Mucky_Duck (u"ࠧࡱ࡮ࡸ࡫࡮ࡴ࠮ࡱࡴࡲ࡫ࡷࡧ࡭࠯࡯ࡤࡪࡼ࡯ࡺࡢࡴࡧࠫऔ"), l111l1Created_By_Mucky_Duck (u"ࠨࡲ࡯ࡹ࡬࡯࡮࠯ࡸ࡬ࡨࡪࡵ࠮࡬ࡴࡤࡸࡴࡹࠧक"),
                    l111l1Created_By_Mucky_Duck (u"ࠩࡵࡩࡵࡵࡳࡪࡶࡲࡶࡾ࠴ࡡ࡯ࡱࡱࡽࡲࡵࡵࡴࡶࡵࡹࡹ࡮ࠧख"), l111l1Created_By_Mucky_Duck (u"ࠪࡴࡱࡻࡧࡪࡰ࠱ࡴࡷࡵࡧࡳࡣࡰ࠲ࡦࡴ࡯࡯ࡻࡰࡳࡺࡹࡴࡳࡷࡷ࡬ࠬग"),
                    l111l1Created_By_Mucky_Duck (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡻ࡯ࡤࡦࡱ࠱࡯ࡷࡧࡴࡰࡵࡩࡹࡨࡱࡳࡥࡷࡦ࡯ࡾ࠭घ"), l111l1Created_By_Mucky_Duck (u"ࠬࡹࡣࡳ࡫ࡳࡸ࠳ࡱࡲࡢࡶࡲࡷ࡫ࡻࡣ࡬ࡵࡧࡹࡨࡱࡹ࠯ࡣࡵࡸࡼࡵࡲ࡬ࠩङ"),
                    l111l1Created_By_Mucky_Duck (u"࠭ࡳࡤࡴ࡬ࡴࡹ࠴࡫ࡳࡣࡷࡳࡸ࡬ࡵࡤ࡭ࡶࡨࡺࡩ࡫ࡺ࠰ࡰࡩࡹࡧࡤࡢࡶࡤࠫच"), l111l1Created_By_Mucky_Duck (u"ࠧࡴࡥࡵ࡭ࡵࡺ࠮࡮ࡱࡧࡹࡱ࡫࠮ࡨ࡫ࡪ࡫࡮ࡺࡹࠨछ")]
        l1111Created_By_Mucky_Duck = any(xbmc.getCondVisibility(l111l1Created_By_Mucky_Duck (u"ࠨࡕࡼࡷࡹ࡫࡭࠯ࡊࡤࡷࡆࡪࡤࡰࡰࠫࠩࡸ࠯ࠧज") % (l11l11lCreated_By_Mucky_Duck)) for l11l11lCreated_By_Mucky_Duck in l11ll1Created_By_Mucky_Duck)
        if l1111Created_By_Mucky_Duck:
                l11l1lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠩ࡜ࡳࡺࠦࡈࡢࡸࡨࠤࡎࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡂࡦࡧࡳࡳࡹࠧझ")
                l1l1111Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠪࡘ࡭ࡧࡴࠡࡏࡸࡧࡰࡿࠠࡅࡷࡦ࡯ࠥࡊ࡯ࡦࡵࠣࡒࡴࡺࠧञ")
                l11lllCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠫࡘࡻࡰࡱࡱࡵࡸࠥࡇ࡮ࡥ࡚ࠢ࡭ࡱࡲࠠࡏࡱࡺࠤࡗ࡫࡭ࡰࡸࡨࠫट")
                l1lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠬࡘࡥ࡮ࡱࡹࡩࡩࠦࡁ࡯ࡱࡱࡽࡲࡵࡵࡴࠢࡕࡩࡵࡵࠠࡂࡰࡧࠤࡆࡪࡤࡰࡰࡶࠫठ")
                l1l11lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡖ࡬ࡦࡣࡶࡩࠥࡊ࡯࡯ࡶࠣࡗࡺࡶࡰࡰࡴࡷࠤࡎࡪࡩࡰࡶࡶࠫड")
                l1l1l1Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠧࡓࡧࡰࡳࡻ࡫ࡤࠡࠧࡶࠫढ") %l1ll1l1Created_By_Mucky_Duck
                l1llllllCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠨࡗࡱࡪࡴࡸࡴࡶࡰࡤࡸࡪࡲࡹ࡛ࠡࡲࡹ࡙ࠥࡵࡱࡲࡲࡶࡹࠦࡉࡥ࡫ࡲࡸࡸ࠭ण")
                l11l11lCreated_By_Mucky_Duck.show_ok_dialog([l11l1lCreated_By_Mucky_Duck, l1l1111Created_By_Mucky_Duck, l11lllCreated_By_Mucky_Duck], l1ll1l1Created_By_Mucky_Duck)
                l1lllll1Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠩ࡜ࡳࡺࡸࠠࡄࡪࡲ࡭ࡨ࡫ࠠࡆ࡫ࡷ࡬ࡪࡸࠠࡖࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣࠩࡸࠦࡏࡳࠢࡘࡲ࡮ࡴࡳࡵࡣ࡯ࡰ࡚ࠥࡨࡦࠢࡄࡲࡴࡴࡹ࡮ࡱࡸࡷࠥࡘࡥࡱࡱࠣ࠯ࠥࡇࡤࡥࡱࡱࡷࠬत") %l1ll1l1Created_By_Mucky_Duck
                if md.dialog_yesno(l1lllll1Created_By_Mucky_Duck,l111l1Created_By_Mucky_Duck (u"ࠪࡅࡳࡵ࡮ࡺ࡯ࡲࡹࡸ࠭थ"),l1ll1l1Created_By_Mucky_Duck):
                        l11l11lCreated_By_Mucky_Duck.log(l111l1Created_By_Mucky_Duck (u"ࠫࡂࡃ࠽ࡅࡇࡏࡉ࡙ࡏࡎࡈ࠿ࡀࡁࡆࡔࡏࡏ࡛ࡐࡓ࡚࡙࠽࠾࠿ࡄࡈࡉࡕࡎࡔ࠿ࡀࡁ࠰ࡃ࠽࠾ࡔࡈࡔࡔࡃ࠽࠾ࠩद"))
                        for root, dirs, files in os.walk(xbmc.translatePath(l111l1Created_By_Mucky_Duck (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠭ध"))):
                                dirs[:] = [d for d in dirs if d in l11ll1Created_By_Mucky_Duck]
                                for d in dirs:
                                        try:
                                                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                                        except OSError:
                                                pass
                        l11l11lCreated_By_Mucky_Duck.show_ok_dialog([l1lCreated_By_Mucky_Duck, l1l11lCreated_By_Mucky_Duck], l1ll1l1Created_By_Mucky_Duck)
                else:
                        l11l11lCreated_By_Mucky_Duck.log(l111l1Created_By_Mucky_Duck (u"࠭࠽࠾࠿ࡇࡉࡑࡋࡔࡊࡐࡊࡁࡂࡃࠥࡴ࠿ࡀࡁࠬन") %l1ll1l1Created_By_Mucky_Duck)
                        l11lCreated_By_Mucky_Duck = l11l11lCreated_By_Mucky_Duck.get_path()
			shutil.rmtree(l11lCreated_By_Mucky_Duck, ignore_errors=True)
			l11l11lCreated_By_Mucky_Duck.show_ok_dialog([l1l1l1Created_By_Mucky_Duck, l1llllllCreated_By_Mucky_Duck], l1ll1l1Created_By_Mucky_Duck)
                time.sleep(2)
                os._exit(0)
def l11l1llCreated_By_Mucky_Duck(url,content):
	link = open_url(url).text
	match=re.compile(l111l1Created_By_Mucky_Duck (u"ࠧ࠽࡮࡬ࡂࠥࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠭ࡃ࠮ࠨࠠࡵ࡫ࡷࡰࡪࡃࠢࡂ࡮࡯ࠤࡲࡵࡶࡪࡧࡶ࠲࠯ࡅࠢ࠿ࠪ࠱࠮ࡄ࠯࠼࠰ࡣࡁࡀ࠴ࡲࡩ࠿ࠩऩ")).findall(link)
	for url,name in match:
		if l111l1Created_By_Mucky_Duck (u"ࠨ࠱ࡼࡩࡦࡸ࠭ࠨप") in url:
			md.addDir({l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧफ"): l111l1Created_By_Mucky_Duck (u"ࠪ࠷ࠬब"), l111l1Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩभ"):l111l1Created_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨम") %name, l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪय"):url,
					   l111l1Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨर"):l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨऱ")})
	setView(l11l111Created_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠩࡩ࡭ࡱ࡫ࡳࠨल"), l111l1Created_By_Mucky_Duck (u"ࠪࡱࡪࡴࡵ࠮ࡸ࡬ࡩࡼ࠭ळ"))
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
def l1lll1Created_By_Mucky_Duck(content, query):
	try:
		if query:
			search = query.replace(l111l1Created_By_Mucky_Duck (u"ࠫࠥ࠭ऴ"),l111l1Created_By_Mucky_Duck (u"ࠬ࠳ࠧव"))
		else:
			search = md.search(l111l1Created_By_Mucky_Duck (u"࠭࠭ࠨश"))
			if search == l111l1Created_By_Mucky_Duck (u"ࠧࠨष"):
				md.notification(l111l1Created_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣ࡛ࡃ࡟ࡈࡑࡕ࡚࡙ࠡࡓࡘࡉࡗ࡟࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡ࠱ࡇࡢࡰࡴࡷ࡭ࡳ࡭ࠠࡴࡧࡤࡶࡨ࡮ࠧस"),l1llll1Created_By_Mucky_Duck)
				return
			else:
				pass
		if content == l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩह"):
			url = l111l1Created_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡴࡢࡩ࠲ࠩࡸ࠭ऺ") %(l1l111lCreated_By_Mucky_Duck,search)
		elif content == l111l1Created_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬऻ"):
			url = l111l1Created_By_Mucky_Duck (u"ࠬࠫࡳ࠰ࡶࡤ࡫ࡹࡼࡳ࠰ࠧࡶ़ࠫ") %(l1l111lCreated_By_Mucky_Duck,search)
		l1Created_By_Mucky_Duck(url,content)
	except:
		md.notification(l111l1Created_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࡠࡈ࡝ࡔࡱࡵࡶࡾࠦࡎࡰࠢࡕࡩࡸࡻ࡬ࡵࡵ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨऽ"),l1llll1Created_By_Mucky_Duck)
def l1ll11lCreated_By_Mucky_Duck(url,name,content,fan_art,l111lllCreated_By_Mucky_Duck):
	link = open_url(url).content
	if content == l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧा"):
		request_url = re.findall(l111l1Created_By_Mucky_Duck (u"ࡳࠩ࡫ࡶࡪ࡬࠽ࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࡁ࡛ࡦࡺࡣࡩࠩि"), str(link), re.I|re.DOTALL)[0]
		link = open_url(request_url).content
		l11ll11Created_By_Mucky_Duck = request_url
	else:
		l11ll11Created_By_Mucky_Duck = url
	value = []
	l111lCreated_By_Mucky_Duck = []
	l1lll1lCreated_By_Mucky_Duck= l111l1Created_By_Mucky_Duck (u"ࠩࠪी")
	match = re.findall(l111l1Created_By_Mucky_Duck (u"ࡵࠫࠧ࡬ࡩ࡭ࡧࠥ࠾ࠧ࠮࡛࡟ࠤࡠ࠯࠮ࠨ࠮ࠫࡁࠥࡰࡦࡨࡥ࡭ࠤ࠽ࠦ࠭ࡡ࡞ࠣ࡟࠮࠭ࠧ࠭ु"), str(link), re.I|re.DOTALL)
	for url,l11l11Created_By_Mucky_Duck in match:
		value.append(int(re.sub(l111l1Created_By_Mucky_Duck (u"ࠫࡡࡊࠧू"), l111l1Created_By_Mucky_Duck (u"ࠬ࠭ृ"), l11l11Created_By_Mucky_Duck)))
		l111lCreated_By_Mucky_Duck.append(url)
	try:
		l1lll1lCreated_By_Mucky_Duck =  l111lCreated_By_Mucky_Duck[md.get_max_value_index(value)[0]]
	except:
		pass
	if not l1lll1lCreated_By_Mucky_Duck:
                try:
                        l11lll1Created_By_Mucky_Duck = re.findall(l111l1Created_By_Mucky_Duck (u"ࡸࠢࡨࡧࡷࡠ࠭࠭ࠨ࡜ࡠࠪࡡ࠯࠯ࠧࠣॄ"), str(link), re.I|re.DOTALL)[0]
                        l11lll1Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.replace(l111l1Created_By_Mucky_Duck (u"ࠧ࠯࠰࠲ࡥ࡯ࡧࡸࠨॅ"),l111l1Created_By_Mucky_Duck (u"ࠨ࠱ࡤ࡮ࡦࡾࠧॆ"))
                        l11lll1Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.replace(l111l1Created_By_Mucky_Duck (u"ࠩ࠱࠳ࡦࡰࡡࡹࠩे"),l111l1Created_By_Mucky_Duck (u"ࠪ࠳ࡦࡰࡡࡹࠩै"))
                        if l1l111lCreated_By_Mucky_Duck not in l11lll1Created_By_Mucky_Duck:
                                l11lll1Created_By_Mucky_Duck = l1l111lCreated_By_Mucky_Duck + l11lll1Created_By_Mucky_Duck
                except:
                        l11lll1Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠫࠪࡹ࠯ࡢ࡬ࡤࡼ࠲ࡺ࡯࡬ࡧࡱ࠱࠷࠴ࡰࡩࡲࡂࡸࡴࡱࡥ࡯࠿ࡰ࠸ࡺ࡬ࡲࡦࡧ࡬ࡷࡹ࡮ࡥࡣࡧࡶࡸ࠶ࠬࡶ࠾ࠩॉ")
		link = link.replace(l111l1Created_By_Mucky_Duck (u"ࠬࠦࠧॊ"),l111l1Created_By_Mucky_Duck (u"࠭ࠧो"))
		try:
			l11111Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck + re.findall(l111l1Created_By_Mucky_Duck (u"ࡲࠨ࡮࡬ࡲࡰࡃࠢࠩ࡝ࡡࠦࡢ࠰ࠩࠣࡀࡖࡩࡷࡼࡥࡳ࠲࠿࠳ࡸࡶࡡ࡯ࡀࠪौ"), str(link), re.I|re.DOTALL)[0]
			l1l1ll1Created_By_Mucky_Duck = open_url(l11111Created_By_Mucky_Duck).content
			l1l1ll1Created_By_Mucky_Duck = l1l1ll1Created_By_Mucky_Duck.replace(l111l1Created_By_Mucky_Duck (u"ࠨ्ࠢࠪ"),l111l1Created_By_Mucky_Duck (u"ࠩࠪॎ"))
			try:
				data = re.findall(l111l1Created_By_Mucky_Duck (u"ࡵࠫࡸࡵࡵࡳࡥࡨࡷ࠿ࡢ࡛ࠩ࠰࠭ࡃ࠮ࡢ࡝ࠨॏ"), str(l1l1ll1Created_By_Mucky_Duck), re.I|re.DOTALL)[0]
				match = re.findall(l111l1Created_By_Mucky_Duck (u"ࡶࠬ࡬ࡩ࡭ࡧ࠱࠮ࡄࡀࠢࠩ࡝ࡡࠦࡢ࠰ࠩࠣࠩॐ"), str(data), re.I|re.DOTALL)
				l1ll111Created_By_Mucky_Duck = re.findall(l111l1Created_By_Mucky_Duck (u"ࡷ࠭࡬ࡢࡤࡨࡰ࠳࠰࠿࠻ࠪ࠱࠮ࡄ࠯ࠬࠨ॑"), str(data), re.I|re.DOTALL)
				for url in match:
					l111lCreated_By_Mucky_Duck.append(url)
				for l11l11Created_By_Mucky_Duck in l1ll111Created_By_Mucky_Duck:
					value.append(int(re.sub(l111l1Created_By_Mucky_Duck (u"࠭࡜ࡅ॒ࠩ"), l111l1Created_By_Mucky_Duck (u"ࠧࠨ॓"), l11l11Created_By_Mucky_Duck)))
				try:
					l1lll1lCreated_By_Mucky_Duck =  l111lCreated_By_Mucky_Duck[md.get_max_value_index(value)[0]]
				except:
					try:
						l1lll1lCreated_By_Mucky_Duck = match[-1]
					except:
						l1lll1lCreated_By_Mucky_Duck = match[0]
			except:
				l1lll1lCreated_By_Mucky_Duck = re.findall(l111l1Created_By_Mucky_Duck (u"ࡳࠩࡶࡳࡺࡸࡣࡦ࠰࠭ࡃࡸࡸࡣ࠾ࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠫ॔"), str(l1l1ll1Created_By_Mucky_Duck), re.I|re.DOTALL)[0]
		except:
			l1111lCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck + re.findall(l111l1Created_By_Mucky_Duck (u"ࡴࠪࡰ࡮ࡴ࡫࠾ࠤࠫ࡟ࡣࠨ࡝ࠫࠫࠥࡂࡘ࡫ࡲࡷࡧࡵ࠵ࡁ࠵ࡳࡱࡣࡱࡂࠬॕ"), str(link), re.I|re.DOTALL)[0]
			l1l1Created_By_Mucky_Duck = open_url(l1111lCreated_By_Mucky_Duck).content
			l1l1Created_By_Mucky_Duck = l1l1Created_By_Mucky_Duck.replace(l111l1Created_By_Mucky_Duck (u"ࠪࠤࠬॖ"),l111l1Created_By_Mucky_Duck (u"ࠫࠬॗ"))
			try:
				data = re.findall(l111l1Created_By_Mucky_Duck (u"ࡷ࠭ࡳࡰࡷࡵࡧࡪࡹ࠺࡝࡝ࠫ࠲࠯ࡅࠩ࡝࡟ࠪक़"), str(l1l1Created_By_Mucky_Duck), re.I|re.DOTALL)[0].replace(l111l1Created_By_Mucky_Duck (u"࠭ࠠࠨख़"),l111l1Created_By_Mucky_Duck (u"ࠧࠨग़"))
				match = re.findall(l111l1Created_By_Mucky_Duck (u"ࡳࠩࡩ࡭ࡱ࡫࠮ࠫࡁ࠽ࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧ࠭ज़"), str(data), re.I|re.DOTALL)
				l1ll111Created_By_Mucky_Duck = re.findall(l111l1Created_By_Mucky_Duck (u"ࡴࠪࡰࡦࡨࡥ࡭࠰࠭ࡃ࠿࠮࠮ࠫࡁࠬ࠰ࠬड़"), str(data), re.I|re.DOTALL)
				for url in match:
					l111lCreated_By_Mucky_Duck.append(url)
				for l11l11Created_By_Mucky_Duck in l1ll111Created_By_Mucky_Duck:
					value.append(int(re.sub(l111l1Created_By_Mucky_Duck (u"ࠪࡠࡉ࠭ढ़"), l111l1Created_By_Mucky_Duck (u"ࠫࠬफ़"), l11l11Created_By_Mucky_Duck)))
				try:
					l1lll1lCreated_By_Mucky_Duck =  l111lCreated_By_Mucky_Duck[md.get_max_value_index(value)[0]]
				except:
					try:
						l1lll1lCreated_By_Mucky_Duck = match[-1]
					except:
						l1lll1lCreated_By_Mucky_Duck = match[0]
			except:
				l1lll1lCreated_By_Mucky_Duck = re.findall(l111l1Created_By_Mucky_Duck (u"ࡷ࠭ࡳࡰࡷࡵࡧࡪ࠴ࠪࡀࡵࡵࡧࡂࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨय़"), str(l1l1Created_By_Mucky_Duck), re.I|re.DOTALL)[0]
	if l111l1Created_By_Mucky_Duck (u"࠭ࡧࡰࡱࡪࡰࡪ࠭ॠ") in l1lll1lCreated_By_Mucky_Duck or l111l1Created_By_Mucky_Duck (u"ࠧࡶࡵࡨࡶࡨࡪ࡮ࠨॡ") in l1lll1lCreated_By_Mucky_Duck or l111l1Created_By_Mucky_Duck (u"ࠨࡣࡰࡥࡿࡵ࡮ࡢࡹࡶ࠲ࡨࡵ࡭ࠨॢ") in l1lll1lCreated_By_Mucky_Duck:
		l1lll1lCreated_By_Mucky_Duck = l1lll1lCreated_By_Mucky_Duck
	else:
		if l1l111lCreated_By_Mucky_Duck not in l1lll1lCreated_By_Mucky_Duck:
			l1lll1lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠩࠨࡷ࠴ࠫࡳࠨॣ") %(l1l111lCreated_By_Mucky_Duck,l1lll1lCreated_By_Mucky_Duck)
	md.resolved(l1lll1lCreated_By_Mucky_Duck, name, fan_art, l111lllCreated_By_Mucky_Duck)
	l11l11lCreated_By_Mucky_Duck.end_of_directory()
md.check_source()
mode = md.args[l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ।")]
url = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨ॥"), None)
name = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ०"), None)
query = md.args.get(l111l1Created_By_Mucky_Duck (u"࠭ࡱࡶࡧࡵࡽࠬ१"), None)
title = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠧࡵ࡫ࡷࡰࡪ࠭२"), None)
l1l1l1lCreated_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠨࡵࡨࡥࡸࡵ࡮ࠨ३"), None)
l11l1l1Created_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࠪ४") ,None)
l111lllCreated_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠪ࡭ࡳ࡬࡯࡭ࡣࡥࡩࡱ࠭५"), None)
content = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬ६"), None)
l11llCreated_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࡢ࡭ࡩ࠭७"), None)
l1l111Created_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱ࡭ࡲࡧࡧࡦࠩ८"), None)
fan_art = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠧࡧࡣࡱࡣࡦࡸࡴࠨ९"), None)
is_folder = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠨ࡫ࡶࡣ࡫ࡵ࡬ࡥࡧࡵࠫ॰"), True)
if mode is None or url is None or len(url)<1:
	l1llll11Created_By_Mucky_Duck()
elif mode == l111l1Created_By_Mucky_Duck (u"ࠩ࠴ࠫॱ"):
	l1111l1Created_By_Mucky_Duck()
elif mode == l111l1Created_By_Mucky_Duck (u"ࠪ࠶ࠬॲ"):
	l11111lCreated_By_Mucky_Duck()
elif mode == l111l1Created_By_Mucky_Duck (u"ࠫ࠸࠭ॳ"):
	l1Created_By_Mucky_Duck(url,content)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠬ࠺ࠧॴ"):
	l1llll1lCreated_By_Mucky_Duck(url,content)
elif mode == l111l1Created_By_Mucky_Duck (u"࠭࠵ࠨॵ"):
	l11l1llCreated_By_Mucky_Duck(url,content)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠧ࠷ࠩॶ"):
	l111l1lCreated_By_Mucky_Duck(title,url,l1l111Created_By_Mucky_Duck,content)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠨ࠹ࠪॷ"):
	l1ll11lCreated_By_Mucky_Duck(url,name,content,fan_art,l111lllCreated_By_Mucky_Duck)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠩࡶࡩࡦࡸࡣࡩࠩॸ"):
	l1lll1Created_By_Mucky_Duck(content,query)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠪࡥࡩࡪ࡯࡯ࡡࡶࡩࡦࡸࡣࡩࠩॹ"):
	md.addon_search(content,query,fan_art,l111lllCreated_By_Mucky_Duck)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠫࡦࡪࡤࡠࡴࡨࡱࡴࡼࡥࡠࡨࡤࡺࠬॺ"):
	md.add_remove_fav(name, url, l111lllCreated_By_Mucky_Duck, fan_art,
			  content, l11llCreated_By_Mucky_Duck, is_folder)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠬ࡬ࡥࡵࡥ࡫ࡣ࡫ࡧࡶࡴࠩॻ"):
	md.fetch_favs(l1l111lCreated_By_Mucky_Duck)
elif mode == l111l1Created_By_Mucky_Duck (u"࠭ࡡࡥࡦࡲࡲࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧॼ"):
	l11l11lCreated_By_Mucky_Duck.show_settings()
elif mode == l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡧࡷࡥࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧॽ"):
	import metahandler
	metahandler.display_settings()
l11l11lCreated_By_Mucky_Duck.end_of_directory()