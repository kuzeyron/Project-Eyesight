from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.utils import platform

from ..long_press import LongPress
from ..utils import importer

__all__ = ('Contacts', 'Contact')

Contacts = importer(f'libs.contacts.contacts_{platform}', 'Contacts')

Builder.load_string('''
<Contact>:
    font_name: app.settings_font
    opacity: 0
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            pos: self.pos
            radius: app.border_radius
            size: self.size
        Color:
            rgba: 1, 1, 1, .1
        SmoothLine:
            width: dp(2)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, app.border_radius[0]

''')


class Contact(LongPress, Image):
    label = ObjectProperty()
    name = StringProperty()
    number = StringProperty()

    def on_kv_post(self, *largs):
        self._app = App.get_running_app()
        self.label = Label(font_name=self.font_name,
                           font_size='45dp',
                           markup=True,
                           padding=('50dp', '10dp'))
        self._app.bind(settings_font=self.on_number,
                       settings_font_border=self.on_number,
                       coloro=self.set_color)

    def on_number(self, *largs):
        font_size = int(self.label.font_size / 1.8)
        self.label.text = (f"{self.name}[size={font_size}]"
                           f"[color=#ddffe7]\n{self.number}"
                           "[/color][/size]")
        self.label.font_name = self._app.settings_font
        self.label.outline_width = self._app.settings_font_border
        self.label.texture_update()
        self.texture = self.label.texture
        Animation(opacity=1, d=.2, transition='in_out_quad').start(self)

    def on_long_press(self, *largs):
        self._app.contact_caller.call(self.number)

    def set_color(self, *largs):
        self.background_color = self._app.coloro
