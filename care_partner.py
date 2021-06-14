from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from database import Database
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.list import IconRightWidget
from kivymd.uix.list import IconLeftWidget
from kivymd.toast import toast
from kivymd.uix.chip import MDChip
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from datetime import datetime
from plyer import storagepath
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.filemanager import MDFileManager
from PIL import Image
from kivy.utils import platform
from kivy.uix.image import Image as PopupImage


# -*- coding: utf-8 -*
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.graphics import Line, Color


class DrawImage(PopupImage):
    # Points of Line object
    Ax = NumericProperty(0)
    Ay = NumericProperty(0)
    Bx = NumericProperty(0)
    By = NumericProperty(0)
    Cx = NumericProperty(0)
    Cy = NumericProperty(0)
    Dx = NumericProperty(0)
    Dy = NumericProperty(0)

    # Object line
    line = ObjectProperty()

    # List of line objects drawn
    list_lines_in_image = ListProperty([])

    # Size of the selected rectangle
    size_selected = ListProperty([0, 0])

    # Size previous of the selected rectangle
    size_selected_previous = ListProperty([0, 0])

    # Size temporary of the selected rectangle
    size_selected_temp = ListProperty([0, 0])

    # Line Color and width
    line_color = ListProperty([1, 1, 1, 1])
    line_width = NumericProperty(3)

    # First tap in TouchSelector
    first_tap = True

    first_touch_x = NumericProperty(0)
    first_touch_y = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(DrawImage, self).__init__(*args, **kwargs)
        self.bind(list_lines_in_image=self.remove_old_line)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.size_selected = abs(self.Cx - self.Dx), abs(self.Cy - self.By)
            self.size_selected_previous = self.size_selected

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(self.line_color)

                # Save initial tap position
                self.Ax, self.Ay = self.first_touch_x, self.first_touch_y = touch.x, touch.y

                # Initilize positions to save
                self.Bx, self.By = 0, 0
                self.Cx, self.Cy = 0, 0
                self.Dx, self.Dy = 0, 0


                # Create initial point with touch x and y postions.
                self.line = Line(points=([self.Ax, self.Ay]), width=self.line_width, joint='miter', joint_precision=30)

                # Save the created line
                self.list_lines_in_image.append(self.line)

                touch_in_modal = (touch.x - self.pos[0], touch.y - self.pos[1])
                #print('touch : ' + str(touch.pos) + ', touch in modal: ' + str(touch_in_modal))
                print(self.pos)
                im = Image.open(self.source)

                # Setting the points for cropped image
                left = touch_in_modal[0]
                top = touch_in_modal[1]
                right = 300
                bottom = 300
                cropped = im.crop((left, top, right, bottom))
                cropped.save("images/profile/cropped.png")

    def remove_old_line(self, instance=None, list_lines=None):
        """Remove the old line draw"""
        if len(self.list_lines_in_image) > 1:
            self.delete_line()

    def delete_line(self, pos=0):
        try:
            self.list_lines_in_image.pop(pos).points = []
        except: pass

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            # Assign the position of the touch at the point C
            self.Cx, self.Cy = touch.x, touch.y

            # There are two known points A (starting point) and C (endpoint)
            # Assign the  positions x and y  known of the points
            self.Bx, self.By = self.Cx, self.Ay
            self.Dx, self.Dy = self.Ax, self.Cy

            # Assign points positions to the last line created
            self.line.points = [self.Ax, self.Ay,
                                self.Bx, self.By,
                                self.Cx, self.Cy,
                                self.Dx, self.Dy,
                                self.Ax, self.Ay]

            self.size_selected_temp = abs(self.Cx - self.Dx), abs(self.Cy - self.By)

    def tap_not_draw_a_line(self):
        """
        When touchdown is called and tap not draw a line.
        """
        return self.size_selected[0] == 0 and self.size_selected[1] == 0


class CarePartner(Screen):
    theme_cls = ThemeManager()

    """Summary"""
    summary = ObjectProperty(None)

    """Skills"""
    # sk_grid = ObjectProperty(None)
    new_skill = ObjectProperty(None)
    new_current_skill = ObjectProperty(None)

    """Work Experience"""
    my_position = ObjectProperty(None)
    my_company = ObjectProperty(None)
    my_address = ObjectProperty(None)
    my_is_current = ObjectProperty(None)
    my_from_date = ObjectProperty(None)
    my_to_date = ObjectProperty(None)
    my_description = ObjectProperty(None)

    """New Work Experience"""
    new_position = ObjectProperty(None)
    new_company = ObjectProperty(None)
    new_address = ObjectProperty(None)
    new_is_current = ObjectProperty(None)
    new_from_date = ObjectProperty(None)
    new_to_date = ObjectProperty(None)
    new_description = ObjectProperty(None)
    """Education"""
    my_school = ObjectProperty(None)
    my_degree = ObjectProperty(None)
    my_field = ObjectProperty(None)
    my_start_date = ObjectProperty(None)
    my_end_date = ObjectProperty(None)
    build_profile_btn = ObjectProperty(None)
    """Edit Summary"""
    edit_summary = ObjectProperty
    current = ""
    position_menu = {}
    company_menu = {}
    school_menu = {}
    degree_menu = {}
    field_menu = {}

    edit_position_menu = {}
    edit_company_menu = {}
    edit_school_menu = {}
    edit_degree_menu = {}
    edit_field_menu = {}

    bp_position_menu = {}
    bp_company_menu = {}
    bp_school_menu = {}
    bp_degree_menu = {}
    bp_field_menu = {}

    selected_job_title = ""
    selected_company = ""
    selected_school = ""
    selected_degree = ""
    selected_field = ""
    original_from_date = ""
    original_to_date = ""
    date_dialog = {}
    page_with_date = ""

    work_experience_id = ""
    work_experience_from_date = ""
    work_experience_to_date = ""
    education_id = ""

    #global variables
    user_id = ""
    care_partners_id = ""
    full_name = ""
    email_address = ""
    short_about = ""
    profile_url = ""
    home_button_url = ""
    user_info = {}

    file_manager = {}
    dialog = {}
    manager_open = False
    manager = None
    storage_path = ""

    def on_enter(self, *args):
        Window.bind(on_keyboard=self.events)
        self.load_home()
        self.load_current_skill()
        self.load_edit_current_skill()
        self.load_skills_chips()
        self.load_edit_skills_chips()
        self.update_toolbar_label('Home')
        self.load_dropdown_menus()

    def load_home(self):
        self.user_id = str(self.current)
        self.user_info = db.get_user_info(str(self.current))
        self.care_partners_id = str(self.user_info['care_partners_id'])
        self.full_name = self.user_info['first_name'] + " " + self.user_info['last_name']
        self.email_address = self.user_info['email_address']
        self.short_about = self.user_info['short_about']
        self.ids.side_full_name.text = self.full_name
        self.ids.side_email.text = self.email_address

        self.ids.home_section.clear_widgets()

        if self.user_info['profile_status'] == 4:
            label = MDLabel(text=f"Welcome, {self.full_name}", halign="center")
            button = MDRaisedButton(text="Go to profile", pos_hint={"center_x": 0.5, "center_y": 0.44}, on_release=self.home_button_callback)
            profile_edit_icon = MDIconButton(icon="camera", theme_text_color="Custom", text_color=(1, 1, 1, 1), pos_hint={"center_x": 0.8, "center_y": 0.2}, on_release=self.bottom_sheet_open)

            self.ids.profile_picture.add_widget(profile_edit_icon)
            self.ids.home_section.add_widget(label)
            self.ids.home_section.add_widget(button)
            self.profile_url = "profile"
            self.home_button_url = "profile"
            self.load_profile_details()
            self.load_profile_photo()
        else:
            if self.user_info['profile_status'] == 0:
                label = MDLabel(text="Please build your profile", halign="center")
                button = MDRaisedButton(text="Build your profile now", pos_hint={"center_x": 0.5, "center_y": 0.44}, on_release=self.home_button_callback)
            else:
                label = MDLabel(text="You are suggested to finish building your profile", halign="center")
                button = MDRaisedButton(text="Continue", pos_hint={"center_x": 0.5, "center_y": 0.44},
                                        on_release=self.home_button_callback)
            self.ids.home_section.add_widget(label)
            self.ids.home_section.add_widget(button)
            self.profile_url = "home"
            self.home_button_url = "build-profile"
            self.summary.text = self.user_info['short_about']

    def home_button_callback(self, instance):
        self.ids.screen_manager.current = self.home_button_url
        self.ids.screen_manager.transition.direction = "left"
        self.change_toolbar_label()

    def load_profile_photo(self):
        profile = db.get_profile_photo(self.care_partners_id)
        if profile != "test":
            self.ids.avatar.source = profile['photo_url']
            self.ids.side_avatar.source = profile['photo_url']

    def load_profile_details(self):
        self.update_toolbar_label("Profile")
        profile_info = self.ids.section_personal_profile
        profile_summary = self.ids.section_summary
        profile_education = self.ids.section_education
        profile_skills = self.ids.section_skills
        profile_work_experience = self.ids.section_work_experience

        info = db.get_user_info(self.user_id)

        self.full_name = info['first_name'] + " " + info['last_name']
        self.email_address = info['email_address']
        self.short_about = info['short_about']

        self.ids.side_full_name.text = self.full_name
        self.ids.side_email.text = self.email_address

        profile_info.secondary_text = self.full_name
        profile_info.tertiary_text = self.email_address

        self.ids.edit_summary.text = self.short_about

        profile_summary.secondary_text = self.short_about
        skills_list = []
        for sl in db.get_current_skills(self.care_partners_id):
            skills_list.append(sl['name'])
        profile_skills.secondary_text = ', '.join(skills_list)

        working_exp = db.get_work_experience(self.care_partners_id)
        profile_work_experience.secondary_text = working_exp['company_name']
        profile_work_experience.tertiary_text = working_exp['name']

        education = db.get_education(self.care_partners_id)
        profile_education.secondary_text = education['school']
        profile_education.tertiary_text = education['field_study']

    def load_user_edit_info(self):
        info = db.get_user_info(self.user_id)
        self.ids.edit_first_name.text = info['first_name']
        self.ids.edit_last_name.text = info['last_name']
        self.ids.edit_street.text = info['street']
        self.ids.edit_city.text = info['city']
        self.ids.edit_state.text = info['state']
        self.ids.edit_zipcode.text = info['zip_code']
        self.ids.edit_mobile_number.text = info['mobile_number']
        self.ids.edit_email.text = info['email_address']
        self.ids.edit_password.text = info['password']

    def update_user_info(self):
        if self.ids.edit_first_name.text != "" and self.ids.edit_last_name.text != "" and self.ids.edit_email.text.count("@") == 1 and self.ids.edit_email.text.count(".") > 0 and self.ids.edit_password.text != "":
            if not db.check_user(self.ids.edit_email.text):
                if len(self.ids.edit_state.text) == 2:
                    db.update_user(self.user_id, self.ids.edit_email.text, self.ids.edit_password.text, self.ids.edit_mobile_number.text)
                    db.update_care_partner(self.care_partners_id, self.ids.edit_first_name.text, self.ids.edit_last_name.text, self.ids.edit_street.text, self.ids.edit_city.text, self.ids.edit_state.text, self.ids.edit_zipcode.text)
                    toast("Updated personal information")
                else:
                    toast("State should be 2 letters")
            else:
                toast("Email is already taken")
        else:
            toast("First name and last name should not be empty")

    def update_summary(self):
        max_length = self.edit_summary.max_text_length
        if self.edit_summary.text != "":
            if len(self.edit_summary.text) <= max_length:
                db.update_summary(self.care_partners_id, self.edit_summary.text)
                toast("Summary updated")
            else:
                toast("Summary should be maximum of 200 letters")
        else:
            toast("Summary should not empty")

    def profile_link(self):
        return self.profile_url

    def add_summary(self):
        max_length = self.summary.max_text_length
        if self.summary.text != "":
            if len(self.summary.text) <= max_length:
                db.add_summary(self.user_id, self.summary.text)
                db.update_profile_status(self.care_partners_id, 1)
                toast("Summary has been added")
                Clock.schedule_once(self.go_to_skills, 2)
            else:
                toast("Summary should be maximum of 200 letters")
        else:
           toast("Summary is empty")

    def go_to_skills(self, instance):
        self.ids.screen_manager.current = "skills"
        self.ids.screen_manager.transition.direction = "left"

    def load_skills_chips(self):
        self.ids.md_chip.clear_widgets()
        skills = db.get_skills()
        current_skills = db.get_current_skills_by_id(self.care_partners_id)
        for skill in skills:
            skills_name = skill['name']
            found = 0
            for cs in current_skills:
                if skill['skills_id'] == cs['skills_id']:
                    found = 1
            if found == 0:
                chips = MDChip(label=f"{skills_name}", icon="plus", selected_chip_color=(.21176470535294, .098039627451, 1, 1), callback=self.chips_skills_callback)
            else:
                chips = MDChip(label=f"{skills_name}", icon="check", color=(.21176470535294, .098039627451, 1, 1))
            chips.skills_id = skill['skills_id']
            chips.type = "add"
            self.ids.md_chip.add_widget(chips)

    def load_edit_skills_chips(self):
        self.ids.sk_chip.clear_widgets()
        skills = db.get_skills()
        current_skills = db.get_current_skills_by_id(self.care_partners_id)
        for skill in skills:
            skills_name = skill['name']
            found = 0
            for cs in current_skills:
                if skill['skills_id'] == cs['skills_id']:
                    found = 1
            if found == 0:
                chips = MDChip(label=f"{skills_name}", icon="plus", selected_chip_color=(.21176470535294, .098039627451, 1, 1), callback=self.chips_skills_callback)
            else:
                chips = MDChip(label=f"{skills_name}", icon="check", color=(.21176470535294, .098039627451, 1, 1))
            chips.skills_id = skill['skills_id']
            chips.type = "edit"
            self.ids.sk_chip.add_widget(chips)

    def chips_skills_callback(self, instance, value):
        if db.add_skills(self.care_partners_id, instance.skills_id):
            if instance.type == "edit":
                self.load_edit_skills_chips()
                self.load_edit_current_skill()
            else:
                db.update_profile_status(self.care_partners_id, 2)
                self.load_skills_chips()
                self.load_current_skill()

            toast("Skills added")
        else:
            toast("Something went wrong")

    def load_current_skill(self):
        self.ids.skills_list.clear_widgets()
        sk_list = db.get_current_skills(self.care_partners_id)
        for sk in sk_list:
            skills_name = sk['name']
            skill = OneLineAvatarIconListItem(text=f"{skills_name}")
            icon = IconRightWidget(icon="delete", on_release=self.delete_skill)
            icon.id = sk['skills_id']
            icon.name = sk['name']
            icon.type = "add"
            skill.add_widget(icon)
            self.ids.skills_list.add_widget(skill)

    def load_edit_current_skill(self):
        self.ids.new_skills_list.clear_widgets()
        sk_list = db.get_current_skills(self.care_partners_id)
        for sk in sk_list:
            skills_name = sk['name']
            skill = OneLineAvatarIconListItem(text=f"{skills_name}")
            icon = IconRightWidget(icon="delete", on_release=self.delete_skill)
            icon.id = sk['skills_id']
            icon.name = sk['name']
            icon.type = "edit"
            skill.add_widget(icon)
            self.ids.new_skills_list.add_widget(skill)

    def delete_skill(self, instance):
        if db.delete_skill(self.care_partners_id, str(instance.id)):
            if instance.type == "edit":
                self.load_edit_skills_chips()
                self.load_edit_current_skill()
            else:
                self.load_skills_chips()
                self.load_current_skill()
            toast("Skills deleted")
        else:
            toast("Something went wrong")

    def typing_skills(self, text, type):
        if type == "add":
            if text != "":
                self.ids.skills_list.clear_widgets()
                search_list = db.search_skills(text)
                current_skills_list = db.get_current_skills(self.care_partners_id)
                unique_skills = []
                for sk in search_list:
                    found = 0
                    for ckl in current_skills_list:
                        if sk['skills_id'] == ckl['skills_id']:
                            found = 1
                    if found == 0:
                        unique_skills.append(sk)
                if unique_skills:
                    for sk in unique_skills:
                        skills_name = sk['name']
                        skill = OneLineAvatarIconListItem(text=f"{skills_name}")
                        icon = IconRightWidget(icon="plus", on_release=self.add_seachable_skill)
                        icon.id = sk['skills_id']
                        icon.name = sk['name']
                        icon.type = "add"
                        skill.add_widget(icon)
                        self.ids.skills_list.add_widget(skill)
                else:
                    self.load_current_skill()
            else:
                self.load_current_skill()
        else:
            if text != "":
                self.ids.new_skills_list.clear_widgets()
                search_list = db.search_skills(text)
                current_skills_list = db.get_current_skills(self.care_partners_id)
                unique_skills = []
                for sk in search_list:
                    found = 0
                    for ckl in current_skills_list:
                        if sk['skills_id'] == ckl['skills_id']:
                            found = 1
                    if found == 0:
                        unique_skills.append(sk)
                if unique_skills:
                    for sk in unique_skills:
                        skills_name = sk['name']
                        skill = OneLineAvatarIconListItem(text=f"{skills_name}")
                        icon = IconRightWidget(icon="plus", on_release=self.add_seachable_skill)
                        icon.id = sk['skills_id']
                        icon.name = sk['name']
                        icon.type = "edit"
                        skill.add_widget(icon)
                        self.ids.new_skills_list.add_widget(skill)
                else:
                    self.load_edit_current_skill()
            else:
                self.load_edit_current_skill()

    def add_seachable_skill(self, instance):
        if db.add_skills(self.care_partners_id, instance.id):
            if instance.type == "edit":
                self.load_edit_current_skill()
                self.new_current_skill.text = ""
            else:
                db.update_profile_status(self.care_partners_id, 2)
                self.load_current_skill()
                self.new_skill.text = ""
            toast("Skills Added")
        else:
            toast("Something went wrong")

    def add_new_skills(self, type):
        if type == "edit":
            if not db.check_skills(self.ids.new_current_skill.text.strip().lower()):
                skill_id = db.add_skills_table(self.ids.new_current_skill.text)
                if skill_id:
                    db.add_skills(self.care_partners_id, skill_id)
                    self.ids.new_current_skill.text = ""
                    self.load_edit_current_skill()
                    toast("Skills added")
                else:
                    toast("Something went wrong")
            else:
                toast("Skills is already exist")
        else:
            if not db.check_skills(self.ids.new_skill.text.strip().lower()):
                skill_id = db.add_skills_table(self.ids.new_skill.text)
                if skill_id:
                    db.add_skills(self.care_partners_id, skill_id)
                    db.update_profile_status(self.care_partners_id, 2)
                    self.ids.new_skill.text = ""
                    self.load_current_skill()
                    toast("Skills Added")
                else:
                    toast("Something went wrong")
            else:
                toast("Skills is already exist")

    def get_all_work_experience(self):
        self.update_toolbar_label("List of Work Experience")
        self.ids.work_list.clear_widgets()
        work_experiences = db.get_all_work_experience(self.care_partners_id)
        for work in work_experiences:
            work_exp = TwoLineAvatarIconListItem(text=f"{work['company_name']}", secondary_text=f"{work['name']}")
            icon1 = IconLeftWidget(icon="pencil", on_release=self.get_edited_work_experience)
            icon1.id = work['work_experiences_id']
            icon2 = IconRightWidget(icon="delete", on_release=self.delete_work_experience)
            icon2.id = work['work_experiences_id']
            work_exp.add_widget(icon1)
            work_exp.add_widget(icon2)
            self.ids.work_list.add_widget(work_exp)

    def get_edited_work_experience(self, instance):
        self.update_toolbar_label("Edit Work Experience")
        self.work_experience_id = str(instance.id)
        work_experience = db.get_specific_work_experience(self.work_experience_id)
        self.ids.screen_manager.current = "edit-specific-work-experience"
        self.ids.screen_manager.transition.direction = "left"

        self.ids.edit_position.set_item(work_experience['name'])
        self.ids.edit_company.set_item(work_experience['company_name'])
        self.ids.edit_address.text = work_experience['state']

        if work_experience['currently_working'] == 1:
            self.ids.edit_is_current.active = True
            self.ids.edit_to_date.opacity = 0
            to_date = ""
        else:
            self.ids.edit_is_current.active = False
            self.ids.edit_to_date.opacity = 1
            to_date = work_experience['end_date']

        self.ids.edit_from_date.text = str(work_experience['start_date'])
        self.ids.edit_to_date.text = str(to_date)
        self.ids.edit_description.text = work_experience['description']

        self.selected_company = work_experience['company_id']
        self.selected_job_title = work_experience['job_titles_id']

        self.work_experience_from_date = str(work_experience['start_date'])
        self.work_experience_to_date = str(work_experience['end_date'])

    def update_work_experience(self):
        if self.ids.edit_position.current_item != "" and self.ids.edit_company.current_item != "":
            if len(self.ids.edit_address.text) == 2:
                compare_date = 0
                if self.ids.edit_is_current.active:
                    current_company = "1"
                    to_date = "1950-01-01"
                else:
                    current_company = "0"
                    to_date = self.ids.edit_to_date.text
                    if to_date != "":
                        if self.ids.edit_from_date.text >= self.ids.edit_to_date.text:
                            compare_date = 1
                            toast("Start date should before end date")
                    else:
                        compare_date = 1
                        toast("End date is required")
                if compare_date == 0:
                    if db.update_work_experience(self.work_experience_id, self.ids.edit_from_date.text, to_date, current_company, self.ids.edit_description.text, self.ids.edit_address.text, self.selected_company, self.selected_job_title):
                        toast("Work Experience Updated")
                    else:
                        toast("Something went wrong")
            else:
                toast("State should be 2 letters")
        else:
            toast("Fill up required fields.")

    def delete_work_experience(self, instance):
        if db.delete_work_experience(str(instance.id)):
            self.get_all_work_experience()
            toast("Work deleted")
        else:
            toast("Something went wrong")

    def on_work_status(self, checkbox, value, type):
        if value:
            if type == "bp":
                self.ids.bp_to_date.disabled = True
                self.ids.bp_to_date.text = ""
                self.ids.bp_to_date.opacity = 0
            elif type == "new":
                self.my_to_date.disabled = True
                self.my_to_date.text = ""
                self.my_to_date.opacity = 0
            else:
                self.ids.edit_to_date.disabled = True
                self.ids.edit_to_date.text = ""
                self.ids.edit_to_date.opacity = 0
        else:
            if type == "bp":
                self.ids.bp_to_date.disabled = False
                self.ids.bp_to_date.opacity = 1
            elif type == "new":
                self.my_to_date.disabled = False
                self.my_to_date.opacity = 1
            else:
                self.ids.edit_to_date.disabled = False
                self.ids.edit_to_date.opacity = 1

    def add_work_experience(self):
        if self.my_position.current_item != "" and self.my_company.current_item != "" and self.my_from_date.text != "":
            if len(self.my_address.text) == 2:
                compare_date = 0
                if self.my_is_current.active:
                    current_company = "1"
                    to_date = "1950-01-01"
                else:
                    current_company = "0"
                    to_date = self.my_to_date.text
                    if to_date != "":
                        if self.my_from_date.text >= self.my_to_date.text:
                            compare_date = 1
                            toast("Start date must before end date")
                    else:
                        compare_date = 1
                        toast("End date is required")
                if compare_date == 0:
                    if db.add_work_experience(self.my_from_date.text, to_date, current_company, self.my_description.text, self.my_address.text, self.care_partners_id, self.selected_company, self.selected_job_title):
                        toast("Word Experience Added")
                        self.clear_work_experience_fields()
                    else:
                        toast("Something went wrong")
            else:
                toast("State should be 2 letters")
        else:
            toast("Fill up required fields.")

    def add_bp_work_experience(self):
        if self.ids.bp_position.current_item != "" and self.ids.bp_company.current_item != "" and self.ids.bp_from_date.text != "":
            if len(self.ids.bp_address.text) == 2:
                compare_date = 0
                if self.ids.bp_is_current.active:
                    current_company = "1"
                    to_date = "1950-01-01"
                else:
                    current_company = "0"
                    to_date = self.ids.bp_to_date.text
                    if to_date != "":
                        if self.ids.bp_from_date.text >= self.ids.bp_to_date.text:
                            compare_date = 1
                            toast("Start date must before end date")
                    else:
                        compare_date = 1
                        toast("End date is required")

                if compare_date == 0:
                    if db.add_work_experience(self.ids.bp_from_date.text, to_date, current_company, self.ids.bp_description.text, self.ids.bp_address.text, self.care_partners_id, self.selected_company, self.selected_job_title):
                        toast("Word Experience Added")
                        db.update_profile_status(self.care_partners_id, 3)
                        Clock.schedule_once(self.go_to_education, 2)
                        self.clear_work_experience_fields()
                    else:
                        toast("Something went wrong")
            else:
                toast("State should be 2 letters")
        else:
            toast("Fill up required fields.")

    def clear_work_experience_fields(self):
        self.ids.bp_position.set_item("Job Title")
        self.ids.bp_company.set_item("Company")
        self.ids.bp_from_date.text = ""
        self.ids.bp_to_date.text = ""
        self.ids.bp_address.text = ""
        self.ids.bp_is_current.active = False
        self.ids.bp_description.text = ""
        self.selected_job_title = ""
        self.selected_company = ""
        self.my_position.set_item("Job Title")
        self.my_company.set_item("Company")
        self.my_from_date.text = ""
        self.my_to_date.text = ""
        self.my_address.text = ""
        self.my_is_current.active = False
        self.my_description.text = ""
        self.selected_job_title = ""
        self.selected_company = ""

    def go_to_education(self, instance):
        self.ids.screen_manager.current = "education"
        self.ids.screen_manager.transition.direction = "left"

    def get_all_education(self):
        self.update_toolbar_label("List of Education")
        self.ids.education_list.clear_widgets()
        educations = db.get_all_education(self.care_partners_id)
        for ed in educations:
            educ = TwoLineAvatarIconListItem(text=f"{ed['school']}", secondary_text=f"{ed['field_study']}")
            icon1 = IconLeftWidget(icon="pencil", on_release=self.get_edited_education)
            icon1.id = ed['education_id']
            icon2 = IconRightWidget(icon="delete", on_release=self.delete_education)
            icon2.id = ed['education_id']
            educ.add_widget(icon1)
            educ.add_widget(icon2)
            self.ids.education_list.add_widget(educ)

    def get_edited_education(self, instance):
        self.update_toolbar_label("Edit Education")
        self.ids.screen_manager.current = "edit-specific-education"
        self.ids.screen_manager.transition.direction = "left"

        self.education_id = str(instance.id)
        education = db.get_specific_education(str(instance.id))
        self.ids.edit_school.set_item(education['school'])
        self.ids.edit_degree.set_item(education['education_level'])
        self.ids.edit_field.set_item(education['field_study'])
        self.ids.edit_start_date.text = str(education['start_date'])
        self.ids.edit_end_date.text = str(education['end_date'])

        self.selected_school = education['school_id']
        self.selected_field = education['field_study_id']
        self.selected_degree = education['education_level_id']

    def update_education(self):
        if self.compare_dates(self.ids.edit_start_date.text, self.ids.edit_end_date.text):
            if db.update_education(self.ids.edit_start_date.text, self.ids.edit_end_date.text, self.selected_degree, self.selected_field, self.selected_school, self.education_id):
                toast("Education updated")
                self.get_all_education()
            else:
                toast("Something went wrong")
        else:
            toast("Start date must before end date")

    def add_education(self):
        if self.ids.bp_school.current_item != "" and self.ids.bp_degree.current_item != "" and self.ids.bp_field.current_item != "" and self.ids.bp_start_date.text != "" and self.ids.bp_end_date.text != "":
            if self.compare_dates(self.ids.bp_start_date.text, self.ids.bp_end_date.text):
                if db.add_education(self.ids.bp_start_date.text, self.ids.bp_end_date.text, self.selected_degree, self.selected_field, self.selected_school, self.care_partners_id):
                    db.update_profile_status(self.care_partners_id, 4)
                    self.clear_education_fields()
                    self.load_profile_details()
                    self.load_edit_skills_chips()
                    self.load_edit_current_skill()
                    self.load_home()
                    toast("Education added. Redirecting to profile")
                    Clock.schedule_once(self.redirect_to_profile, 4)
                else:
                    toast("Something went wrong")
            else:
                toast("Start date must before end date")
        else:
            toast("Fill up all fields.")

    def add_new_education(self):
        if self.my_school.current_item != "" and self.my_degree.current_item != "" and self.my_field.current_item != "" and self.my_start_date.text != "" and self.my_end_date.text:
            if self.compare_dates(self.my_start_date.text, self.my_end_date.text):
                if db.add_education(self.my_start_date.text, self.my_end_date.text, self.selected_degree, self.selected_field, self.selected_school, self.care_partners_id):
                    toast("Education added")
                    self.clear_education_fields()
                else:
                    toast("Something went wrong")
            else:
                toast("Start date must before end date")
        else:
            toast("Fill up all fields.")

    def delete_education(self, instance):
        if db.delete_education(str(instance.id)):
            self.get_all_education()
            toast("Education deleted")
        else:
            toast("Something went wrong")

    def clear_education_fields(self):
        self.ids.bp_school.set_item("School")
        self.ids.bp_degree.set_item("Degree")
        self.ids.bp_field.set_item("Field")
        self.ids.bp_start_date.text = ""
        self.ids.bp_end_date.text = ""
        self.selected_school = ""
        self.selected_field = ""
        self.selected_degree = ""
        self.my_school.set_item("School")
        self.my_degree.set_item("Degree")
        self.my_field.set_item("Field")
        self.my_start_date.text = ""
        self.my_end_date.text = ""
        self.selected_school = ""
        self.selected_field = ""
        self.selected_degree = ""

    def compare_dates(self, from_date, to_date):
        if from_date >= to_date:
            return False
        else:
            return True

    def skills_step(self):
        userinfo = db.get_user_info(self.user_id)
        if userinfo['short_about'] == "" and self.ids.summary.text != "":
            toast("Please save your professional summary")
        elif self.ids.summary.text == "":
            toast("Please add your professional summary")
            self.ids.summary.focus = True
        else:
            self.ids.screen_manager.current = "skills"

    def work_experience_step(self):
        if db.get_current_skills(self.care_partners_id):
            self.ids.screen_manager.current = "work-experience"
        else:
            toast("Please add skills")

    def education_step(self):
        if db.get_all_work_experience(self.care_partners_id):
            self.ids.screen_manager.current = "education"
        else:
            toast("Please add your work experience")

    def update_toolbar_label(self, label):
        self.ids.tool_bar.title = label

    def change_toolbar_label(self):
        if self.profile_url == "home":
            self.update_toolbar_label("Build your profile")
        if self.profile_url == "profile":
            self.update_toolbar_label("Profile")

    def redirect_to_profile(self, instance):
        self.ids.screen_manager.current = "profile"
        self.ids.screen_manager.transition.direction = "down"

    def load_dropdown_menus(self):
        job_title_list = db.get_job_titles()
        job_menu_items = [{"text": f"{i['name']}", "icon": f"{i['job_titles_id']}"} for i in job_title_list]
        if not self.position_menu:
            self.position_menu = MDDropdownMenu(
                caller=self.my_position,
                items=job_menu_items,
                width_mult=4.5,
                callback=self.job_callback
            )
        if not self.edit_position_menu:
            self.edit_position_menu = MDDropdownMenu(
                caller=self.ids.edit_position,
                items=job_menu_items,
                width_mult=4.5,
                callback=self.edit_job_callback
            )
        if not self.bp_position_menu:
            self.bp_position_menu = MDDropdownMenu(
                caller=self.ids.bp_position,
                items=job_menu_items,
                width_mult=4.5,
                callback=self.bp_job_callback
            )

        company_list = db.get_companies()
        company_menu_items = [{"text": f"{i['company_name']}", "icon": f"{i['company_id']}"} for i in company_list]
        if not self.company_menu:
            self.company_menu = MDDropdownMenu(
                caller=self.my_company,
                items=company_menu_items,
                width_mult=4.5,
                callback=self.company_callback
            )
        if not self.edit_company_menu:
            self.edit_company_menu = MDDropdownMenu(
                caller=self.ids.edit_company,
                items=company_menu_items,
                width_mult=4.5,
                callback=self.edit_company_callback
            )
        if not self.bp_company_menu:
            self.bp_company_menu = MDDropdownMenu(
                caller=self.ids.bp_company,
                items=company_menu_items,
                width_mult=4.5,
                callback=self.bp_company_callback
            )

        school_list = db.get_school()
        school_menu_items = [{"text": f"{i['name']}", "icon": f"{i['school_id']}"} for i in school_list]
        if not self.school_menu:
            self.school_menu = MDDropdownMenu(
                caller=self.my_school,
                items=school_menu_items,
                width_mult=4.5,
                callback=self.school_callback
            )
        if not self.edit_school_menu:
            self.edit_school_menu = MDDropdownMenu(
                caller=self.ids.edit_school,
                items=school_menu_items,
                width_mult=4.5,
                callback=self.edit_school_callback
            )
        if not self.bp_school_menu:
            self.bp_school_menu = MDDropdownMenu(
                caller=self.ids.bp_school,
                items=school_menu_items,
                width_mult=4.5,
                callback=self.bp_school_callback
            )

        degree_list = db.get_degree()
        degree_menu_items = [{"text": f"{i['name']}", "icon": f"{i['education_level_id']}"} for i in degree_list]
        if not self.degree_menu:
            self.degree_menu = MDDropdownMenu(
                caller=self.my_degree,
                items=degree_menu_items,
                width_mult=4.5,
                callback=self.degree_callback
            )
        if not self.edit_degree_menu:
            self.edit_degree_menu = MDDropdownMenu(
                caller=self.ids.edit_degree,
                items=degree_menu_items,
                width_mult=4.5,
                callback=self.edit_degree_callback
            )
        if not self.bp_degree_menu:
            self.bp_degree_menu = MDDropdownMenu(
                caller=self.ids.bp_degree,
                items=degree_menu_items,
                width_mult=4.5,
                callback=self.bp_degree_callback
            )

        field_list = db.get_field()
        field_menu_items = [{"text": f"{i['name']}", "icon": f"{i['field_study_id']}"} for i in field_list]
        if not self.field_menu:
            self.field_menu = MDDropdownMenu(
                caller=self.my_field,
                items=field_menu_items,
                width_mult=4.5,
                callback=self.field_callback
            )
        if not self.edit_field_menu:
            self.edit_field_menu = MDDropdownMenu(
                caller=self.ids.edit_field,
                items=field_menu_items,
                width_mult=4.5,
                callback=self.edit_field_callback
            )
        if not self.bp_field_menu:
            self.bp_field_menu = MDDropdownMenu(
                caller=self.ids.bp_field,
                items=field_menu_items,
                width_mult=4.5,
                callback=self.bp_field_callback
            )

    def job_callback(self, instance):
        self.my_position.set_item(instance.text)
        self.selected_job_title = str(instance.icon)
        self.position_menu.dismiss()

    def edit_job_callback(self, instance):
        self.ids.edit_position.set_item(instance.text)
        self.selected_job_title = str(instance.icon)
        self.edit_position_menu.dismiss()

    def bp_job_callback(self, instance):
        self.ids.bp_position.set_item(instance.text)
        self.selected_job_title = str(instance.icon)
        self.bp_position_menu.dismiss()

    def company_callback(self, instance):
        self.my_company.set_item(instance.text)
        self.selected_company = str(instance.icon)
        self.company_menu.dismiss()

    def edit_company_callback(self, instance):
        self.ids.edit_company.set_item(instance.text)
        self.selected_company = str(instance.icon)
        self.edit_company_menu.dismiss()

    def bp_company_callback(self, instance):
        self.ids.bp_company.set_item(instance.text)
        self.selected_company = str(instance.icon)
        self.bp_company_menu.dismiss()

    def school_callback(self, instance):
        self.my_school.set_item(instance.text)
        self.selected_school = str(instance.icon)
        self.school_menu.dismiss()

    def edit_school_callback(self, instance):
        self.ids.edit_school.set_item(instance.text)
        self.selected_school = str(instance.icon)
        self.edit_school_menu.dismiss()

    def bp_school_callback(self, instance):
        self.ids.bp_school.set_item(instance.text)
        self.selected_school = str(instance.icon)
        self.bp_school_menu.dismiss()

    def degree_callback(self, instance):
        self.my_degree.set_item(instance.text)
        self.selected_degree = str(instance.icon)
        self.degree_menu.dismiss()

    def edit_degree_callback(self, instance):
        self.ids.edit_degree.set_item(instance.text)
        self.selected_degree = str(instance.icon)
        self.edit_degree_menu.dismiss()

    def bp_degree_callback(self, instance):
        self.ids.bp_degree.set_item(instance.text)
        self.selected_degree = str(instance.icon)
        self.bp_degree_menu.dismiss()

    def field_callback(self, instance):
        self.my_field.set_item(instance.text)
        self.selected_field = str(instance.icon)
        self.field_menu.dismiss()

    def edit_field_callback(self, instance):
        self.ids.edit_field.set_item(instance.text)
        self.selected_field = str(instance.icon)
        self.edit_field_menu.dismiss()

    def bp_field_callback(self, instance):
        self.ids.bp_field.set_item(instance.text)
        self.selected_field = str(instance.icon)
        self.bp_field_menu.dismiss()

    def do_logout(self):
        self.ids.home_section.clear_widgets()
        self.ids.screen_manager.current = "home"
        self.ids.screen_manager.transition.direction = "left"
        spinner = MDSpinner(size_hint=(None, None), size=("46dp", "46dp"),  pos_hint={'center_x': 0.5, 'center_y': 0.5}, active=True)
        self.ids.home_section.add_widget(spinner)
        self.clear_work_experience_fields()
        self.clear_education_fields()
        Clock.schedule_once(self.clear_home, 2)

    def clear_home(self, instance):
        self.ids.home_section.clear_widgets()
        label = MDLabel(text="Please wait...", halign="center")
        self.ids.home_section.add_widget(label)

    def bottom_sheet_open(self, instance):
        if platform == "win":
            self.storage_path = storagepath.get_downloads_dir()
            bottom_sheet_menu = MDListBottomSheet()
            bottom_sheet_menu.add_item("Upload Photo", callback=self.file_manager_open, icon='camera')
            bottom_sheet_menu.add_item("View Profile Photo", callback=self.view_profile_photo, icon='eye')
            bottom_sheet_menu.open()
        else:
            self.storage_path = storagepath.get_external_storage_dir()
            bottom_sheet_menu = MDListBottomSheet()
            bottom_sheet_menu.add_item("Choose Photo", callback=self.file_manager_open, icon='cellphone-android')
            bottom_sheet_menu.add_item("View Profile Photo", callback=self.view_profile_photo, icon='eye')
            bottom_sheet_menu.open()

    def file_manager_open(self, instance):
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
        self.file_manager.show(self.storage_path)  # output manager to the screen
        self.manager_open = True

    def view_profile_photo(self, instance):
        profile_pic = PopupImage(source=self.ids.avatar.source)
        profile_pic.size = 300, 300
        self.dialog = MDDialog(
            type="custom",
            content_cls=profile_pic,
            buttons=[
                MDFlatButton(
                    text="CLOSE", text_color=self.theme_cls.primary_color, on_release=self.dialog_close
                )
            ],
        )
        self.dialog.width = 360
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss()

    def select_path(self, path):
        if path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            img = Image.open(path)
            img_size = int(str(len(img.fp.read()))) / 1000
            if img_size < 1000:
                file_path = 'images/profile/' + self.care_partners_id + '_' + str(datetime.now().microsecond) + '_photo.png'
                base_width = 300
                percent = (base_width / float(img.size[0]))
                height = int((float(img.size[1]) * float(percent)))
                img = img.resize((base_width, height), Image.ANTIALIAS)
                img.save(file_path, optimize=True)
                db.update_profile_photo(file_path, self.care_partners_id)
                toast("Profile photo updated")
                Clock.schedule_once(self.update_profile_photo, 2)
            else:
                toast("Image should be less than 1 MB")
        else:
            toast("Invalid file type")

    def update_profile_photo(self, instance):
        self.load_profile_photo()
        self.exit_manager()

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device..'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


class DateMDTextField(MDTextField):

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


db = Database()

