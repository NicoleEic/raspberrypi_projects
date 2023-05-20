import sys
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.input.providers.hidinput import HIDMotionEvent
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import *
import numpy as np
from colorthief import ColorThief
import math
import colorsys
from skimage import io
from skimage.segmentation import felzenszwalb, find_boundaries
import numpy as np
from kivy.uix.slider import Slider
import random

Window.clearcolor = (0.9, 0.9, 0.9, 1)

class MyBackground(Widget):
    def __init__(self, mysize, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        self.fpath = 'sunflower.jpeg'
        self.mysize = mysize
        print(self.mysize)
        with self.canvas:
            img = io.imread(self.fpath)
            img_segments = felzenszwalb(img, scale=300, sigma=2, min_size=1000)
            imgmat = find_boundaries(img_segments).astype(np.uint8)
            io.imsave('test.png', imgmat*-255)
            self.bg = Rectangle(source='test.png', pos=(0,0), size=self.mysize)


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.draw_background()
        self.dirs = np.ones(3)

    def draw_background(self):
        self.bg = MyBackground(mysize=self.size)
        self.add_widget(self.bg)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not isinstance(touch, HIDMotionEvent):
                with self.canvas:
                    Color(rgba=self.pencolor)
                    d = self.pendiameter
                    Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                    touch.ud['line'] = Line(points=(touch.x, touch.y))



    def on_touch_move(self, touch):
        first_col = np.array(self.btncol[0:3])*255
        current_col = np.array(self.pencolor[0:3])*255
        max_steps = np.array([4,4,4])
        max_limit = 20
        ranges = [np.arange(first_col[i]-max_limit, first_col[i]+max_limit) for i in np.arange(3)]

        if self.collide_point(*touch.pos):
            if not isinstance(touch, HIDMotionEvent):
                touch.ud['line'].width = self.pendiameter/2
                touch.ud['line'].points += [touch.x, touch.y]
                new_col = np.zeros(3)
                for i in np.arange(3):
                    change = np.random.randint(1, max_steps[i])
                    changed = current_col[i] + (change * self.dirs[i])
                    if (changed not in ranges[i]) or changed > 255 or changed < 0 :
                        self.dirs[i] = -self.dirs[i]
                        print(i)
                    new_col[i] = current_col[i] + (change * self.dirs[i])
                print(new_col)
                self.pencolor = tuple(np.hstack((new_col/255, 1)))
                self.on_touch_down(touch)




class MyPaintApp(App):

    
    def build(self):
        parent = Widget()
        self.imagefile = 'sunflower.jpeg'
        self.painter = MyPaintWidget(size=(Window.size[0], Window.size[1]-200))
        parent.add_widget(self.painter)
        
        closebtn = Button(text='Close', size_hint=(None, None), size=(100, 50), pos=(Window.width - 100, Window.height - 50))
        closebtn.bind(on_release=self.myclose)
        parent.add_widget(closebtn)

        clearbtn = Button(text='Clear', size_hint=(None, None), size=(100, 50), pos=(Window.width - 200, Window.height - 50))
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(clearbtn)
        
        savebtn = Button(text='Save', size_hint=(None, None), size=(100, 50), pos=(Window.width - 300, Window.height - 50))
        savebtn.bind(on_release=self.mysave)
        parent.add_widget(savebtn)

        blankbtn = Button(text='blank', size_hint=(None, None), size=(100, 50), pos=(Window.width - 400, Window.height - 50))
        blankbtn.bind(on_release=self.blank)
        parent.add_widget(blankbtn)

        init_pendiameter = 25
        myslider = Slider(min=2, max=100, value=init_pendiameter, size=(400, 50), pos=(10, Window.height - 50))
        myslider.bind(value=self.OnSliderValueChange)
        parent.add_widget(myslider)
        self.painter.pendiameter = init_pendiameter

        def step(r, g, b, repetitions=1):
            lum = math.sqrt(.241 * r + .691 * g + .068 * b)
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            h2 = int(h * repetitions)
            v2 = int(v * repetitions)
            if h2 % 2 == 1:
                v2 = repetitions - v2
                lum = repetitions - lum
            return (h2, lum, v2)

        n_cols = 20
        color_thief = ColorThief('sunflower.jpeg')
        col_list = np.array(color_thief.get_palette(color_count=n_cols))
        col_list = sorted(col_list, key=lambda color: step(color[0], color[1], color[2], 8))
        col_list = np.array(col_list)/255
        self.init_color = tuple(np.hstack((col_list[0], 1)))
        self.painter.pencolor = self.init_color
        self.painter.btncol = self.init_color

        btn_width = 20
        btn_height = 50
        if Window.width - (n_cols*btn_width+btn_width) < 0:
            print('too many buttons')
            self.myclose_empty()

        for i_c, col in enumerate(col_list):
            bt = Button(text='',
                        background_color=col,
                        background_normal='',
                        size_hint=(None, None), size=(btn_width, btn_height),
                        pos=(Window.width - (i_c*btn_width+btn_width), Window.height - 100))
            bt.bind(on_release=self.newclr)
            parent.add_widget(bt)
        
        return parent

    def OnSliderValueChange(self, instance, value):
        self.painter.pendiameter = value

    def newclr(self, instance):
        newcol = instance.background_color
        newcol = tuple(newcol)
        self.painter.pencolor = newcol
        self.painter.btncol = newcol
        print(newcol)

    def myclose_empty(self):
        self.stop()
        sys.exit()

    def myclose(self, args):
        self.myclose_empty()
        
    def clear_canvas(self, obj):
        self.painter.pencolor = self.init_color
        self.painter.canvas.clear()
        self.painter.draw_background()

    def blank(self, obj):
        print('blank')
        self.painter.pencolor = self.init_color
        self.painter.canvas.clear()

    def mysave(self, obj):
        print('save')
        self.painter.export_as_image().save('image.jpg')
        

if __name__ == '__main__':
    MyPaintApp().run()
