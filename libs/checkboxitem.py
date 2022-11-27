from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout

from libs.configuration import get_value, locales

__all__ = ['BaseLayout', 'CheckBoxItem', 'ContactsCrawler', 'Crawler',
           'DateFormatCrawler', 'LangCheckBoxItem', 'LanguageCrawler',
           'PressDelayCrawler', 'TimeFormatCrawler']

Builder.load_string('''
<CheckBoxLabel>:
    color: .9, .9, .9, 1
    font_size: dp(25)
    size: self.texture_size
    size_hint_x: None

<LanguageCrawler>:
    LangCheckBoxItem:
        group: 'language'
        id: sv
        content: 'sv'
    CheckBoxLabel:
        on_release:
            sv.active = True
            sv.change_language()
        text: 'Svenska'

    LangCheckBoxItem:
        group: 'language'
        id: en
        content: 'en'
    CheckBoxLabel:
        on_release:
            en.active = True
            en.change_language()
        text: 'English'

    LangCheckBoxItem:
        group: 'language'
        id: fi
        content: 'fi'
    CheckBoxLabel:
        on_release:
            fi.active = True
            fi.change_language()
        text: 'Suomea'

    LangCheckBoxItem:
        group: 'language'
        id: auto
        content: 'auto'
    CheckBoxLabel:
        on_release:
            auto.active = True
            auto.change_language()
        text: 'Auto'

<DateFormatCrawler>:
    CheckBoxItem:
        group: 'dateformat'
        id: obliquestroke
        content: 'obliquestroke'
    CheckBoxLabel:
        on_release:
            obliquestroke.active = True
            # obliquestroke.change_language()
        text: 'dd/mm/yyyy'

    CheckBoxItem:
        group: 'dateformat'
        id: fullstop
        content: 'fullstop'
    CheckBoxLabel:
        on_release:
            fullstop.active = True
            # fullstop.change_language()
        text: 'dd.mm.yyyy'

    CheckBoxItem:
        group: 'dateformat'
        id: hyphen
        content: 'hyphen'
    CheckBoxLabel:
        on_release:
            hyphen.active = True
            # hyphen.change_language()
        text: 'dd-mm-yyyy'

<TimeFormatCrawler>:
    CheckBoxItem:
        group: 'timeformat'
        id: h241
        content: 'h241'
    CheckBoxLabel:
        on_release:
            h241.active = True
            # h241.change_language()
        text: 'hh:mm'

    CheckBoxItem:
        group: 'timeformat'
        id: h242
        content: 'h242'
    CheckBoxLabel:
        on_release:
            h242.active = True
            # h242.change_language()
        text: 'hh.mm'

    CheckBoxItem:
        group: 'timeformat'
        id: am12
        content: 'am12'
    CheckBoxLabel:
        on_release:
            am12.active = True
            # am12.change_language()
        text: 'AM/PM'

<CheckBoxItem>:
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

''')


class CheckBoxItem(CheckBox):
    allow_no_selection = BooleanProperty(False)
    content = StringProperty()


class LangCheckBoxItem(CheckBoxItem):

    def on_kv_post(self, *largs):
        self.bind(active=self.change_language)

    def change_language(self, *largs):
        instance = App.get_running_app()

        if self.content == 'auto':
            lang = locales()
            auto = True
        else:
            lang = self.content
            auto = False

        changes = instance.lang_changes
        changes['1'] = (auto, lang)

        if all([
            changes['0'] != changes['1'],
            changes['changed'] is False
        ]):
            changes['0'] = changes['1']
            changes['changed'] = True
            instance.set_language(lang, auto)
        else:
            changes['changed'] = False

        changes['1'] = self.content


class BaseLayout(TouchRippleBehavior, GridLayout):
    ripple_scale = NumericProperty(.25)
    show_traces = BooleanProperty(True)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point and self.show_traces:
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            return True
        return False


class ContactsCrawler(BaseLayout):
    pass


class PressDelayCrawler(BaseLayout):
    pass


class Crawler(BaseLayout):
    from_settings = ListProperty()
    hasbool = BooleanProperty(False)

    def on_kv_post(self, *largs):
        s = self.from_settings
        content = get_value(s[0])
        usebool = False
        usecat = content[s[1]]

        if self.hasbool:
            usebool = bool(content[s[1]])
            usecat = content[s[0]]

        subject = s[1] if self.hasbool and usebool else usecat
        self.ids[subject].active = True


class LanguageCrawler(Crawler):
    from_settings = ListProperty(('language', 'auto'))
    hasbool = BooleanProperty(True)


class DateFormatCrawler(Crawler):
    from_settings = ListProperty(('format', 'date'))


class TimeFormatCrawler(Crawler):
    from_settings: tuple = ('format', 'time')

