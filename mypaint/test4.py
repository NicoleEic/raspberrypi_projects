from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.button import Button



class MyPaintWidget(Widget):
    global counter
    counter = 1
    def getcounter(self):
        global counter
        return counter
    def setcounter(self):
        global counter
        counter = self.getcounter()
        counter = counter + 1
        return counter
    def on_touch_down(self, touch):
        global counter
        counter = self.getcounter()
        print(counter)
        if counter % 2 == 0:
            with self.canvas:
                Color(1, 1, 0)
                d = 30.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                touch.ud['line'] = Line(points=(touch.x, touch.y))
                self.setcounter()
        else:
            self.setcounter()
            

    def on_touch_move(self, touch):
        counter = self.getcounter() + 1
        if counter % 2 == 0:
            touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):

    def build(self):
        self.counter = 0
        return MyPaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()