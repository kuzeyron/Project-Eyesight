from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import (BooleanProperty, ColorProperty, NumericProperty,
                             StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.colorpicker import ColorWheel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.utils import get_hex_from_color

from libs.configuration import get_value, set_value
from libs.dropdown import DropDownConfig
from libs.long_press import LongPress

__all__ = ['DeviceSettings', ]


Builder.load_string('''
#:import DropDownSettings libs.dropdown.DropDownSettings
#:import PhotoGallery libs.gallery.PhotoGallery
#:import CheckBoxItem libs.checkboxitem.CheckBoxItem
#:import LanguageCrawler libs.checkboxitem.LanguageCrawler
#:import tr __main__.tr

<CategoryBox@BoxLayout>:
    size_hint_y: None
    height: self.minimum_height
    orientation: 'vertical'
    padding: dp(10), dp(10)
    spacing: dp(10)

    canvas.before:
        Color:
            rgba: app.color[:3] + [.2]
        RoundedRectangle:
            radius: [dp(15), ]
            size: self.size
            pos: self.pos
        Color:
            rgba: app.color
        SmoothLine:
            width: dp(2)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, dp(15)


<ContentBox>:
    opacity: 0
    orientation: 'vertical'
    padding: dp(10), dp(10)
    spacing: dp(5)
    canvas.before:
        Color:
            rgba: 1, 1, 1, .15
        RoundedRectangle:
            pos: self.pos
            radius: [dp(10), ]
            size: self.size

<ContentBoxCategory@Label>:
    color: 1, 1, 1, .6
    font_size: dp(28)
    halign: 'left'
    height: dp(42)
    outline_width: dp(1)
    size_hint_y: None
    text_size: self.size

<BackButton>:
    cols: 2
    height: sp(60)
    padding: dp(5), dp(5)
    size_hint_y: None
    canvas.before:
        Color:
            rgba: root.background_color if root.state == 'down' else app.color
        RoundedRectangle:
            pos: self.pos
            radius: [dp(10), ]
            size: self.size
        Color:
            rgba: 1,1,1,.1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, dp(10)

<ToggleStarredContacts>:
    size: dp(50), dp(50)
    size_hint: None, 1
    canvas:
        Clear
        Color:
            rgba: self.color
        Rectangle:
            pos: int(self.center_x - dp(21)), int(self.center_y - dp(21))
            size: dp(42), dp(42)
            source: self._radio_image if self.group else self._checkbox_image

<ContactsCrawler>:
    cols: 2
    canvas.before:
        Color:
            rgba: app.color
        RoundedRectangle:
            pos: self.pos
            radius: [dp(15), ]
            size: self.size

    ToggleStarredContacts:
        id: contacts_type
        on_active:
    CheckBoxLabel:
        font_size: dp(25)
        outline_width: dp(1)
        on_release:
            contacts_type.active = False if contacts_type.active else True
        text: tr._( \
            'Favorite contacts' if contacts_type.active else 'All contacts')
<Crawler>:
    cols: 2
    canvas.before:
        Color:
            rgba: app.color
        RoundedRectangle:
            pos: self.pos
            radius: [dp(15), ]
            size: self.size

<PressDelayCrawler>:
    padding: dp(5), dp(5)
    rows: 2
    canvas.before:
        Color:
            rgba: app.color
        RoundedRectangle:
            pos: self.pos
            radius: [dp(15), ]
            size: self.size

    CheckBoxLabel:
        text: f"  {tr._('Seconds')}: {slider.value}"

    PressDelayItem:
        id: slider

<DeviceSettings>:
    padding: dp(10), dp(15)
    spacing: dp(15)

    BackButton:
        id: backbutton
        Image:
            opacity: .4
            size_hint_x: .1
            source: 'assets/images/back.png'
        Label:
            font_size: sp(25)
            halign: 'left'
            outline_width: dp(1)
            text: tr._('Back')
            text_size: self.size
            valign: 'middle'

    ScrollView:
        bar_width: 0
        do_scroll_x: False
        effect_cls: 'ScrollEffect'

        BoxLayout:
            height: self.minimum_height
            orientation: 'vertical'
            size_hint_y: None
            spacing: dp(20)

            DropDownSettings:
                category: tr._('Press delay')
                ContentBox:
                    PressDelayCrawler

            CategoryBox:
                DropDownSettings:
                    category: tr._('Device language')
                    ContentBox:
                        LanguageCrawler:

                DropDownSettings:
                    category: tr._('Date format')
                    ContentBox:
                        DateFormatCrawler

                DropDownSettings:
                    category: tr._('Time format')
                    ContentBox:
                        TimeFormatCrawler

            DropDownSettings:
                category: tr._('Device contacts')
                ContentBox:
                    ContactsCrawler

            DropDownSettings:
                category: tr._('Color theme')
                ContentBox:
                    custom_height: dp(450)
                    AppColor:
                        opacity: .7

            DropDownSettings:
                category: tr._('Wallpapers')
                id: gallery
                ContentBox:
                    custom_height: dp(450)
                    ScrollView:
                        do_scroll_x: False
                        effect_cls: 'ScrollEffect'
                        PhotoGallery
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: dp(5)
                            is_open: gallery._is_open

''')


class ContentBox(DropDownConfig, BoxLayout):
    pass


class BackButton(LongPress, GridLayout):
    long_press_time = NumericProperty(.5)
    override = BooleanProperty(True)

    def on_short_press(self, *largs):
        instance = App.get_running_app()
        instance.root.transition.direction = 'down'
        instance.root.current = 'home'


class CheckBoxLabel(ButtonBehavior, Label):
    pass


class ToggleStarredContacts(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = get_value('settings').get('starred_contacts')
        self.bind(active=self.set_state)

    def set_state(self, *largs):
        set_value('settings', 'starred_contacts', int(self.active))
        App.get_running_app().starred = self.active


class PressDelayItem(Slider):
    max = NumericProperty(3)
    min = NumericProperty(.1)
    opacity = NumericProperty(.8)
    step = NumericProperty(.1)
    value = NumericProperty(1.5)
    value_track = BooleanProperty(True)
    value_track_color = ColorProperty((0, .8, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self.time_set)

    def on_kv_post(self, *largs):
        instance = App.get_running_app()
        self.value = instance.press_delay

    def time_set(self, *largs):
        instance = App.get_running_app()
        value = float(format(self.value, ".2f"))
        set_value('settings', 'press_delay', value)
        self.value = value
        instance.press_delay = value
        self.value_track_color = (0, .8, 0) if value == 1.5 else (0, 0, .8)

class AppColor(ColorWheel):
    def on_color(self, *largs):
        color = self.color[:3] + [.35]
        cl_ = App.get_running_app()
        set_value('settings', 'bg_color', get_hex_from_color(color))
        cl_.color = color


class DeviceSettings(BoxLayout):
    orientation = StringProperty('vertical')
