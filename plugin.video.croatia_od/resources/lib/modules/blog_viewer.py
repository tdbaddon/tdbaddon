# -*- coding: utf-8 -*-
# Import PyXBMCt module.
import pyxbmct.addonwindow as pyxbmct
import xbmcgui
import xbmc

class Viewer(pyxbmct.AddonDialogWindow):

    def __init__(self, title='', text='', image='', video=None):
        # You need to call base class' constructor.
        super(Viewer, self).__init__(title)
        self.video = video
        self.title = title
        self.pos = 0
        self.image = image
        self.text = text
    
        import textwrap
        dedented_text = textwrap.dedent(self.text).strip()
        self.text = textwrap.fill(dedented_text, width=60)
        self.setGeometry(1100, 500, 6, 3)

        img = pyxbmct.Image(self.image)
        self.placeControl(img, 0, 0, rowspan = 3)

        self.textb = pyxbmct.TextBox()
        self.placeControl(self.textb,0,1, rowspan=6, columnspan=2)
        self.textb.setText(self.text)

        self.textb.autoScroll(1000,1500,1000)
        
        if self.video:
            video_button = pyxbmct.Button("Play video")
            self.placeControl(video_button,2,1)
            self.connect(video_button,self.play)
        

    def play(self):
        self.close()
        li = xbmcgui.ListItem(self.title)
        li.setInfo('video', { 'title': self.title })
        li.setThumbnailImage(self.image)
        player = xbmc.Player()
        player.play(item=self.video, listitem=li)