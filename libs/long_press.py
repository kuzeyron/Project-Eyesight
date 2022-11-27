from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (BooleanProperty, ColorProperty, NumericProperty,
                             ObjectProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from libs.android_vibrator import vibrate

__all__ = ['LongPress', ]


class LongPress(ButtonBehavior, TouchRippleBehavior):
    __events__ = ('on_long_press', 'on_short_press', )
    _vib = ObjectProperty(None, allow_none=True)
    always_release = BooleanProperty(True)
    long_press_time = NumericProperty(1.5)
    short_press_time = NumericProperty(.08)
    min_state_time = NumericProperty(.5)
    background_color = ColorProperty((.25, .15, .25, .5))
    background_up = ColorProperty((.25, .15, .25, .5))
    always_release = BooleanProperty(True)
    ripple_scale = NumericProperty(.25)
    show_traces = BooleanProperty(True)
    override = BooleanProperty(False)

    def on_state(self, instance, value):
        instance = App.get_running_app()
        if self.override:
            self.long_press_time = instance.press_delay

        if value == 'down':
            color = instance.color[:3]
            self.background_color = [self.c_switch(x, step=.25)
                                     for x in color] + [.5]
            self._clock1 = Clock.schedule_once(self._do_long_press,
                                               self.long_press_time)
            self._clock2 = Clock.schedule_once(self._do_short_press,
                                               self.short_press_time)
        else:
            self._clock1.cancel()
            self._clock2.cancel()

    def c_switch(self, value, step, *largs):
        if sum(App.get_running_app().color[:3]) < 1.5:
            return value + step

        return value - step

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

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def _do_short_press(self, dt):
        self.dispatch('on_short_press')

    def on_long_press(self, *largs):
        pass

    def on_short_press(self, *largs):
        self._vib = vibrate(self.long_press_time - self.short_press_time)

    def on_press(self, *largs):
        pass

    def on_release(self, *largs):
        if self._vib is not None:
            self._vib.cancel()
