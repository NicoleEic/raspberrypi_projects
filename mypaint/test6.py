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


class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='sunflower.jpeg', pos=(0,0), size=Window.size)


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.penrad = 30
        self.pencolor = (0, 0, 0, 1)
        bg = MyBackground()
        self.add_widget(bg)


    def on_touch_down(self, touch):
        if not isinstance(touch, HIDMotionEvent):
            with self.canvas:
                print(self.pencolor)
                Color(rgba=self.pencolor)
                d = self.penrad
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        if not isinstance(touch, HIDMotionEvent):
            touch.ud['line'].width = self.penrad/2
            touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):

    
    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget(size=Window.size)
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
        
        col_list = [(1,0,0,1), (0,1,0,1)]
        
        for i_c, col in enumerate(col_list):
            bt = Button(text='',
                        background_color=col,
                        background_normal='',
                        size_hint=(None, None), size=(100, 50),
                        pos=(Window.width - (i_c*100+100), Window.height - 100))
            bt.bind(on_release=self.newclr)
            parent.add_widget(bt)
        
        return parent


    def newclr(self, instance):
        newcol = instance.background_color
        newcol = tuple(newcol)
        self.painter.pencolor = newcol
        print(newcol)


    def myclose(self, args):
        self.stop()
        sys.exit()
        
    def clear_canvas(self, obj):
        self.painter.pencolor = (0,0,0,1)
        self.painter.canvas.clear()

    def mysave(self, obj):
        print('save')
        self.painter.export_as_image().save('image.jpg')

if __name__ == '__main__':
    MyPaintApp().run()
