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

class MyPaintWidget(Widget):
    Window.clearcolor = (1, 1, 1, 1)
    penrad = NumericProperty(10)
    pencolor = ListProperty([1, 0, 0, 1])  # Red
    
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        colbtn = Button(text='Color', size_hint=(None, None), size=(100, 50), pos=(Window.width - 300, Window.height - 50))
        colbtn.bind(on_release=self.newclr)
        self.add_widget(colbtn)
        

    def on_touch_down(self, touch):
        if not isinstance(touch, HIDMotionEvent):
            color = (random(), 1, 1)
            with self.canvas:
                Color(*color, mode='hsv')
                d = 30.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        if not isinstance(touch, HIDMotionEvent):
            touch.ud['line'].points += [touch.x, touch.y]

    def newclr(self, instance):
        print("Before Change@newclr: pencolor=", self.pencolor)
        self.pencolor = instance.background_color
        print("After Change@newclr: pencolor=", self.pencolor)


class MyPaintApp(App):
    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()
        parent.add_widget(self.painter)
        
        closebtn = Button(text='Close', size_hint=(None, None), size=(100, 50), pos=(Window.width - 100, Window.height - 50))
        closebtn.bind(on_release=self.myclose)
        parent.add_widget(closebtn)
        
        clearbtn = Button(text='Clear', size_hint=(None, None), size=(100, 50), pos=(Window.width - 200, Window.height - 50))
        clearbtn.bind(on_release=self.clear_canvas)
        self.add_widget(clearbtn)
        return parent

    def myclose(self, args):
        self.stop()
        sys.exit()
        
    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    MyPaintApp().run()

