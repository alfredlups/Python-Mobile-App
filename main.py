from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from database import Database
from patient import Patient
from care_partner import CarePartner
from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField
from datetime import datetime
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton


class Front(Screen):

    def care_partner_registration(self):
        sm.current = "register-care-partner"

    def patient_registration(self):
        sm.current = "register-patient"

    def go_to_login(self):
        sm.current = "login"


class RegisterCarePartner(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    mobile_number = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    street = ObjectProperty(None)
    city = ObjectProperty(None)
    state = ObjectProperty(None)
    zipcode = ObjectProperty(None)
    male = ObjectProperty(None)
    female = ObjectProperty(None)
    birth_date = ObjectProperty(None)
    user_type = "care_partner"

    date_dialog = {}
    original_date = ""

    def register(self):
        if self.first_name.text != "" and self.last_name.text != "" and self.street.text != "" and self.city.text != "" and self.state.text != "" and self.zipcode.text != "" and self.mobile_number.text and self.birth_date.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0 and self.password.text != "":
            if len(self.password.text) < self.password.min_length:
                toast("Password should at least 4 digits")
                return False
            if len(self.state.text) != self.state.text_length:
                toast("State should be 2 letters")
                return False
            if not db.check_user(self.email.text):
                if not self.male.active and not self.female.active:
                    toast("Please select a gender")
                else:
                    user_id = db.add_user(self.email.text, self.mobile_number.text, self.password.text, 2)
                    if user_id:
                        mi = "a"
                        if self.male.active:
                            gender = "M"
                        else:
                            gender = "F"
                        if db.add_care_partner(self.first_name.text, mi, self.last_name.text, self.street.text, self.city.text, self.state.text, self.zipcode.text, self.birth_date.text, gender, user_id):
                            login = db.login(self.email.text, self.password.text)
                            if login["user_role_id"] == 2:
                                CarePartner.current = login['users_id']
                                toast("You registered successfully. Redirecting to account")
                                Clock.schedule_once(self.redirect_to_care_partner, 4)
                            else:
                                toast("Patient features is ongoing")
                            self.clear_fields()
                        else:
                            toast("Something went wrong")
                    else:
                        toast("Something went wrong")
            else:
                toast("Email is already taken.")
                self.email.text = ""
        else:
            toast("All fields is required")

    def clear_fields(self):
        self.first_name.text = ""
        self.last_name.text = ""
        self.street.text = ""
        self.city.text = ""
        self.state.text = ""
        self.zipcode.text = ""
        self.male.active = False
        self.female.active = False
        self.mobile_number.text = ""
        self.password.text = ""
        self.email.text = ""
        self.birth_date.text = ""

    def redirect_to_patient(self, instance):
        sm.current = "patient"

    def redirect_to_care_partner(self, instance):
        sm.current = "care-partner"


class RegisterPatient(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    mobile_number = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    user_type = "patient"

    def register(self):
        if self.first_name.text != "" and self.last_name.text != "" and self.mobile_number.text and self.email.text.count("@") == 1 and self.email.text.count(".") > 0 and self.password.text != "":
            if not db.check_user(self.email.text):
                register = db.add_patient(self.first_name.text, self.last_name.text, self.mobile_number.text,self.email.text, self.password.text, self.user_type)
                if register:
                    login = db.login(self.email.text, self.password.text)
                    if login:
                        if login[6] == "patient":
                            Patient.current = str(login[0])
                            sm.current = "patient"
                        else:
                            CarePartner.current = str(login[0])
                            sm.current = "care-partner"
                else:
                    toast("Something went wrong. Please try again later.")
            else:
                toast("Email is already taken")
        else:
            toast("Make sure all fields are correct!")


class Login(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    spinner = {}

    def login(self):
        if self.email.text.count("@") == 1 and self.email.text.count(".") > 0 and self.password.text != "":
            login = db.login(self.email.text, self.password.text)
            if login:
                self.spinner = MDSpinner(size_hint=(None, None), size=("46dp", "46dp"), pos_hint={'center_x': 0.5, 'center_y': 0.14}, active=True)
                self.ids.login_section.add_widget(self.spinner)
                if login["user_role_id"] == 2:
                    CarePartner.current = login["users_id"]
                    Clock.schedule_once(self.redirect_to_care_partner, 2)
                else:
                    toast("Patient features is ongoing")
                    self.spinner.active = False

            else:
                toast("Email or password is incorrect")
                self.clear_login_fields()
        else:
            toast("Email and password must valid!")
            self.clear_login_fields()

    def redirect_to_patient(self, instance):
        sm.current = "patient"

    def redirect_to_care_partner(self, instance):
        self.spinner.active = False
        sm.current = "care-partner"
        self.clear_login_fields()

    def clear_login_fields(self):
        self.email.text = ""
        self.password.text = ""


class DateTextField(MDTextField):

    date_dialog = {}
    text_field = {}
    dialog = {}

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            icon = MDIconButton(icon="pencil", theme_text_color="Custom", text_color=(1, 1, 1, 1),
                                pos_hint={"center_x": 0.87, "center_y": 0.88}, on_release=self.show_year)
            if self.text == "":
                self.date_dialog = MDDatePicker(max_date=datetime.today().date(), callback=self.date_picker_callback)
                self.date_dialog.add_widget(icon)
                self.date_dialog.open()
            else:
                f_date = self.text.split('-')
                self.date_dialog = MDDatePicker(max_date=datetime.today().date(), year=int(f_date[0]), month=int(f_date[1]), day=int(f_date[2]), callback=self.date_picker_callback)
                self.date_dialog.add_widget(icon)
                self.date_dialog.open()

    def date_picker_callback(self, instance):
        self.text = str(instance)

    def show_year(self, instance):
        self.text_field = MDTextField(input_filter="int", max_text_length=4)
        self.dialog = MDDialog(
            title="INPUT YEAR",
            type="custom",
            content_cls=self.text_field,
            buttons=[
                MDFlatButton(
                    text="CANCEL", on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="FILTER", on_release=self.filter_year
                ),
            ],
        )
        self.dialog.width = 300
        self.dialog.height = 200
        self.dialog.open()

    def filter_year(self, instance):
        current_year = datetime.today().year
        year = self.text_field.text
        if year == "":
            toast("Enter year")
            return False
        if len(year) != 4:
            toast("Invalid date")
            return False
        if int(year) > int(current_year):
            toast("Should not be future year")
            self.text_field.focus = True
            return False
        self.date_dialog.set_date(int(year), 1, 1)
        self.dialog.dismiss()

    def close_dialog(self, instance):
        self.dialog.dismiss()


class WindowManager(ScreenManager):
    pass


def show_error(message):
    dialog = MDDialog(text=message)
    dialog.open()


kv = Builder.load_file("main.kv")
sm = ScreenManager()
db = Database()


class MainApp(MDApp):

    def back_to_front(self):
        sm.current = "front"

    def logout(self):
        Clock.schedule_once(self.do_logout, 2)

    def do_logout(self, instance):
        sm.current = "login"

    def build(self):
        Window.size = (400, 750)
        screens = [Front(name="front"), RegisterCarePartner(name="register-care-partner"), RegisterPatient(name="register-patient"), Login(name="login"), Patient(name="patient"), CarePartner(name="care-partner")]
        for screen in screens:
            sm.add_widget(screen)
        sm.current = "front"
        self.theme_cls.primary_palette = "Purple"
        return sm


if __name__ == "__main__":
    MainApp().run()
