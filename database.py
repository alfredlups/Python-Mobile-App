import MySQLdb as db
import MySQLdb.cursors
from datetime import datetime


class Database:

    def __init__(self):
        self.host = "db-mysql-nyc1-61341-do-user-8664437-0.b.db.ondigitalocean.com"
        self.port = 25060
        self.user = "alfred"
        self.password = "usv33qwuhzghhkr4"
        self.dbase = "phscp_database"
        self.connection = db.Connection(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.dbase, cursorclass=MySQLdb.cursors.DictCursor)
        self.current_date = datetime.today().strftime('%Y-%m-%d')

    def check_user(self, email):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM users WHERE email_address='"+email+"'"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def add_user(self, email, mobile_number, password, role_id):
        dbhandler = self.connection.cursor()
        query = "INSERT INTO users (username, email_address, mobile_number, password, user_role_id, date_created) VALUES (%s,%s,%s,%s,%s,%s)"
        result = dbhandler.execute(query, ('user', email, mobile_number, password, role_id, self.current_date))
        self.connection.commit()
        return dbhandler.lastrowid

    def add_care_partner(self, first_name, mi, last_name, street, city, state, zipcode, date_of_birth, gender, user_id):
        dbhandler = self.connection.cursor()
        query = "INSERT INTO care_partners (first_name, middle_initial, last_name, street, city, state, zip_code, short_about, date_of_birth, gender, date_created, photo_url, users_id, profile_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result = dbhandler.execute(query, (first_name, mi, last_name, street, city, state, zipcode, '', date_of_birth, gender, self.current_date, "test", user_id, 0))
        self.connection.commit()
        return result

    def login(self, email, password):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM users WHERE email_address='" + email + "' AND password='" + password + "'"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def get_user_info(self, user_id):
        dbhandler = self.connection.cursor()
        query = "SELECT u.users_id, cp.care_partners_id, first_name, last_name, email_address, password,  short_about, street, city, state, zip_code, mobile_number, profile_status FROM users u JOIN care_partners cp USING(users_id) WHERE cp.users_id='"+user_id+"' LIMIT 1"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def add_summary(self, user_id, summary):
        dbhandler = self.connection.cursor()
        query = "UPDATE care_partners SET short_about=%s WHERE users_id=%s"
        result = dbhandler.execute(query, (summary, user_id))
        self.connection.commit()
        return result

    def update_profile_status(self, care_partner_id, profile_status):
        dbhandler = self.connection.cursor()
        query = "UPDATE care_partners SET profile_status=%s WHERE care_partners_id=%s"
        result = dbhandler.execute(query, (profile_status, care_partner_id))
        self.connection.commit()
        return result

    def check_skills(self, skills):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM skills WHERE LOWER(name)='" + skills + "'"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def get_skills(self):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM skills LIMIT 6"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def add_skills_table(self, skills):
        dbhandler = self.connection.cursor()
        query = "INSERT INTO skills (name) VALUES ('" + skills + "')"
        result = dbhandler.execute(query)
        self.connection.commit()
        return dbhandler.lastrowid

    def add_skills(self, care_partner_id, skills_id):
        dbhandler = self.connection.cursor()
        query = "INSERT INTO care_partner_skills (care_partners_id, skills_id) VALUES (%s,%s)"
        result = dbhandler.execute(query, (care_partner_id, skills_id))
        self.connection.commit()
        return result

    def get_current_skills_by_id(self, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM care_partner_skills WHERE care_partners_id='"+care_partner_id+"'"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def get_current_skills(self, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM care_partner_skills cps JOIN skills s USING(skills_id) WHERE care_partners_id='" + care_partner_id + "'"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def search_skills(self, value):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM skills WHERE name LIKE '%"+value+"%' AND skills_id > 6 "
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def delete_skill(self, care_partners_id, skill_id):
        dbhandler = self.connection.cursor()
        query = "DELETE FROM care_partner_skills WHERE care_partners_id='" + care_partners_id + "' AND skills_id='" + skill_id + "'"
        result = dbhandler.execute(query)
        self.connection.commit()
        return result

    def get_job_titles(self):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM job_titles"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def get_companies(self):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM companies"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def add_work_experience(self, from_date, to_date, current_company, description, address, care_partners_id, company_id, job_title_id):
        dbhandler = self.connection.cursor()
        query = "INSERT INTO work_experiences (start_date, end_date, currently_working, description, state, care_partners_id, company_id, job_titles_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        result = dbhandler.execute(query, (from_date, to_date, current_company, description, address, care_partners_id, company_id, job_title_id))
        self.connection.commit()
        return result

    def get_school(self):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM school"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def get_degree(self):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM education_level"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def get_field(self):
        dbhandler = self.connection.cursor()
        query = "SELECT * FROM field_study"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def add_education(self, start_date, end_date, degree_id, field_id, school_id, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "INSERT INTO education (start_date, end_date, education_level_id, field_study_id, school_id, care_partners_id) VALUES (%s,%s,%s,%s,%s,%s)"
        result = dbhandler.execute(query, (start_date, end_date, degree_id, field_id, school_id, care_partner_id))
        self.connection.commit()
        return result

    def get_work_experience(self, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "SELECT wx.*, c.company_name, jt.name FROM work_experiences wx JOIN companies c USING (company_id) JOIN job_titles jt USING (job_titles_id) WHERE wx.care_partners_id='"+care_partner_id+"' ORDER BY wx.currently_working DESC LIMIT 1"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def get_education(self, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "SELECT e.education_id, e.start_date, e.end_date, el.name AS education_level, fs.name AS field_study, s.name AS school FROM education e JOIN education_level el USING (education_level_id) JOIN field_study fs USING (field_study_id) JOIN school s USING (school_id) WHERE e.care_partners_id='"+care_partner_id+"' ORDER BY e.end_date DESC LIMIT 1"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def get_all_education(self, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "SELECT e.education_id, e.start_date, e.end_date, el.name AS education_level, fs.name AS field_study, s.name AS school FROM education e JOIN education_level el USING (education_level_id) JOIN field_study fs USING (field_study_id) JOIN school s USING (school_id) WHERE e.care_partners_id='"+care_partner_id+"'"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def update_education(self, start_date, end_date, degree_id, field_id, company_id, education_id):
        dbhandler = self.connection.cursor()
        query = "UPDATE education SET start_date=%s, end_date=%s, education_level_id=%s, field_study_id=%s, school_id=%s  WHERE education_id=%s"
        result = dbhandler.execute(query, (start_date, end_date, degree_id, field_id, company_id, education_id))
        self.connection.commit()
        return result

    def get_specific_education(self, education_id):
        dbhandler = self.connection.cursor()
        query = "SELECT e.education_id, e.education_level_id, e.field_study_id, e.school_id, e.start_date, e.end_date, el.name AS education_level, fs.name AS field_study, s.name AS school FROM education e JOIN education_level el USING (education_level_id) JOIN field_study fs USING (field_study_id) JOIN school s USING (school_id) WHERE e.education_id='"+education_id+"'"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def update_user(self, user_id, email, password, mobile_number):
        dbhandler = self.connection.cursor()
        query = "UPDATE users SET email_address=%s, password=%s, mobile_number=%s WHERE users_id=%s"
        result = dbhandler.execute(query, (email, password, mobile_number, user_id))
        self.connection.commit()
        return result

    def update_care_partner(self, care_partner_id, first_name, last_name, street, city, state, zipcode):
        dbhandler = self.connection.cursor()
        query = "UPDATE care_partners SET first_name=%s, last_name=%s, street=%s, city=%s, state=%s, zip_code=%s WHERE care_partners_id=%s"
        result = dbhandler.execute(query, (first_name, last_name, street, city, state, zipcode, care_partner_id))
        self.connection.commit()
        return result

    def update_summary(self, care_partner_id, summary):
        dbhandler = self.connection.cursor()
        query = "UPDATE care_partners SET short_about=%s WHERE care_partners_id=%s"
        result = dbhandler.execute(query, (summary, care_partner_id))
        self.connection.commit()
        return result

    def get_all_work_experience(self, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "SELECT wx.*, c.company_name, jt.name FROM work_experiences wx JOIN companies c USING (company_id) JOIN job_titles jt USING (job_titles_id) WHERE wx.care_partners_id='" + care_partner_id + "'"
        dbhandler.execute(query)
        result = dbhandler.fetchall()
        return result

    def get_specific_work_experience(self, work_experience_id):
        dbhandler = self.connection.cursor()
        query = "SELECT wx.*, c.company_name, jt.name FROM work_experiences wx JOIN companies c USING (company_id) JOIN job_titles jt USING (job_titles_id) WHERE wx.work_experiences_id='" + work_experience_id + "'"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def update_work_experience(self, work_id, start_date, end_date, currently_working, description, state, company_id, job_title_id):
        dbhandler = self.connection.cursor()
        query = "UPDATE work_experiences SET start_date=%s, end_date=%s, currently_working=%s, description=%s, state=%s, company_id=%s, job_titles_id=%s  WHERE work_experiences_id=%s"
        result = dbhandler.execute(query, (start_date, end_date, currently_working, description, state, company_id, job_title_id, work_id))
        self.connection.commit()
        return result

    def delete_work_experience(self, work_id):
        dbhandler = self.connection.cursor()
        query = "DELETE FROM work_experiences WHERE work_experiences_id='" + work_id + "'"
        result = dbhandler.execute(query)
        self.connection.commit()
        return result

    def delete_education(self, education_id):
        dbhandler = self.connection.cursor()
        query = "DELETE FROM education WHERE education_id='" + education_id + "'"
        result = dbhandler.execute(query)
        self.connection.commit()
        return result

    def update_profile_photo(self, photo_url, care_partners_id):
        dbhandler = self.connection.cursor()
        query = "UPDATE care_partners SET photo_url=%s WHERE care_partners_id=%s"
        result = dbhandler.execute(query, (photo_url, care_partners_id))
        self.connection.commit()
        return result

    def get_profile_photo(self, care_partner_id):
        dbhandler = self.connection.cursor()
        query = "SELECT photo_url FROM care_partners WHERE care_partners_id='" + care_partner_id + "' LIMIT 1"
        dbhandler.execute(query)
        result = dbhandler.fetchone()
        return result

    def add_patient(self, one ,two, tree, four, five, six):
        pass



