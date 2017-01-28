# script constantes
__script__ = "MyFont.py"
__author__ = "Ppic, Frost, AjDeveloped"
__credits__ = "Team XBMC-Passion, http://passion-xbmc.org/"
__platform__ = "xbmc media center, [LINUX, OS X, WIN32, XBOX]"
__date__ = "08-01-2010"
__version__ = "1.2"

# python librairy to add font to the current skin. need to have font_filename.ttf in /resources/fonts/, this script will automatically add it to current skin when called.

import os
import elementtree.ElementTree as ET
import shutil
from traceback import print_exc
import xbmc  # @UnresolvedImport


class FontModifier:

    def __init__(self, addon_path):
        self.skin_font_path = xbmc.translatePath("special://skin/fonts/")
        self.script_font_path = os.path.join(addon_path , "resources" , "fonts")
        self.skin_dir = xbmc.translatePath("special://skin/")
        self.list_dir = os.listdir(self.skin_dir)
    
    
    def loadMyFontFile(self):
        try:
            myfont_xml = os.path.join(self.script_font_path, "MyFont.xml")
            if os.path.exists(myfont_xml):
                root = ET.parse(open(myfont_xml, "r")).getroot()
                for myfont in root.getchildren():
                    style = ""
                    if myfont.attrib.has_key('style'):
                        style = myfont.attrib['style']
                    aspect = ""
                    if myfont.attrib.has_key('aspect'):
                        aspect = myfont.attrib['aspect']
                    
                    self.addFont(myfont.attrib['name'], myfont.attrib['filename'], myfont.attrib['size'], style, aspect)
        except:
            print_exc()
        
    
    def getFontsXML(self):
        fontxml_paths = []
        try:
            for item in self.list_dir:
                item = os.path.join(self.skin_dir, item)
                if os.path.isdir(item):
                    font_xml = os.path.join(item, "Font.xml")
                    if os.path.exists(font_xml):
                        fontxml_paths.append(font_xml)
        except:
            print_exc()
        return fontxml_paths
    
    
    def isFontInstalled(self, fontxml_path, fontname):
        name = "<name>%s</name>" % fontname
        if not name in file(fontxml_path, "r").read():
            print "font name not installed!", fontname
            return False
        else:
            print "font name already installed!", fontname
            return True
    
    
    def addFont(self, fontname, filename, size, style="", aspect=""):
        try:
            reload_skin = False
            fontxml_paths = self.getFontsXML()
    
            if fontxml_paths:
                for fontxml_path in fontxml_paths:
                    print "analyse du fichier: " + fontxml_path
                    if not self.isFontInstalled(fontxml_path, fontname):
                        tree = ET.parse(fontxml_path)
                        root = tree.getroot()
                        print "modification du fichier: " + fontxml_path
                        for sets in root.getchildren():
                            sets.findall("font")[ -1 ].tail = "\n\t\t"  # "\n\n\t\t"
                            new = ET.SubElement(sets, "font")
                            new.text, new.tail = "\n\t\t\t", "\n\t"
                            subnew1 = ET.SubElement(new , "name")
                            subnew1.text = fontname
                            subnew1.tail = "\n\t\t\t"
                            subnew2 = ET.SubElement(new , "filename")
                            subnew2.text = (filename, "Arial.ttf")[ sets.attrib.get("id") == "Arial" ]
                            subnew2.tail = "\n\t\t\t"
                            subnew3 = ET.SubElement(new , "size")
                            subnew3.text = size
                            subnew3.tail = "\n\t\t\t"
                            last_elem = subnew3
                            if style in [ "normal", "bold", "italics", "bolditalics" ]:
                                subnew4 = ET.SubElement(new , "style")
                                subnew4.text = style
                                subnew4.tail = "\n\t\t\t"
                                last_elem = subnew4
                            if aspect:    
                                subnew5 = ET.SubElement(new , "aspect")
                                subnew5.text = aspect
                                subnew5.tail = "\n\t\t\t"
                                last_elem = subnew5
                            reload_skin = True
     
                            last_elem.tail = "\n\t\t"
                        tree.write(fontxml_path)
                        reload_skin = True
        except:
            print_exc()
    
        if reload_skin:
            if not os.path.exists(os.path.join(self.skin_font_path, filename)) and os.path.exists(os.path.join(self.script_font_path, filename)):
                shutil.copyfile(os.path.join(self.script_font_path, filename), os.path.join(self.skin_font_path, filename))
    
            xbmc.executebuiltin("XBMC.ReloadSkin()")
            return True
    
        return False

