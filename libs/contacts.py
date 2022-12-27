from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView

from libs.android_call import dial_up
from libs.android_contacts import get_kind_of_contacts
from libs.long_press import LongPress

Builder.load_string('''
<Contact>:
    canvas.before:
        Color:
            rgba: root.background_color if root.state == 'down' else app.coloro
        RoundedRectangle:
            pos: self.pos
            radius: app.border_radius
            size: self.size
        Color:
            rgba: 1, 1, 1, .1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, app.border_radius[0]

<Contacts>:
    do_scroll_y: False
    effect_cls: 'ScrollEffect'
    scroll_wheel_distance: 120
    viewclass: 'Contact'

    RecycleBoxLayout:
        default_size_hint: None, 1
        default_size: dp(350), dp(400)
        size_hint: None, 1
        spacing: dp(10)
        width: self.minimum_width

''')


class Contact(LongPress, Image):
    font_name = StringProperty('assets/fonts/font.ttf')
    label = ObjectProperty()
    name = StringProperty()
    number = StringProperty()
    outline_width = NumericProperty(3)

    def on_kv_post(self, *largs):
        self.label = Label(font_name=self.font_name,
                           font_size='35sp',
                           markup=True,
                           outline_width=self.outline_width)
        self.bind(number=self.set_text)

    def set_text(self, *largs):
        long_sign = '..' if len(self.name) > 18 else ''
        font_size = int(self.label.font_size / 1.8)
        self.label.text = (f"{self.name[:18]}[size={font_size}]"
                           f"{long_sign}\n{self.number}[/size]")
        Clock.schedule_once(self.changes, 0)

    def changes(self, *largs):
        self.label.texture_update()
        self.texture = self.label.texture

    def on_long_press(self, *largs):
        dial_up(caller=self.number)


class Contacts(RecycleView):
    bar_width = NumericProperty(0)
    starred = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(data=self.refresh_content, starred=self.refresh_content)
        Clock.schedule_once(self.refresh_content, 0)

    def refresh_content(self, *largs):
        """ Refresh contacts every 6 hour """
        Clock.unschedule(self.refresh_content)
        Clock.schedule_once(self.access_contacts, 0)
        Clock.schedule_once(self.refresh_content, 21600)

    def access_contacts(self, *largs):
        self.data = get_kind_of_contacts(self.starred)


if __name__ == '__main__':
    from kivy.app import App

    class ContactCaller(App):
        def build(self):
            return Contacts()

    ContactCaller().run()
