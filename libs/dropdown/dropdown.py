from os.path import dirname, join, realpath

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from libs.long_press import LongPress

__all__ = ('DropDownSettings', )

Builder.load_string('''
<DropDownButton>:
    short_press_time: .1 
    long_press_time: .1
    override: True
    cols: 2
    size_hint_y: None

<DropDownSettings>:
    orientation: 'tb-lr'
    size_hint_y: None
    spacing: dp(5)
    rows: 2
    height: dp(55)

    canvas.before:
        StencilPush
        Rectangle:
            pos: self.pos
            size: self.size
        StencilUse
        Color:
            rgba: app.coloro
        RoundedRectangle:
            pos: self.pos
            radius: app.border_radius
            size: self.size
        Color:
            rgba: 1, 1, 1, .2
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, app.border_radius[0]

    canvas.after:
        StencilUnUse
        Rectangle:
            pos: self.pos
            size: self.size
        StencilPop

    DropDownButton:
        padding: dp(15), dp(10)
        height: self.parent._original_height

        Label:
            color: 1, 1, 1, .6
            font_size: dp(26)
            size_hint_x: None
            outline_width: dp(1)
            size: self.texture_size
            text: root.category

        AnchorLayout:
            anchor_x: 'right'
            Image:
                allow_stretch: True
                size_hint_x: None
                source: root.source
                opacity: .7
                width: dp(30)
                canvas.before:
                    PushMatrix
                    Rotate:
                        angle: root._angle
                        origin: self.center
                canvas.after:
                    PopMatrix

''')


class DropDownButton(LongPress, GridLayout):

    def on_release(self, *largs):
        p = self.parent
        if p._is_open:
            self.animate(p._original_height)
        else:
            self.animate(p.children[0].custom_height)

    def animate(self, box_height, *largs):
        p = self.parent
        anim1 = Animation(_angle=0 if p._is_open else 180,
                          height=box_height,
                          t='out_quad',
                          d=p.delay)
        anim2 = Animation(opacity=0 if p._is_open else 1,
                          t='out_quad',
                          d=p.delay)
        anim1.bind(on_complete=self.set_state)
        anim1.start(p)
        anim2.start(p.children[0])

    def set_state(self, *largs):
        p = self.parent
        p._is_open = p.height > p._original_height


class DropDownSettings(GridLayout):
    _angle = NumericProperty(0)
    _is_open = BooleanProperty(False)
    _original_height = NumericProperty("60dp")
    category = StringProperty('Category')
    delay = NumericProperty(.2)
    source = StringProperty(None, allownone=True)
    orientation = StringProperty('vertical')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = self.source or join(dirname(realpath(__file__)),
                                          'rotate.png')

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return super().on_touch_up(touch)
