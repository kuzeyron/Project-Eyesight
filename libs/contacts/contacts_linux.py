from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.recycleview import RecycleView

from libs.utils import path_getter, split_nrs

__all__ = ('Contacts', )

Builder.load_file(path_getter(__file__, 'contacts.kv'))

class Contacts(RecycleView):
    __events__ = ('on_accessing_permissions', 'on_permission_validation')
    starred = BooleanProperty(True)
    bar_width = NumericProperty(0)
    opacity = NumericProperty(0)

    def on_kv_post(self, *largs):
        self.dispatch('on_permission_validation')

    def on_accessing_permissions(self, *largs) -> None:
        pass
    
    def on_permission_validation(self, *largs) -> None:
        self.data = [{'name': 'John Smith', 'number': split_nrs('+35812345678')},
                     {'name': 'Sally Sweet', 'number': split_nrs('+35876543210')},
                     {'name': 'John Doe', 'number': split_nrs('+35813253647')}] * 5
