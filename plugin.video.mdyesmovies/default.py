# -*- coding: utf-8 -*-
import sys
l1ll1l11Created_By_Mucky_Duck = sys.version_info [0] == 2
l11ll11Created_By_Mucky_Duck = 2048
l1llll1lCreated_By_Mucky_Duck = 7
def l11lCreated_By_Mucky_Duck (l1ll1lCreated_By_Mucky_Duck):
    global l11lll1Created_By_Mucky_Duck
    l1111llCreated_By_Mucky_Duck = ord (l1ll1lCreated_By_Mucky_Duck [-1])
    l1ll1l1lCreated_By_Mucky_Duck = l1ll1lCreated_By_Mucky_Duck [:-1]
    l1ll11lCreated_By_Mucky_Duck = l1111llCreated_By_Mucky_Duck % len (l1ll1l1lCreated_By_Mucky_Duck)
    l1l11lCreated_By_Mucky_Duck = l1ll1l1lCreated_By_Mucky_Duck [:l1ll11lCreated_By_Mucky_Duck] + l1ll1l1lCreated_By_Mucky_Duck [l1ll11lCreated_By_Mucky_Duck:]
    if l1ll1l11Created_By_Mucky_Duck:
        l1l1lCreated_By_Mucky_Duck = unicode () .join ([unichr (ord (char) - l11ll11Created_By_Mucky_Duck - (l1llCreated_By_Mucky_Duck + l1111llCreated_By_Mucky_Duck) % l1llll1lCreated_By_Mucky_Duck) for l1llCreated_By_Mucky_Duck, char in enumerate (l1l11lCreated_By_Mucky_Duck)])
    else:
        l1l1lCreated_By_Mucky_Duck = str () .join ([chr (ord (char) - l11ll11Created_By_Mucky_Duck - (l1llCreated_By_Mucky_Duck + l1111llCreated_By_Mucky_Duck) % l1llll1lCreated_By_Mucky_Duck) for l1llCreated_By_Mucky_Duck, char in enumerate (l1l11lCreated_By_Mucky_Duck)])
    return eval (l1l1lCreated_By_Mucky_Duck)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import jsunfuck,os,re,sys,shutil,time
# Yes Movies Add-on Created By Mucky Duck (10/2016)
l111l1lCreated_By_Mucky_Duck = xbmcaddon.Addon().getAddonInfo(l11lCreated_By_Mucky_Duck (u"ࠫ࡮ࡪࠧࠀ"))
l111Created_By_Mucky_Duck = Addon(l111l1lCreated_By_Mucky_Duck, sys.argv)
l1lllCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_name()
l11111lCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_path()
md = md(l111l1lCreated_By_Mucky_Duck, sys.argv)
l1l1ll1Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠬࡧࡵࡵࡱࡳࡰࡦࡿࠧࠁ"))
l11ll1Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥ࡭ࡦࡶࡤࠫࠂ"))
l11l111Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠧࡦࡰࡤࡦࡱ࡫࡟ࡴࡪࡲࡻࡸ࠭ࠃ"))
l1llllllCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠨࡧࡱࡥࡧࡲࡥࡠ࡯ࡲࡺ࡮࡫ࡳࠨࠄ"))
l1l1l1lCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠩࡨࡲࡦࡨ࡬ࡦࡡࡩࡥࡻࡹࠧࠅ"))
l1lCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠪࡥࡩࡪ࡟ࡴࡧࡷࠫࠆ"))
l1l11ll1Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠫࡪࡴࡡࡣ࡮ࡨࡣࡲ࡫ࡴࡢࡡࡶࡩࡹ࠭ࠇ"))
l1l1llCreated_By_Mucky_Duck = md.get_art()
l1l1ll1lCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_icon()
l1l11l1Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_fanart()
l11l1l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡹࡦࡵࡰࡳࡻ࡯ࡥࡴ࠰ࡷࡳࠬࠈ")
reload(sys)
sys.setdefaultencoding(l11lCreated_By_Mucky_Duck (u"ࠨࡵࡵࡨ࠰࠼ࠧࠉ"))
l1l11Created_By_Mucky_Duck = [l11lCreated_By_Mucky_Duck (u"ࠧࡳࡣࡷ࡭ࡳ࡭ࠧࠊ"),l11lCreated_By_Mucky_Duck (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨࠋ"),l11lCreated_By_Mucky_Duck (u"ࠩࡹ࡭ࡪࡽࠧࠌ"),l11lCreated_By_Mucky_Duck (u"ࠪࡪࡦࡼ࡯ࡳ࡫ࡷࡩࠬࠍ"),l11lCreated_By_Mucky_Duck (u"ࠫ࡮ࡳࡤࡣࡡࡰࡥࡷࡱࠧࠎ")]
sort = [l11lCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤ࡮ࡴࡤࡪࡣࡱࡶࡪࡪ࡝ࡎࡱࡶࡸࠥࡘࡡࡵࡧࡧ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ࠏ"), l11lCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞ࡔࡨࡧࡪࡴࡴ࡭ࡻࠣࡅࡩࡪࡥࡥ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫࠐ"),
	l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡩ࡯ࡦ࡬ࡥࡳࡸࡥࡥ࡟ࡐࡳࡸࡺࠠࡗ࡫ࡨࡻࡪࡪ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࠑ"), l11lCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡴࡹࡴࠡࡈࡤࡺࡴࡻࡲࡪࡶࡨࡨࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࠒ"),
	l11lCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࡎࡓࡄࡃࠢࡕࡥࡹ࡯࡮ࡨ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫࠓ")]
def l1lll1Created_By_Mucky_Duck():
	if l1llllllCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨࠔ"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࠕ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠷ࠧࠖ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࠗ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠ࡟ࡇࡣࡍࡐࡘࡌࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫ࠘"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࠙"):l11lCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ࠚ"), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࠛ"):l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶࠫࠜ")})
	if l11l111Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡲࡶࡧࠪࠝ"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࠞ"): l11lCreated_By_Mucky_Duck (u"ࠧ࠲ࠩࠟ"), l11lCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࠠ"):l11lCreated_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢ࡬ࡲࡩ࡯ࡡ࡯ࡴࡨࡨࡢࡡࡂ࡞ࡖ࡙ࠤࡘࡎࡏࡘࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨࠡ"), l11lCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࠢ"):l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠣ"), l11lCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࠤ"):l11lCreated_By_Mucky_Duck (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹࠧࠥ")})
	if l1l1l1lCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬࠦ"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠧ"): l11lCreated_By_Mucky_Duck (u"ࠩࡩࡩࡹࡩࡨࡠࡨࡤࡺࡸ࠭ࠨ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠩ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡮ࡴࡤࡪࡣࡱࡶࡪࡪ࡝࡜ࡄࡠࡑ࡞ࠦࡆࡂࡘࡒ࡙ࡗࡏࡔࡆࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨࠪ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠫ"):l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠬ")})
	if l11ll1Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬ࠭"):
		if l1l11ll1Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭࠮"):
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ࠯"):l11lCreated_By_Mucky_Duck (u"ࠪࡱࡪࡺࡡࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ࠰"), l11lCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ࠱"):l11lCreated_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞࡝ࡅࡡࡒࡋࡔࡂࠢࡖࡉ࡙࡚ࡉࡏࡉࡖ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ࠲"), l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࠳"):l11lCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࠴")}, is_folder=False, is_playable=False)
	if l1lCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭࠵"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ࠶"):l11lCreated_By_Mucky_Duck (u"ࠪࡥࡩࡪ࡯࡯ࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ࠷"), l11lCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ࠸"):l11lCreated_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞࡝ࡅࡡࡆࡊࡄࡐࡐࠣࡗࡊ࡚ࡔࡊࡐࡊࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ࠹"), l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࠺"):l11lCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࠻")}, is_folder=False, is_playable=False)
	l1lllll1Created_By_Mucky_Duck()
        l1llllCreated_By_Mucky_Duck()
	setView(l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨࡨ࡬ࡰࡪࡹࠧ࠼"), l11lCreated_By_Mucky_Duck (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬ࠽"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1l1l111Created_By_Mucky_Duck(content):
	if l1l1l1lCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨ࠾"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩ࠿"): l11lCreated_By_Mucky_Duck (u"ࠬ࡬ࡥࡵࡥ࡫ࡣ࡫ࡧࡶࡴࠩࡀ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡁ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠ࡟ࡇࡣࡍ࡚ࠢࡄࡈࡉ࠳ࡏࡏࠢࡉࡅ࡛ࡕࡕࡓࡋࡗࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡂ"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡃ"):l11lCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ࡄ")})
	if content == l11lCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪࡅ"):
		l111111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࠪࡆ")
	elif content == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࡇ"):
		l111111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࠭ࡳࡦࡴ࡬ࡩࡸ࠭ࡈ")
	l1l1111Created_By_Mucky_Duck = l11l1l1Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"ࠧ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࠦࡵ࠲ࠩࡸ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࡣ࡯ࡰࠬࡉ")
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡊ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠵ࠫࡋ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡌ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡔࡈࡇࡊࡔࡔࡍ࡛ࠣࡅࡉࡊࡅࡅ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࡍ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡎ"):l1l1111Created_By_Mucky_Duck %(l111111Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ࡏ")), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡐ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡑ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠵ࠫࡒ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡓ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡈࡄ࡚ࡔ࡛ࡒࡊࡖࡈࡈࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࡔ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡕ"):l1l1111Created_By_Mucky_Duck %(l111111Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"࠭ࡦࡢࡸࡲࡶ࡮ࡺࡥࠨࡖ")), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡗ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡘ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠵࡙ࠫ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ࡚"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡔࡄࡘࡎࡔࡇࡔ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣ࡛ࠧ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ࡜"):l1l1111Created_By_Mucky_Duck %(l111111Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"࠭ࡲࡢࡶ࡬ࡲ࡬࠭࡝")), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࡞"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭࡟"): l11lCreated_By_Mucky_Duck (u"ࠩ࠵ࠫࡠ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡡ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡑࡔ࡙ࡔࠡࡘࡌࡉ࡜ࡋࡄ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࡢ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡣ"):l1l1111Created_By_Mucky_Duck %(l111111Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"࠭ࡶࡪࡧࡺࠫࡤ")), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡥ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡦ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠵ࠫࡧ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡨ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡘࡔࡖࠠࡊࡏࡇࡆࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࡩ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡪ"):l1l1111Created_By_Mucky_Duck %(l111111Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"࠭ࡩ࡮ࡦࡥࡣࡲࡧࡲ࡬ࠩ࡫")), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࡬"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭࡭"): l11lCreated_By_Mucky_Duck (u"ࠩ࠹ࠫ࡮"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ࡯"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡇࡔ࡛ࡎࡕࡔ࡜࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩࡰ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡱ"):l11l1l1Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"࠭࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠭ࡲ"), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡳ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡴ"): l11lCreated_By_Mucky_Duck (u"ࠩࡶࡩࡦࡸࡣࡩࠩࡵ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡶ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡗࡊࡇࡒࡄࡊ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨࡷ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡸ"):l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࡹ"), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࡺ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡻ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠷ࠫࡼ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡽ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࡋࡊࡔࡒࡆ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࡾ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡿ"):l11l1l1Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"࠭࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠭ࢀ"), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࢁ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࢂ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠸ࠫࢃ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࢄ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠ࡝ࡊࡇࡒ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࢅ"), l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࢆ"):l11l1l1Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"࠭࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠭ࢇ"), l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࢈"):content})
	setView(l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨࡨ࡬ࡰࡪࡹࠧࢉ"), l11lCreated_By_Mucky_Duck (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬࢊ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1ll11Created_By_Mucky_Duck(url,content):
	link = open_url(url,verify=False).content
	l1ll1Created_By_Mucky_Duck = md.regex_get_all(link, l11lCreated_By_Mucky_Duck (u"ࠪࡧࡱࡧࡳࡴ࠿ࠥࡱࡱ࠳ࡩࡵࡧࡰࠦࡃ࠭ࢋ"), l11lCreated_By_Mucky_Duck (u"ࠫࡁ࠵ࡤࡪࡸࡁࠫࢌ"))
	items = len(l1ll1Created_By_Mucky_Duck)
	for a in l1ll1Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠬࡺࡩࡵ࡮ࡨࡁࠧ࠭ࢍ"), l11lCreated_By_Mucky_Duck (u"࠭ࠢࠨࢎ"))
		name = l111Created_By_Mucky_Duck.unescape(name).replace(l11lCreated_By_Mucky_Duck (u"ࠢ࡝࡞ࠪࠦ࢏"),l11lCreated_By_Mucky_Duck (u"ࠣࠩࠥ࢐"))
		url = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠩ࡫ࡶࡪ࡬࠽ࠣࠩ࢑"), l11lCreated_By_Mucky_Duck (u"ࠪࠦࠬ࢒")).replace(l11lCreated_By_Mucky_Duck (u"ࠫ࠳࡮ࡴ࡮࡮ࠪ࢓"),l11lCreated_By_Mucky_Duck (u"ࠬ࠵ࡷࡢࡶࡦ࡬࡮ࡴࡧ࠯ࡪࡷࡱࡱ࠭࢔"))
		l11Created_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"࠭ࡤࡢࡶࡤ࠱ࡴࡸࡩࡨ࡫ࡱࡥࡱࡃࠢࠨ࢕"), l11lCreated_By_Mucky_Duck (u"ࠧࠣࠩ࢖"))
		l11l11lCreated_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠨ࡯࡯࡭࠲ࡷࡵࡢ࡮࡬ࡸࡾࠨ࠾ࠨࢗ"), l11lCreated_By_Mucky_Duck (u"ࠩ࠿ࠫ࢘"))
		l1l1l11lCreated_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠪࠦࡲࡲࡩ࠮ࡧࡳࡷࠧࡄ࢙ࠧ"), l11lCreated_By_Mucky_Duck (u"ࠫࡁ࠵࢚ࠧ"))
		l1l1l11lCreated_By_Mucky_Duck = l1l1l11lCreated_By_Mucky_Duck.replace(l11lCreated_By_Mucky_Duck (u"ࠬࡂࡳࡱࡣࡱࡂ࢛ࠬ"),l11lCreated_By_Mucky_Duck (u"࠭ࠠࠨ࢜")).replace(l11lCreated_By_Mucky_Duck (u"ࠧ࠽࡫ࡁࠫ࢝"),l11lCreated_By_Mucky_Duck (u"ࠨࠢࠪ࢞"))
		if content == l11lCreated_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩ࢟"):
			if l11l11lCreated_By_Mucky_Duck:
				md.addDir({l11lCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࢠ"): l11lCreated_By_Mucky_Duck (u"ࠫ࠼࠭ࢡ"), l11lCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࢢ"):l11lCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡪࡰࡧ࡭ࡦࡴࡲࡦࡦࡠࠬࠪࡹࠩ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࢣ") %(name,l11l11lCreated_By_Mucky_Duck),
					   l11lCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࢤ"):url, l11lCreated_By_Mucky_Duck (u"ࠨ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠫࢥ"):l11Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࢦ"):content}, {l11lCreated_By_Mucky_Duck (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪ࠭ࢧ"):name},
					  fan_art={l11lCreated_By_Mucky_Duck (u"ࠫ࡮ࡩ࡯࡯ࠩࢨ"):l11Created_By_Mucky_Duck}, is_folder=False, item_count=items)
		elif content == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࢩ"):
			if l1l1l11lCreated_By_Mucky_Duck:
				data = name.split(l11lCreated_By_Mucky_Duck (u"࠭࠭ࠡࡕࡨࡥࡸࡵ࡮ࠨࢪ"))
				l1111l1Created_By_Mucky_Duck = data[0].strip()
				try:
					l11l1llCreated_By_Mucky_Duck = data[1].strip()
				except:
					l11l1llCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧࠨࢫ")
				md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࢬ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠶ࠫࢭ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࢮ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠣ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡩ࡯ࡦ࡬ࡥࡳࡸࡥࡥ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࢯ") %(name,l1l1l11lCreated_By_Mucky_Duck),
					   l11lCreated_By_Mucky_Duck (u"ࠬࡺࡩࡵ࡮ࡨࠫࢰ"):l1111l1Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࢱ"):url, l11lCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࠪࢲ"):l11Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࢳ"):content, l11lCreated_By_Mucky_Duck (u"ࠩࡶࡩࡦࡹ࡯࡯ࠩࢴ"):l11l1llCreated_By_Mucky_Duck},
					  {l11lCreated_By_Mucky_Duck (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪ࠭ࢵ"):l1111l1Created_By_Mucky_Duck}, fan_art={l11lCreated_By_Mucky_Duck (u"ࠫ࡮ࡩ࡯࡯ࠩࢶ"):l11Created_By_Mucky_Duck}, item_count=items)
	try:
		l1l1Created_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠬࡂ࡬ࡪࠢࡦࡰࡦࡹࡳ࠾ࠤࡱࡩࡽࡺࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠰࠿ࠪࠤࠣࡨࡦࡺࡡ࠮ࡥ࡬࠱ࡵࡧࡧࡪࡰࡤࡸ࡮ࡵ࡮࠮ࡲࡤ࡫ࡪࡃࠢ࠯ࠬࡂࠦࠥࡸࡥ࡭࠿ࠥࡲࡪࡾࡴࠣࡀࠪࢷ")).findall(link)[0]
		md.addDir({l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࢸ"): l11lCreated_By_Mucky_Duck (u"ࠧ࠳ࠩࢹ"), l11lCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࢺ"):l11lCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࡃࡄࡎࡦࡺࡷࠤࡕࡧࡧࡦࡀࡁࡂࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࢻ"), l11lCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࢼ"):l1l1Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࢽ"):content})
	except: pass
	if content == l11lCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࢾ"):
		setView(l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࢿ"), l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪ࠳ࡶࡪࡧࡺࠫࣀ"))
	elif content == l11lCreated_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࣁ"):
		setView(l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࣂ"), l11lCreated_By_Mucky_Duck (u"ࠪࡷ࡭ࡵࡷ࠮ࡸ࡬ࡩࡼ࠭ࣃ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l111l11Created_By_Mucky_Duck(title, url, l11l1lCreated_By_Mucky_Duck, content, l11l1llCreated_By_Mucky_Duck):
	link = open_url(url,verify=False).content
	l111lllCreated_By_Mucky_Duck = url
	l11ll1lCreated_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠫ࡮ࡪ࠺ࠡࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠫࣄ")).findall(link)[0]
	request_url = l11lCreated_By_Mucky_Duck (u"ࠬࠫࡳ࠰ࡣ࡭ࡥࡽ࠵ࡶ࠵ࡡࡰࡳࡻ࡯ࡥࡠࡧࡳ࡭ࡸࡵࡤࡦࡵ࠲ࠩࡸ࠭ࣅ") %(l11l1l1Created_By_Mucky_Duck,l11ll1lCreated_By_Mucky_Duck)
	headers = {l11lCreated_By_Mucky_Duck (u"࠭ࡁࡤࡥࡨࡴࡹ࠳ࡅ࡯ࡥࡲࡨ࡮ࡴࡧࠨࣆ"):l11lCreated_By_Mucky_Duck (u"ࠧࡨࡼ࡬ࡴ࠱ࠦࡤࡦࡨ࡯ࡥࡹ࡫ࠬࠡࡵࡧࡧ࡭࠲ࠠࡣࡴࠪࣇ"), l11lCreated_By_Mucky_Duck (u"ࠨࡔࡨࡪࡪࡸࡥࡳࠩࣈ"):l111lllCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭ࣉ"):md.User_Agent()}
	l1ll11llCreated_By_Mucky_Duck = open_url(request_url, headers=headers, verify=False).json()
	l11llllCreated_By_Mucky_Duck = md.regex_get_all(l1ll11llCreated_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠪ࡬ࡹࡳ࡬ࠨ࣊")], l11lCreated_By_Mucky_Duck (u"ࠫࠧ࡫ࡰࡪࡵࡲࡨࡪࡹ࠭ࡴࡸ࠰࠵࠵ࠨࠧ࣋"), l11lCreated_By_Mucky_Duck (u"ࠬࡂ࠯ࡶ࡮ࡁࠫ࣌"))
	l1ll1Created_By_Mucky_Duck = md.regex_get_all(str(l11llllCreated_By_Mucky_Duck), l11lCreated_By_Mucky_Duck (u"࠭࠼࡭࡫ࠪ࣍"), l11lCreated_By_Mucky_Duck (u"ࠧ࠽࠱࡯࡭ࡃ࠭࣎"))
	items = len(l1ll1Created_By_Mucky_Duck)
	for a in l1ll1Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠨࡶ࡬ࡸࡱ࡫࠽࣏ࠣࠩ"), l11lCreated_By_Mucky_Duck (u"࣐ࠩࠥࠫ"))
		name = name.replace(l11lCreated_By_Mucky_Duck (u"ࠪࡉࡵ࡯ࡳࡰࡦࡨ࣑ࠫ"),l11lCreated_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡮ࡴࡤࡪࡣࡱࡶࡪࡪ࡝ࡆࡲ࡬ࡷࡴࡪࡥ࡜࠱ࡆࡓࡑࡕࡒ࡞࣒ࠩ"))
                name = l111Created_By_Mucky_Duck.unescape(name).replace(l11lCreated_By_Mucky_Duck (u"ࠧࡢ࡜ࠨࠤ࣓"),l11lCreated_By_Mucky_Duck (u"ࠨࠧࠣࣔ"))
		l1ll111lCreated_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠧࡥࡣࡷࡥ࠲࡯ࡤ࠾ࠤࠪࣕ"), l11lCreated_By_Mucky_Duck (u"ࠨࠤࠪࣖ"))
		headers = l111lllCreated_By_Mucky_Duck + l11lCreated_By_Mucky_Duck (u"ࠩࡿࠫࣗ") + l1ll111lCreated_By_Mucky_Duck + l11lCreated_By_Mucky_Duck (u"ࠪࢀࠬࣘ") + l11ll1lCreated_By_Mucky_Duck
		url =  l11lCreated_By_Mucky_Duck (u"ࠫࠪࡹ࠯ࡢ࡬ࡤࡼ࠴ࡳ࡯ࡷ࡫ࡨࡣࡸࡵࡵࡳࡥࡨࡷ࠴ࠫࡳࠨࣙ") %(l11l1l1Created_By_Mucky_Duck,l1ll111lCreated_By_Mucky_Duck)
		try:
			l1l1ll11Created_By_Mucky_Duck = name.split(l11lCreated_By_Mucky_Duck (u"ࠬࡋࡰࡪࡵࡲࡨࡪ࠭ࣚ"))[1].strip()[:2]
		except:pass
		fan_art = {l11lCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫࣛ"):l11l1lCreated_By_Mucky_Duck}
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࣜ"): l11lCreated_By_Mucky_Duck (u"ࠨ࠹ࠪࣝ"), l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࣞ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࣟ") %name,
			   l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨ࣠"):url, l11lCreated_By_Mucky_Duck (u"ࠬ࡯ࡣࡰࡰ࡬ࡱࡦ࡭ࡥࠨ࣡"):l11l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧ࣢"):l11lCreated_By_Mucky_Duck (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࣣࠩ"), l11lCreated_By_Mucky_Duck (u"ࠨࡳࡸࡩࡷࡿࠧࣤ"):headers},
			  {l11lCreated_By_Mucky_Duck (u"ࠩࡶࡳࡷࡺࡴࡪࡶ࡯ࡩࠬࣥ"):title, l11lCreated_By_Mucky_Duck (u"ࠪࡷࡪࡧࡳࡰࡰࣦࠪ"):l11l1llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠫࡪࡶࡩࡴࡱࡧࡩࠬࣧ"):l1l1ll11Created_By_Mucky_Duck},
			  fan_art, is_folder=False, item_count=items)
	setView(l111l1lCreated_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࠧࣨ"), l11lCreated_By_Mucky_Duck (u"࠭ࡥࡱ࡫࠰ࡺ࡮࡫ࡷࠨࣩ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1l11lllCreated_By_Mucky_Duck(url, content):
	l11l11Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠧࡔࡧ࡯ࡩࡨࡺࠠࡔࡱࡵࡸࠥࡓࡥࡵࡪࡲࡨࠬ࣪"),sort)
	l111ll1Created_By_Mucky_Duck = l1l11Created_By_Mucky_Duck[l11l11Created_By_Mucky_Duck]
	link = open_url(url,verify=False).content
	match = re.compile(l11lCreated_By_Mucky_Duck (u"ࠨ࠾࡬ࡲࡵࡻࡴࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡩࡨࡲࡷ࡫࠭ࡪࡦࡶࠦࠥࡼࡡ࡭ࡷࡨࡁࠧ࠮࠮ࠫࡁࠬࠦࠥࡴࡡ࡮ࡧࡀࠦ࠳࠰࠿ࠣ࡞ࡱ࠲࠯ࡅࡴࡺࡲࡨࡁࠧࡩࡨࡦࡥ࡮ࡦࡴࡾࠢࠡࡀࠫ࠲࠯ࡅࠩ࠽࠱࡯ࡥࡧ࡫࡬࠿ࠩ࣫")).findall(link)
	for l11111Created_By_Mucky_Duck,name in match:
		name = name.replace(l11lCreated_By_Mucky_Duck (u"ࠩࠣࠫ࣬"),l11lCreated_By_Mucky_Duck (u"࣭ࠪࠫ"))
		if content == l11lCreated_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷ࣮ࠬ"):
			url = l11lCreated_By_Mucky_Duck (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࡴࡧࡵ࡭ࡪࡹ࠯ࠦࡵ࠲ࠩࡸ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨ࣯") %(l11l1l1Created_By_Mucky_Duck,l111ll1Created_By_Mucky_Duck,l11111Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࣰࠫ"): l11lCreated_By_Mucky_Duck (u"ࠧ࠳ࣱࠩ"), l11lCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪࣲ࠭"):l11lCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩࣳ") %name, l11lCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࣴ"):url, l11lCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࣵ"):content})
		elif content == l11lCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࣶࠬ"):
			url = l11lCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰࡯ࡲࡺ࡮࡫࠯ࠦࡵ࠲ࠩࡸ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨࣷ") %(l11l1l1Created_By_Mucky_Duck,l111ll1Created_By_Mucky_Duck,l11111Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࣸ"): l11lCreated_By_Mucky_Duck (u"ࠨ࠴ࣹࠪ"), l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࣺࠧ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢ࡬ࡲࡩ࡯ࡡ࡯ࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࣻ") %name, l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࣼ"):url, l11lCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࣽ"):content})
	setView(l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࡷࠬࣾ"), l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪࣿ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l11llCreated_By_Mucky_Duck(url, content):
	l11l11Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠨࡕࡨࡰࡪࡩࡴࠡࡕࡲࡶࡹࠦࡍࡦࡶ࡫ࡳࡩ࠭ऀ"),sort)
	l111ll1Created_By_Mucky_Duck = l1l11Created_By_Mucky_Duck[l11l11Created_By_Mucky_Duck]
	l1l111Created_By_Mucky_Duck = md.numeric_select(l11lCreated_By_Mucky_Duck (u"ࠩࡈࡲࡹ࡫ࡲ࡛ࠡࡨࡥࡷ࠭ँ"), l11lCreated_By_Mucky_Duck (u"ࠪ࠶࠵࠷࠷ࠨं"))
	if content == l11lCreated_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬः"):
		l1ll11Created_By_Mucky_Duck(l11lCreated_By_Mucky_Duck (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࡴࡧࡵ࡭ࡪࡹ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨऄ") %(l11l1l1Created_By_Mucky_Duck,l111ll1Created_By_Mucky_Duck,l1l111Created_By_Mucky_Duck), content)
	elif content == l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭अ"):
		l1ll11Created_By_Mucky_Duck(l11lCreated_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳ࠱ࡰࡳࡻ࡯ࡥ࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࠫࡳ࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࠩआ") %(l11l1l1Created_By_Mucky_Duck,l111ll1Created_By_Mucky_Duck,l1l111Created_By_Mucky_Duck), content)
	setView(l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨࡨ࡬ࡰࡪࡹࠧइ"), l11lCreated_By_Mucky_Duck (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬई"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1llllCreated_By_Mucky_Duck():
	link = open_url(l11lCreated_By_Mucky_Duck (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡵࡧࡳࡵࡧࡥ࡭ࡳ࠴ࡣࡰ࡯࠲ࡶࡦࡽ࠯ࡄࡨ࠷ࡇ࠸ࡻࡈ࠲ࠩउ")).content
	version = re.findall(l11lCreated_By_Mucky_Duck (u"ࡶࠬࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠡࠤࠫ࡟ࡣࠨ࡝ࠬࠫࠥࠫऊ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l11lCreated_By_Mucky_Duck (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࡳࡤࡴ࡬ࡴࡹ࠴࡭ࡰࡦࡸࡰࡪ࠴࡭ࡶࡥ࡮ࡽࡸ࠴ࡣࡰ࡯ࡰࡳࡳ࠵ࡡࡥࡦࡲࡲ࠳ࡾ࡭࡭ࠩऋ")), l11lCreated_By_Mucky_Duck (u"࠭ࡲࠬࠩऌ")) as f:
		l111llCreated_By_Mucky_Duck = f.read()
		if re.search(l11lCreated_By_Mucky_Duck (u"ࡲࠨࡸࡨࡶࡸ࡯࡯࡯࠿ࠥࠩࡸࠨࠧऍ") %version, l111llCreated_By_Mucky_Duck):
			l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠨࡘࡨࡶࡸ࡯࡯࡯ࠢࡆ࡬ࡪࡩ࡫ࠡࡑࡎࠫऎ"))
		else:
			l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠤ࡚ࡶࡴࡴࡧࠡࡘࡨࡶࡸ࡯࡯࡯ࠢࡒࡪࠥࡓࡵࡤ࡭ࡼࡷࠥࡉ࡯࡮࡯ࡲࡲࠥࡓ࡯ࡥࡷ࡯ࡩࠧए")
			l1ll1lllCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠥࡔࡱ࡫ࡡࡴࡧࠣࡍࡳࡹࡴࡢ࡮࡯ࠤࡈࡵࡲࡳࡧࡦࡸࠥ࡜ࡥࡳࡵ࡬ࡳࡳࠦࡆࡳࡱࡰࠤ࡙࡮ࡥࠡࡔࡨࡴࡴࠨऐ")
			l1lll111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠦࡅࡡࡃࡐࡎࡒࡖࠥ࡯࡮ࡥ࡫ࡤࡲࡷ࡫ࡤ࡞ࡪࡷࡸࡵࡀ࠯࠰࡯ࡸࡧࡰࡿࡳ࠯࡯ࡨࡨ࡮ࡧࡰࡰࡴࡷࡥࡱ࠺࡫ࡰࡦ࡬࠲ࡲࡲ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣऑ")
			l111Created_By_Mucky_Duck.show_ok_dialog([l1Created_By_Mucky_Duck, l1ll1lllCreated_By_Mucky_Duck, l1lll111Created_By_Mucky_Duck], l1lllCreated_By_Mucky_Duck)
			xbmc.executebuiltin(l11lCreated_By_Mucky_Duck (u"ࠧ࡞ࡂࡎࡅ࠱ࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡕࡱࡦࡤࡸࡪ࠮ࡰࡢࡶ࡫࠰ࡷ࡫ࡰ࡭ࡣࡦࡩ࠮ࠨऒ"))
			xbmc.executebuiltin(l11lCreated_By_Mucky_Duck (u"ࠨࡘࡃࡏࡆ࠲ࡆࡩࡴࡪࡸࡤࡸࡪ࡝ࡩ࡯ࡦࡲࡻ࠭ࡎ࡯࡮ࡧࠬࠦओ"))
def l1l1l1Created_By_Mucky_Duck(url, content):
	l11l11Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠧࡔࡧ࡯ࡩࡨࡺࠠࡔࡱࡵࡸࠥࡓࡥࡵࡪࡲࡨࠬऔ"),sort)
	l111ll1Created_By_Mucky_Duck = l1l11Created_By_Mucky_Duck[l11l11Created_By_Mucky_Duck]
	link = open_url(url,verify=False).content
	match=re.compile(l11lCreated_By_Mucky_Duck (u"ࠨ࠾࡬ࡲࡵࡻࡴࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡥࡲࡹࡳࡺࡲࡺ࠯࡬ࡨࡸࠨࠠࡷࡣ࡯ࡹࡪࡃࠢࠩ࠰࠭ࡃ࠮ࠨࠠ࡯ࡣࡰࡩࡂࠨ࠮ࠫࡁࠥࡠࡳ࠴ࠪࡀࡶࡼࡴࡪࡃࠢࡤࡪࡨࡧࡰࡨ࡯ࡹࠤࠣࡂ࠭࠴ࠪࡀࠫ࠿࠳ࡱࡧࡢࡦ࡮ࡁࠫक")).findall(link)
	for l1llll1Created_By_Mucky_Duck,name in match:
		name = name.replace(l11lCreated_By_Mucky_Duck (u"ࠩࠣࠫख"),l11lCreated_By_Mucky_Duck (u"ࠪࠫग"))
		if content == l11lCreated_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬघ"):
			url = l11lCreated_By_Mucky_Duck (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࡴࡧࡵ࡭ࡪࡹ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨङ") %(l11l1l1Created_By_Mucky_Duck,l111ll1Created_By_Mucky_Duck,l1llll1Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫच"): l11lCreated_By_Mucky_Duck (u"ࠧ࠳ࠩछ"), l11lCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ज"):l11lCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡ࡫ࡱࡨ࡮ࡧ࡮ࡳࡧࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩझ") %name, l11lCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧञ"):url, l11lCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬट"):content})
		elif content == l11lCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬठ"):
			url = l11lCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰࡯ࡲࡺ࡮࡫࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࠦࡵ࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨड") %(l11l1l1Created_By_Mucky_Duck,l111ll1Created_By_Mucky_Duck,l1llll1Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬढ"): l11lCreated_By_Mucky_Duck (u"ࠨ࠴ࠪण"), l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧत"):l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢ࡬ࡲࡩ࡯ࡡ࡯ࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪथ") %name, l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨद"):url, l11lCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ध"):content})
	setView(l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࡷࠬन"), l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪऩ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l11lllCreated_By_Mucky_Duck(content, query):
	try:
		if query:
			search = query.replace(l11lCreated_By_Mucky_Duck (u"ࠨࠢࠪप"),l11lCreated_By_Mucky_Duck (u"ࠩ࠮ࠫफ"))
		else:
			search = md.search()
			if search == l11lCreated_By_Mucky_Duck (u"ࠪࠫब"):
				md.notification(l11lCreated_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟࡞ࡆࡢࡋࡍࡑࡖ࡜ࠤࡖ࡛ࡅࡓ࡛࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝࠭ࡃࡥࡳࡷࡺࡩ࡯ࡩࠣࡷࡪࡧࡲࡤࡪࠪभ"),l1l1ll1lCreated_By_Mucky_Duck)
				return
			else:
				pass
		url = l11lCreated_By_Mucky_Duck (u"ࠬࠫࡳ࠰࡯ࡲࡺ࡮࡫࠯ࡴࡧࡤࡶࡨ࡮࠯ࠦࡵࠪम") %(l11l1l1Created_By_Mucky_Duck,search)
		l1ll11Created_By_Mucky_Duck(url,content)
	except:
		md.notification(l11lCreated_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࡠࡈ࡝ࡔࡱࡵࡶࡾࠦࡎࡰࠢࡕࡩࡸࡻ࡬ࡵࡵ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨय"),l1l1ll1lCreated_By_Mucky_Duck)
def l1lllll1Created_By_Mucky_Duck():
        l1l111lCreated_By_Mucky_Duck = [l11lCreated_By_Mucky_Duck (u"ࠧࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼ࠲ࡲࡧࡦࠨर"), l11lCreated_By_Mucky_Duck (u"ࠨࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡰࡥ࡫ࡽࡩࡻࡣࡵࡨࠬऱ"), l11lCreated_By_Mucky_Duck (u"ࠩࡳࡰࡺ࡭ࡩ࡯࠰ࡹ࡭ࡩ࡫࡯࠯࡭ࡵࡥࡹࡵࡳࠨल"),
                    l11lCreated_By_Mucky_Duck (u"ࠪࡶࡪࡶ࡯ࡴ࡫ࡷࡳࡷࡿ࠮ࡢࡰࡲࡲࡾࡳ࡯ࡶࡵࡷࡶࡺࡺࡨࠨळ"), l11lCreated_By_Mucky_Duck (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡵࡸ࡯ࡨࡴࡤࡱ࠳ࡧ࡮ࡰࡰࡼࡱࡴࡻࡳࡵࡴࡸࡸ࡭࠭ऴ"),
                    l11lCreated_By_Mucky_Duck (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡰࡸࡡࡵࡱࡶࡪࡺࡩ࡫ࡴࡦࡸࡧࡰࡿࠧव"), l11lCreated_By_Mucky_Duck (u"࠭ࡳࡤࡴ࡬ࡴࡹ࠴࡫ࡳࡣࡷࡳࡸ࡬ࡵࡤ࡭ࡶࡨࡺࡩ࡫ࡺ࠰ࡤࡶࡹࡽ࡯ࡳ࡭ࠪश"),
                    l11lCreated_By_Mucky_Duck (u"ࠧࡴࡥࡵ࡭ࡵࡺ࠮࡬ࡴࡤࡸࡴࡹࡦࡶࡥ࡮ࡷࡩࡻࡣ࡬ࡻ࠱ࡱࡪࡺࡡࡥࡣࡷࡥࠬष"), l11lCreated_By_Mucky_Duck (u"ࠨࡵࡦࡶ࡮ࡶࡴ࠯࡯ࡲࡨࡺࡲࡥ࠯ࡩ࡬࡫࡬࡯ࡴࡺࠩस")]
        l1lllll1Created_By_Mucky_Duck = any(xbmc.getCondVisibility(l11lCreated_By_Mucky_Duck (u"ࠩࡖࡽࡸࡺࡥ࡮࠰ࡋࡥࡸࡇࡤࡥࡱࡱࠬࠪࡹࠩࠨह") % (l111Created_By_Mucky_Duck)) for l111Created_By_Mucky_Duck in l1l111lCreated_By_Mucky_Duck)
        if l1lllll1Created_By_Mucky_Duck:
                l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪ࡝ࡴࡻࠠࡉࡣࡹࡩࠥࡏ࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡃࡧࡨࡴࡴࡳࠨऺ")
                l1ll1lllCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࡙ࠫ࡮ࡡࡵࠢࡐࡹࡨࡱࡹࠡࡆࡸࡧࡰࠦࡄࡰࡧࡶࠤࡓࡵࡴࠨऻ")
                l1lll111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࡙ࠬࡵࡱࡲࡲࡶࡹࠦࡁ࡯ࡦ࡛ࠣ࡮ࡲ࡬ࠡࡐࡲࡻࠥࡘࡥ࡮ࡱࡹࡩ़ࠬ")
                l1lll11lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࠭ࡒࡦ࡯ࡲࡺࡪࡪࠠࡂࡰࡲࡲࡾࡳ࡯ࡶࡵࠣࡖࡪࡶ࡯ࠡࡃࡱࡨࠥࡇࡤࡥࡱࡱࡷࠬऽ")
                l1lll1l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡐ࡭ࡧࡤࡷࡪࠦࡄࡰࡰࡷࠤࡘࡻࡰࡱࡱࡵࡸࠥࡏࡤࡪࡱࡷࡷࠬा")
                l1lll1llCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠨࡔࡨࡱࡴࡼࡥࡥࠢࠨࡷࠬि") %l1lllCreated_By_Mucky_Duck
                l1llll11Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠩࡘࡲ࡫ࡵࡲࡵࡷࡱࡥࡹ࡫࡬ࡺࠢ࡜ࡳࡺࠦࡓࡶࡲࡳࡳࡷࡺࠠࡊࡦ࡬ࡳࡹࡹࠧी")
                l111Created_By_Mucky_Duck.show_ok_dialog([l1Created_By_Mucky_Duck, l1ll1lllCreated_By_Mucky_Duck, l1lll111Created_By_Mucky_Duck], l1lllCreated_By_Mucky_Duck)
                l1lll1lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪ࡝ࡴࡻࡲࠡࡅ࡫ࡳ࡮ࡩࡥࠡࡇ࡬ࡸ࡭࡫ࡲࠡࡗࡱ࡭ࡳࡹࡴࡢ࡮࡯ࠤࠪࡹࠠࡐࡴ࡙ࠣࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡔࡩࡧࠣࡅࡳࡵ࡮ࡺ࡯ࡲࡹࡸࠦࡒࡦࡲࡲࠤ࠰ࠦࡁࡥࡦࡲࡲࡸ࠭ु") %l1lllCreated_By_Mucky_Duck
                if md.dialog_yesno(l1lll1lCreated_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠫࡆࡴ࡯࡯ࡻࡰࡳࡺࡹࠧू"),l1lllCreated_By_Mucky_Duck):
                        l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠬࡃ࠽࠾ࡆࡈࡐࡊ࡚ࡉࡏࡉࡀࡁࡂࡇࡎࡐࡐ࡜ࡑࡔ࡛ࡓ࠾࠿ࡀࡅࡉࡊࡏࡏࡕࡀࡁࡂ࠱࠽࠾࠿ࡕࡉࡕࡕ࠽࠾࠿ࠪृ"))
                        for root, dirs, files in os.walk(xbmc.translatePath(l11lCreated_By_Mucky_Duck (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹࠧॄ"))):
                                dirs[:] = [d for d in dirs if d in l1l111lCreated_By_Mucky_Duck]
                                for d in dirs:
                                        try:
                                                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                                        except OSError:
                                                pass
                        l111Created_By_Mucky_Duck.show_ok_dialog([l1lll11lCreated_By_Mucky_Duck, l1lll1l1Created_By_Mucky_Duck], l1lllCreated_By_Mucky_Duck)
                else:
                        l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠧ࠾࠿ࡀࡈࡊࡒࡅࡕࡋࡑࡋࡂࡃ࠽ࠦࡵࡀࡁࡂ࠭ॅ") %l1lllCreated_By_Mucky_Duck)
                        llCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_path()
			shutil.rmtree(llCreated_By_Mucky_Duck, ignore_errors=True)
			l111Created_By_Mucky_Duck.show_ok_dialog([l1lll1llCreated_By_Mucky_Duck, l1llll11Created_By_Mucky_Duck], l1lllCreated_By_Mucky_Duck)
                time.sleep(2)
                os._exit(0)
def __1l1lll1Created_By_Mucky_Duck(data):
	l1ll111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠨࠩॆ")
	l1l1lllCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠩࠪे")
	try:
	    data = l11lCreated_By_Mucky_Duck (u"ࠪࠬࠬै") + data.split(l11lCreated_By_Mucky_Duck (u"ࠦ࠭ࡥࠤࠥࠫࠬࠤ࠭࠭࡟ࠨࠫ࠾ࠦॉ"))[0].split(l11lCreated_By_Mucky_Duck (u"ࠧ࠵ࠪࠡࡢࠧࠨࡥࠦࠪ࠰ࠤॊ"))[-1].strip()
	    data = data.replace(l11lCreated_By_Mucky_Duck (u"࠭ࠨࡠࡡࠧ࠭ࡠࠪࠤࠥ࡟ࠪो"), l11lCreated_By_Mucky_Duck (u"ࠧ࡝ࠩࠥࡠࠬ࠭ौ"))
	    data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠨࠪࡢࡣࠩ࠯࡛ࡠࠦࡠ्ࠫ"), l11lCreated_By_Mucky_Duck (u"ࠩࠥࡠࡡࡢ࡜ࠣࠩॎ"))
	    data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠪࠬࡴࡤ࡟࡟ࡱࠬࠫॏ"), l11lCreated_By_Mucky_Duck (u"ࠫ࠸࠭ॐ"))
	    data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠬ࠮ࡣ࡟ࡡࡡࡳ࠮࠭॑"), l11lCreated_By_Mucky_Duck (u"࠭࠰ࠨ॒"))
	    data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠧࠩࡡࠧࠨ࠮࠭॓"), l11lCreated_By_Mucky_Duck (u"ࠨ࠳ࠪ॔"))
	    data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠩࠫࠨࠩࡥࠩࠨॕ"), l11lCreated_By_Mucky_Duck (u"ࠪ࠸ࠬॖ"))
	    code = l11lCreated_By_Mucky_Duck (u"ࠫࠬ࠭ࡤࡦࡨࠣࡶࡪࡺࡁࠩࠫ࠽ࠎࠥࠦࠠࠡࡥ࡯ࡥࡸࡹࠠࡊࡰࡩ࡭ࡽࡀࠊࠊࡦࡨࡪࠥࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠨࡴࡧ࡯ࡪ࠱ࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠪ࠼ࠍࠍࠥࠦࠠࠡࡵࡨࡰ࡫࠴ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࠿ࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠏࠏࡤࡦࡨࠣࡣࡤࡸ࡯ࡳࡡࡢࠬࡸ࡫࡬ࡧ࠮ࠣࡳࡹ࡮ࡥࡳࠫ࠽ࠎࠎࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡌࡲ࡫࡯ࡸࠩ࡮ࡤࡱࡧࡪࡡࠡࡺ࠯ࠤࡸ࡫࡬ࡧ࠿ࡶࡩࡱ࡬ࠬࠡࡱࡷ࡬ࡪࡸ࠽ࡰࡶ࡫ࡩࡷࡀࠠࡴࡧ࡯ࡪ࠳࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠨࡰࡶ࡫ࡩࡷ࠲ࠠࡹࠫࠬࠎࠎࡪࡥࡧࠢࡢࡣࡴࡸ࡟ࡠࠪࡶࡩࡱ࡬ࠬࠡࡱࡷ࡬ࡪࡸࠩ࠻ࠌࠌࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠࡴࡧ࡯ࡪ࠳࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠨࡰࡶ࡫ࡩࡷ࠯ࠊࠊࡦࡨࡪࠥࡥ࡟ࡳ࡮ࡶ࡬࡮࡬ࡴࡠࡡࠫࡷࡪࡲࡦ࠭ࠢࡲࡸ࡭࡫ࡲࠪ࠼ࠍࠍࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡋࡱࡪ࡮ࡾࠨ࡭ࡣࡰࡦࡩࡧࠠࡹ࠮ࠣࡷࡪࡲࡦ࠾ࡵࡨࡰ࡫࠲ࠠࡰࡶ࡫ࡩࡷࡃ࡯ࡵࡪࡨࡶ࠿ࠦࡳࡦ࡮ࡩ࠲࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮࡯ࡵࡪࡨࡶ࠱ࠦࡸࠪࠫࠍࠍࡩ࡫ࡦࠡࡡࡢࡶࡸ࡮ࡩࡧࡶࡢࡣ࠭ࡹࡥ࡭ࡨ࠯ࠤࡴࡺࡨࡦࡴࠬ࠾ࠏࠏࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡷࡪࡲࡦ࠯ࡨࡸࡲࡨࡺࡩࡰࡰࠫࡳࡹ࡮ࡥࡳࠫࠍࠍࡩ࡫ࡦࠡࡡࡢࡧࡦࡲ࡬ࡠࡡࠫࡷࡪࡲࡦ࠭ࠢࡹࡥࡱࡻࡥ࠲࠮ࠣࡺࡦࡲࡵࡦ࠴ࠬ࠾ࠏࠏࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡷࡪࡲࡦ࠯ࡨࡸࡲࡨࡺࡩࡰࡰࠫࡺࡦࡲࡵࡦ࠳࠯ࠤࡻࡧ࡬ࡶࡧ࠵࠭ࠏࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡺࡡࡤࡨࡩ࠮ࡸ࠭ࠢࡼ࠭࠿ࠐࠉࡵࡴࡼ࠾ࠥࡸࡥࡵࡷࡵࡲࠥࡾࠠࠬࠢࡼࠎࠎ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡵࡩࡹࡻࡲ࡯ࠢࡶࡸࡷ࠮ࡸࠪࠢ࠮ࠤࡸࡺࡲࠩࡻࠬࠎࠥࠦࠠࠡࡺࠣࡁࠥࡏ࡮ࡧ࡫ࡻࠬࡲࡿ࡟ࡢࡦࡧ࠭ࠏࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࠨࡷࠏࡶࡡࡳࡣࡰࠤࡂࠦࡲࡦࡶࡄࠬ࠮࠭ࠧࠨॗ")
	    l1l1l1llCreated_By_Mucky_Duck = {l11lCreated_By_Mucky_Duck (u"ࠧࡥ࡟ࡣࡷ࡬ࡰࡹ࡯࡮ࡴࡡࡢࠦक़"): None, l11lCreated_By_Mucky_Duck (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨख़"):__name__, l11lCreated_By_Mucky_Duck (u"ࠧࡴࡶࡵࠫग़"):str, l11lCreated_By_Mucky_Duck (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫज़"):Exception}
	    l1l11llCreated_By_Mucky_Duck = { l11lCreated_By_Mucky_Duck (u"ࠩࡳࡥࡷࡧ࡭ࠨड़"): None }
	    exec( code % data.replace(l11lCreated_By_Mucky_Duck (u"ࠪ࠯ࠬढ़"),l11lCreated_By_Mucky_Duck (u"ࠫࢁࡾࡼࠨफ़")), l1l1l1llCreated_By_Mucky_Duck, l1l11llCreated_By_Mucky_Duck)
	    data = l1l11llCreated_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠬࡶࡡࡳࡣࡰࠫय़")].decode(l11lCreated_By_Mucky_Duck (u"࠭ࡳࡵࡴ࡬ࡲ࡬ࡥࡥࡴࡥࡤࡴࡪ࠭ॠ"))
	    data = re.compile(l11lCreated_By_Mucky_Duck (u"ࠧࠨࠩࡀ࡟ࠬࠨ࡝ࠩ࡝ࡡࠦࡣ࠭࡝ࠬࡁࠬ࡟ࠬࠨ࡝ࠨࠩࠪॡ")).findall(data)
	    l1ll111Created_By_Mucky_Duck = data[0]
	    l1l1lllCreated_By_Mucky_Duck = data[1]
	except Exception as e:
	    l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡹ࠱ࡼࠤࡩ࡫ࡣࡰࡦࡨࠤ࠭࠷ࠩࠨॢ"))
	return {l11lCreated_By_Mucky_Duck (u"ࠩࡻࠫॣ"): x, l11lCreated_By_Mucky_Duck (u"ࠪࡽࠬ।"): y}
def __1l1llllCreated_By_Mucky_Duck(script):
	try:
	    l111l1Created_By_Mucky_Duck = jsunfuck.l11l1Created_By_Mucky_Duck(script).decode()
	    x = re.search(l11lCreated_By_Mucky_Duck (u"ࠫࠬ࠭࡟ࡹ࠿࡞ࠫࠧࡣࠨ࡜ࡠࠥࠫࡢ࠱ࠩࠨࠩࠪ॥"), l111l1Created_By_Mucky_Duck).group(1)
	    y = re.search(l11lCreated_By_Mucky_Duck (u"ࠬ࠭ࠧࡠࡻࡀ࡟ࠬࠨ࡝ࠩ࡝ࡡࠦࠬࡣࠫࠪࠩࠪࠫ०"), l111l1Created_By_Mucky_Duck).group(1)
	    return {l11lCreated_By_Mucky_Duck (u"࠭ࡸࠨ१"): x, l11lCreated_By_Mucky_Duck (u"ࠧࡺࠩ२"): y}
	except Exception as e:
	    l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡹ࠱ࡼࠤࡩ࡫ࡣࡰࡦࡨࠤ࠭࠸ࠩࠨ३"))
def __1ll1111Created_By_Mucky_Duck(script):
	try:
	    l1ll111Created_By_Mucky_Duck = re.search(l11lCreated_By_Mucky_Duck (u"ࠩࠪࠫࡤࡾ࠽࡜ࠩࠥࡡ࠭ࡡ࡞ࠣࠩࡠ࠯࠮࠭ࠧࠨ४"), script).group(1)
	    l1l1lllCreated_By_Mucky_Duck = re.search(l11lCreated_By_Mucky_Duck (u"ࠪࠫࠬࡥࡹ࠾࡝ࠪࠦࡢ࠮࡛࡟ࠤࠪࡡ࠰࠯ࠧࠨࠩ५"), script).group(1)
	    return {l11lCreated_By_Mucky_Duck (u"ࠫࡽ࠭६"): l1ll111Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠬࡿࠧ७"): l1l1lllCreated_By_Mucky_Duck}
	except Exception as e:
	    l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡾࡸ࠰ࡺࡼࠤࡩ࡫ࡣࡰࡦࡨࠤ࠭࠹ࠩࠨ८"))
def l1111Created_By_Mucky_Duck(url,name,l11l1lCreated_By_Mucky_Duck,content,l111lCreated_By_Mucky_Duck,query):
	if content == l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧ९"):
		link = open_url(url,verify=False).content
		l111lllCreated_By_Mucky_Duck = url
		headers = {l11lCreated_By_Mucky_Duck (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬ॰"):md.User_Agent()}
		link = open_url(url, headers=headers).content
		l11ll1lCreated_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠩ࡬ࡨ࠿ࠦࠢࠩ࡝ࡡࠦࡢ࠱ࠩࠣࠩॱ")).findall(link)[0]
		request_url = l11lCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡻ࠺࡟࡮ࡱࡹ࡭ࡪࡥࡥࡱ࡫ࡶࡳࡩ࡫ࡳ࠰ࠧࡶࠫॲ") %(l11l1l1Created_By_Mucky_Duck,l11ll1lCreated_By_Mucky_Duck)
		headers = {l11lCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷ࠱ࡊࡴࡣࡰࡦ࡬ࡲ࡬࠭ॳ"):l11lCreated_By_Mucky_Duck (u"ࠬ࡭ࡺࡪࡲ࠯ࠤࡩ࡫ࡦ࡭ࡣࡷࡩ࠱ࠦࡳࡥࡥ࡫࠰ࠥࡨࡲࠨॴ"), l11lCreated_By_Mucky_Duck (u"࠭ࡒࡦࡨࡨࡶࡪࡸࠧॵ"):l111lllCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫॶ"):md.User_Agent()}
		l1ll11llCreated_By_Mucky_Duck = open_url(request_url, headers=headers, verify=False).json()
		l1ll111lCreated_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠨࡦࡤࡸࡦ࠳ࡳࡦࡴࡹࡩࡷࡃࠢ࠲࠲ࠥࠤࡩࡧࡴࡢ࠯࡬ࡨࡂࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨॷ")).findall(l1ll11llCreated_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡲࡲࠧॸ")])[0]
	else:
		l111lllCreated_By_Mucky_Duck = query.split(l11lCreated_By_Mucky_Duck (u"ࠪࢀࠬॹ"))[0]
		l1ll111lCreated_By_Mucky_Duck = query.split(l11lCreated_By_Mucky_Duck (u"ࠫࢁ࠭ॺ"))[1]
		l11ll1lCreated_By_Mucky_Duck = query.split(l11lCreated_By_Mucky_Duck (u"ࠬࢂࠧॻ"))[2]
	l1ll1ll1Created_By_Mucky_Duck = int(time.time() * 10000)
        l1lllllCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡤ࡮ࡦࡾ࠯࡮ࡱࡹ࡭ࡪࡥࡴࡰ࡭ࡨࡲࠬॼ") %l11l1l1Created_By_Mucky_Duck
        params = {l11lCreated_By_Mucky_Duck (u"ࠧࡦ࡫ࡧࠫॽ"):l1ll111lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨ࡯࡬ࡨࠬॾ"):l11ll1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠩࡢࠫॿ"):l1ll1ll1Created_By_Mucky_Duck}
        headers = {l11lCreated_By_Mucky_Duck (u"ࠪࡅࡨࡩࡥࡱࡶࠪঀ"):l11lCreated_By_Mucky_Duck (u"ࠫࡹ࡫ࡸࡵ࠱࡭ࡥࡻࡧࡳࡤࡴ࡬ࡴࡹ࠲ࠠࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡡࡷࡣࡶࡧࡷ࡯ࡰࡵ࠮ࠣࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡧࡦࡱࡦࡹࡣࡳ࡫ࡳࡸ࠱ࠦࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡥࡤ࡯ࡤࡷࡨࡸࡩࡱࡶ࠯ࠤ࠯࠵ࠪ࠼ࠢࡴࡁ࠵࠴࠰࠲ࠩঁ"),
                   l11lCreated_By_Mucky_Duck (u"ࠬࡇࡣࡤࡧࡳࡸ࠲ࡋ࡮ࡤࡱࡧ࡭ࡳ࡭ࠧং"):l11lCreated_By_Mucky_Duck (u"࠭ࡧࡻ࡫ࡳ࠰ࠥࡪࡥࡧ࡮ࡤࡸࡪ࠲ࠠࡴࡦࡦ࡬࠱ࠦࡢࡳࠩঃ"), l11lCreated_By_Mucky_Duck (u"ࠧࡂࡥࡦࡩࡵࡺ࠭ࡍࡣࡱ࡫ࡺࡧࡧࡦࠩ঄"):l11lCreated_By_Mucky_Duck (u"ࠨࡧࡱ࠱࡚࡙ࠬࡦࡰ࠾ࡵࡂ࠶࠮࠹ࠩঅ"),
                   l11lCreated_By_Mucky_Duck (u"ࠩࡕࡩ࡫࡫ࡲࡦࡴࠪআ"):l111lllCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧই"):md.User_Agent(), l11lCreated_By_Mucky_Duck (u"ࠫ࡝࠳ࡒࡦࡳࡸࡩࡸࡺࡥࡥ࠯࡚࡭ࡹ࡮ࠧঈ"):l11lCreated_By_Mucky_Duck (u"ࠬ࡞ࡍࡍࡊࡷࡸࡵࡘࡥࡲࡷࡨࡷࡹ࠭উ")}
        data = open_url(l1lllllCreated_By_Mucky_Duck, params=params, headers=headers, verify=False).content
	if l11lCreated_By_Mucky_Duck (u"࠭ࠤࡠࠦࠪঊ") in data:
	    params = __1l1lll1Created_By_Mucky_Duck(data)
	elif data.startswith(l11lCreated_By_Mucky_Duck (u"ࠧ࡜࡟ࠪঋ")) and data.endswith(l11lCreated_By_Mucky_Duck (u"ࠨࠪࠬࠫঌ")):
	    params = __1l1llllCreated_By_Mucky_Duck(data)
	else:
	    params = __1ll1111Created_By_Mucky_Duck(data)
	if params is None:
	    l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠩࡘࡲࡷ࡫ࡣࡰࡩࡱ࡭ࡿ࡫ࡤࠡ࡬ࡶࠤ࡮ࡴࠠࠦࡵࠪ঍") % (l1lllllCreated_By_Mucky_Duck))
        l1ll1l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡲࡵࡶࡪࡧࡢࡷࡴࡻࡲࡤࡧࡶ࠳ࠪࡹࠧ঎") %(l11l1l1Created_By_Mucky_Duck,l1ll111lCreated_By_Mucky_Duck)
	headers = {l11lCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷࠫএ"):l11lCreated_By_Mucky_Duck (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮࠭ࠢࡷࡩࡽࡺ࠯࡫ࡣࡹࡥࡸࡩࡲࡪࡲࡷ࠰ࠥ࠰࠯ࠫ࠽ࠣࡵࡂ࠶࠮࠱࠳ࠪঐ"),
		   l11lCreated_By_Mucky_Duck (u"࠭ࡁࡤࡥࡨࡴࡹ࠳ࡅ࡯ࡥࡲࡨ࡮ࡴࡧࠨ঑"):l11lCreated_By_Mucky_Duck (u"ࠧࡨࡼ࡬ࡴ࠱ࠦࡤࡦࡨ࡯ࡥࡹ࡫ࠬࠡࡵࡧࡧ࡭࠲ࠠࡣࡴࠪ঒"), l11lCreated_By_Mucky_Duck (u"ࠨࡃࡦࡧࡪࡶࡴ࠮ࡎࡤࡲ࡬ࡻࡡࡨࡧࠪও"):l11lCreated_By_Mucky_Duck (u"ࠩࡨࡲ࠲࡛ࡓ࠭ࡧࡱ࠿ࡶࡃ࠰࠯࠺ࠪঔ"),
		   l11lCreated_By_Mucky_Duck (u"ࠪࡖࡪ࡬ࡥࡳࡧࡵࠫক"):l111lllCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨখ"):md.User_Agent(), l11lCreated_By_Mucky_Duck (u"ࠬ࡞࠭ࡓࡧࡴࡹࡪࡹࡴࡦࡦ࠰࡛࡮ࡺࡨࠨগ"):l11lCreated_By_Mucky_Duck (u"࠭ࡘࡎࡎࡋࡸࡹࡶࡒࡦࡳࡸࡩࡸࡺࠧঘ")}
	final = open_url(l1ll1l1Created_By_Mucky_Duck, params=params, headers=headers, verify=False).json()
	l1111lCreated_By_Mucky_Duck = []
	l1lll11Created_By_Mucky_Duck = []
	l1l1l11Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧࠨঙ")
	if l1l1ll1Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭চ"):
		url = max(final[l11lCreated_By_Mucky_Duck (u"ࠩࡳࡰࡦࡿ࡬ࡪࡵࡷࠫছ")][0][l11lCreated_By_Mucky_Duck (u"ࠪࡷࡴࡻࡲࡤࡧࡶࠫজ")], key=lambda l1ll11l1Created_By_Mucky_Duck: int(re.sub(l11lCreated_By_Mucky_Duck (u"ࠫࡡࡊࠧঝ"), l11lCreated_By_Mucky_Duck (u"ࠬ࠭ঞ"), l1ll11l1Created_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"࠭࡬ࡢࡤࡨࡰࠬট")])))
		url = url[l11lCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࠬঠ")]
	else:
		match = final[l11lCreated_By_Mucky_Duck (u"ࠨࡲ࡯ࡥࡾࡲࡩࡴࡶࠪড")][0][l11lCreated_By_Mucky_Duck (u"ࠩࡶࡳࡺࡸࡣࡦࡵࠪঢ")]
		for a in match:
			l1l1l11Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢ࡬ࡲࡩ࡯ࡡ࡯ࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪণ") %a[l11lCreated_By_Mucky_Duck (u"ࠫࡱࡧࡢࡦ࡮ࠪত")]
			l1111lCreated_By_Mucky_Duck.append(l1l1l11Created_By_Mucky_Duck)
			l1lll11Created_By_Mucky_Duck.append(a[l11lCreated_By_Mucky_Duck (u"ࠬ࡬ࡩ࡭ࡧࠪথ")])
		if len(match) >1:
			l11l11Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"࠭ࡓࡦ࡮ࡨࡧࡹࠦࡓࡵࡴࡨࡥࡲࠦࡑࡶࡣ࡯࡭ࡹࡿࠧদ"),l1111lCreated_By_Mucky_Duck)
			if l11l11Created_By_Mucky_Duck == -1:
				return
			elif l11l11Created_By_Mucky_Duck > -1:
				url = l1lll11Created_By_Mucky_Duck[l11l11Created_By_Mucky_Duck]
		else:
			url = final[l11lCreated_By_Mucky_Duck (u"ࠧࡱ࡮ࡤࡽࡱ࡯ࡳࡵࠩধ")][0][l11lCreated_By_Mucky_Duck (u"ࠨࡵࡲࡹࡷࡩࡥࡴࠩন")][0][l11lCreated_By_Mucky_Duck (u"ࠩࡩ࡭ࡱ࡫ࠧ঩")]
	md.resolved(url, name, fan_art, l111lCreated_By_Mucky_Duck)
	l111Created_By_Mucky_Duck.end_of_directory()
md.check_source()
mode = md.args[l11lCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨপ")]
url = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨফ"), None)
name = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪব"), None)
query = md.args.get(l11lCreated_By_Mucky_Duck (u"࠭ࡱࡶࡧࡵࡽࠬভ"), None)
title = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠧࡵ࡫ࡷࡰࡪ࠭ম"), None)
l11l1llCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠨࡵࡨࡥࡸࡵ࡮ࠨয"), None)
l1l1ll11Created_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࠪর") ,None)
l111lCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠪ࡭ࡳ࡬࡯࡭ࡣࡥࡩࡱࡹࠧ঱"), None)
content = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬল"), None)
l1ll1llCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࡢ࡭ࡩ࠭঳"), None)
l11l1lCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱ࡭ࡲࡧࡧࡦࠩ঴"), None)
fan_art = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡣࡦࡸࡴࠨ঵"), None)
is_folder = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠨ࡫ࡶࡣ࡫ࡵ࡬ࡥࡧࡵࠫশ"), True)
if mode is None or url is None or len(url)<1:
	l1lll1Created_By_Mucky_Duck()
elif mode == l11lCreated_By_Mucky_Duck (u"ࠩ࠴ࠫষ"):
	l1l1l111Created_By_Mucky_Duck(content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠪ࠶ࠬস"):
	l1ll11Created_By_Mucky_Duck(url,content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠫ࠸࠭হ"):
	l111l11Created_By_Mucky_Duck(title, url, l11l1lCreated_By_Mucky_Duck, content, l11l1llCreated_By_Mucky_Duck)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠬ࠺ࠧ঺"):
	l1l11lllCreated_By_Mucky_Duck(url, content)
elif mode == l11lCreated_By_Mucky_Duck (u"࠭࠵ࠨ঻"):
	l11llCreated_By_Mucky_Duck(url, content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠧ࠷়ࠩ"):
	l1l1l1Created_By_Mucky_Duck(url, content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠨ࠹ࠪঽ"):
	l1111Created_By_Mucky_Duck(url,name,l11l1lCreated_By_Mucky_Duck,content,l111lCreated_By_Mucky_Duck,query)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠩࡶࡩࡦࡸࡣࡩࠩা"):
	l11lllCreated_By_Mucky_Duck(content,query)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠪࡥࡩࡪ࡯࡯ࡡࡶࡩࡦࡸࡣࡩࠩি"):
	md.addon_search(content,query,fan_art,l111lCreated_By_Mucky_Duck)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠫ࡬࡫ࡴࡠࡲࡵࡳࡽࡿࠧী"):
	l1l1l1l1Created_By_Mucky_Duck(url)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠬࡧࡤࡥࡡࡵࡩࡲࡵࡶࡦࡡࡩࡥࡻ࠭ু"):
	md.add_remove_fav(name, url, l111lCreated_By_Mucky_Duck, fan_art,
			  content, l1ll1llCreated_By_Mucky_Duck, is_folder)
elif mode == l11lCreated_By_Mucky_Duck (u"࠭ࡦࡦࡶࡦ࡬ࡤ࡬ࡡࡷࡵࠪূ"):
	md.fetch_favs(l11l1l1Created_By_Mucky_Duck)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠧࡢࡦࡧࡳࡳࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨৃ"):
	l111Created_By_Mucky_Duck.show_settings()
elif mode == l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡨࡸࡦࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨৄ"):
	import metahandler
	metahandler.display_settings()