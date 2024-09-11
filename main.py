import requests
import mysql.connector
from gtts import gTTS
import pygame
import os
import time
import json
import datetime
import win32print
import win32ui

db_config = {
    "host": "xxx.xxx.xxx.xxx",
    "user": "xx",
    "password": "xx",
    "database": "sak_connect"
}

def con_db():
    return mysql.connector.connect(**db_config)

def get_patient_data():
    try:
        url = "http://localhost:8189/api/smartcard/read?readImageFlag=false"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching patient data: {e}")
        return None

def check_existing_record(pid, cursor):
    check_query = "SELECT pid FROM sak_Q_register WHERE pid = %s AND DATE(service_datetime) = DATE(NOW())"
    cursor.execute(check_query, (pid,))
    return cursor.fetchone()

def insert_patient_data(data, cursor):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_query = """
        INSERT INTO sak_Q_register (pid, ptname, birthDate, sex, service_datetime)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (data["pid"], f"{data['fname']} {data['lname']}", data["birthDate"], data["sex"], current_datetime))

def play_text_to_speech(text):
    tts = gTTS(text, lang="th")
    tts.save("output.mp3")
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def print_receipt(ptname, hn_pt, q_regis, sit, claimCode):
    printer_name = "EPSON TM-T82X Receipt"
    thai_font_name = "Angsana New"
    hprinter = win32print.OpenPrinter(printer_name)
    printer_dc = win32ui.CreateDC()
    printer_dc.CreatePrinterDC(printer_name)

    printer_dc.StartDoc('Sample Document')
    printer_dc.StartPage()

    def print_text(x, y, text, height=70):
        printer_dc.SelectObject(win32ui.CreateFont({"name": thai_font_name, "height": height}))
        printer_dc.TextOut(x, y, text)

    print_text(80, 0, "ศูนย์สุขภาพชุมชนตำบลจักราช", 70)
    print_text(140, 50, "รพ.จักราช", 100)
    print_text(50, 140, ptname, 120)
    print_text(80, 250, f"คิวที่ {q_regis}", 180)
    print_text(80, 400, f"HN: {hn_pt}", 120)
    print_text(20, 500, sit, 60)
    print_text(80, 550, f"AUTHEN Code: {claimCode}", 60)
    print_text(100, 620, f"**** {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ****", 60)

    printer_dc.EndPage()
    printer_dc.EndDoc()
    win32print.ClosePrinter(hprinter)

def handle_patient_data(data):
    try:
        connection = con_db()
        cursor = connection.cursor()

        if check_existing_record(data["pid"], cursor):
            print(f"Record with PID {data['pid']} already exists.")
        else:
            print(f"Booking queue for {data['fname']} {data['lname']}")
            insert_patient_data(data, cursor)
            connection.commit()

            ptname = f"คุณ {data['fname']} {data['lname']}"
            name = f"{ptname} ระบบกำลังทำงาน กรุณารอสักครู่ค่ะ"
            play_text_to_speech(name)

            # Additional code to handle auth and printing
            # Assuming we get hn_pt, q_regis, sit, claimCode from some logic
            hn_pt = "123456"
            q_regis = "5"
            sit = data["subInscl"]
            claimCode = "AUTH123"

            print_receipt(ptname, hn_pt, q_regis, sit, claimCode)
            print("Data saved and printed successfully.")
            
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    pygame.mixer.init()
    polling_interval = 5  # seconds

    while True:
        patient_data = get_patient_data()
        if patient_data:
            handle_patient_data(patient_data)
        else:
            print("No valid data received.")
        
        time.sleep(polling_interval)

if __name__ == "__main__":
    main()
