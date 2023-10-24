from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QDialog, QMessageBox, QTableWidgetItem)
from PyQt6.QtGui import QIcon
from LLMCDI.admin_dashboard import Ui_ADMIN_DB
from userLogin import Login_Window
from datetime import datetime, date
import sys
import psycopg2
import psycopg2.extras


class DB_Window(QMainWindow, Ui_ADMIN_DB):

    def __init__(self):
        super(DB_Window, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("LAPU-LAPU MEDICAL DIAGNOSTIC CENTER, INC.")
        self.doLogin()
        self.admin_name.setText(self.login.Userlbl.text())

        self.hostname = 'localhost'
        self.database = 'llmdci'
        self.username = 'postgres'
        self.pword = '123456'
        self.port_id = 5432

        self.notificataionBTN.setDisabled(True)
        self.icon_only_widget.hide()
        self.stackedWidget.setCurrentIndex(0)
        self.dashboardBTN_2.setChecked(True)

        self.logoutBTN.clicked.connect(self.message_box)
        self.logoutBTN_2.clicked.connect(self.message_box)

        self.timer = QTimer()
        self.timer.timeout.connect(self.LCD_clock)

        self.timer.start(1000)
        self.LCD_clock()

        curr_date = QDateTime.currentDateTime()
        self.sched_date.setText(str(curr_date.toString("dddd, MMMM dd, yyyy")))
        self.cal_date.setText(str(curr_date.toString("dddd, MMMM dd, yyyy")))
        self.avail_datelbl.setText(str(curr_date.toString("dddd, MMMM dd, yyyy")))
        self.resched_date.setText(str(curr_date.toString("dddd, MMMM dd, yyyy")))

        self.sched_calendar.selectionChanged.connect(self.get_date)
        self.main_calendar.selectionChanged.connect(self.get_date)
        self.calendarWidget.selectionChanged.connect(self.get_date)
        self.sched_calendar_2.selectionChanged.connect(self.get_date)

        self.admin_submit.clicked.connect(self.admin_register)
        self.show_pass.toggled.connect(self.show_password)
        self.deact_no.clicked.connect(self.on_dashboardBTN_clicked)
        self.deact_yes.clicked.connect(self.acc_deactivate)
        self.sched_btn.clicked.connect(self.schedule)
        self.sched_btn_2.clicked.connect(self.schedule)
        self.data_btn.clicked.connect(self.appointment_data)
        self.cancel_schedBTN.clicked.connect(self.delete_row)
        self.rescheduling_btn.clicked.connect(self.rescheduling)
        self.done_btn.clicked.connect(self.done_appointment)
        self.admin_data_btn.clicked.connect(self.admin_data)
        self.show_data_info.clicked.connect(self.new_pat_data)
        self.app_hist_btn.clicked.connect(self.app_hist_tbldata)
        self.delete_info.clicked.connect(self.delete_pat_info)
        self.hist_delete.clicked.connect(self.delete_app_hist)
        self.app_made_btn.clicked.connect(self.app_made_table)
        self.loyalty_id.textChanged.connect(self.btnvisibility)
        self.show()

    # deactivate account page
    def on_deac_btn_clicked(self):
        self.stackedWidget.setCurrentIndex(10)

    # reschedule page
    def on_resched_btn_clicked(self):
        self.stackedWidget.setCurrentIndex(11)

    # add user page
    def on_add_userBTN_clicked(self):
        self.stackedWidget.setCurrentIndex(9)

    # remove the 'focus' on every button
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.icon_only_widget.findChildren(QPushButton) + self.full_menu_widget.findChildren(QPushButton)

        for btn in btn_list:
            if index in [9, 1, 2, 3, 4]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    # dashboard page
    def on_dashboardBTN_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    def on_dashboardBTN_2_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    # schedule page
    def on_scheduleBTN_clicked(self):
        self.stackedWidget.setCurrentIndex(12)

    def on_scheduleBTN_2_clicked(self):
        self.stackedWidget.setCurrentIndex(12)

    # history page
    def on_historyBTN_clicked(self):
        self.stackedWidget.setCurrentIndex(5)

    def on_historyBTN_2_clicked(self):
        self.stackedWidget.setCurrentIndex(5)

    # calendar page
    def on_calendarBTN_clicked(self):
        self.stackedWidget.setCurrentIndex(6)

    def on_calendarBTN_2_clicked(self):
        self.stackedWidget.setCurrentIndex(6)

    # regular patient page
    def on_reg_patientBTN_clicked(self):
        self.stackedWidget.setCurrentIndex(7)

    def on_reg_patientBTN_2_clicked(self):
        self.stackedWidget.setCurrentIndex(7)

    # doctor's availability page
    def on_availabilityBTN_clicked(self):
        self.stackedWidget.setCurrentIndex(8)

    def on_availabilityBTN_2_clicked(self):
        self.stackedWidget.setCurrentIndex(8)

    # admin user's page
    def on_users_info_clicked(self):
        self.stackedWidget.setCurrentIndex(4)

    # appointments made page
    def on_appointments_made_clicked(self):
        self.stackedWidget.setCurrentIndex(3)

    # ongoing appointments page
    def on_on_going_appointments_clicked(self):
        self.stackedWidget.setCurrentIndex(2)

    # patient information's page
    def on_pat_information_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    def on_YES_BTN_clicked(self):
        self.loyalty_id.setVisible(True)
        self.sched_btn_2.setVisible(False)

    def on_NO_BTN_clicked(self):
        self.sched_btn_2.setVisible(True)
        self.loyalty_id.setVisible(False)
        self.sched_btn.setVisible(False)
        self.loyalty_id.clear()

    def btnvisibility(self):
        self.sched_btn.setVisible(True)

    def LCD_clock(self):
        time = datetime.now().time()
        formatted_time = time.strftime("%I:%M:%S %p")

        self.cal_time.setDigitCount(12)
        self.cal_time.display(formatted_time)

    def get_date(self):
        dateSelected = self.sched_calendar.selectedDate()
        dateSelected2 = self.main_calendar.selectedDate()
        dateSelected3 = self.calendarWidget.selectedDate()
        dateSelected4 = self.sched_calendar_2.selectedDate()

        self.sched_date.setText(str(dateSelected.toString("dddd, MMMM dd, yyyy")))
        self.cal_date.setText(str(dateSelected2.toString("dddd, MMMM dd, yyyy")))
        self.avail_datelbl.setText(str(dateSelected3.toString("dddd, MMMM dd, yyyy")))
        self.resched_date.setText(str(dateSelected4.toString("dddd, MMMM dd, yyyy")))

        # Qmessage box

    def message_box(self):
        msg = QMessageBox()
        msg.setWindowTitle("LLMDCI")
        msg.setWindowIcon(QIcon("icon.png"))
        msg.setFixedWidth(150)
        msg.setText("Are you sure, Do you want to sign out?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        button = msg.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.SIGN_OUT()

    def required_box(self):
        msg = QMessageBox()
        msg.setWindowTitle("LLMDCI")
        msg.setWindowIcon(QIcon("icon.png"))
        msg.setFixedWidth(150)
        msg.setText("Validation Error " + "Please enter a value.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        button = msg.exec()

        if button == QMessageBox.StandardButton.Ok:
            msg.close()

    def clear_text(self):
        self.admin_fname.clear()
        self.admin_lname.clear()
        self.admin_phnum.clear()
        self.admin_pword.clear()
        self.admin_confirm.clear()
        self.admin_email.clear()
        self.admin_username.clear()
        self.fname.clear()
        self.fname.clear()
        self.lname.clear()
        self.mid_name.clear()
        self.barangay.clear()
        self.city.clear()
        self.gender.clear()
        self.email_ad.clear()
        self.contact_num.clear()
        self.date_box.clear()
        self.sched_date.clear()

    # T H E   S Q L    Q U E R Y    S T A R T S      H E R E

    # admin registration
    def admin_register(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    fname = self.admin_fname.text()
                    lname = self.admin_lname.text()
                    ad_user = self.admin_username.text()
                    contact = self.admin_phnum.text()
                    ad_pword = self.admin_pword.text()
                    pass_confirm = self.admin_confirm.text()
                    ad_email = self.admin_email.text()
                    created = datetime.now().date()

                    insert_script = 'INSERT INTO ADMIN_STAFF (admin_fname, admin_lname, admin_uname, admin_contact, ' \
                                    'admin_pass, admin_email, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                    insert_values = (fname.title(), lname.title(), ad_user, contact, pass_confirm, ad_email, created)

                    if fname.strip() == "":
                        self.required_box()
                    elif lname.strip() == "":
                        self.required_box()
                    elif ad_user.strip() == "":
                        self.required_box()
                    elif ad_pword.strip() == "":
                        self.required_box()
                    elif pass_confirm.strip() == "":
                        self.required_box()
                    elif ad_email.strip() == "":
                        self.required_box()
                    elif contact.strip() == "":
                        self.required_box()
                    else:
                        if ad_pword != pass_confirm:
                            self.Xpass_lbl.setText("PASSWORD DIDN'T MATCH!!")
                        # elif not self.phone_validator.validate(contact.strip(), 0)[0]:
                        #     self.required_box()
                        else:
                            cur.execute(insert_script, insert_values)
                            self.clear_text()
                            self.Xpass_lbl.clear()

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    # scheduling a patient
    def schedule(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    myfname = self.fname.text().title()
                    mylname = self.lname.text().title()
                    mymidname = self.mid_name.text().title()
                    mybrgy = self.barangay.text().title()
                    mycity = self.city.text().title()
                    mygender = self.gender.text()
                    myemail = self.email_ad.text()
                    mynum = self.contact_num.text()
                    mybday = self.date_box.text()
                    mysched = self.sched_date.text()
                    user = self.login.Userlbl.text()
                    mypass = self.login.Passlbl.text()
                    time = self.sched_time.time()
                    format_time = time.toString("h:mm:ss")
                    address = mybrgy + " " + mycity

                    if self.loyalty_id.text().strip() == "":
                        loyalID = 0
                    else:
                        loyalID = int(self.loyalty_id.text())

                    myid = 'SELECT ADMIN_ID FROM ADMIN_STAFF WHERE ADMIN_UNAME = %s AND ADMIN_PASS = %s'
                    myid_values = (user, mypass)

                    if myfname.strip() == "":
                        self.required_box()
                    elif mylname.strip() == "":
                        self.required_box()
                    elif mymidname.strip() == "":
                        self.required_box()
                    elif mybrgy.strip() == "":
                        self.required_box()
                    elif mycity.strip() == "":
                        self.required_box()
                    elif mygender.strip() == "":
                        self.required_box()
                    elif myemail.strip() == "":
                        self.required_box()
                    elif mynum.strip() == "":
                        self.required_box()
                    elif mybday.strip() == "":
                        self.required_box()
                    elif mysched.strip() == "":
                        self.required_box()

                    else:
                        cur.execute(myid, myid_values)

                        for record in cur.fetchall():
                            insert = 'INSERT INTO ON_GOING_APPOINTMENT (pat_fname, pat_lname, pat_midname, ' \
                                     'pat_birthday, pat_gender, pat_address, pat_contact, pat_email, ' \
                                     'appointment_date, appointment_time, admin_id, loyalty_id) ' \
                                     'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                            insert_value = (
                                myfname, mylname, mymidname, mybday, mygender, address, mynum, myemail, mysched,
                                format_time, record["admin_id"], loyalID)

                            cur.execute(insert, insert_value)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                self.clear_text()

    # showing the patient's ongoing appointments
    def appointment_data(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = 'SELECT PAT_ID, PAT_FNAME, PAT_LNAME, PAT_MIDNAME, APPOINTMENT_DATE, APPOINTMENT_TIME, ' \
                            'ADMIN_ID, LOYALTY_ID FROM ON_GOING_APPOINTMENT'

                    cur.execute(query)
                    result = cur.fetchall()
                    num_rows = len(result)
                    num_columns = len(result[0])

                    for row in range(num_rows):
                        for column in range(num_columns):
                            item = QTableWidgetItem(str(result[row][column]))
                            self.tableWidget.setItem(row, column, item)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    # showing all the admins information
    def admin_data(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = 'SELECT ADMIN_ID, ADMIN_FNAME, ADMIN_LNAME, ADMIN_CONTACT, ADMIN_EMAIL, DATE_CREATED, ' \
                            'DEACTIVATE FROM ADMIN_STAFF'

                    cur.execute(query)
                    result = cur.fetchall()
                    num_rows = len(result)
                    num_columns = len(result[0])

                    for row in range(num_rows):
                        for column in range(num_columns):
                            item = QTableWidgetItem(str(result[row][column]))
                            self.admin_tbl.setItem(row, column, item)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    # showing the patient's information
    def new_pat_data(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = 'SELECT PAT_ID, PAT_INFO_FNAME, PAT_INFO_LNAME, PAT_INFO_MIDNAME, PAT_INFO_BIRTHDAY,' \
                            'PAT_INFO_GENDER, PAT_INFO_ADDRESS, PAT_INFO_CONTACT, PAT_INFO_EMAIL FROM NEW_PATIENT'

                    cur.execute(query)
                    result = cur.fetchall()
                    num_rows = len(result)
                    num_columns = len(result[0])

                    for row in range(num_rows):
                        for column in range(num_columns):
                            item = QTableWidgetItem(str(result[row][column]))
                            self.pat_info_tbl.setItem(row, column, item)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    # showing the appointment history through table
    def app_hist_tbldata(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = 'SELECT PAT_INFO_FNAME, PAT_INFO_LNAME, PAT_INFO_MIDNAME, APP_HIST_DATE, ' \
                            'APP_HIST_TIME, APPOINTMENT_HISTORY.PAT_ID, APPOINTMENT_HISTORY.ADMIN_ID ' \
                            'FROM NEW_PATIENT, APPOINTMENT_HISTORY WHERE APPOINTMENT_HISTORY.PAT_ID = ' \
                            'NEW_PATIENT.PAT_ID'

                    cur.execute(query)
                    result = cur.fetchall()
                    num_rows = len(result)
                    num_columns = len(result[0])

                    for row in range(num_rows):
                        for column in range(num_columns):
                            item = QTableWidgetItem(str(result[row][column]))
                            self.app_hist_tbl.setItem(row, column, item)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    def app_made_table(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = 'SELECT APP_ID, APP_FNAME, APP_LNAME, APP_MIDNAME, APP_DATE, APP_TIME, ' \
                            'PAT_ID FROM APPOINTMENT_MADE'

                    cur.execute(query)
                    result = cur.fetchall()
                    num_rows = len(result)
                    num_columns = len(result[0])

                    for row in range(num_rows):
                        for column in range(num_columns):
                            item = QTableWidgetItem(str(result[row][column]))
                            self.app_made_tbl.setItem(row, column, item)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    # deactivating admins account
    def acc_deactivate(self):
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    my_user = self.login.Userlbl.text()
                    my_pass = self.login.Passlbl.text()

                    update = 'UPDATE ADMIN_STAFF SET DEACTIVATE = 1 WHERE ADMIN_UNAME = %s AND ADMIN_PASS = %s'
                    update_val = (my_user, my_pass)

                    cur.execute(update, update_val)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                self.SIGN_OUT()

    # deleting a row from ongoing appointments table
    def delete_row(self):
        conn = None

        selected_row = self.tableWidget.currentRow()
        app_id = self.tableWidget.item(selected_row, 0).text()
        self.tableWidget.removeRow(selected_row)

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = f"DELETE FROM ON_GOING_APPOINTMENT WHERE PAT_ID = '{app_id}';"
                    cur.execute(query)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    # deleting a row from patient's information table
    def delete_pat_info(self):
        conn = None
        selected_row = self.pat_info_tbl.currentRow()
        app_id = self.pat_info_tbl.item(selected_row, 0).text()

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = f"DELETE FROM NEW_PATIENT WHERE PAT_ID = '{app_id}';"
                    cur.execute(query)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                self.pat_info_tbl.removeRow(selected_row)

    # deleting a row from appointment history table
    def delete_app_hist(self):
        conn = None
        selected_row = self.app_hist_tbl.currentRow()
        app_id = self.app_hist_tbl.item(selected_row, 5).text()
        app_date = self.app_hist_tbl.item(selected_row, 3).text()

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = f"DELETE FROM APPOINTMENT_HISTORY WHERE PAT_ID = '{app_id}' AND " \
                            f"APP_HIST_DATE = '{app_date}';"
                    cur.execute(query)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                self.app_hist_tbl.removeRow(selected_row)

    # re-scheduling page
    def rescheduling(self):
        conn = None
        time = self.resched_time.time()
        myresched = self.resched_date.text()
        format_time = time.toString("h:mm:ss")
        selected_row = self.tableWidget.currentRow()
        app_id = self.tableWidget.item(selected_row, 0).text()
        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:
                    query = f"UPDATE ON_GOING_APPOINTMENT SET APPOINTMENT_DATE = %s, " \
                            f"APPOINTMENT_TIME = %s WHERE PAT_ID = %s"
                    query_values = (myresched, format_time, app_id)
                    cur.execute(query, query_values)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                self.on_on_going_appointments_clicked()

    # an action everytime I pressed the done appointment button
    def done_appointment(self):
        selected_row = self.tableWidget.currentRow()
        app_id = self.tableWidget.item(selected_row, 0).text()
        conn = None

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pword,
                    port=self.port_id) as conn:
                with conn.cursor() as cur:

                    query2 = f"DELETE FROM ON_GOING_APPOINTMENT WHERE PAT_ID = '{app_id}';"
                    cur.execute(query2)

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                self.tableWidget.removeRow(selected_row)
                self.on_dashboardBTN_clicked()

    def show_password(self):
        if self.sender().isChecked() is True:
            self.admin_pword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.admin_pword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def SIGN_OUT(self):
        self.admin_name.clear()
        self.hide()  # hide main window
        self.doLogin()  # show login
        self.show()
        self.admin_name.setText(self.login.Userlbl.text())

    def doLogin(self):
        self.login = Login_Window()
        if self.login.exec() != QDialog.accepted:
            self.close()


app = QApplication(sys.argv)
with open("Login.css", "r") as file:
    app.setStyleSheet(file.read())
with open("DBstyle.css", "r") as file:
    app.setStyleSheet(file.read())

win = DB_Window()
sys.exit(app.exec())
