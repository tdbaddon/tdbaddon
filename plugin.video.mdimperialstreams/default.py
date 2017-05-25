# -*- coding: utf-8 -*-
import sys
l11lll1lCreated_By_Mucky_Duck = sys.version_info [0] == 2
l1lllll1Created_By_Mucky_Duck = 2048
l1l1l111Created_By_Mucky_Duck = 7
def l1lllCreated_By_Mucky_Duck (l11ll1Created_By_Mucky_Duck):
    global l111111Created_By_Mucky_Duck
    l1ll111lCreated_By_Mucky_Duck = ord (l11ll1Created_By_Mucky_Duck [-1])
    l1l11111Created_By_Mucky_Duck = l11ll1Created_By_Mucky_Duck [:-1]
    l11lll1Created_By_Mucky_Duck = l1ll111lCreated_By_Mucky_Duck % len (l1l11111Created_By_Mucky_Duck)
    l111l1Created_By_Mucky_Duck = l1l11111Created_By_Mucky_Duck [:l11lll1Created_By_Mucky_Duck] + l1l11111Created_By_Mucky_Duck [l11lll1Created_By_Mucky_Duck:]
    if l11lll1lCreated_By_Mucky_Duck:
        l1lll111Created_By_Mucky_Duck = unicode () .join ([unichr (ord (char) - l1lllll1Created_By_Mucky_Duck - (l11lCreated_By_Mucky_Duck + l1ll111lCreated_By_Mucky_Duck) % l1l1l111Created_By_Mucky_Duck) for l11lCreated_By_Mucky_Duck, char in enumerate (l111l1Created_By_Mucky_Duck)])
    else:
        l1lll111Created_By_Mucky_Duck = str () .join ([chr (ord (char) - l1lllll1Created_By_Mucky_Duck - (l11lCreated_By_Mucky_Duck + l1ll111lCreated_By_Mucky_Duck) % l1l1l111Created_By_Mucky_Duck) for l11lCreated_By_Mucky_Duck, char in enumerate (l111l1Created_By_Mucky_Duck)])
    return eval (l1lll111Created_By_Mucky_Duck)
import os,re,shutil,sys,time,urllib,urlresolver,random,jsunpack
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
### Imperial Streams Add-on Created By Mucky Duck (5/2016) completely recoded with new sources 8/2016 ###
l1ll1ll1Created_By_Mucky_Duck = xbmcaddon.Addon().getAddonInfo(l1lllCreated_By_Mucky_Duck (u"ࠫ࡮ࡪࠧࠀ"))
l1ll1Created_By_Mucky_Duck = Addon(l1ll1ll1Created_By_Mucky_Duck, sys.argv)
l1l1lCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_name()
l1l1ll1lCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_path()
md = md(l1ll1ll1Created_By_Mucky_Duck, sys.argv)
l11l1l11Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࠪࠁ"))
l11l11lCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥࡦࡢࡸࡶࠫࠂ"))
l11Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠧࡢࡦࡧࡣࡸ࡫ࡴࠨࠃ"))
l111lllCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠨࡧࡱࡥࡧࡲࡥࡠࡦࡲࡧࡸ࠭ࠄ"))
l1l1ll1Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠩࡨࡲࡦࡨ࡬ࡦࡡࡷࡳࡴࡴࡳࠨࠅ"))
l1lll1l1Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠪࡩࡳࡧࡢ࡭ࡧࡢࡷ࡭ࡵࡷࡴࠩࠆ"))
l1l1l1l1Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠫࡪࡴࡡࡣ࡮ࡨࡣࡲࡵࡶࡪࡧࡶࠫࠇ"))
l1ll1l1lCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡧ࡮ࡪ࡯ࡨࠫࠈ"))
l1l111l1Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥࡡࡥࡷ࡯ࡸࠬࠉ"))
l11l1111Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠧࡦࡰࡤࡦࡱ࡫࡟࡮ࡧࡷࡥࡤࡹࡥࡵࠩࠊ"))
l11l1l1Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_setting(l1lllCreated_By_Mucky_Duck (u"ࠨࡣࡸࡸࡴࡶ࡬ࡢࡻࠪࠋ"))
l11l11Created_By_Mucky_Duck = md.get_art()
l11l1ll1Created_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_icon()
l111ll1Created_By_Mucky_Duck = [l1lllCreated_By_Mucky_Duck (u"ࠩ࠴࠲࡯ࡶࡧࠨࠌ"),l1lllCreated_By_Mucky_Duck (u"ࠪ࠶࠳ࡰࡰࡨࠩࠍ"),l1lllCreated_By_Mucky_Duck (u"ࠫ࠺࠴ࡰ࡯ࡩࠪࠎ"),l1lllCreated_By_Mucky_Duck (u"ࠬ࠼࠮࡫ࡲࡪࠫࠏ"),l1lllCreated_By_Mucky_Duck (u"࠭࠷࠯࡬ࡳ࡫ࠬࠐ"),l1lllCreated_By_Mucky_Duck (u"ࠧ࠹࠰࡭ࡴ࡬࠭ࠑ"),
	  l1lllCreated_By_Mucky_Duck (u"ࠨ࠻࠱࡮ࡵ࡭ࠧࠒ"),l1lllCreated_By_Mucky_Duck (u"ࠩ࠴࠴࠳ࡰࡰࡨࠩࠓ"),l1lllCreated_By_Mucky_Duck (u"ࠪ࠵࠶࠴ࡪࡱࡩࠪࠔ"),l1lllCreated_By_Mucky_Duck (u"ࠫ࠶࠸࠮࡫ࡲࡪࠫࠕ"),l1lllCreated_By_Mucky_Duck (u"ࠬ࠷࠳࠯࡬ࡳ࡫ࠬࠖ")]
l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck + random.choice(l111ll1Created_By_Mucky_Duck)
l1llll11Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡴࡱ࡯ࡥࡷࡳ࡯ࡷ࡫ࡨࡾ࠳ࡺ࡯ࠨࠗ")#l1lllCreated_By_Mucky_Duck (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡵࡨࡶ࡮࡫ࡳࡰࡰ࡯࡭ࡳ࡫࠮ࡪࡱࠪ࠘")
l1ll11Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡭࡬ࡷࡸࡩࡡࡳࡶࡲࡳࡳ࠴ࡥࡶࠩ࠙")
l1lll1Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡧࡳࡨࡻ࡭ࡦࡰࡷࡥࡷࡿࡳࡵࡱࡵࡱ࠳ࡩ࡯࡮ࠩࠚ")
l1ll1lCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡯࡮ࡹࡳࡢࡰ࡬ࡱࡪ࡮ࡤ࠯ࡤ࡬ࡾࠬࠛ")
reload(sys)
sys.setdefaultencoding(l1lllCreated_By_Mucky_Duck (u"ࠦࡺࡺࡦ࠮࠺ࠥࠜ"))
def l1l111Created_By_Mucky_Duck():
	if l111lllCreated_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠬࡺࡲࡶࡧࠪࠝ"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࠞ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࠷࠲ࠪࠟ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࠠ"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡉࡕࡃࡖࡏࡈࡒ࡙ࡇࡒࡊࡇࡖ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩࠡ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࠢ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠣ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬࠤ"):l111ll1Created_By_Mucky_Duck})
	if l1l1ll1Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠥ"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࠦ"):l1lllCreated_By_Mucky_Duck (u"ࠨ࠶࠳ࠫࠧ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠨ"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡉࡁࡓࡖࡒࡓࡓ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬࠩ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠪ"):l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠫ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡢࡰࡤࡶࡹ࠭ࠬ"):l111ll1Created_By_Mucky_Duck})
	if l1lll1l1Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬ࠭"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭࠮"):l1lllCreated_By_Mucky_Duck (u"ࠩ࠴ࠫ࠯"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ࠰"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡔࡗࠢࡖࡌࡔ࡝ࡓ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭࠱"), l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ࠲"):l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࠳"), l1lllCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࠴"):l1lllCreated_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩ࠵")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩ࠶"):l111ll1Created_By_Mucky_Duck})
	if l1l1l1l1Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨ࠷"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩ࠸"):l1lllCreated_By_Mucky_Duck (u"ࠬ࠷ࠧ࠹"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ࠺"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡐࡓ࡛ࡏࡅࡔ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧ࠻"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࠼"):l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭࠽"), l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫ࠾"):l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࡶࠫ࠿")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬࡀ"):l111ll1Created_By_Mucky_Duck})
	if l1ll1l1lCreated_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࡁ"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࡂ"):l1lllCreated_By_Mucky_Duck (u"ࠨ࠷࠳ࠫࡃ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࡄ"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡇࡎࡊࡏࡈ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩࡅ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࡆ"):l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡇ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡢࡰࡤࡶࡹ࠭ࡈ"):l111ll1Created_By_Mucky_Duck})
	if l11l11lCreated_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬࡉ"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡊ"): l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡩࡹࡩࡨࡠࡨࡤࡺࡸ࠭ࡋ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡌ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡍ࡚ࠢࡉࡅ࡛ࡕࡕࡓࡋࡗࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡍ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡎ"):l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࡏ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧࡐ"):l111ll1Created_By_Mucky_Duck})
	if l11l1l11Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭ࡑ"):
		if l11l1111Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠩࡷࡶࡺ࡫ࠧࡒ"):
			md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࡓ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡲ࡫ࡴࡢࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠫࡔ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࡕ"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡡࡂ࡞ࡏࡈࡘࡆࠦࡓࡆࡖࡗࡍࡓࡍࡓ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࡖ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࡗ"):l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡘ")}, is_folder=False, is_playable=False, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵ࡙ࠩ"):l111ll1Created_By_Mucky_Duck})
	if l11Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨ࡚"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦ࡛ࠩ"):l1lllCreated_By_Mucky_Duck (u"ࠬࡧࡤࡥࡱࡱࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭࡜"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ࡝"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣ࡛ࡃ࡟ࡄࡈࡉࡕࡎࠡࡕࡈࡘ࡙ࡏࡎࡈࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࡞"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࡟"):l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ࡠ")}, is_folder=False, is_playable=False, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪࡡ"):l111ll1Created_By_Mucky_Duck})
	setView(l1ll1ll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪࡢ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨࡣ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
l1111Created_By_Mucky_Duck = [l1lllCreated_By_Mucky_Duck (u"࠭ࡲࡢࡶ࡬ࡲ࡬࠭ࡤ"),l1lllCreated_By_Mucky_Duck (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧࡥ"),l1lllCreated_By_Mucky_Duck (u"ࠨࡸ࡬ࡩࡼ࠭ࡦ"),l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡻࡵࡲࡪࡶࡨࠫࡧ"),l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡲࡪࡢࡠ࡯ࡤࡶࡰ࠭ࡨ")]
sort = [l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡋࡠ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࡏࡲࡷࡹࠦࡒࡢࡶࡨࡨࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡊ࡟࡞࠳ࡇࡣࠧࡩ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟ࡕࡩࡨ࡫࡮ࡵ࡮ࡼࠤࡆࡪࡤࡦࡦ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬࡪ"),
	l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠࡑࡴࡹࡴࠡࡘ࡬ࡩࡼ࡫ࡤ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪ࡫"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࡒࡵࡳࡵࠢࡉࡥࡻࡵࡵࡳ࡫ࡷࡩࡩࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨ࡬"),
	l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡏࡍࡅࡄࠣࡖࡦࡺࡩ࡯ࡩ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬ࡭")]
def l11l11l1Created_By_Mucky_Duck(content):
	if l11l11lCreated_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠩࡷࡶࡺ࡫ࠧ࡮"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ࡯"): l1lllCreated_By_Mucky_Duck (u"ࠫ࡫࡫ࡴࡤࡪࡢࡪࡦࡼࡳࠨࡰ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࡱ"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࡠࡈ࡝ࡎ࡛ࠣࡅࡉࡊ࠭ࡐࡐࠣࡊࡆ࡜ࡏࡖࡔࡌࡘࡊ࡙࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࡲ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࡳ"):l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡴ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩࡵ"):l111ll1Created_By_Mucky_Duck})
	if content == l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪࡶ"):
		l1l1ll11Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧࠪࡷ")
	elif content == l1lllCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࡸ"):
		l1l1ll11Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"࠭ࡳࡦࡴ࡬ࡩࡸ࠭ࡹ")
	l1111llCreated_By_Mucky_Duck = l1llll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠧ࠰࡯ࡲࡺ࡮࡫࠯ࡧ࡫࡯ࡸࡪࡸ࠯ࠦࡵ࠲ࠩࡸ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࡣ࡯ࡰࠬࡺ")
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࡻ"): l1lllCreated_By_Mucky_Duck (u"ࠩ࠵ࠫࡼ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࡽ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡍࡐࡕࡗࠤࡗࡋࡃࡆࡐࡗࡐ࡞ࠦࡁࡅࡆࡈࡈࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࡾ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡿ"):l1111llCreated_By_Mucky_Duck %(l1l1ll11Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ࢀ")), l1lllCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࢁ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨࢂ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࢃ"): l1lllCreated_By_Mucky_Duck (u"ࠪ࠶ࠬࢄ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࢅ"):l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡎࡑࡖࡘࠥࡌࡁࡗࡑࡘࡖࡎ࡚ࡅࡅ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࢆ"), l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࢇ"):l1111llCreated_By_Mucky_Duck %(l1l1ll11Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡹࡳࡷ࡯ࡴࡦࠩ࢈")), l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࢉ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩࢊ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࢋ"): l1lllCreated_By_Mucky_Duck (u"ࠫ࠷࠭ࢌ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࢍ"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࡏࡒࡗ࡙ࠦࡒࡂࡖࡌࡒࡌ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬࢎ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ࢏"):l1111llCreated_By_Mucky_Duck %(l1l1ll11Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠨࡴࡤࡸ࡮ࡴࡧࠨ࢐")), l1lllCreated_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪ࢑"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪ࢒"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩ࢓"): l1lllCreated_By_Mucky_Duck (u"ࠬ࠸ࠧ࢔"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ࢕"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡐࡓࡘ࡚ࠠࡗࡋࡈ࡛ࡊࡊ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ࢖"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࢗ"):l1111llCreated_By_Mucky_Duck %(l1l1ll11Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠩࡹ࡭ࡪࡽࠧ࢘")), l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷ࢙ࠫ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷ࢚ࠫ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧ࢛ࠪ"): l1lllCreated_By_Mucky_Duck (u"࠭࠲ࠨ࢜"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ࢝"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡘࡔࡖࠠࡊࡏࡇࡆࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪ࢞"), l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭࢟"):l1111llCreated_By_Mucky_Duck %(l1l1ll11Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡲࡪࡢࡠ࡯ࡤࡶࡰ࠭ࢠ")), l1lllCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࢡ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬࢢ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࢣ"): l1lllCreated_By_Mucky_Duck (u"ࠧ࠷ࠩࢤ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࢥ"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡈࡕࡕࡏࡖࡕ࡝ࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࢦ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࢧ"):l1llll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫ࠴ࡳ࡯ࡷ࡫ࡨ࠳࡫࡯࡬ࡵࡧࡵࠫࢨ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࢩ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡢࡰࡤࡶࡹ࠭ࢪ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࢫ"): l1lllCreated_By_Mucky_Duck (u"ࠨࡵࡨࡥࡷࡩࡨࠨࢬ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࢭ"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢ࡙ࡅࡂࡔࡆࡌࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪࢮ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࢯ"):l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࢰ"), l1lllCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࢱ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲࠬࢲ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠨࡕࡈࡅࡗࡉࡈ࠯ࡲࡱ࡫ࠬࢳ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩࢴ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࢵ"): l1lllCreated_By_Mucky_Duck (u"ࠫ࠹࠭ࢶ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࢷ"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࡉࡈࡒࡗࡋ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬࢸ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࢹ"):l1llll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠨ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲࠨࢺ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࢻ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨࢼ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫࡌࡋࡎࡓࡇ࠱ࡴࡳ࡭ࠧࢽ"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬࢾ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࢿ"): l1lllCreated_By_Mucky_Duck (u"ࠧ࠶ࠩࣀ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࣁ"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡ࡞ࡋࡁࡓ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࣂ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࣃ"):l1llll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫ࠴ࡳ࡯ࡷ࡫ࡨ࠳࡫࡯࡬ࡵࡧࡵࠫࣄ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࣅ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡢࡰࡤࡶࡹ࠭ࣆ"):l111ll1Created_By_Mucky_Duck})
	setView(l1ll1ll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭ࣇ"), l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫࣈ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l11l1lCreated_By_Mucky_Duck(url,content):
	link = open_url(url,verify=False).content
	l1l11Created_By_Mucky_Duck = md.regex_get_all(link, l1lllCreated_By_Mucky_Duck (u"ࠩࡦࡰࡦࡹࡳ࠾ࠤࡰࡰ࠲࡯ࡴࡦ࡯ࠥࡂࠬࣉ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡀ࠴ࡪࡩࡷࡀࠪ࣊"))
	items = len(l1l11Created_By_Mucky_Duck)
	for a in l1l11Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠫࡹ࡯ࡴ࡭ࡧࡀࠦࠬ࣋"), l1lllCreated_By_Mucky_Duck (u"ࠬࠨࠧ࣌"))
		name = l1ll1Created_By_Mucky_Duck.unescape(name).replace(l1lllCreated_By_Mucky_Duck (u"ࠨ࡜࡝ࠩࠥ࣍"),l1lllCreated_By_Mucky_Duck (u"ࠢࠨࠤ࣎"))
		url = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠨࡪࡵࡩ࡫ࡃࠢࠨ࣏"), l1lllCreated_By_Mucky_Duck (u"࣐ࠩࠥࠫ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠪ࠲࡭ࡺ࡭࡭࣑ࠩ"),l1lllCreated_By_Mucky_Duck (u"ࠫ࠴ࡽࡡࡵࡥ࡫࡭ࡳ࡭࠮ࡩࡶࡰࡰ࣒ࠬ"))
		l1llCreated_By_Mucky_Duck = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠬࡪࡡࡵࡣ࠰ࡳࡷ࡯ࡧࡪࡰࡤࡰࡂࠨ࣓ࠧ"), l1lllCreated_By_Mucky_Duck (u"࠭ࠢࠨࣔ"))
		l1lll1llCreated_By_Mucky_Duck = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠧ࡮࡮࡬࠱ࡶࡻࡡ࡭࡫ࡷࡽࠧࡄࠧࣕ"), l1lllCreated_By_Mucky_Duck (u"ࠨ࠾ࠪࣖ"))
		l11l11llCreated_By_Mucky_Duck = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠩࠥࡱࡱ࡯࠭ࡦࡲࡶࠦࡃ࠭ࣗ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡀ࠴࠭ࣘ"))
		l11l11llCreated_By_Mucky_Duck = l11l11llCreated_By_Mucky_Duck.replace(l1lllCreated_By_Mucky_Duck (u"ࠫࡁࡹࡰࡢࡰࡁࠫࣙ"),l1lllCreated_By_Mucky_Duck (u"ࠬࠦࠧࣚ")).replace(l1lllCreated_By_Mucky_Duck (u"࠭࠼ࡪࡀࠪࣛ"),l1lllCreated_By_Mucky_Duck (u"ࠧࠡࠩࣜ"))
		if content == l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨࣝ"):
			if l1lll1llCreated_By_Mucky_Duck:
                                title = name
				md.remove_punctuation(title)
				md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࣞ"): l1lllCreated_By_Mucky_Duck (u"ࠪ࠻ࠬࣟ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ࣠"):l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡ࠭ࠫࡳࠪ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫ࣡") %(name,l1lll1llCreated_By_Mucky_Duck),
					   l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ࣢"):url, l1lllCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࣣࠪ"):l1llCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࣤ"):content}, {l1lllCreated_By_Mucky_Duck (u"ࠩࡶࡳࡷࡺࡴࡪࡶ࡯ࡩࠬࣥ"):title},
					  fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨࣦ"):l1llCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫࣧ"):l111ll1Created_By_Mucky_Duck}, is_folder=False, item_count=items)
		elif content == l1lllCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࣨ"):
			if l11l11llCreated_By_Mucky_Duck:
				data = name.split(l1lllCreated_By_Mucky_Duck (u"࠭࠭ࠡࡕࡨࡥࡸࡵ࡮ࠨࣩ"))
				l1l1llllCreated_By_Mucky_Duck = data[0].strip()
				md.remove_punctuation(l1l1llllCreated_By_Mucky_Duck)
				try:
					l1llll1lCreated_By_Mucky_Duck = data[1].strip()
				except:
					l1llll1lCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠧࠨ࣪")
				md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭࣫"): l1lllCreated_By_Mucky_Duck (u"ࠩ࠶ࠫ࣬"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ࣭"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠣ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞࣮ࠩ") %(name,l11l11llCreated_By_Mucky_Duck),
					   l1lllCreated_By_Mucky_Duck (u"ࠬࡺࡩࡵ࡮ࡨ࣯ࠫ"):l1l1llllCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࣰࠪ"):url, l1lllCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࣱࠪ"):l1llCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࣲࠩ"):content, l1lllCreated_By_Mucky_Duck (u"ࠩࡶࡩࡦࡹ࡯࡯ࠩࣳ"):l1llll1lCreated_By_Mucky_Duck},
					  {l1lllCreated_By_Mucky_Duck (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪ࠭ࣴ"):l1l1llllCreated_By_Mucky_Duck}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠫ࡮ࡩ࡯࡯ࠩࣵ"):l1llCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࣶࠬ"):l111ll1Created_By_Mucky_Duck}, item_count=items)
	try:
		l111Created_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"࠭࠼࡭࡫ࠣࡧࡱࡧࡳࡴ࠿ࠥࡲࡪࡾࡴࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠪࡀࠫࠥࠤࡩࡧࡴࡢ࠯ࡦ࡭࠲ࡶࡡࡨ࡫ࡱࡥࡹ࡯࡯࡯࠯ࡳࡥ࡬࡫࠽ࠣ࠰࠭ࡃࠧࠦࡲࡦ࡮ࡀࠦࡳ࡫ࡸࡵࠤࡁࠫࣷ")).findall(link)[0]
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࣸ"): l1lllCreated_By_Mucky_Duck (u"ࠨ࠴ࣹࠪ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࣺࠧ"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝࠿ࡀࡑࡩࡽࡺࠠࡑࡣࡪࡩࡃࡄ࠾࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࣻ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࣼ"):l111Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ࣽ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫࣾ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡧࡻࡸ࠳ࡶ࡮ࡨࠩࣿ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨऀ"):l111ll1Created_By_Mucky_Duck})
	except: pass
	if content == l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩँ"):
		setView(l1ll1ll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪं"), l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡶࡪࡧ࠰ࡺ࡮࡫ࡷࠨः"))
	elif content == l1lllCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ऄ"):
		setView(l1ll1ll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࠭ࡴࡷࡵ࡫ࡳࡼࡹࠧअ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡴࡪࡲࡻ࠲ࡼࡩࡦࡹࠪआ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1ll11llCreated_By_Mucky_Duck(title, url, l1lll1lCreated_By_Mucky_Duck, content, l1llll1lCreated_By_Mucky_Duck):
	link = open_url(url,verify=False).content
	l1lll11lCreated_By_Mucky_Duck = url
	l1llllllCreated_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠨ࡫ࡧ࠾ࠥࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨइ")).findall(link)[0]
	request_url = l1lllCreated_By_Mucky_Duck (u"ࠩࠨࡷ࠴ࡧࡪࡢࡺ࠲ࡺ࠹ࡥ࡭ࡰࡸ࡬ࡩࡤ࡫ࡰࡪࡵࡲࡨࡪࡹ࠯ࠦࡵࠪई") %(l1llll11Created_By_Mucky_Duck,l1llllllCreated_By_Mucky_Duck)
	headers = {l1lllCreated_By_Mucky_Duck (u"ࠪࡅࡨࡩࡥࡱࡶ࠰ࡉࡳࡩ࡯ࡥ࡫ࡱ࡫ࠬउ"):l1lllCreated_By_Mucky_Duck (u"ࠫ࡬ࢀࡩࡱ࠮ࠣࡨࡪ࡬࡬ࡢࡶࡨ࠰ࠥࡹࡤࡤࡪ࠯ࠤࡧࡸࠧऊ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡘࡥࡧࡧࡵࡩࡷ࠭ऋ"):l1lll11lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪऌ"):md.User_Agent()}
	l11lll11Created_By_Mucky_Duck = open_url(request_url, headers=headers, verify=False).json()
	l11111lCreated_By_Mucky_Duck = md.regex_get_all(l11lll11Created_By_Mucky_Duck[l1lllCreated_By_Mucky_Duck (u"ࠧࡩࡶࡰࡰࠬऍ")], l1lllCreated_By_Mucky_Duck (u"ࠨࠤࡨࡴ࡮ࡹ࡯ࡥࡧࡶ࠱ࡸࡼ࠭࠲࠲ࠥࠫऎ"), l1lllCreated_By_Mucky_Duck (u"ࠩ࠿࠳ࡺࡲ࠾ࠨए"))
	l1l11Created_By_Mucky_Duck = md.regex_get_all(str(l11111lCreated_By_Mucky_Duck), l1lllCreated_By_Mucky_Duck (u"ࠪࡀࡱ࡯ࠧऐ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡁ࠵࡬ࡪࡀࠪऑ"))
	items = len(l1l11Created_By_Mucky_Duck)
	for a in l1l11Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠬࡺࡩࡵ࡮ࡨࡁࠧ࠭ऒ"), l1lllCreated_By_Mucky_Duck (u"࠭ࠢࠨओ"))
		name = name.replace(l1lllCreated_By_Mucky_Duck (u"ࠧࡆࡲ࡬ࡷࡴࡪࡥࠨऔ"),l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࡅࡱ࡫ࡶࡳࡩ࡫࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨक"))
		name = l1ll1Created_By_Mucky_Duck.unescape(name).replace(l1lllCreated_By_Mucky_Duck (u"ࠤ࡟ࡠࠬࠨख"),l1lllCreated_By_Mucky_Duck (u"ࠥࠫࠧग"))
		l11ll11lCreated_By_Mucky_Duck = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠫࡩࡧࡴࡢ࠯࡬ࡨࡂࠨࠧघ"), l1lllCreated_By_Mucky_Duck (u"ࠬࠨࠧङ"))
		headers = l1lll11lCreated_By_Mucky_Duck + l1lllCreated_By_Mucky_Duck (u"࠭ࡼࠨच") + l11ll11lCreated_By_Mucky_Duck + l1lllCreated_By_Mucky_Duck (u"ࠧࡽࠩछ") + l1llllllCreated_By_Mucky_Duck
		url =  l1lllCreated_By_Mucky_Duck (u"ࠨࠧࡶ࠳ࡦࡰࡡࡹ࠱ࡰࡳࡻ࡯ࡥࡠࡵࡲࡹࡷࡩࡥࡴ࠱ࠨࡷࠬज") %(l1llll11Created_By_Mucky_Duck,l11ll11lCreated_By_Mucky_Duck)
		try:
			l11l1l1lCreated_By_Mucky_Duck = name.split(l1lllCreated_By_Mucky_Duck (u"ࠩࡈࡴ࡮ࡹ࡯ࡥࡧࠪझ"))[1].strip()[:2]
		except:pass
		fan_art = {l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨञ"):l1lll1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫट"):l111ll1Created_By_Mucky_Duck}
		md.remove_punctuation(title)
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪठ"): l1lllCreated_By_Mucky_Duck (u"࠭࠷ࠨड"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬढ"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫण") %name,
			   l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭त"):url, l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭थ"):l1lll1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬद"):l1lllCreated_By_Mucky_Duck (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࠧध"), l1lllCreated_By_Mucky_Duck (u"࠭ࡱࡶࡧࡵࡽࠬन"):headers},
			  {l1lllCreated_By_Mucky_Duck (u"ࠧࡴࡱࡵࡸࡹ࡯ࡴ࡭ࡧࠪऩ"):title, l1lllCreated_By_Mucky_Duck (u"ࠨࡵࡨࡥࡸࡵ࡮ࠨप"):l1llll1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࠪफ"):l11l1l1lCreated_By_Mucky_Duck},
			  fan_art, is_folder=False, item_count=items)
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࡷࠬब"), l1lllCreated_By_Mucky_Duck (u"ࠫࡪࡶࡩ࠮ࡸ࡬ࡩࡼ࠭भ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l11l111lCreated_By_Mucky_Duck(url, content):
	l1lll11Created_By_Mucky_Duck = md.dialog_select(l1lllCreated_By_Mucky_Duck (u"࡙ࠬࡥ࡭ࡧࡦࡸ࡙ࠥ࡯ࡳࡶࠣࡑࡪࡺࡨࡰࡦࠪम"),sort)
	l1l1Created_By_Mucky_Duck = l1111Created_By_Mucky_Duck[l1lll11Created_By_Mucky_Duck]
	link = open_url(url,verify=False).content
	match = re.compile(l1lllCreated_By_Mucky_Duck (u"࠭࠼ࡪࡰࡳࡹࡹࠦࡣ࡭ࡣࡶࡷࡂࠨࡧࡦࡰࡵࡩ࠲࡯ࡤࡴࠤࠣࡺࡦࡲࡵࡦ࠿ࠥࠬ࠳࠰࠿ࠪࠤࠣࡲࡦࡳࡥ࠾ࠤ࠱࠮ࡄࠨ࡜࡯࠰࠭ࡃࡹࡿࡰࡦ࠿ࠥࡧ࡭࡫ࡣ࡬ࡤࡲࡼࠧࠦ࠾ࠩ࠰࠭ࡃ࠮ࡂ࠯࡭ࡣࡥࡩࡱࡄࠧय")).findall(link)
	for l11ll1lCreated_By_Mucky_Duck,name in match:
		name = name.replace(l1lllCreated_By_Mucky_Duck (u"ࠧࠡࠩर"),l1lllCreated_By_Mucky_Duck (u"ࠨࠩऱ"))
		if content == l1lllCreated_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪल"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵࡭ࡰࡸ࡬ࡩ࠴࡬ࡩ࡭ࡶࡨࡶ࠴ࡹࡥࡳ࡫ࡨࡷ࠴ࠫࡳ࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭࠱ࡤࡰࡱ࠭ळ") %(l1llll11Created_By_Mucky_Duck,l1l1Created_By_Mucky_Duck,l11ll1lCreated_By_Mucky_Duck)
			md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩऴ"): l1lllCreated_By_Mucky_Duck (u"ࠬ࠸ࠧव"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫश"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡌࡡࡠ࠵ࡂ࡞ࠩष") %name, l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬस"):url, l1lllCreated_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪह"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨऺ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫࡌࡋࡎࡓࡇ࠱ࡴࡳ࡭ࠧऻ"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸ़ࠬ"):l111ll1Created_By_Mucky_Duck})
		elif content == l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ऽ"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳ࠱ࡰࡳࡻ࡯ࡥ࠰ࠧࡶ࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࠩा") %(l1llll11Created_By_Mucky_Duck,l1l1Created_By_Mucky_Duck,l11ll1lCreated_By_Mucky_Duck)
			md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ि"): l1lllCreated_By_Mucky_Duck (u"ࠩ࠵ࠫी"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨु"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡋࡠ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ू") %name, l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩृ"):url, l1lllCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧॄ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲࠬॅ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠨࡉࡈࡒࡗࡋ࠮ࡱࡰࡪࠫॆ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩे"):l111ll1Created_By_Mucky_Duck})
	setView(l1ll1ll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠪࡪ࡮ࡲࡥࡴࠩै"), l1lllCreated_By_Mucky_Duck (u"ࠫࡲ࡫࡮ࡶ࠯ࡹ࡭ࡪࡽࠧॉ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1llllCreated_By_Mucky_Duck(url, content):
	l1lll11Created_By_Mucky_Duck = md.dialog_select(l1lllCreated_By_Mucky_Duck (u"࡙ࠬࡥ࡭ࡧࡦࡸ࡙ࠥ࡯ࡳࡶࠣࡑࡪࡺࡨࡰࡦࠪॊ"),sort)
	l1l1Created_By_Mucky_Duck = l1111Created_By_Mucky_Duck[l1lll11Created_By_Mucky_Duck]
	l11111Created_By_Mucky_Duck = md.numeric_select(l1lllCreated_By_Mucky_Duck (u"࠭ࡅ࡯ࡶࡨࡶࠥ࡟ࡥࡢࡴࠪो"), l1lllCreated_By_Mucky_Duck (u"ࠧ࠳࠲࠴࠻ࠬौ"))
	if content == l1lllCreated_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴ्ࠩ"):
		l11l1lCreated_By_Mucky_Duck(l1lllCreated_By_Mucky_Duck (u"ࠩࠨࡷ࠴ࡳ࡯ࡷ࡫ࡨ࠳࡫࡯࡬ࡵࡧࡵ࠳ࡸ࡫ࡲࡪࡧࡶ࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࡣ࡯ࡰࠬॎ") %(l1llll11Created_By_Mucky_Duck,l1l1Created_By_Mucky_Duck,l11111Created_By_Mucky_Duck), content)
	elif content == l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪॏ"):
		l11l1lCreated_By_Mucky_Duck(l1lllCreated_By_Mucky_Duck (u"ࠫࠪࡹ࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠵࡭ࡰࡸ࡬ࡩ࠴ࠫࡳ࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭࠱ࠨࡷ࠴ࡧ࡬࡭࠱ࡤࡰࡱ࠭ॐ") %(l1llll11Created_By_Mucky_Duck,l1l1Created_By_Mucky_Duck,l11111Created_By_Mucky_Duck), content)
	setView(l1ll1ll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡩ࡭ࡧࡶࠫ॑"), l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡦࡰࡸ࠱ࡻ࡯ࡥࡸ॒ࠩ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1l11lCreated_By_Mucky_Duck():
	link = open_url(l1lllCreated_By_Mucky_Duck (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡲࡤࡷࡹ࡫ࡢࡪࡰ࠱ࡧࡴࡳ࠯ࡳࡣࡺ࠳ࡈ࡬࠴ࡄ࠵ࡸࡌ࠶࠭॓")).content
	version = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡳࠩࡹࡩࡷࡹࡩࡰࡰࠣࡁࠥࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨ॔"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l1lllCreated_By_Mucky_Duck (u"ࠩࡶࡴࡪࡩࡩࡢ࡮࠽࠳࠴࡮࡯࡮ࡧ࠲ࡥࡩࡪ࡯࡯ࡵ࠲ࡷࡨࡸࡩࡱࡶ࠱ࡱࡴࡪࡵ࡭ࡧ࠱ࡱࡺࡩ࡫ࡺࡵ࠱ࡧࡴࡳ࡭ࡰࡰ࠲ࡥࡩࡪ࡯࡯࠰ࡻࡱࡱ࠭ॕ")), l1lllCreated_By_Mucky_Duck (u"ࠪࡶ࠰࠭ॖ")) as f:
		l1ll11lCreated_By_Mucky_Duck = f.read()
		if re.search(l1lllCreated_By_Mucky_Duck (u"ࡶࠬࡼࡥࡳࡵ࡬ࡳࡳࡃࠢࠦࡵࠥࠫॗ") %version, l1ll11lCreated_By_Mucky_Duck):
			l1ll1Created_By_Mucky_Duck.log(l1lllCreated_By_Mucky_Duck (u"ࠬ࡜ࡥࡳࡵ࡬ࡳࡳࠦࡃࡩࡧࡦ࡯ࠥࡕࡋࠨक़"))
		else:
			l1l111llCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠨࡗࡳࡱࡱ࡫ࠥ࡜ࡥࡳࡵ࡬ࡳࡳࠦࡏࡧࠢࡐࡹࡨࡱࡹࡴࠢࡆࡳࡲࡳ࡯࡯ࠢࡐࡳࡩࡻ࡬ࡦࠤख़")
			l1l11l11Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠢࡑ࡮ࡨࡥࡸ࡫ࠠࡊࡰࡶࡸࡦࡲ࡬ࠡࡅࡲࡶࡷ࡫ࡣࡵ࡙ࠢࡩࡷࡹࡩࡰࡰࠣࡊࡷࡵ࡭ࠡࡖ࡫ࡩࠥࡘࡥࡱࡱࠥग़")
			l1l11l1lCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠣࡂ࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝ࡩࡶࡷࡴ࠿࠵࠯࡮ࡷࡦ࡯ࡾࡹ࠮࡮ࡧࡧ࡭ࡦࡶ࡯ࡳࡶࡤࡰ࠹ࡱ࡯ࡥ࡫࠱ࡱࡱࡡ࠯ࡄࡑࡏࡓࡗࡣࠢज़")
			l1ll1Created_By_Mucky_Duck.show_ok_dialog([l1l111llCreated_By_Mucky_Duck, l1l11l11Created_By_Mucky_Duck, l1l11l1lCreated_By_Mucky_Duck], l1l1lCreated_By_Mucky_Duck)
			xbmc.executebuiltin(l1lllCreated_By_Mucky_Duck (u"ࠤ࡛ࡆࡒࡉ࠮ࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱࡙ࡵࡪࡡࡵࡧࠫࡴࡦࡺࡨ࠭ࡴࡨࡴࡱࡧࡣࡦࠫࠥड़"))
			xbmc.executebuiltin(l1lllCreated_By_Mucky_Duck (u"ࠥ࡜ࡇࡓࡃ࠯ࡃࡦࡸ࡮ࡼࡡࡵࡧ࡚࡭ࡳࡪ࡯ࡸࠪࡋࡳࡲ࡫ࠩࠣढ़"))
def l111llCreated_By_Mucky_Duck(url, content):
	l1lll11Created_By_Mucky_Duck = md.dialog_select(l1lllCreated_By_Mucky_Duck (u"ࠫࡘ࡫࡬ࡦࡥࡷࠤࡘࡵࡲࡵࠢࡐࡩࡹ࡮࡯ࡥࠩफ़"),sort)
	l1l1Created_By_Mucky_Duck = l1111Created_By_Mucky_Duck[l1lll11Created_By_Mucky_Duck]
	link = open_url(url,verify=False).content
	match=re.compile(l1lllCreated_By_Mucky_Duck (u"ࠬࡂࡩ࡯ࡲࡸࡸࠥࡩ࡬ࡢࡵࡶࡁࠧࡩ࡯ࡶࡰࡷࡶࡾ࠳ࡩࡥࡵࠥࠤࡻࡧ࡬ࡶࡧࡀࠦ࠭࠴ࠪࡀࠫࠥࠤࡳࡧ࡭ࡦ࠿ࠥ࠲࠯ࡅࠢ࡝ࡰ࠱࠮ࡄࡺࡹࡱࡧࡀࠦࡨ࡮ࡥࡤ࡭ࡥࡳࡽࠨࠠ࠿ࠪ࠱࠮ࡄ࠯࠼࠰࡮ࡤࡦࡪࡲ࠾ࠨय़")).findall(link)
	for l1l1l11Created_By_Mucky_Duck,name in match:
		name = name.replace(l1lllCreated_By_Mucky_Duck (u"࠭ࠠࠨॠ"),l1lllCreated_By_Mucky_Duck (u"ࠧࠨॡ"))
		if content == l1lllCreated_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩॢ"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠩࠨࡷ࠴ࡳ࡯ࡷ࡫ࡨ࠳࡫࡯࡬ࡵࡧࡵ࠳ࡸ࡫ࡲࡪࡧࡶ࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࡣ࡯ࡰࠬॣ") %(l1llll11Created_By_Mucky_Duck,l1l1Created_By_Mucky_Duck,l1l1l11Created_By_Mucky_Duck)
			md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ।"): l1lllCreated_By_Mucky_Duck (u"ࠫ࠷࠭॥"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ०"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡍࡢࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨ१") %name, l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ२"):url, l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ३"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩ४"):l111ll1Created_By_Mucky_Duck})
		elif content == l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪ५"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠫࠪࡹ࠯࡮ࡱࡹ࡭ࡪ࠵ࡦࡪ࡮ࡷࡩࡷ࠵࡭ࡰࡸ࡬ࡩ࠴ࠫࡳ࠰ࡣ࡯ࡰ࠴ࠫࡳ࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭࠱ࡤࡰࡱ࠭६") %(l1llll11Created_By_Mucky_Duck,l1l1Created_By_Mucky_Duck,l1l1l11Created_By_Mucky_Duck)
			md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ७"): l1lllCreated_By_Mucky_Duck (u"࠭࠲ࠨ८"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ९"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪ॰") %name, l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ॱ"):url, l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫॲ"):content}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫॳ"):l111ll1Created_By_Mucky_Duck})
	setView(l1ll1ll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡩ࡭ࡧࡶࠫॴ"), l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡦࡰࡸ࠱ࡻ࡯ࡥࡸࠩॵ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1l1llCreated_By_Mucky_Duck(url,name,l1lll1lCreated_By_Mucky_Duck,content,l1l111lCreated_By_Mucky_Duck,query):
	if content == l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧॶ"):
		link = open_url(url,verify=False).content
		l1lll11lCreated_By_Mucky_Duck = url
		headers = {l1lllCreated_By_Mucky_Duck (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬॷ"):md.User_Agent()}
		link = open_url(url, headers=headers).content
		l1llllllCreated_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠩ࡬ࡨ࠿ࠦࠢࠩ࡝ࡡࠦࡢ࠱ࠩࠣࠩॸ")).findall(link)[0]
		request_url = l1lllCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡻ࠺࡟࡮ࡱࡹ࡭ࡪࡥࡥࡱ࡫ࡶࡳࡩ࡫ࡳ࠰ࠧࡶࠫॹ") %(l1llll11Created_By_Mucky_Duck,l1llllllCreated_By_Mucky_Duck)
		headers = {l1lllCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷ࠱ࡊࡴࡣࡰࡦ࡬ࡲ࡬࠭ॺ"):l1lllCreated_By_Mucky_Duck (u"ࠬ࡭ࡺࡪࡲ࠯ࠤࡩ࡫ࡦ࡭ࡣࡷࡩ࠱ࠦࡳࡥࡥ࡫࠰ࠥࡨࡲࠨॻ"), l1lllCreated_By_Mucky_Duck (u"࠭ࡒࡦࡨࡨࡶࡪࡸࠧॼ"):l1lll11lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫॽ"):md.User_Agent()}
		l11lll11Created_By_Mucky_Duck = open_url(request_url, headers=headers, verify=False).json()
		l11ll11lCreated_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠨࡦࡤࡸࡦ࠳ࡳࡦࡴࡹࡩࡷࡃࠢ࠲࠲ࠥࠤࡩࡧࡴࡢ࠯࡬ࡨࡂࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨॾ")).findall(l11lll11Created_By_Mucky_Duck[l1lllCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡲࡲࠧॿ")])[0]
	else:
		l1lll11lCreated_By_Mucky_Duck = query.split(l1lllCreated_By_Mucky_Duck (u"ࠪࢀࠬঀ"))[0]
		l11ll11lCreated_By_Mucky_Duck = query.split(l1lllCreated_By_Mucky_Duck (u"ࠫࢁ࠭ঁ"))[1]
		l1llllllCreated_By_Mucky_Duck = query.split(l1lllCreated_By_Mucky_Duck (u"ࠬࢂࠧং"))[2]
	l1lCreated_By_Mucky_Duck = int(time.time() * 10000)
	l1l1l1lCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡤ࡮ࡦࡾ࠯࡮ࡱࡹ࡭ࡪࡥࡴࡰ࡭ࡨࡲࠬঃ") %l1llll11Created_By_Mucky_Duck
	params = {l1lllCreated_By_Mucky_Duck (u"ࠧࡦ࡫ࡧࠫ঄"):l11ll11lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠨ࡯࡬ࡨࠬঅ"):l1llllllCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠩࡢࠫআ"):l1lCreated_By_Mucky_Duck}
	headers = {l1lllCreated_By_Mucky_Duck (u"ࠪࡅࡨࡩࡥࡱࡶࠪই"):l1lllCreated_By_Mucky_Duck (u"ࠫࡹ࡫ࡸࡵ࠱࡭ࡥࡻࡧࡳࡤࡴ࡬ࡴࡹ࠲ࠠࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡡࡷࡣࡶࡧࡷ࡯ࡰࡵ࠮ࠣࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡧࡦࡱࡦࡹࡣࡳ࡫ࡳࡸ࠱ࠦࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡥࡤ࡯ࡤࡷࡨࡸࡩࡱࡶ࠯ࠤ࠯࠵ࠪ࠼ࠢࡴࡁ࠵࠴࠰࠲ࠩঈ"),
		   l1lllCreated_By_Mucky_Duck (u"ࠬࡇࡣࡤࡧࡳࡸ࠲ࡋ࡮ࡤࡱࡧ࡭ࡳ࡭ࠧউ"):l1lllCreated_By_Mucky_Duck (u"࠭ࡧࡻ࡫ࡳ࠰ࠥࡪࡥࡧ࡮ࡤࡸࡪ࠲ࠠࡴࡦࡦ࡬࠱ࠦࡢࡳࠩঊ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡂࡥࡦࡩࡵࡺ࠭ࡍࡣࡱ࡫ࡺࡧࡧࡦࠩঋ"):l1lllCreated_By_Mucky_Duck (u"ࠨࡧࡱ࠱࡚࡙ࠬࡦࡰ࠾ࡵࡂ࠶࠮࠹ࠩঌ"),
		   l1lllCreated_By_Mucky_Duck (u"ࠩࡕࡩ࡫࡫ࡲࡦࡴࠪ঍"):l1lll11lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧ঎"):md.User_Agent(), l1lllCreated_By_Mucky_Duck (u"ࠫ࡝࠳ࡒࡦࡳࡸࡩࡸࡺࡥࡥ࠯࡚࡭ࡹ࡮ࠧএ"):l1lllCreated_By_Mucky_Duck (u"ࠬ࡞ࡍࡍࡊࡷࡸࡵࡘࡥࡲࡷࡨࡷࡹ࠭ঐ")}
	data = open_url(l1l1l1lCreated_By_Mucky_Duck, params=params, headers=headers, verify=False).content
	l11ll11Created_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠨ࡟ࡹ࠿ࠪࠬࡠࡤࠧ࡞࠭ࠬࠫࠧ঑")).findall(data)[0]
	l11l1llCreated_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠢࡠࡻࡀࠫ࠭ࡡ࡞ࠨ࡟࠮࠭ࠬࠨ঒")).findall(data)[0]
	l11llllCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠨࠧࡶ࠳ࡦࡰࡡࡹ࠱ࡰࡳࡻ࡯ࡥࡠࡵࡲࡹࡷࡩࡥࡴ࠱ࠨࡷࠬও") %(l1llll11Created_By_Mucky_Duck,l11ll11lCreated_By_Mucky_Duck)
	l1Created_By_Mucky_Duck = {l1lllCreated_By_Mucky_Duck (u"ࠩࡻࠫঔ"):l11ll11Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠪࡽࠬক"):l11l1llCreated_By_Mucky_Duck}
	headers = {l1lllCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷࠫখ"):l1lllCreated_By_Mucky_Duck (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮࠭ࠢࡷࡩࡽࡺ࠯࡫ࡣࡹࡥࡸࡩࡲࡪࡲࡷ࠰ࠥ࠰࠯ࠫ࠽ࠣࡵࡂ࠶࠮࠱࠳ࠪগ"),
		   l1lllCreated_By_Mucky_Duck (u"࠭ࡁࡤࡥࡨࡴࡹ࠳ࡅ࡯ࡥࡲࡨ࡮ࡴࡧࠨঘ"):l1lllCreated_By_Mucky_Duck (u"ࠧࡨࡼ࡬ࡴ࠱ࠦࡤࡦࡨ࡯ࡥࡹ࡫ࠬࠡࡵࡧࡧ࡭࠲ࠠࡣࡴࠪঙ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡃࡦࡧࡪࡶࡴ࠮ࡎࡤࡲ࡬ࡻࡡࡨࡧࠪচ"):l1lllCreated_By_Mucky_Duck (u"ࠩࡨࡲ࠲࡛ࡓ࠭ࡧࡱ࠿ࡶࡃ࠰࠯࠺ࠪছ"),
		   l1lllCreated_By_Mucky_Duck (u"ࠪࡖࡪ࡬ࡥࡳࡧࡵࠫজ"):l1lll11lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨঝ"):md.User_Agent(), l1lllCreated_By_Mucky_Duck (u"ࠬ࡞࠭ࡓࡧࡴࡹࡪࡹࡴࡦࡦ࠰࡛࡮ࡺࡨࠨঞ"):l1lllCreated_By_Mucky_Duck (u"࠭ࡘࡎࡎࡋࡸࡹࡶࡒࡦࡳࡸࡩࡸࡺࠧট")}
	final = open_url(l11llllCreated_By_Mucky_Duck, params=l1Created_By_Mucky_Duck, headers=headers, verify=False).json()
	l1ll111Created_By_Mucky_Duck = []
	l1l11llCreated_By_Mucky_Duck = []
	l11l111Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠧࠨঠ")
	if l11l1l1Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭ড"):
		url = max(final[l1lllCreated_By_Mucky_Duck (u"ࠩࡳࡰࡦࡿ࡬ࡪࡵࡷࠫঢ")][0][l1lllCreated_By_Mucky_Duck (u"ࠪࡷࡴࡻࡲࡤࡧࡶࠫণ")], key=lambda l11ll1l1Created_By_Mucky_Duck: int(re.sub(l1lllCreated_By_Mucky_Duck (u"ࠫࡡࡊࠧত"), l1lllCreated_By_Mucky_Duck (u"ࠬ࠭থ"), l11ll1l1Created_By_Mucky_Duck[l1lllCreated_By_Mucky_Duck (u"࠭࡬ࡢࡤࡨࡰࠬদ")])))
		url = url[l1lllCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࠬধ")]
	else:
		match = final[l1lllCreated_By_Mucky_Duck (u"ࠨࡲ࡯ࡥࡾࡲࡩࡴࡶࠪন")][0][l1lllCreated_By_Mucky_Duck (u"ࠩࡶࡳࡺࡸࡣࡦࡵࠪ঩")]
		for a in match:
			l11l111Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬপ") %a[l1lllCreated_By_Mucky_Duck (u"ࠫࡱࡧࡢࡦ࡮ࠪফ")]
			l1ll111Created_By_Mucky_Duck.append(l11l111Created_By_Mucky_Duck)
			l1l11llCreated_By_Mucky_Duck.append(a[l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡩ࡭ࡧࠪব")])
		if len(match) >1:
			l1lll11Created_By_Mucky_Duck = md.dialog_select(l1lllCreated_By_Mucky_Duck (u"࠭ࡓࡦ࡮ࡨࡧࡹࠦࡓࡵࡴࡨࡥࡲࠦࡑࡶࡣ࡯࡭ࡹࡿࠧভ"),l1ll111Created_By_Mucky_Duck)
			if l1lll11Created_By_Mucky_Duck == -1:
				return
			elif l1lll11Created_By_Mucky_Duck > -1:
				url = l1l11llCreated_By_Mucky_Duck[l1lll11Created_By_Mucky_Duck]
		else:
			url = final[l1lllCreated_By_Mucky_Duck (u"ࠧࡱ࡮ࡤࡽࡱ࡯ࡳࡵࠩম")][0][l1lllCreated_By_Mucky_Duck (u"ࠨࡵࡲࡹࡷࡩࡥࡴࠩয")][0][l1lllCreated_By_Mucky_Duck (u"ࠩࡩ࡭ࡱ࡫ࠧর")]
	md.resolved(url, name, fan_art, l1l111lCreated_By_Mucky_Duck)
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1l1l11lCreated_By_Mucky_Duck():
	l111lCreated_By_Mucky_Duck = xbmc.translatePath(l1lllCreated_By_Mucky_Duck (u"ࠪࡷࡵ࡫ࡣࡪࡣ࡯࠾࠴࠵ࡨࡰ࡯ࡨ࠳ࡦࡪࡤࡰࡰࡶ࠳ࡷ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹ࠯࡯ࡤࡪࠬ঱"))
	l11llCreated_By_Mucky_Duck = xbmc.translatePath(l1lllCreated_By_Mucky_Duck (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷ࠴ࡶ࡬ࡶࡩ࡬ࡲ࠳ࡶࡲࡰࡩࡵࡥࡲ࠴ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡰࡳࡱࡪࡶࡦࡳ࠮࡮ࡣࡩࡻ࡮ࢀࡡࡳࡦࠪল"))
	l11l1Created_By_Mucky_Duck = xbmc.translatePath(l1lllCreated_By_Mucky_Duck (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡶࡪࡦࡨࡳ࠳ࡱࡲࡢࡶࡲࡷࠬ঳"))
	if os.path.exists(l111lCreated_By_Mucky_Duck):
		l1l111llCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"࡙࠭ࡰࡷࠣࡌࡦࡼࡥࠡࡋࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡋࡸ࡯࡮ࠢࡄࡲࠬ঴")
		l1l11l11Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠧࡖࡰࡲࡪ࡫࡯ࡣࡪࡣ࡯ࠤࡘࡵࡵࡳࡥࡨࠤࠫࠦࡗࡪ࡮࡯ࠤࡓࡵࡷࠡࡆࡨࡰࡪࡺࡥࠡࡒ࡯ࡩࡦࡹࡥࠨ঵")
		l1l11l1lCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠨࡋࡱࡷࡹࡧ࡬࡭ࠢࡃ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࡪࡷࡸࡵࡀ࠯࠰࡯ࡸࡧࡰࡿࡳ࠯࡯ࡨࡨ࡮ࡧࡰࡰࡴࡷࡥࡱ࠺࡫ࡰࡦ࡬࠲ࡲࡲ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨশ")
		l1l11ll1Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠩࡕࡩࡲࡵࡶࡦࡦࠣࡅࡳࡵ࡮ࡺ࡯ࡲࡹࡸࠦࡒࡦࡲࡲࠤࡆࡴࡤࠡࡃࡧࡨࡴࡴࡳࠨষ")
		l1l11lllCreated_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠪࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡓࡰࡪࡧࡳࡦࠢࡇࡳࡳࡺࠠࡔࡷࡳࡴࡴࡸࡴࠡࡋࡧ࡭ࡴࡺࡳࠨস")
		l1ll1Created_By_Mucky_Duck.show_ok_dialog([l1l111llCreated_By_Mucky_Duck, l1l11l11Created_By_Mucky_Duck, l1l11l1lCreated_By_Mucky_Duck], l1l1lCreated_By_Mucky_Duck)
		llCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.get_path()
		shutil.rmtree(llCreated_By_Mucky_Duck, ignore_errors=True)
		shutil.rmtree(l111lCreated_By_Mucky_Duck, ignore_errors=True)
		shutil.rmtree(l11llCreated_By_Mucky_Duck, ignore_errors=True)
		shutil.rmtree(l11l1Created_By_Mucky_Duck, ignore_errors=True)
		l1ll1Created_By_Mucky_Duck.log(l1lllCreated_By_Mucky_Duck (u"ࠫࡂࡃ࠽ࡅࡇࡏࡉ࡙ࡏࡎࡈ࠿ࡀࡁࡆࡔࡏࡏ࡛ࡐࡓ࡚࡙࠽࠾࠿ࡄࡈࡉࡕࡎࡔ࠿ࡀࡁ࠰ࡃ࠽࠾ࡔࡈࡔࡔࡃ࠽࠾ࠩহ"))
		l1ll1Created_By_Mucky_Duck.show_ok_dialog([l1l11ll1Created_By_Mucky_Duck, l1l11lllCreated_By_Mucky_Duck], l1l1lCreated_By_Mucky_Duck)
		time.sleep(2)
		os._exit(0)
def l1ll1111Created_By_Mucky_Duck():
	l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠬ࠹࠮࡫ࡲࡪࠫ঺")
	if l11l11lCreated_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫ঻"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩ়ࠬ"): l1lllCreated_By_Mucky_Duck (u"ࠨࡨࡨࡸࡨ࡮࡟ࡧࡣࡹࡷࠬঽ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧা"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞࡝ࡅࡡࡒ࡟ࠠࡂࡆࡇ࠱ࡔࡔࠠࡇࡃ࡙ࡓ࡚ࡘࡉࡕࡇࡖ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩি"), l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨী"):l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩু")})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫূ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࠵࠳ࠪৃ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ৄ"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡗࡋࡑࡖࡇࡖࡘࡊࡊ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ৅"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ৆"):l1ll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫ࠴ࡩࡡࡵࡧࡪࡳࡷࡿ࠯࡭࡫ࡶࡸ࠲ࡩࡡࡳࡶࡲࡳࡳࡹ࠭ࡳࡧࡴࡹࡪࡹࡴ࠰ࠩে"), l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ৈ"):l1lllCreated_By_Mucky_Duck (u"࠭ࡣࡢࡴࡷࡳࡴࡴࡳࠨ৉")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧ৊"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ো"):l1lllCreated_By_Mucky_Duck (u"ࠩ࠷࠵ࠬৌ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ্"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡌࡂࡖࡈࡗ࡙ࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫৎ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ৏"):l1ll11Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧ৐"):l1lllCreated_By_Mucky_Duck (u"ࠧࡤࡣࡵࡸࡴࡵ࡮ࡴࠩ৑")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨ৒"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ৓"):l1lllCreated_By_Mucky_Duck (u"ࠪ࠸࠶࠭৔"), l1lllCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ৕"):l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡅࡋࡖࡒࡊ࡟࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ৖"), l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪৗ"):l1ll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠧ࠰ࡥࡤࡸࡪ࡭࡯ࡳࡻ࠲ࡨ࡮ࡹ࡮ࡦࡻ࠲ࠫ৘"), l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ৙"):l1lllCreated_By_Mucky_Duck (u"ࠩࡦࡥࡷࡺ࡯ࡰࡰࡶࠫ৚")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪ৛"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩড়"):l1lllCreated_By_Mucky_Duck (u"ࠬ࠺࠱ࠨঢ়"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ৞"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡖࡉࡗࡏࡅࡔ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧয়"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬৠ"):l1ll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠩ࠲ࡸࡦ࡭࠯ࡴࡧࡵ࡭ࡪࡹ࠯ࠨৡ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫৢ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡨࡧࡲࡵࡱࡲࡲࡸ࠭ৣ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬ৤"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫ৥"):l1lllCreated_By_Mucky_Duck (u"ࠧ࠵࠳ࠪ০"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭১"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡒࡕࡖࡊࡇࡖ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩ২"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ৩"):l1ll11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫ࠴ࡩࡡࡵࡧࡪࡳࡷࡿ࠯࡮ࡱࡹ࡭ࡪ࠵ࠧ৪"), l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭৫"):l1lllCreated_By_Mucky_Duck (u"࠭ࡣࡢࡴࡷࡳࡴࡴࡳࠨ৬")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧ৭"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭৮"):l1lllCreated_By_Mucky_Duck (u"ࠩࡶࡩࡦࡸࡣࡩࠩ৯"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨৰ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡓࡆࡃࡕࡇࡍࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫৱ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ৲"):l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ৳"), l1lllCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ৴"):l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡤࡶࡹࡵ࡯࡯ࡵࠪ৵")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࠧ৶"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠪࡗࡊࡇࡒࡄࡊ࠱ࡴࡳ࡭ࠧ৷"), l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫ৸"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ৹"):l1lllCreated_By_Mucky_Duck (u"࠭࠴࠴ࠩ৺"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ৻"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡋࡊࡔࡒࡆ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧৼ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭৽"):l1ll11Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫ৾"):l1lllCreated_By_Mucky_Duck (u"ࠫࡨࡧࡲࡵࡱࡲࡲࡸ࠭৿")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡯ࡣࡰࡰࠪ਀"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"࠭ࡇࡆࡐࡕࡉ࠳ࡶ࡮ࡨࠩਁ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧਂ"):l111ll1Created_By_Mucky_Duck})
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠨࡨ࡬ࡰࡪࡹࠧਃ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡩࡳࡻ࠭ࡷ࡫ࡨࡻࠬ਄"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l111l11Created_By_Mucky_Duck(url,content):
	if l1ll11Created_By_Mucky_Duck in url:
		l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠪ࠷࠳ࡰࡰࡨࠩਅ")
	else:
		l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫ࠹࠴ࡪࡱࡩࠪਆ")
	link = open_url(url).content
	l1l11Created_By_Mucky_Duck = md.regex_get_all(link, l1lllCreated_By_Mucky_Duck (u"ࠬࡂࡡࡳࡶ࡬ࡧࡱ࡫ࠧਇ"), l1lllCreated_By_Mucky_Duck (u"࠭࠼࠰ࡣࡵࡸ࡮ࡩ࡬ࡦࠩਈ"))
	items = len(l1l11Created_By_Mucky_Duck)
	for a in l1l11Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠧࡳࡧ࡯ࡁࠧࡨ࡯ࡰ࡭ࡰࡥࡷࡱࠢ࠿ࠩਉ"), l1lllCreated_By_Mucky_Duck (u"ࠨ࠾࠲ࠫਊ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠩࡉࡹࡱࡲࠠࡉࡆࠪ਋"),l1lllCreated_By_Mucky_Duck (u"ࠪࠫ਌")).strip()
		name = l1ll1Created_By_Mucky_Duck.unescape(name)
		name = name.encode(l1lllCreated_By_Mucky_Duck (u"ࠫࡦࡹࡣࡪ࡫ࠪ਍"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬ਎")).decode(l1lllCreated_By_Mucky_Duck (u"࠭ࡡࡴࡥ࡬࡭ࠬਏ"))
		url = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠧࡩࡴࡨࡪࡂࠨࠧਐ"), l1lllCreated_By_Mucky_Duck (u"ࠨࠤࠪ਑"))
		l1llCreated_By_Mucky_Duck = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠩࡶࡶࡨࡃࠢࠨ਒"), l1lllCreated_By_Mucky_Duck (u"ࠪࠦࠬਓ"))
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩਔ"):l1lllCreated_By_Mucky_Duck (u"ࠬ࠺࠲ࠨਕ"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫਖ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪਗ") %name, l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬਘ"):url,
			   l1lllCreated_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪਙ"):content, l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭ਚ"):l1llCreated_By_Mucky_Duck}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠫ࡮ࡩ࡯࡯ࠩਛ"):l1llCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬਜ"):l111ll1Created_By_Mucky_Duck}, item_count=items)
	try:
		l11lllllCreated_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"࠭࠼࡭࡫ࡱ࡯ࠥࡸࡥ࡭࠿ࠥࡲࡪࡾࡴࠣࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪਝ")).findall(link)[0]
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬਞ"):l1lllCreated_By_Mucky_Duck (u"ࠨ࠶࠴ࠫਟ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧਠ"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡎࡣ࡛ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝࠿ࡀࡊࡳ࡚ࠥ࡯ࠡࡐࡨࡼࡹࠦࡐࡢࡩࡨࡂࡃࡄ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࡠ࠵ࡉ࡞ࠩਡ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨਢ"):l11lllllCreated_By_Mucky_Duck},
			  fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡯ࡣࡰࡰࠪਣ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡦࡺࡷ࠲ࡵࡴࡧࠨਤ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧਥ"):l111ll1Created_By_Mucky_Duck})
	except:pass
	if l1ll11Created_By_Mucky_Duck in url:
		setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨਦ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡷࡳࡴࡴ࠭ࡷ࡫ࡨࡻࠬਧ"))
	else:
		setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪਨ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡦࡴࡩ࡮ࡧ࠰ࡺ࡮࡫ࡷࠨ਩"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1ll1llCreated_By_Mucky_Duck(name,url,l1lll1lCreated_By_Mucky_Duck):
	l1lll11lCreated_By_Mucky_Duck = url
	if l1ll11Created_By_Mucky_Duck in url:
		l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠬ࠹࠮࡫ࡲࡪࠫਪ")
	else:
		l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"࠭࠴࠯࡬ࡳ࡫ࠬਫ")
	l1ll1l11Created_By_Mucky_Duck = name.replace(l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠪਬ"),l1lllCreated_By_Mucky_Duck (u"ࠨࠩਭ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠩ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨਮ"),l1lllCreated_By_Mucky_Duck (u"ࠪࠫਯ"))
	link = open_url(url).content
	if l1lllCreated_By_Mucky_Duck (u"ࠫࡊࡶࡩࡴࡱࡧࡩࠥࡒࡩࡴࡶࠪਰ") in link or l1lllCreated_By_Mucky_Duck (u"ࠬࡋࡰࡪࡵࡲࡨࡪࡹࠠࡍ࡫ࡶࡸࠬ਱") in link:
		l1l11Created_By_Mucky_Duck = md.regex_get_all(link, l1lllCreated_By_Mucky_Duck (u"࠭ࡅࡱ࡫ࡶࡳࡩ࡫࡛࡟ࡀࡠ࠮ࡡࡹࡌࡪࡵࡷࠫਲ"), l1lllCreated_By_Mucky_Duck (u"ࠧ࠽࠱ࡸࡰࠬਲ਼"))
		match = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠨ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠰࠿ࠪࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦ࠳࠰࠿࠿ࠪ࠱࠮ࡄ࠯࠼࠰ࡣࡁࠫ਴")).findall(str(l1l11Created_By_Mucky_Duck))
		for url, name in match:
			name = l1ll1Created_By_Mucky_Duck.unescape(name)
			name = l1ll1Created_By_Mucky_Duck.unescape(name).replace(l1lllCreated_By_Mucky_Duck (u"ࠤ࡟ࡠࠬࠨਵ"),l1lllCreated_By_Mucky_Duck (u"ࠥࠫࠧਸ਼"))
			name = name.encode(l1lllCreated_By_Mucky_Duck (u"ࠫࡦࡹࡣࡪ࡫ࠪ਷"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬਸ")).decode(l1lllCreated_By_Mucky_Duck (u"࠭ࡡࡴࡥ࡬࡭ࠬਹ"))
			name = name.replace(l1lllCreated_By_Mucky_Duck (u"ࠧࡆࡲ࡬ࡷࡴࡪࡥࠨ਺"),l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࡅࡱ࡫ࡶࡳࡩ࡫࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ਻"))
			name = name.replace(l1lllCreated_By_Mucky_Duck (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧ਼ࠪ"),l1lllCreated_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࡇࡳ࡭ࡸࡵࡤࡦ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ਽"))
			if l1ll1l11Created_By_Mucky_Duck in name:
				name = name.replace(l1ll1l11Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠫࠬਾ"))
			md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪਿ"):l1lllCreated_By_Mucky_Duck (u"࠭࠴࠷ࠩੀ"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬੁ"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫੂ") %name, l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭੃"):url},
				  fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨ੄"):l1lll1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫ੅"):l111ll1Created_By_Mucky_Duck}, is_folder=False)
	else:
		try:
			try:
				url = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠬࠨࡦࡪ࡮ࡨࠦ࠳࠰࠿ࠣࠪ࠱࠮ࡄ࠯ࠢࠨ੆")).findall(link)[-1]
			except:
				url = re.compile(l1lllCreated_By_Mucky_Duck (u"࠭ࠢࡧ࡫࡯ࡩࠧ࠴ࠪࡀࠤࠫ࠲࠯ࡅࠩࠣࠩੇ")).findall(link)[0]
		except:
			l1ll1l1Created_By_Mucky_Duck = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡲࠨ࡫ࡩࡶࡦࡳࡥ࡜ࡠࡁࡡ࠯ࡢࡳࡴࡴࡦࡁࠧ࠮࡛࡟ࠤࡠ࠯࠮ࠨࠧੈ"), str(link), re.I|re.DOTALL)[0]
			l11lll11Created_By_Mucky_Duck = open_url(l1ll1l1Created_By_Mucky_Duck).content
			data = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡳࠩࠫࡃࡁࡃ࡜ࡼࠫࠫ࡟ࡣࡢࡽ࡞࠭ࠬࠬࡄࡃ࡜ࡾࠫࠪ੉"), str(l11lll11Created_By_Mucky_Duck), re.I|re.DOTALL)[0]
			l111l1lCreated_By_Mucky_Duck = l1ll1l1Created_By_Mucky_Duck.split(l1lllCreated_By_Mucky_Duck (u"ࠩࡀࠫ੊"))[1]
			l1l1l1Created_By_Mucky_Duck = l1ll1l1Created_By_Mucky_Duck.split(l1lllCreated_By_Mucky_Duck (u"ࠪࡩࡲࡨࡥࡥ࠯ࠪੋ"))[1].split(l1lllCreated_By_Mucky_Duck (u"ࠫ࠴࠭ੌ"))[0]
			l1l1lllCreated_By_Mucky_Duck = re.findall(l1lllCreated_By_Mucky_Duck (u"ࠬࠨࡡ࡫ࡣࡻࡣࡺࡸ࡬ࠣ࠼ࠥࠬࡠࡤࠢ࡞੍࠭ࠬࠦࠬ"),data)[0].replace(l1lllCreated_By_Mucky_Duck (u"࠭࡜࡝࠱ࠪ੎"),l1lllCreated_By_Mucky_Duck (u"ࠧ࠰ࠩ੏"))
			info = re.findall(l1lllCreated_By_Mucky_Duck (u"ࠨࠤࡤ࡮ࡦࡾ࡟ࡨࡧࡷࡣࡻ࡯ࡤࡦࡱࡢ࡭ࡳ࡬࡯ࠣ࠼ࠥࠬࡠࡤࠢ࡞࠭ࠬࠦࠬ੐"),data)[0]
			l1l1lll1Created_By_Mucky_Duck = {l1lllCreated_By_Mucky_Duck (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩੑ"):l1lllCreated_By_Mucky_Duck (u"ࠪࡥ࡯ࡧࡸࡠࡩࡨࡸࡤࡼࡩࡥࡧࡲࡣ࡮ࡴࡦࡰࠩ੒"), l1lllCreated_By_Mucky_Duck (u"ࠫࡻ࡯ࡤࡠ࡫ࡧࠫ੓"):l111l1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠬࡴ࡯࡯ࡥࡨࠫ੔"):info, l1lllCreated_By_Mucky_Duck (u"࠭ࡳࡦࡴࡹࡩࡷ࠭੕"):l1l1l1Created_By_Mucky_Duck}
			headers = {l1lllCreated_By_Mucky_Duck (u"ࠧࡂࡥࡦࡩࡵࡺࠧ੖"):l1lllCreated_By_Mucky_Duck (u"ࠨࠬ࠲࠮ࠬ੗"), l1lllCreated_By_Mucky_Duck (u"ࠩࡄࡧࡨ࡫ࡰࡵ࠯ࡈࡲࡨࡵࡤࡪࡰࡪࠫ੘"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡫ࡿ࡯ࡰ࠭ࠢࡧࡩ࡫ࡲࡡࡵࡧࠪਖ਼"), l1lllCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷ࠱ࡑࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ਗ਼"):l1lllCreated_By_Mucky_Duck (u"ࠬ࡫࡮࠮ࡗࡖ࠰ࡪࡴ࠻ࡲ࠿࠳࠲࠽࠭ਜ਼"),
				   l1lllCreated_By_Mucky_Duck (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬੜ"):l1lllCreated_By_Mucky_Duck (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡸࡹࡺ࠱࡫ࡵࡲ࡮࠯ࡸࡶࡱ࡫࡮ࡤࡱࡧࡩࡩࡁࠠࡤࡪࡤࡶࡸ࡫ࡴ࠾ࡗࡗࡊ࠲࠾ࠧ੝"),
				   l1lllCreated_By_Mucky_Duck (u"ࠨࡑࡵ࡭࡬࡯࡮ࠨਫ਼"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡲࡲࡱ࡯࡮ࡦ࠵ࡶ࠲ࡳ࡫ࡴࠨ੟"), l1lllCreated_By_Mucky_Duck (u"ࠪࡖࡪ࡬ࡥࡳࡧࡵࠫ੠"):l1ll1l1Created_By_Mucky_Duck,
				   l1lllCreated_By_Mucky_Duck (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨ੡"):md.User_Agent(), l1lllCreated_By_Mucky_Duck (u"ࠬ࡞࠭ࡓࡧࡴࡹࡪࡹࡴࡦࡦ࠰࡛࡮ࡺࡨࠨ੢"):l1lllCreated_By_Mucky_Duck (u"࠭ࡘࡎࡎࡋࡸࡹࡶࡒࡦࡳࡸࡩࡸࡺࠧ੣")}
			final = open_url(l1l1lllCreated_By_Mucky_Duck, method=l1lllCreated_By_Mucky_Duck (u"ࠧࡱࡱࡶࡸࠬ੤"), data=l1l1lll1Created_By_Mucky_Duck, headers=headers).json()
			l1ll111Created_By_Mucky_Duck = []
			l1l11llCreated_By_Mucky_Duck = []
			l11l111Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠨࠩ੥")
			if l11l1l1Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠩࡷࡶࡺ࡫ࠧ੦"):
				try:
					from operator import itemgetter
					url = max(final, key=itemgetter(l1lllCreated_By_Mucky_Duck (u"ࠪࡰࡦࡨࡥ࡭ࠩ੧")))
				except:
					url = max(final, key=lambda l11ll1l1Created_By_Mucky_Duck: int(re.sub(l1lllCreated_By_Mucky_Duck (u"ࠫࡡࡊࠧ੨"), l1lllCreated_By_Mucky_Duck (u"ࠬ࠭੩"), l11ll1l1Created_By_Mucky_Duck[l1lllCreated_By_Mucky_Duck (u"࠭࡬ࡢࡤࡨࡰࠬ੪")])))
				url = url[l1lllCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࠬ੫")]
			else:
				match = final
				for a in match:
					l11l111Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪ੬") %a[l1lllCreated_By_Mucky_Duck (u"ࠩ࡯ࡥࡧ࡫࡬ࠨ੭")]
					l1ll111Created_By_Mucky_Duck.append(l11l111Created_By_Mucky_Duck)
					l1l11llCreated_By_Mucky_Duck.append(a[l1lllCreated_By_Mucky_Duck (u"ࠪࡪ࡮ࡲࡥࠨ੮")])
				if len(match) >1:
					l1lll11Created_By_Mucky_Duck = md.dialog_select(l1lllCreated_By_Mucky_Duck (u"ࠫࡘ࡫࡬ࡦࡥࡷࠤࡘࡺࡲࡦࡣࡰࠤࡖࡻࡡ࡭࡫ࡷࡽࠬ੯"),l1ll111Created_By_Mucky_Duck)
					if l1lll11Created_By_Mucky_Duck == -1:
						return
					elif l1lll11Created_By_Mucky_Duck > -1:
						url = l1l11llCreated_By_Mucky_Duck[l1lll11Created_By_Mucky_Duck]
				else:
					url = final[0][l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡩ࡭ࡧࠪੰ")]
		if l1lllCreated_By_Mucky_Duck (u"࠭࠯ࡱࡴࡨࡺ࡮࡫ࡷࠨੱ") in url:
			headers = {l1lllCreated_By_Mucky_Duck (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫੲ"):md.User_Agent()}
			link = open_url(url, headers=headers,allow_redirects=False, verify=False).content
			match=re.compile(l1lllCreated_By_Mucky_Duck (u"ࠨࠤࡸࡶࡱࡥࡥ࡯ࡥࡲࡨࡪࡪ࡟ࡧ࡯ࡷࡣࡸࡺࡲࡦࡣࡰࡣࡲࡧࡰࠣ࠮ࠥ࡭ࡹࡧࡧ࡝࡞࡟ࡹ࠵࠶࠳ࡥ࠰࠭ࡃࡡࡢ࡜ࡶ࠲࠳࠶࠻ࡻࡲ࡭࡞࡟ࡠࡺ࠶࠰࠴ࡦࠫ࠲࠯ࡅࠩࠦ࠵ࡅࠫੳ")).findall(link)[0]
			url = urllib.unquote(match)
			url = url.replace(l1lllCreated_By_Mucky_Duck (u"ࠩ࡟ࡠࡺ࠶࠰࠴ࡦࠪੴ"),l1lllCreated_By_Mucky_Duck (u"ࠪࡁࠬੵ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠫࡡࡢࡵ࠱࠲࠵࠺ࠬ੶"),l1lllCreated_By_Mucky_Duck (u"ࠬࠬࠧ੷"))
			if l1lllCreated_By_Mucky_Duck (u"࠭ࡶࡪࡦࡨࡳ࠴ࡾ࠭ࡧ࡮ࡹࠫ੸") in url:
				url = url.partition(l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࡁࠬ੹"))[2]
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭੺"):l1lllCreated_By_Mucky_Duck (u"ࠩࡵࡩࡸࡵ࡬ࡷࡧࠪ੻"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ੼"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡏ࡝࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࡒ࡯ࡥࡾࠦࡍࡰࡸ࡬ࡩࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟࡞࠳ࡎࡣࠧ੽"),
			   l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ੾"):str(url)}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫ੿"):l1lll1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧ઀"):l111ll1Created_By_Mucky_Duck}, is_folder=False)
	if l1ll11Created_By_Mucky_Duck in l1lll11lCreated_By_Mucky_Duck:
		setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨઁ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡷࡳࡴࡴ࠭ࡷ࡫ࡨࡻࠬં"))
	else:
		setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪઃ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡦࡴࡩ࡮ࡧ࠰ࡺ࡮࡫ࡷࠨ઄"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l11ll111Created_By_Mucky_Duck(url):
	link = open_url(url).content
	match = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠬࡂ࡯ࡱࡶ࡬ࡳࡳࠦࡣ࡭ࡣࡶࡷࡂࠨ࡬ࡦࡸࡨࡰ࠲࠶ࠢࠡࡸࡤࡰࡺ࡫࠽ࠣࠪ࠱࠮ࡄ࠯ࠢ࠿ࠪ࠱࠮ࡄ࠯࠼࠰ࡱࡳࡸ࡮ࡵ࡮࠿ࠩઅ")).findall(link)
	for url,name in match:
		name = name.replace(l1lllCreated_By_Mucky_Duck (u"࠭ࠦ࡯ࡤࡶࡴࡀ࠭આ"),l1lllCreated_By_Mucky_Duck (u"ࠧࠡࠩઇ"))
		url = l1lllCreated_By_Mucky_Duck (u"ࠨࠧࡶ࠳ࡄࡩࡡࡵ࠿ࠨࡷࠬઈ") %(l1ll11Created_By_Mucky_Duck,url)
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧઉ"):l1lllCreated_By_Mucky_Duck (u"ࠪ࠸࠶࠭ઊ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩઋ"):l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨઌ") %name,
			   l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪઍ"):url}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲࠬ઎"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠨࡉࡈࡒࡗࡋ࠮ࡱࡰࡪࠫએ"), l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩઐ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠪ࠷࠳ࡰࡰࡨࠩઑ")})
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪ઒"), l1lllCreated_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨઓ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1111lCreated_By_Mucky_Duck(url,name,content,fan_art,l1l111lCreated_By_Mucky_Duck):
	link = open_url(url).content
	try:
		try:
			url = re.compile(l1lllCreated_By_Mucky_Duck (u"࠭ࠢࡧ࡫࡯ࡩࠧ࠴ࠪࡀࠤࠫ࠲࠯ࡅࠩࠣࠩઔ")).findall(link)[-1]
		except:
			url = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠧࠣࡨ࡬ࡰࡪࠨ࠮ࠫࡁࠥࠬ࠳࠰࠿ࠪࠤࠪક")).findall(link)[0]
	except:
		l1ll1l1Created_By_Mucky_Duck = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡳࠩ࡬ࡪࡷࡧ࡭ࡦ࡝ࡡࡂࡢ࠰࡜ࡴࡵࡵࡧࡂࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨખ"), str(link), re.I|re.DOTALL)[0]
		l11lll11Created_By_Mucky_Duck = open_url(l1ll1l1Created_By_Mucky_Duck).content
		data = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡴࠪࠬࡄࡂ࠽࡝ࡽࠬࠬࡠࡤ࡜ࡾ࡟࠮࠭࠭ࡅ࠽࡝ࡿࠬࠫગ"), str(l11lll11Created_By_Mucky_Duck), re.I|re.DOTALL)[0]
		l111l1lCreated_By_Mucky_Duck = l1ll1l1Created_By_Mucky_Duck.split(l1lllCreated_By_Mucky_Duck (u"ࠪࡁࠬઘ"))[1]
		l1l1l1Created_By_Mucky_Duck = l1ll1l1Created_By_Mucky_Duck.split(l1lllCreated_By_Mucky_Duck (u"ࠫࡪࡳࡢࡦࡦ࠰ࠫઙ"))[1].split(l1lllCreated_By_Mucky_Duck (u"ࠬ࠵ࠧચ"))[0]
		l1l1lllCreated_By_Mucky_Duck = re.findall(l1lllCreated_By_Mucky_Duck (u"࠭ࠢࡢ࡬ࡤࡼࡤࡻࡲ࡭ࠤ࠽ࠦ࠭ࡡ࡞ࠣ࡟࠮࠭ࠧ࠭છ"),data)[0].replace(l1lllCreated_By_Mucky_Duck (u"ࠧ࡝࡞࠲ࠫજ"),l1lllCreated_By_Mucky_Duck (u"ࠨ࠱ࠪઝ"))
		info = re.findall(l1lllCreated_By_Mucky_Duck (u"ࠩࠥࡥ࡯ࡧࡸࡠࡩࡨࡸࡤࡼࡩࡥࡧࡲࡣ࡮ࡴࡦࡰࠤ࠽ࠦ࠭ࡡ࡞ࠣ࡟࠮࠭ࠧ࠭ઞ"),data)[0]
		l1l1lll1Created_By_Mucky_Duck = {l1lllCreated_By_Mucky_Duck (u"ࠪࡥࡨࡺࡩࡰࡰࠪટ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡦࡰࡡࡹࡡࡪࡩࡹࡥࡶࡪࡦࡨࡳࡤ࡯࡮ࡧࡱࠪઠ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡼࡩࡥࡡ࡬ࡨࠬડ"):l111l1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡰࡰࡦࡩࠬઢ"):info, l1lllCreated_By_Mucky_Duck (u"ࠧࡴࡧࡵࡺࡪࡸࠧણ"):l1l1l1Created_By_Mucky_Duck}
		headers = {l1lllCreated_By_Mucky_Duck (u"ࠨࡃࡦࡧࡪࡶࡴࠨત"):l1lllCreated_By_Mucky_Duck (u"ࠩ࠭࠳࠯࠭થ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡅࡨࡩࡥࡱࡶ࠰ࡉࡳࡩ࡯ࡥ࡫ࡱ࡫ࠬદ"):l1lllCreated_By_Mucky_Duck (u"ࠫ࡬ࢀࡩࡱ࠮ࠣࡨࡪ࡬࡬ࡢࡶࡨࠫધ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡇࡣࡤࡧࡳࡸ࠲ࡒࡡ࡯ࡩࡸࡥ࡬࡫ࠧન"):l1lllCreated_By_Mucky_Duck (u"࠭ࡥ࡯࠯ࡘࡗ࠱࡫࡮࠼ࡳࡀ࠴࠳࠾ࠧ઩"),
			   l1lllCreated_By_Mucky_Duck (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭પ"):l1lllCreated_By_Mucky_Duck (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡹࡺࡻ࠲࡬࡯ࡳ࡯࠰ࡹࡷࡲࡥ࡯ࡥࡲࡨࡪࡪ࠻ࠡࡥ࡫ࡥࡷࡹࡥࡵ࠿ࡘࡘࡋ࠳࠸ࠨફ"),
			   l1lllCreated_By_Mucky_Duck (u"ࠩࡒࡶ࡮࡭ࡩ࡯ࠩબ"):l1lllCreated_By_Mucky_Duck (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡳࡳࡲࡩ࡯ࡧ࠶ࡷ࠳ࡴࡥࡵࠩભ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡗ࡫ࡦࡦࡴࡨࡶࠬમ"):l1ll1l1Created_By_Mucky_Duck,
			   l1lllCreated_By_Mucky_Duck (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩય"):md.User_Agent(), l1lllCreated_By_Mucky_Duck (u"࠭ࡘ࠮ࡔࡨࡵࡺ࡫ࡳࡵࡧࡧ࠱࡜࡯ࡴࡩࠩર"):l1lllCreated_By_Mucky_Duck (u"࡙ࠧࡏࡏࡌࡹࡺࡰࡓࡧࡴࡹࡪࡹࡴࠨ઱")}
		final = open_url(l1l1lllCreated_By_Mucky_Duck, method=l1lllCreated_By_Mucky_Duck (u"ࠨࡲࡲࡷࡹ࠭લ"), data=l1l1lll1Created_By_Mucky_Duck, headers=headers).json()
		l1ll111Created_By_Mucky_Duck = []
		l1l11llCreated_By_Mucky_Duck = []
		l11l111Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠩࠪળ")
		if l11l1l1Created_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨ઴"):
			try:
				from operator import itemgetter
				url = max(final, key=itemgetter(l1lllCreated_By_Mucky_Duck (u"ࠫࡱࡧࡢࡦ࡮ࠪવ")))
			except:
				url = max(final, key=lambda l11ll1l1Created_By_Mucky_Duck: int(re.sub(l1lllCreated_By_Mucky_Duck (u"ࠬࡢࡄࠨશ"), l1lllCreated_By_Mucky_Duck (u"࠭ࠧષ"), l11ll1l1Created_By_Mucky_Duck[l1lllCreated_By_Mucky_Duck (u"ࠧ࡭ࡣࡥࡩࡱ࠭સ")])))
			url = url[l1lllCreated_By_Mucky_Duck (u"ࠨࡨ࡬ࡰࡪ࠭હ")]
		else:
			match = final
			for a in match:
				l11l111Created_By_Mucky_Duck = l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫ઺") %a[l1lllCreated_By_Mucky_Duck (u"ࠪࡰࡦࡨࡥ࡭ࠩ઻")]
				l1ll111Created_By_Mucky_Duck.append(l11l111Created_By_Mucky_Duck)
				l1l11llCreated_By_Mucky_Duck.append(a[l1lllCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦ઼ࠩ")])
			if len(match) >1:
				l1lll11Created_By_Mucky_Duck = md.dialog_select(l1lllCreated_By_Mucky_Duck (u"࡙ࠬࡥ࡭ࡧࡦࡸ࡙ࠥࡴࡳࡧࡤࡱࠥࡗࡵࡢ࡮࡬ࡸࡾ࠭ઽ"),l1ll111Created_By_Mucky_Duck)
				if l1lll11Created_By_Mucky_Duck == -1:
					return
				elif l1lll11Created_By_Mucky_Duck > -1:
					url = l1l11llCreated_By_Mucky_Duck[l1lll11Created_By_Mucky_Duck]
			else:
				url = final[0][l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࠫા")]
	url = url.replace(l1lllCreated_By_Mucky_Duck (u"ࠧࠡࠩિ"),l1lllCreated_By_Mucky_Duck (u"ࠨࠩી")).replace(l1lllCreated_By_Mucky_Duck (u"ࠩ࡟ࡸࠬુ"),l1lllCreated_By_Mucky_Duck (u"ࠪࠫૂ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠫࡡࡸࠧૃ"),l1lllCreated_By_Mucky_Duck (u"ࠬ࠭ૄ")).replace(l1lllCreated_By_Mucky_Duck (u"࠭࡜࡯ࠩૅ"),l1lllCreated_By_Mucky_Duck (u"ࠧࠨ૆"))
	if l1lllCreated_By_Mucky_Duck (u"ࠨ࠱ࡳࡶࡪࡼࡩࡦࡹࠪે") in url:
		headers = {l1lllCreated_By_Mucky_Duck (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭ૈ"):md.User_Agent()}
		link = open_url(url, headers=headers,allow_redirects=False, verify=False).text
		match=re.compile(l1lllCreated_By_Mucky_Duck (u"ࠪࠦࡺࡸ࡬ࡠࡧࡱࡧࡴࡪࡥࡥࡡࡩࡱࡹࡥࡳࡵࡴࡨࡥࡲࡥ࡭ࡢࡲࠥ࠰ࠧ࡯ࡴࡢࡩ࡟ࡠࡡࡻ࠰࠱࠵ࡧ࠲࠯ࡅ࡜࡝࡞ࡸ࠴࠵࠸࠶ࡶࡴ࡯ࡠࡡࡢࡵ࠱࠲࠶ࡨ࠭࠴ࠪࡀࠫࠨ࠷ࡇ࠭ૉ")).findall(link)[0]
		url = urllib.unquote(match)
		url = url.replace(l1lllCreated_By_Mucky_Duck (u"ࠫࡡࡢࡵ࠱࠲࠶ࡨࠬ૊"),l1lllCreated_By_Mucky_Duck (u"ࠬࡃࠧો")).replace(l1lllCreated_By_Mucky_Duck (u"࠭࡜࡝ࡷ࠳࠴࠷࠼ࠧૌ"),l1lllCreated_By_Mucky_Duck (u"્ࠧࠧࠩ"))
		if l1lllCreated_By_Mucky_Duck (u"ࠨࡸ࡬ࡨࡪࡵ࠯ࡹ࠯ࡩࡰࡻ࠭૎") in url:
			url = url.partition(l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱࡃࠧ૏"))[2]
	md.resolved(url, name, fan_art, l1l111lCreated_By_Mucky_Duck)
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1l1l1llCreated_By_Mucky_Duck():
	l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠪ࠸࠳ࡰࡰࡨࠩૐ")
	if l11l11lCreated_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠫࡹࡸࡵࡦࠩ૑"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ૒"): l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡦࡶࡦ࡬ࡤ࡬ࡡࡷࡵࠪ૓"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ૔"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣ࡛ࡃ࡟ࡐ࡝ࠥࡇࡄࡅ࠯ࡒࡒࠥࡌࡁࡗࡑࡘࡖࡎ࡚ࡅࡔ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧ૕"), l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭૖"):l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ૗")})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩ૘"):l1lllCreated_By_Mucky_Duck (u"ࠬ࠺࠱ࠨ૙"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ૚"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡈࡒࡌࡒࡉࡔࡊࠣࡗ࡚ࡈࡂࡆࡆ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨ૛"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ૜"):l1ll1lCreated_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠩ࠲ࡧࡦࡺࡥࡨࡱࡵࡽ࠴࡫࡮ࡨ࡮࡬ࡷ࡭࠳ࡳࡶࡤࡥࡩࡩ࠵ࠧ૝"), l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫ૞"):l1lllCreated_By_Mucky_Duck (u"ࠫࡦࡴࡩ࡮ࡧࠪ૟")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬૠ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫૡ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࠵࠳ࠪૢ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ૣ"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡊࡔࡇࡍࡋࡖࡌࠥࡊࡕࡃࡄࡈࡈࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪ૤"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ૥"):l1ll1lCreated_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫ࠴ࡩࡡࡵࡧࡪࡳࡷࡿ࠯ࡦࡰࡪࡰ࡮ࡹࡨ࠮ࡦࡸࡦࡧ࡫ࡤ࠰ࠩ૦"), l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭૧"):l1lllCreated_By_Mucky_Duck (u"࠭ࡡ࡯࡫ࡰࡩࠬ૨")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧ૩"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭૪"):l1lllCreated_By_Mucky_Duck (u"ࠩ࠷࠵ࠬ૫"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ૬"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡌࡂࡖࡈࡗ࡙ࠦࡁࡅࡆࡈࡈࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪ૭"), l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ૮"):l1ll1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧ૯"):l1lllCreated_By_Mucky_Duck (u"ࠧࡢࡰ࡬ࡱࡪ࠭૰")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨ૱"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ૲"):l1lllCreated_By_Mucky_Duck (u"ࠪ࠸࠶࠭૳"), l1lllCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ૴"):l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡔࡇࡕࡍࡊ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ૵"), l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ૶"):l1ll1lCreated_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠧ࠰ࡥࡤࡸࡪ࡭࡯ࡳࡻ࠲ࡥࡳ࡯࡭ࡦ࠯ࡶ࡬ࡴࡽࡳ࠰ࠩ૷"), l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ૸"):l1lllCreated_By_Mucky_Duck (u"ࠩࡤࡲ࡮ࡳࡥࠨૹ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪૺ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩૻ"):l1lllCreated_By_Mucky_Duck (u"ࠬ࠺࠱ࠨૼ"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ૽"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡐࡓ࡛ࡏࡅࡔ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧ૾"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ૿"):l1ll1lCreated_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠩ࠲ࡧࡦࡺࡥࡨࡱࡵࡽ࠴ࡧ࡮ࡪ࡯ࡨ࠱ࡲࡵࡶࡪࡧࡶ࠳ࠬ଀"), l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫଁ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡦࡴࡩ࡮ࡧࠪଂ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬଃ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫ଄"):l1lllCreated_By_Mucky_Duck (u"ࠧࡴࡧࡤࡶࡨ࡮ࠧଅ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ଆ"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡘࡋࡁࡓࡅࡋ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩଇ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧଈ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨଉ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ଊ"):l1lllCreated_By_Mucky_Duck (u"࠭ࡡ࡯࡫ࡰࡩࠬଋ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲࠬଌ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠨࡕࡈࡅࡗࡉࡈ࠯ࡲࡱ࡫ࠬ଍"), l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩ଎"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨଏ"):l1lllCreated_By_Mucky_Duck (u"ࠫ࠺࠷ࠧଐ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ଑"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࡉࡈࡒࡗࡋ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ଒"), l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫଓ"):l1ll1lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩଔ"):l1lllCreated_By_Mucky_Duck (u"ࠩࡤࡲ࡮ࡳࡥࠨକ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨଖ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫࡌࡋࡎࡓࡇ࠱ࡴࡳ࡭ࠧଗ"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬଘ"):l111ll1Created_By_Mucky_Duck})
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࡷࠬଙ"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪଚ"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1l1111lCreated_By_Mucky_Duck(url):
	link = open_url(url).content
	match = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠨ࠾ࡲࡴࡹ࡯࡯࡯ࠢࡦࡰࡦࡹࡳ࠾ࠤ࡯ࡩࡻ࡫࡬࠮࠲ࠥࠤࡻࡧ࡬ࡶࡧࡀࠦ࠭࠴ࠪࡀࠫࠥࡂ࠭࠴ࠪࡀࠫ࠿࠳ࡴࡶࡴࡪࡱࡱࡂࠬଛ")).findall(link)
	for url,name in match:
		name = name.replace(l1lllCreated_By_Mucky_Duck (u"ࠩࠩࡲࡧࡹࡰ࠼ࠩଜ"),l1lllCreated_By_Mucky_Duck (u"ࠪࠤࠬଝ"))
		url = l1lllCreated_By_Mucky_Duck (u"ࠫࠪࡹ࠯ࡀࡥࡤࡸࡂࠫࡳࠨଞ") %(l1ll1lCreated_By_Mucky_Duck,url)
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪଟ"):l1lllCreated_By_Mucky_Duck (u"࠭࠴࠲ࠩଠ"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬଡ"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫଢ") %name,
			   l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ଣ"):url}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨତ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫࡌࡋࡎࡓࡇ࠱ࡴࡳ࡭ࠧଥ"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬଦ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"࠭࠴࠯࡬ࡳ࡫ࠬଧ")})
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭ନ"), l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫ଩"))
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l11ll1llCreated_By_Mucky_Duck():
	l111ll1Created_By_Mucky_Duck = l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠩ࠸࠲ࡵࡴࡧࠨପ")
	if l11l11lCreated_By_Mucky_Duck == l1lllCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨଫ"):
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩବ"): l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡥࡵࡥ࡫ࡣ࡫ࡧࡶࡴࠩଭ"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫମ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡡࡂ࡞ࡏ࡜ࠤࡆࡊࡄ࠮ࡑࡑࠤࡋࡇࡖࡐࡗࡕࡍ࡙ࡋࡓ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ଯ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬର"):l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭଱")})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨଲ"):l1lllCreated_By_Mucky_Duck (u"ࠫ࠻࠷ࠧଳ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ଴"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࡖࡕࡉࡓࡊࡉࡏࡉࠣࡈࡔࡉࡕࡎࡇࡑࡘࡆࡘࡉࡆࡕ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨଵ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫଶ"):l1lll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩଷ"):l1lllCreated_By_Mucky_Duck (u"ࠩࡧࡳࡨࡹࠧସ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪହ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩ଺"):l1lllCreated_By_Mucky_Duck (u"ࠬ࠼࠱ࠨ଻"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨ଼ࠫ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡗࡓࡕࠦ࠱࠱࠲ࠣࡈࡔࡉࡕࡎࡇࡑࡘࡆࡘࡉࡆࡕ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨଽ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬା"):l1lll1Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠩ࠲ࡸࡴࡶ࠭࠲࠲࠳࠱ࡩࡵࡣࡶ࡯ࡨࡲࡹࡧࡲࡺ࠯ࡩ࡭ࡱࡳࡳ࠰ࠩି"), l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫୀ"):l1lllCreated_By_Mucky_Duck (u"ࠫࡩࡵࡣࡴࠩୁ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬୂ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫୃ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࠷࠳ࠪୄ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭୅"):l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡓࡋࡗࠡࡃࡕࡖࡎ࡜ࡁࡍࡕ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨ୆"), l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧେ"):l1lll1Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫ࠴ࡴࡥࡸ࠯ࡤࡶࡷ࡯ࡶࡢ࡮ࡶ࠳ࠬୈ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭୉"):l1lllCreated_By_Mucky_Duck (u"࠭ࡤࡰࡥࡶࠫ୊")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧୋ"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ୌ"):l1lllCreated_By_Mucky_Duck (u"ࠩ࠹࠺୍ࠬ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ୎"):l1lllCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠢࡔࡗࡕࡔࡗࡏࡓࡆࠢࡐࡉࠦࠨ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ୏"), l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ୐"):l1lll1Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"࠭࠯ࡀࡴࡤࡲࡩࡵ࡭ࠨ୑"), l1lllCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ୒"):l1lllCreated_By_Mucky_Duck (u"ࠨࡦࡲࡧࡸ࠭୓")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩ୔"):l111ll1Created_By_Mucky_Duck}, is_folder=False)
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨ୕"):l1lllCreated_By_Mucky_Duck (u"ࠫ࠻࠷ࠧୖ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪୗ"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࡔࡄࡒࡉࡕࡍࠡࡒࡌࡇࡐ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ୘"), l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ୙"):l1lll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ୚"):l1lllCreated_By_Mucky_Duck (u"ࠩࡧࡳࡨࡹࠧ୛")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪࡪࡦࡴࡡࡳࡶࠪଡ଼"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩଢ଼"):l1lllCreated_By_Mucky_Duck (u"ࠬ࠼࠱ࠨ୞"), l1lllCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫୟ"):l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡗࡓࡕࠦࡒࡂࡖࡈࡈࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪୠ"), l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬୡ"):l1lll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪୢ"):l1lllCreated_By_Mucky_Duck (u"ࠪࡨࡴࡩࡳࠨୣ")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫ୤"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ୥"):l1lllCreated_By_Mucky_Duck (u"࠭ࡳࡦࡣࡵࡧ࡭࠭୦"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ୧"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡗࡊࡇࡒࡄࡊ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨ୨"), l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭୩"):l1lllCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ୪"), l1lllCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬ୫"):l1lllCreated_By_Mucky_Duck (u"ࠬࡪ࡯ࡤࡵࠪ୬")}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫ୭"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠧࡔࡇࡄࡖࡈࡎ࠮ࡱࡰࡪࠫ୮"),l1lllCreated_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨ୯"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ୰"):l1lllCreated_By_Mucky_Duck (u"ࠪ࠺࠸࠭ୱ"), l1lllCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩ୲"):l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡈࡇࡑࡖࡊࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫ୳"), l1lllCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪ୴"):l1lll1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ୵"):l1lllCreated_By_Mucky_Duck (u"ࠨࡦࡲࡧࡸ࠭୶")}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࠧ୷"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠪࡋࡊࡔࡒࡆ࠰ࡳࡲ࡬࠭୸"), l1lllCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࠫ୹"):l111ll1Created_By_Mucky_Duck})
	md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ୺"):l1lllCreated_By_Mucky_Duck (u"࠭࠶࠵ࠩ୻"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ୼"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡅ࠴ࡠ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ୽"), l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭୾"):l1lll1Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠪ࠳࡫ࡻ࡬࡭࠯ࡧࡳࡨࡻ࡭ࡦࡰࡷࡥࡷࡿ࠭࡭࡫ࡶࡸ࠴࠭୿"), l1lllCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬ஀"):l1lllCreated_By_Mucky_Duck (u"ࠬࡪ࡯ࡤࡵࠪ஁")}, fan_art={l1lllCreated_By_Mucky_Duck (u"࠭ࡦࡢࡰࡤࡶࡹ࠭ஂ"):l111ll1Created_By_Mucky_Duck})
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭ஃ"), l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫ஄"))
def l1ll11l1Created_By_Mucky_Duck(name,url,content):
	link = open_url(url,verify=False).content
	name = name.replace(l1lllCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࠬஅ"),l1lllCreated_By_Mucky_Duck (u"ࠪࠫஆ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠫࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪஇ"),l1lllCreated_By_Mucky_Duck (u"ࠬ࠭ஈ"))
	index2 = (l1lllCreated_By_Mucky_Duck (u"࠭ࡔࡐࡒࠣ࠵࠵࠶ࠠࡅࡑࡆ࡙ࡒࡋࡎࡕࡃࡕࡍࡊ࡙ࠧஉ"), l1lllCreated_By_Mucky_Duck (u"ࠧࡏࡇ࡚ࠤࡆࡘࡒࡊࡘࡄࡐࡘ࠭ஊ"))
	if name in index2:
		l1l11Created_By_Mucky_Duck = md.regex_get_all(link, l1lllCreated_By_Mucky_Duck (u"ࠨࡥ࡯ࡥࡸࡹ࠽ࠣࡶ࡬ࡰࡪ࠭஋"), l1lllCreated_By_Mucky_Duck (u"ࠩࡥࡸࡳ࠳ࡰࡳ࡫ࡰࡥࡷࡿࠠࡣࡶࡱ࠱ࡧࡲ࡯ࡤ࡭ࠪ஌"))
	else:
		link = link.replace(l1lllCreated_By_Mucky_Duck (u"ࠪࡠࡷ࠭஍"),l1lllCreated_By_Mucky_Duck (u"ࠫࠬஎ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠬࡢ࡮ࠨஏ"),l1lllCreated_By_Mucky_Duck (u"࠭ࠧஐ"))
		l11111lCreated_By_Mucky_Duck = md.regex_get_all(link, l1lllCreated_By_Mucky_Duck (u"ࠧ࠽ࡪ࠴ࠤࡨࡲࡡࡴࡵࡀࠦࡻ࡯ࡤࡦࡱ࠰ࡶࡴࡽ࠭ࡩࡧࡤࡨ࡮ࡴࡧࠣࡀࠨࡷࠬ஑") %name, l1lllCreated_By_Mucky_Duck (u"ࠨ࠾࠲ࡨ࡮ࡼ࠾࠽࠱ࡧ࡭ࡻࡄࠧஒ"))
		l1l11Created_By_Mucky_Duck = md.regex_get_all(str(l11111lCreated_By_Mucky_Duck), l1lllCreated_By_Mucky_Duck (u"ࠩࠥ࡭ࡹ࡫࡭ࠣࠩஓ"), l1lllCreated_By_Mucky_Duck (u"ࠪࡦࡹࡴ࠭ࡱࡴ࡬ࡱࡦࡸࡹࠡࡤࡷࡲ࠲ࡨ࡬ࡰࡥ࡮ࠫஔ"))
	items = len(l1l11Created_By_Mucky_Duck)
	for a in l1l11Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠫࡁ࡮࠱࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿࠱࠮ࡄࡄࠧக"), l1lllCreated_By_Mucky_Duck (u"ࠬࡂ࠯ࠨ஖"))
		name = l1ll1Created_By_Mucky_Duck.unescape(name)
		url = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"࠭ࡨࡳࡧࡩࡁࠧ࠭஗"), l1lllCreated_By_Mucky_Duck (u"ࠧࠣࠩ஘"))
		l1llCreated_By_Mucky_Duck = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠨࡵࡵࡧࡂࠨࠧங"), l1lllCreated_By_Mucky_Duck (u"ࠩࠥࠫச"))
		l11lllCreated_By_Mucky_Duck = md.regex_from_to(a, l1lllCreated_By_Mucky_Duck (u"ࠪࡀࡵࡄࠧ஛"), l1lllCreated_By_Mucky_Duck (u"ࠫࡁ࠵ࡰ࠿ࠩஜ"))
		l11lllCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.unescape(l11lllCreated_By_Mucky_Duck)
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ஝"):l1lllCreated_By_Mucky_Duck (u"࠭࠶࠷ࠩஞ"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬட"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫ஠") %name, l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭஡"):url, l1lllCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫ஢"):l1lllCreated_By_Mucky_Duck (u"ࠫࡩࡵࡣࡴࠩண")},
			  {l1lllCreated_By_Mucky_Duck (u"ࠬࡶ࡬ࡰࡶࠪத"):l11lllCreated_By_Mucky_Duck}, {l1lllCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫ஥"):l1llCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡣࡱࡥࡷࡺࠧ஦"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠨ࠷࠱ࡴࡳ࡭ࠧ஧")}, is_folder=False, item_count=items)
	try:
		l1111l1Created_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠤ࠿ࡷࡵࡧ࡮ࠡࡥ࡯ࡥࡸࡹ࠽ࠨࡲࡤ࡫ࡪࡹࠧ࠿ࠪ࠱࠮ࡄ࠯࠼࠰ࡵࡳࡥࡳࡄࠢந")).findall(link)[0]
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨன"):l1lllCreated_By_Mucky_Duck (u"ࠫࡩࡻ࡭࡮ࡻࠪப"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ஫"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡊ࡟࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠ࡟࠴ࡏ࡝ࠨ஬") %l1111l1Created_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫ஭"):l1lllCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬம")},
			  fan_art={l1lllCreated_By_Mucky_Duck (u"ࠩࡩࡥࡳࡧࡲࡵࠩய"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠪ࠹࠳ࡶ࡮ࡨࠩர")}, is_folder=False, is_playable=False)
	except: pass
	try:
		l11lllllCreated_By_Mucky_Duck = re.compile(l1lllCreated_By_Mucky_Duck (u"ࠫࡁࡧࠠࡤ࡮ࡤࡷࡸࡃࠢ࡯ࡧࡻࡸࡵࡵࡳࡵࡵ࡯࡭ࡳࡱࠢࠡࡴࡨࡰࡂࠨ࡮ࡦࡺࡷࠦࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠪࡀࠫࠥࡂࠬற")).findall(link)[0]
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪல"):l1lllCreated_By_Mucky_Duck (u"࠭࠶࠲ࠩள"), l1lllCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬழ"):l1lllCreated_By_Mucky_Duck (u"ࠨ࡝ࡌࡡࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡄ࠾ࡈࡱࠣࡘࡴࠦࡎࡦࡺࡷࠤࡕࡧࡧࡦࡀࡁࡂࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟࡞࠳ࡎࡣࠧவ"),
			   l1lllCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ஶ"):l11lllllCreated_By_Mucky_Duck}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨஷ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫࡳ࡫ࡸࡵ࠰ࡳࡲ࡬࠭ஸ"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬஹ"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"࠭࠵࠯ࡲࡱ࡫ࠬ஺")})
	except:pass
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧ஻"), l1lllCreated_By_Mucky_Duck (u"ࠨࡦࡲࡧ࠲ࡼࡩࡦࡹࠪ஼"))
def l1ll1lllCreated_By_Mucky_Duck(url):
	link = open_url(url,verify=False).content
	match=re.compile(l1lllCreated_By_Mucky_Duck (u"ࠩ࠿ࡰ࡮ࠦࡣ࡭ࡣࡶࡷࡂࠨࡣࡢࡶ࠰࡭ࡹ࡫࡭ࠡࡥࡤࡸ࠲࡯ࡴࡦ࡯࠰࠲࠯ࡅࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠰࠿ࠪࠤࠣࡸ࡮ࡺ࡬ࡦ࠿ࠥ࠲࠯ࡅࠢ࠿ࠪ࠱࠮ࡄ࠯࠼࠰ࡣࡁࠫ஽")).findall(link)
	for url,name in match:
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨா"):l1lllCreated_By_Mucky_Duck (u"ࠫ࠻࠷ࠧி"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪீ"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩு") %name, l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫூ"):url, l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩ௃"):l1lllCreated_By_Mucky_Duck (u"ࠩࡧࡳࡨࡹࠧ௄")},
			  fan_art={l1lllCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࠨ௅"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠫࡌࡋࡎࡓࡇ࠱ࡴࡳ࡭ࠧெ"), l1lllCreated_By_Mucky_Duck (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࠬே"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"࠭࠵࠯ࡲࡱ࡫ࠬை")})
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭௉"), l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫொ"))
def l11llll1Created_By_Mucky_Duck(url):
	link = open_url(url,verify=False).content
	match=re.compile(l1lllCreated_By_Mucky_Duck (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡤࡱ࡯࠱ࡸࡳ࠭࠲࠲ࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯ࠬࡂ࠭ࠧࠦࡲࡦ࡮ࡀࠦࡧࡵ࡯࡬࡯ࡤࡶࡰࠨࠠࡵ࡫ࡷࡰࡪࡃࠢ࠯ࠬࡂࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡲࡩࡴࡶ࠰࡭ࡹ࡫࡭࠮ࡶ࡬ࡸࡱ࡫ࠢ࠿ࠪ࠱࠮ࡄ࠯࠼࠰ࡣࡁࡀ࠴ࡪࡩࡷࡀࠪோ")).findall(link)
	for url,name in match:
		name = l1ll1Created_By_Mucky_Duck.unescape(name)
		md.addDir({l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨௌ"):l1lllCreated_By_Mucky_Duck (u"ࠫ࠻࠼்ࠧ"), l1lllCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪ௎"):l1lllCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩ௏") %name, l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫௐ"):url}, fan_art={l1lllCreated_By_Mucky_Duck (u"ࠨࡨࡤࡲࡦࡸࡴࠨ௑"):l11l11Created_By_Mucky_Duck+l1lllCreated_By_Mucky_Duck (u"ࠩ࠸࠲ࡵࡴࡧࠨ௒")})
	setView(l1ll1ll1Created_By_Mucky_Duck,l1lllCreated_By_Mucky_Duck (u"ࠪࡪ࡮ࡲࡥࡴࠩ௓"), l1lllCreated_By_Mucky_Duck (u"ࠫࡲ࡫࡮ࡶ࠯ࡹ࡭ࡪࡽࠧ௔"))
def l1l11l1Created_By_Mucky_Duck(url,name,content,fan_art,l1l111lCreated_By_Mucky_Duck):
	l1lll11lCreated_By_Mucky_Duck = url
	link = open_url(url,verify=False).content
	if name == l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠣࡕࡘࡖࡕࡘࡉࡔࡇࠣࡑࡊࠧࠢ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭௕"):
		name = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡸࠧ࠽ࡪ࠴ࠤࡨࡲࡡࡴࡵࡀࠦࡵࡵࡳࡵ࠯ࡷ࡭ࡹࡲࡥࠣࠢ࡬ࡸࡪࡳࡰࡳࡱࡳࡁࠧࡴࡡ࡮ࡧࠥࡂ࠭࠴ࠪࡀࠫ࠿࠳࡭࠷࠾ࠨ௖"), str(link), re.I|re.DOTALL)[0]
		name = l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠪௗ") %name
		name = l1ll1Created_By_Mucky_Duck.unescape(name)
		l11lllCreated_By_Mucky_Duck = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡳࠩ࠿ࡴࡃ࠮࠮ࠫࡁࠬࡀࡵࡄ࠼ࡴࡲࡤࡲࠬ௘"), str(link), re.I|re.DOTALL)[0]
		l11lllCreated_By_Mucky_Duck = l11lllCreated_By_Mucky_Duck.replace(l1lllCreated_By_Mucky_Duck (u"ࠩ࠿ࡴࡃ࠭௙"),l1lllCreated_By_Mucky_Duck (u"ࠪࠫ௚")).replace(l1lllCreated_By_Mucky_Duck (u"ࠫࡁ࠵ࡰ࠿ࠩ௛"),l1lllCreated_By_Mucky_Duck (u"ࠬ࠭௜"))
		l11lllCreated_By_Mucky_Duck = l1ll1Created_By_Mucky_Duck.unescape(l11lllCreated_By_Mucky_Duck)
		l1l111lCreated_By_Mucky_Duck = {l1lllCreated_By_Mucky_Duck (u"࠭ࡰ࡭ࡱࡷࠫ௝"):l11lllCreated_By_Mucky_Duck}
	request_url = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡲࠨ࠾࡬ࡪࡷࡧ࡭ࡦ࠰࠭ࡃࡸࡸࡣ࠾ࠤࠫ࠲࠯ࡅࠩࠣࠢ࠱࠮ࡄࡄࠧ௞"), str(link), re.I|re.DOTALL)[0]
	request_url = request_url.replace(l1lllCreated_By_Mucky_Duck (u"ࠨࡪࡷࡸࡵࡹ࠺ࠨ௟"),l1lllCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶ࠺ࠨ௠"))
	if l1lllCreated_By_Mucky_Duck (u"ࠪ࡬ࡹࡺࡰ࠻ࠩ௡") not in request_url:
		request_url = l1lllCreated_By_Mucky_Duck (u"ࠫ࡭ࡺࡴࡱ࠼ࠪ௢") + request_url
	if l1lllCreated_By_Mucky_Duck (u"ࠬࡻࡰࡵࡱࡹ࡭ࡩ࡫࡯ࠨ௣") in request_url:
		try:
			headers = {l1lllCreated_By_Mucky_Duck (u"࠭ࡁࡤࡥࡨࡴࡹ࠭௤"):l1lllCreated_By_Mucky_Duck (u"ࠧࡵࡧࡻࡸ࠴࡮ࡴ࡮࡮࠯ࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࡫ࡸࡲࡲࠫࡹ࡯࡯࠰ࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻࡱࡱࡁࡱ࠾࠲࠱࠽࠱࡯࡭ࡢࡩࡨ࠳ࡼ࡫ࡢࡱ࠮࠭࠳࠯ࡁࡱ࠾࠲࠱࠼ࠬ௥"),
				   l1lllCreated_By_Mucky_Duck (u"ࠨࡃࡦࡧࡪࡶࡴ࠮ࡇࡱࡧࡴࡪࡩ࡯ࡩࠪ௦"):l1lllCreated_By_Mucky_Duck (u"ࠩࡪࡾ࡮ࡶࠬࠡࡦࡨࡪࡱࡧࡴࡦ࠮ࠣࡷࡩࡩࡨࠨ௧"), l1lllCreated_By_Mucky_Duck (u"ࠪࡅࡨࡩࡥࡱࡶ࠰ࡐࡦࡴࡧࡶࡣࡪࡩࠬ௨"):l1lllCreated_By_Mucky_Duck (u"ࠫࡪࡴ࠭ࡖࡕ࠯ࡩࡳࡁࡱ࠾࠲࠱࠼ࠬ௩"),
				   l1lllCreated_By_Mucky_Duck (u"ࠬࡉ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩ௪"):l1lllCreated_By_Mucky_Duck (u"࠭࡫ࡦࡧࡳ࠱ࡦࡲࡩࡷࡧࠪ௫"), l1lllCreated_By_Mucky_Duck (u"ࠧࡓࡧࡩࡩࡷ࡫ࡲࠨ௬"):l1lll11lCreated_By_Mucky_Duck, l1lllCreated_By_Mucky_Duck (u"ࠨࡗࡳ࡫ࡷࡧࡤࡦ࠯ࡌࡲࡸ࡫ࡣࡶࡴࡨ࠱ࡗ࡫ࡱࡶࡧࡶࡸࡸ࠭௭"):l1lllCreated_By_Mucky_Duck (u"ࠩ࠴ࠫ௮"), l1lllCreated_By_Mucky_Duck (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧ௯"): md.User_Agent()}
			link = open_url(request_url,headers=headers).content
			if jsunpack.detect(link):
				l11l1lllCreated_By_Mucky_Duck = jsunpack.unpack(link)
				match = re.findall(l1lllCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦ࠼ࠥࠬࡠࡤࠢ࡞࠭ࠬࠫ௰"), l11l1lllCreated_By_Mucky_Duck)
			for url in match:
				if l1lllCreated_By_Mucky_Duck (u"ࠬ࠵ࡶ࠯࡯ࡳ࠸ࠬ௱") in url:
					md.resolved(url, name, fan_art, l1l111lCreated_By_Mucky_Duck)
		except:
			url = urlresolver.resolve(request_url)
	elif l1lllCreated_By_Mucky_Duck (u"࠭ࡲࡵࡦ࠱ࡶࡹ࠴ࡣࡰ࡯ࠪ௲") in request_url:
		link = open_url(request_url).content
		match = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡲࠣࡨ࡬ࡰࡪࡀࠠࠨࠪ࠱࠮ࡄ࠯ࠧࡾࠤ௳"), str(link), re.I|re.DOTALL)[0]
		if l1lllCreated_By_Mucky_Duck (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡵࡸࡩ࠴ࡲࡵ࠰ࡦࡳࡲ࠭௴") not in match:
			match = l1lllCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡶࡹࡪ࠮ࡳࡶ࠱ࡧࡴࡳࠧ௵") + match
		if l1lllCreated_By_Mucky_Duck (u"ࠥࠫࠥ࠱ࠠࠨࠤ௶") in match:
			match = match.replace(l1lllCreated_By_Mucky_Duck (u"ࠦࠬࠦࠫࠡࠩࠥ௷"),l1lllCreated_By_Mucky_Duck (u"ࠧࠨ௸"))
		url = match
	elif l1lllCreated_By_Mucky_Duck (u"࠭ࡹࡰࡷࡷࡹࡧ࡫ࠧ௹") in request_url:
		if l1lllCreated_By_Mucky_Duck (u"ࠧࡷ࡫ࡧࡩࡴࡹࡥࡳ࡫ࡨࡷࡄࡲࡩࡴࡶࠪ௺") in request_url:
			l111l1lCreated_By_Mucky_Duck = request_url.partition(l1lllCreated_By_Mucky_Duck (u"ࠨࡁ࡯࡭ࡸࡺ࠽ࠨ௻"))[2]
			l111l1lCreated_By_Mucky_Duck = l111l1lCreated_By_Mucky_Duck.partition(l1lllCreated_By_Mucky_Duck (u"ࠩࡂࠫ௼"))[0]
			url = l1lllCreated_By_Mucky_Duck (u"ࠪࡴࡱࡻࡧࡪࡰ࠽࠳࠴ࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡾࡵࡵࡵࡷࡥࡩ࠴ࡶ࡬ࡢࡻ࠲ࡃࡵࡲࡡࡺ࡮࡬ࡷࡹࡥࡩࡥ࠿ࠨࡷࠬ௽") % l111l1lCreated_By_Mucky_Duck
		else:
			l111l1lCreated_By_Mucky_Duck = request_url.partition(l1lllCreated_By_Mucky_Duck (u"ࠫࡪࡳࡢࡦࡦ࠲ࠫ௾"))[2]
			l111l1lCreated_By_Mucky_Duck = l111l1lCreated_By_Mucky_Duck.partition(l1lllCreated_By_Mucky_Duck (u"ࠬࡅࠧ௿"))[0]
			url = l1lllCreated_By_Mucky_Duck (u"࠭ࡰ࡭ࡷࡪ࡭ࡳࡀ࠯࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡸ࡬ࡨࡪࡵ࠮ࡺࡱࡸࡸࡺࡨࡥ࠰ࡲ࡯ࡥࡾ࠵࠿ࡷ࡫ࡧࡩࡴࡥࡩࡥ࠿ࠨࡷࠬఀ") % l111l1lCreated_By_Mucky_Duck
	elif l1lllCreated_By_Mucky_Duck (u"ࠧࡴࡰࡤ࡫࡫࡯࡬࡮ࡵ࠱ࡧࡴࡳࠧఁ") in request_url:
		request_url = request_url.replace(l1lllCreated_By_Mucky_Duck (u"ࠨࡧࡰࡦࡪࡪ࠮ࡴࡰࡤ࡫࡫࡯࡬࡮ࡵ࠱ࡧࡴࡳࠧం"), l1lllCreated_By_Mucky_Duck (u"ࠩࡶࡲࡦ࡭ࡦࡪ࡮ࡰࡷ࠳ࡩ࡯࡮ࠩః"))
		link = open_url(request_url).content
		link = link.replace(l1lllCreated_By_Mucky_Duck (u"ࠪࡠࡹ࠭ఄ"),l1lllCreated_By_Mucky_Duck (u"ࠫࠬఅ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠬࡢ࡮ࠨఆ"),l1lllCreated_By_Mucky_Duck (u"࠭ࠧఇ")).replace(l1lllCreated_By_Mucky_Duck (u"ࠧ࡝ࡤࠪఈ"),l1lllCreated_By_Mucky_Duck (u"ࠨࠩఉ"))
		try:
			url = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡴࠪࡪ࡮ࡲ࡭ࡊࡰࡩࡳ࠳ࡹࡲࡤ࠰࠭ࡃࡸࡸࡣ࠻ࠢࠥࠬ࠳࠰࠿ࠪࠤࠪఊ"), str(link), re.I|re.DOTALL)[-1]
		except:
			url = re.findall(l1lllCreated_By_Mucky_Duck (u"ࡵࠫ࡫࡯࡬࡮ࡋࡱࡪࡴ࠴ࡳࡳࡥ࠱࠮ࡄࡹࡲࡤ࠼ࠣࠦ࠭࠴ࠪࡀࠫࠥࠫఋ"), str(link), re.I|re.DOTALL)[0]
	else:
		url = urlresolver.resolve(request_url)
	md.resolved(url, name, fan_art, l1l111lCreated_By_Mucky_Duck)
	l1ll1Created_By_Mucky_Duck.end_of_directory()
def l1lllllCreated_By_Mucky_Duck(content, query):
	try:
		if query:
			search = query.replace(l1lllCreated_By_Mucky_Duck (u"ࠫࠥ࠭ఌ"),l1lllCreated_By_Mucky_Duck (u"ࠬ࠱ࠧ఍"))
		else:
			search = md.search()
			if search == l1lllCreated_By_Mucky_Duck (u"࠭ࠧఎ"):
				md.notification(l1lllCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡡࡂ࡞ࡇࡐࡔ࡙࡟ࠠࡒࡗࡈࡖ࡞ࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠ࠰ࡆࡨ࡯ࡳࡶ࡬ࡲ࡬ࠦࡳࡦࡣࡵࡧ࡭࠭ఏ"),l11l1ll1Created_By_Mucky_Duck)
				return
			else:
				pass
		if content == l1lllCreated_By_Mucky_Duck (u"ࠨࡥࡤࡶࡹࡵ࡯࡯ࡵࠪఐ"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠩࠨࡷ࠴ࡅࡳ࠾ࠧࡶࠫ఑") %(l1ll11Created_By_Mucky_Duck,search)
			l111l11Created_By_Mucky_Duck(url,content)
		elif content == l1lllCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪఒ"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠫࠪࡹ࠯࡮ࡱࡹ࡭ࡪ࠵ࡳࡦࡣࡵࡧ࡭࠵ࠥࡴࠩఓ") %(l1llll11Created_By_Mucky_Duck,search)
			l11l1lCreated_By_Mucky_Duck(url,content)
		elif content == l1lllCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ఔ"):
			url = l1lllCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡵࡨࡥࡷࡩࡨ࠰ࠧࡶࠫక") %(l1llll11Created_By_Mucky_Duck,search)
			l11l1lCreated_By_Mucky_Duck(url,content)
		elif content == l1lllCreated_By_Mucky_Duck (u"ࠧࡥࡱࡦࡷࠬఖ"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠨࠧࡶ࠳ࡄࡹ࠽ࠦࡵࠪగ") %(l1lll1Created_By_Mucky_Duck,search)
			l1ll11l1Created_By_Mucky_Duck(l1lllCreated_By_Mucky_Duck (u"ࠩࠪఘ"),url,content)
		elif content == l1lllCreated_By_Mucky_Duck (u"ࠪࡥࡳ࡯࡭ࡦࠩఙ"):
			url = l1lllCreated_By_Mucky_Duck (u"ࠫࠪࡹ࠯ࡀࡵࡀࠩࡸ࠭చ") %(l1ll1lCreated_By_Mucky_Duck,search)
			l111l11Created_By_Mucky_Duck(url,content)
	except:
		md.notification(l1lllCreated_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠ࡟ࡇࡣࡓࡰࡴࡵࡽ࡙ࠥ࡯࡮ࡧࡷ࡬࡮ࡴࡧ࡙ࠡࡨࡲࡹࠦࡗࡳࡱࡱ࡫ࠥࡇࡢࡰࡴࡷ࡭ࡳ࡭ࠠࡔࡧࡤࡶࡨ࡮࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬఛ"),l11l1ll1Created_By_Mucky_Duck)
md.check_source()
mode = md.args[l1lllCreated_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫజ")]
url = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫఝ"), None)
name = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ఞ"), None)
query = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠩࡴࡹࡪࡸࡹࠨట"), None)
title = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠪࡸ࡮ࡺ࡬ࡦࠩఠ"), None)
l1llll1lCreated_By_Mucky_Duck = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠫࡸ࡫ࡡࡴࡱࡱࠫడ"), None)
l11l1l1lCreated_By_Mucky_Duck = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪ࠭ఢ") ,None)
l1l111lCreated_By_Mucky_Duck = md.args.get(l1lllCreated_By_Mucky_Duck (u"࠭ࡩ࡯ࡨࡲࡰࡦࡨࡥ࡭ࡵࠪణ"), None)
content = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨత"), None)
l1l1111Created_By_Mucky_Duck = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪࡥࡩࡥࠩథ"), None)
l1lll1lCreated_By_Mucky_Duck = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠬద"), None)
fan_art = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠪࡪࡦࡴ࡟ࡢࡴࡷࠫధ"), None)
is_folder = md.args.get(l1lllCreated_By_Mucky_Duck (u"ࠫ࡮ࡹ࡟ࡧࡱ࡯ࡨࡪࡸࠧన"), True)
if mode is None or url is None or len(url)<1:
	l1l111Created_By_Mucky_Duck()
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠬ࠷ࠧ఩"):
	l11l11l1Created_By_Mucky_Duck(content)
elif mode == l1lllCreated_By_Mucky_Duck (u"࠭࠲ࠨప"):
	l11l1lCreated_By_Mucky_Duck(url,content)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠧ࠴ࠩఫ"):
	l1ll11llCreated_By_Mucky_Duck(title, url, l1lll1lCreated_By_Mucky_Duck, content, l1llll1lCreated_By_Mucky_Duck)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠨ࠶ࠪబ"):
	l11l111lCreated_By_Mucky_Duck(url, content)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠩ࠸ࠫభ"):
	l1llllCreated_By_Mucky_Duck(url, content)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠪ࠺ࠬమ"):
	l111llCreated_By_Mucky_Duck(url, content)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠫ࠼࠭య"):
	l1l1llCreated_By_Mucky_Duck(url,name,l1lll1lCreated_By_Mucky_Duck,content,l1l111lCreated_By_Mucky_Duck,query)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠬ࠺࠰ࠨర"):
	l1ll1111Created_By_Mucky_Duck()
elif mode == l1lllCreated_By_Mucky_Duck (u"࠭࠴࠲ࠩఱ"):
	l111l11Created_By_Mucky_Duck(url,content)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠧ࠵࠴ࠪల"):
	l1ll1llCreated_By_Mucky_Duck(name,url,l1lll1lCreated_By_Mucky_Duck)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠨ࠶࠶ࠫళ"):
	l11ll111Created_By_Mucky_Duck(url)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠩ࠷࠺ࠬఴ"):
	l1111lCreated_By_Mucky_Duck(url,name,content,fan_art,l1l111lCreated_By_Mucky_Duck)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠪ࠹࠵࠭వ"):
	l1l1l1llCreated_By_Mucky_Duck()
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠫ࠺࠷ࠧశ"):
	l1l1111lCreated_By_Mucky_Duck(url)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠬ࠼࠰ࠨష"):
	l11ll1llCreated_By_Mucky_Duck()
elif mode == l1lllCreated_By_Mucky_Duck (u"࠭࠶࠲ࠩస"):
	l1ll11l1Created_By_Mucky_Duck(name,url,content)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠧ࠷࠵ࠪహ"):
	l1ll1lllCreated_By_Mucky_Duck(url)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠨ࠸࠷ࠫ఺"):
	l11llll1Created_By_Mucky_Duck(url)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠩ࠹࠺ࠬ఻"):
	l1l11l1Created_By_Mucky_Duck(url,name,content,fan_art,l1l111lCreated_By_Mucky_Duck)
elif mode==99:
	l1llll1Created_By_Mucky_Duck(url)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠪࡶࡪࡹ࡯࡭ࡸࡨ఼ࠫ"):
	md.resolved(url, name, fan_art, l1l111lCreated_By_Mucky_Duck)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠫࡸ࡫ࡡࡳࡥ࡫ࠫఽ"):
	l1lllllCreated_By_Mucky_Duck(content,query)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠬࡧࡤࡥࡱࡱࡣࡸ࡫ࡡࡳࡥ࡫ࠫా"):
	md.addon_search(content,query,fan_art,l1l111lCreated_By_Mucky_Duck)
elif mode == l1lllCreated_By_Mucky_Duck (u"࠭ࡡࡥࡦࡢࡶࡪࡳ࡯ࡷࡧࡢࡪࡦࡼࠧి"):
	md.add_remove_fav(name, url, l1l111lCreated_By_Mucky_Duck, fan_art,
			  content, l1l1111Created_By_Mucky_Duck, is_folder)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠧࡧࡧࡷࡧ࡭ࡥࡦࡢࡸࡶࠫీ"):
	md.fetch_favs(l1llll11Created_By_Mucky_Duck)
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠨࡣࡧࡨࡴࡴ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠩు"):
	l1ll1Created_By_Mucky_Duck.show_settings()
elif mode == l1lllCreated_By_Mucky_Duck (u"ࠩࡰࡩࡹࡧ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠩూ"):
	import metahandler
	metahandler.display_settings()
l1ll1Created_By_Mucky_Duck.end_of_directory()