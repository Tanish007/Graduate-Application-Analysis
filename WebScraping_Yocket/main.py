import time
from Tools.scripts.dutree import display
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By


class StudentProfile:
    def __init__(self):
        self.handleId = ''
        self.Applied_university = ''
        self.Applied_course = ''
        self.Year = 0
        self.Status = ''


# creating class to store student details in an object
class StudentDetails:
    def __init__(self):
        self.Student_Name = ''
        self.Student_intake_Type = ''
        self.Student_intake_Year = ''
        self.Student_application_status = ''
        self.Student_applied_university = ''
        self.Student_applied_course = ''
        self.Student_undergrad_score = ''
        self.Student_undergrad_college = ''
        self.Student_undergrad_course = ''
        self.Student_Gre_score = ''
        self.Student_proficiency_test = ''
        self.Student_proficiency_score = ''
        self.Student_skills = ''
        self.Student_Company = ''
        self.Student_job_description = ''
        self.Student_work_type = ''
        self.Student_work_duration = ''


# login yocket using your credentials
chromedriver_autoinstaller.install()
driver = webdriver.Firefox()
driver.get("https://yocket.com/login")
a = input()
# this will stop the automated script so u can add the credentials on the yocket website

# maximize the size of window
driver.maximize_window()

# start year to find the application of students
application_year = "2022"
# application status 6 -> rejected , 7-> admitted
application_status = ["6", "7"]

# loop will run till 2018
while int(application_year) >= 2018:
    # run for both admitted and rejected students for that current year
    for status_code in application_status:
        profileName_of_student_data = []

        # creating dataframe to store all student profile(link) details
        df_student_details = pd.DataFrame(
            columns=['Full_Name', 'University', 'Course', 'Year', 'Intake', 'GRE', 'English_test', 'English_test_score',
                     'Undergrad_college', 'Undergrad_score', 'Undergrad_course', 'Skills', 'Work_company', 'Work_type',
                     'Work_jd', 'Work_duration', 'Status'])
        df_student_profile = pd.DataFrame(columns=['StudentID', 'University', 'Course', 'Year', 'Status'])
        while len(driver.window_handles) > 1:
            driver.close()
        driver.refresh()
        driver.get(
            "https://yocket.com/connect?university=2621,729,710,713,705,2596,2777,708,868,802,707,795,745,810,2638,1480,711,764,736,2587,752,861,782,734&course=Computer%20Science&country=United%20States&status=" + "7" + "&year=" + application_year)
        time.sleep(7)

        counter = 0
        # keep on clicking load more till it's available on the web page
        while len(driver.find_elements(by=By.XPATH,
                                       value="/html/body/div/div/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/button")) > 0:
            element = driver.find_element(by=By.XPATH,
                                          value="/html/body/div/div/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/button")
            element.click()
            time.sleep(3)
            if counter == 50:
                break
            counter += 1

        # Counting no of results obtained on this search
        Students_count_element = driver.find_elements(by=By.XPATH,
                                                      value="/html/body/div/div/div/div[2]/div/main/div/div[2]/div/div[1]/div/div/div/span/p")
        Student_count = int(Students_count_element[0].text.split(' ')[3])

        if status_code == "6":
            app_status = "Reject"
        else:
            app_status = "Admit"

        # in a loop to get the details of a single student in the search history.
        fileName = 'studentLinks' + str(application_year) + app_status + '.json'
        with open(fileName, 'a') as fp:
            pass

        json_file = open(fileName, 'r')
        json_file_content = json_file.readlines()
        if len(json_file_content) > 0:
            json_df = pd.read_json(fileName)
        else:
            json_df = []
        for i in range(max(1, len(json_df) - 1), Student_count):
            try:
                Student_1 = StudentProfile()
                Student_1.Year = application_year
                Student_1.Status = app_status
                card_element_student = driver.find_elements(by=By.XPATH,
                                                            value="/html/body/div/div/div/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div[" + str(
                                                                i) + "]")
                if len(card_element_student) > 0:
                    Student_1.Applied_university = card_element_student[0].text.split('\n')[3]
                    Student_1.Applied_course = card_element_student[0].text.split('\n')[4]
                    profileName_of_student_data.append(Student_1)

                Xpath_Value = "/html/body/div/div/div/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div[" + str(
                    i) + "]/div[1]/div/div[3]/button"
                message_element_student = driver.find_elements(by=By.XPATH, value=Xpath_Value)
                if len(message_element_student) > 0:
                    desired_y = (message_element_student[0].size['height'] / 2) + message_element_student[0].location[
                        'y']
                    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script(
                        'return window.pageYOffset')
                    scroll_y_by = desired_y - current_y
                    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
                    time.sleep(2)
                    message_element_student[0].click()
                    profile_name_element = ''
                    time.sleep(3)
                    driver.switch_to.window(driver.window_handles[1])
                    while profile_name_element == '':
                        time.sleep(10)
                        profile_name_element = driver.find_elements(by=By.XPATH,
                                                                    value="/html/body/div/div/div/div/div/main/div/div/div/div/div/div[2]/div[1]/div[1]/div[2]/p")

                    Student_1.handleId = profile_name_element[0].text[1:]
                    df_student_profile = df_student_profile.append(
                        {'StudentID': Student_1.handleId, 'University': Student_1.Applied_university,
                         'Course': Student_1.Applied_course, 'Year': Student_1.Year, 'Status': Student_1.Status},
                        ignore_index=True)
                    time.sleep(2)
                    driver.close()
                    time.sleep(4)
                    driver.switch_to.window(driver.window_handles[0])
            except:
                with open('ErrorLogStudentLinks.txt', 'a') as f:
                    f.write('-' + application_year + '-' + app_status + '-' + str(i) + '\n')
                continue

        json_file = open(fileName, 'r')
        json_file_content = json_file.readlines()
        if len(json_file_content) > 0:
            already_existing_links = pd.read_json(fileName)
            new_links = pd.concat([already_existing_links, df_student_profile], ignore_index=True)
        else:
            new_links = df_student_profile

        json_new_content = new_links.to_json()
        with open(fileName, 'w') as fp:
            fp.write(json_new_content)
        fp.close()
        with open('lstStudentLinks.txt', 'a') as f:
            # f.write('\n' + '-----' + application_year + '-' + app_status + '--------------' + '\n')
            for data_row in df_student_profile.values:
                f.write(data_row[0] + '\t' + data_row[1] + '\t' + data_row[2] + '\n')

        filename_student_profile = 'studentProfile_' + app_status + '_' + application_year +'.json'
        df_studentProfiles = pd.read_json(filename_student_profile)
        with open(filename_student_profile, 'a') as fp:
            pass
        for student_profile in df_studentProfiles.values:
            try:
                # creating object of student class to store student details.
                Student = StudentDetails()
                while len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                driver.get("https://yocket.com/profile/" + str(student_profile[0]))
                # if status_code == "6":
                Student.Student_application_status = student_profile[4]
                # else:
                #     Student.Student_application_status = "Admit"

                Student.Student_applied_university = student_profile[1]
                Student.Student_applied_course = student_profile[2]
                time.sleep(4)
                name_element = driver.find_elements(by=By.CLASS_NAME, value="mx-auto")
                if len(name_element) > 0:
                    for values in name_element:
                        if values.tag_name == 'p':
                            Student.Student_Name = values.text
                        elif values.text.startswith("Fall") or values.text.startswith("Spring"):
                            Student.Student_intake_Type = values.text.split(" ")[0]
                            Student.Student_intake_Year = values.text.split(" ")[1]

                undergrad_details_element = driver.find_elements(by=By.ID, value="CollegeDetails")
                if len(undergrad_details_element) > 0:
                    if 'CGPA' in undergrad_details_element[0].text:
                        Student.Student_undergrad_score = undergrad_details_element[0].text.split('\n')[1]
                        Student.Student_undergrad_college = undergrad_details_element[0].text.split('\n')[3]
                        Student.Student_undergrad_course = undergrad_details_element[0].text.split('\n')[4]
                    else:
                        Student.Student_undergrad_score = undergrad_details_element[0].text.split('\n')[1]
                        Student.Student_undergrad_college = undergrad_details_element[0].text.split('\n')[2]
                        Student.Student_undergrad_course = undergrad_details_element[0].text.split('\n')[3]

                Student_test_score_element = driver.find_elements(by=By.ID, value="TestScores")
                if len(Student_test_score_element) > 0:
                    Student_score_list = list(Student_test_score_element[0].text.split('\n'))
                    if 'GRE' in Student_score_list:
                        index_Gre = Student_score_list.index('GRE')
                        Student.Student_Gre_score = Student_score_list[index_Gre + 1]
                    if 'English test scores' in Student_score_list:
                        index_test = Student_score_list.index('English test scores')
                        Student.Student_proficiency_test = Student_score_list[index_test + 1]
                        Student.Student_proficiency_score = Student_score_list[index_test + 2]

                Student_skills_element = driver.find_elements(by=By.ID, value="Skills")
                if len(Student_skills_element) > 0:
                    Student.Student_skills = str(Student_skills_element[0].text.split('\n')[1:])

                Student_Company = ""
                Student_job_description = ""
                Student_work_duration = ""
                Student_WorkExperience_element = driver.find_elements(by=By.ID, value="WorkExperience")
                if len(Student_WorkExperience_element) > 0:
                    for value in Student_WorkExperience_element:
                        Student_Company += value.text.split('\n')[2].split('•')[0] + " "
                        Student_job_description += value.text.split('\n')[1] + " "
                        Student.Student_work_type = value.text.split('\n')[2].split('•')[1]
                        Student_work_duration += value.text.split('\n')[3].split('•')[1] + " "
                    Student.Student_Company = Student_Company
                    Student.Student_job_description = Student_job_description
                    Student.Student_work_duration = Student_work_duration
                df_student_details = df_student_details.append(
                    {'Full_Name': Student.Student_Name, 'University': Student.Student_applied_university,
                     'Course': Student.Student_applied_course, 'Year': Student.Student_intake_Year,
                     'Intake': Student.Student_intake_Type, 'GRE': Student.Student_Gre_score,
                     'English_test': Student.Student_proficiency_test,
                     'English_test_score': Student.Student_proficiency_score,
                     'Undergrad_college': Student.Student_undergrad_college,
                     'Undergrad_score': Student.Student_undergrad_score,
                     'Undergrad_course': Student.Student_undergrad_course, 'Skills': Student.Student_skills,
                     'Work_company': Student.Student_Company, 'Work_type': Student.Student_work_type,
                     'Work_jd': Student.Student_job_description, 'Work_duration': Student.Student_work_duration,
                     'Status': Student.Student_application_status},
                    ignore_index=True)

            except:
                # with open('ErrorLogStudentProfiles.txt', 'a') as f:
                #     f.write('-' + student_profile.handleId + '-' + application_year + '-' + '-' + '\n')
                continue

        json_file = open(filename_student_profile, 'r')
        json_file_content = json_file.readlines()
        if len(json_file_content) > 0:
            already_existing_links = pd.read_json(filename_student_profile)
            new_profiles = pd.concat([already_existing_links, df_student_details], ignore_index=True)
        else:
            new_profiles = df_student_details

        json_new_profile_content = new_profiles.to_json()
        with open(filename_student_profile, 'w') as fp:
            fp.write(json_new_profile_content)
        fp.close()
        with open('lstStudentDetails.txt', 'a') as f:
            f.write('\n' + '-----' + application_year + '-' + app_status + '--------------' + '\n')
            for data_row_stud in df_student_details.values:
                f.write(
                    data_row_stud[0] + '\t' + data_row_stud[1] + '\t' + data_row_stud[2] + ' \t' + data_row_stud[
                        3] + '\t' + data_row_stud[
                        4] + '\t' + data_row_stud[5] + '\t' + data_row_stud[6] + '\t' + data_row_stud[7] + '\t' +
                    data_row_stud[8] + '\t' + data_row_stud[
                        9] + '\t' + data_row_stud[10] + '\t' + data_row_stud[11] + '\t' + data_row_stud[12] + '\t' +
                    data_row_stud[13] + '\t' +
                    data_row_stud[14] + '\t' + data_row_stud[15] + '\t' + data_row_stud[16] + '\n')
    application_year = str(int(application_year) - 1)


