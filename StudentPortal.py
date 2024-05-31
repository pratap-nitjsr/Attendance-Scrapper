from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
import os
import time

class StudentPortal:
    def __init__(self, headless=True):
        load_dotenv()
        self.chrome_options = webdriver.ChromeOptions()
        self.deafult_usename = os.getenv('DEFAULT_USERNAME')
        self.pwd = os.getenv('PASSWORD')
        if headless:
            self.chrome_options.add_argument("--headless")
    def __make_driver(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def __refresh(self):
        self.driver.refresh()

    def __login(self):
        self.driver.get('https://online.nitjsr.ac.in/endsem/Login.aspx')

        self.driver.find_element(By.NAME, 'txtuser_id').send_keys(self.deafult_usename)
        self.driver.find_element(By.NAME, 'txtpassword').send_keys(self.pwd)
        try:
            self.driver.find_element(By.NAME, 'btnsubmit').click()
        except:
            pass

    def __access_attendance(self, username):

        self.driver.get('https://online.nitjsr.ac.in/endsem/StudentAttendance/ClassAttendance.aspx')

        self.driver.execute_script(f"document.getElementsByName('ctl00$ContentPlaceHolder1$ddlroll')[0].disabled = false;")
        dropdown = Select(self.driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlroll'))
        dropdown.select_by_value(username)

        time.sleep(5)

        attendance_table = self.driver.find_element(By.ID, 'ContentPlaceHolder1_gv')
        attendance = []

        rows = attendance_table.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if not cells:
                cells = row.find_elements(By.TAG_NAME, 'th')
            row_data = [cell.text for cell in cells]
            attendance.append(row_data)

        return attendance

    def __quit(self):
        self.driver.quit()

    def get_attendance(self, username):
        self.__make_driver()
        self.__refresh()
        self.__login()
        attendance = self.__access_attendance(username)
        self.__quit()
        return attendance
