from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemableBehavior
from kivy.properties import ObjectProperty
from kivymd.uix.list import MDList
from kivymd.theming import ThemeManager
from database import Database
from kivymd.uix.list import OneLineListItem


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Patient(Screen):
    current = ""
    theme_cls = ThemeManager()

    first_name = ObjectProperty(None)
    email = ObjectProperty(None)

    def on_enter(self, *args):
        user_info = db.get_user_info("5")
        self.first_name.text = user_info[2]
        self.email.text = user_info[7]
        print(user_info)

    def load_care_partners(self):
        self.ids.cp_list.clear_widgets()
        care_partners = db.get_care_partners()
        for cp in care_partners:
            cp_fullname = cp[2] + " " + cp[3]
            cp_list = OneLineListItem(text=f"{cp_fullname}", on_release=self.mycallback)
            cp_list.id = cp[0]
            self.ids.cp_list.add_widget(cp_list)

    def mycallback(self, instance):
        cp_id = str(instance.id)
        self.ids.screen_manager.current = "care-partners-profile"
        self.ids.screen_manager.transition.direction = "down"
        self.ids.cp_current.text = instance.text + " Profile"
        profile = db.get_profile(cp_id)
        print(profile)

db = Database()
