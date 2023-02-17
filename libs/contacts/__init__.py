from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.utils import platform

from libs.android_call import CallService
from libs.long_press import LongPress
from libs.utils import importer

__all__ = ('Contacts', 'Contact')

Contacts = importer(f'libs.contacts.contacts_{platform}', 'Contacts')

Builder.load_string('''
<Contact>:
    font_name: 'assets/fonts/font.ttf'
    opacity: 0
    outline_width: 3
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

''')


class Contact(LongPress, Image):
    label = ObjectProperty()
    name = StringProperty()
    number = StringProperty()

    def on_kv_post(self, *largs):
        self.label = Label(font_name=self.font_name,
                           font_size='45dp',
                           markup=True,
                           outline_width=self.outline_width,
                           padding=('50dp', '10dp'))

    def on_number(self, *largs):
        font_size = int(self.label.font_size / 1.8)
        self.label.text = (f"{self.name}[size={font_size}]"
                           f"[color=#ddffe7]\n{self.number}"
                           "[/color][/size]")
        self.label.texture_update()
        self.texture = self.label.texture
        Animation(opacity=1, d=.2, transition='in_out_quad').start(self)

    def on_long_press(self, *largs):
        CallService(caller=self.number)


if __name__ == '__main__':
    class ContactCaller(App):
        def build(self):
            return Contacts()

    ContactCaller().run()
