import cv2
import csv
import time
import tkinter as tk
import RPi.GPIO as GPIO
from ultralytics import YOLO
from tkinter import messagebox

buzzer_pin = 17
gled_pin = 22
rled_pin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(gled_pin, GPIO.OUT)
GPIO.setup(rled_pin, GPIO.OUT)
frame_skip = 5
frame_count = 0

max_cap = None
model = YOLO("yolov8n.pt")  

cap = cv2.VideoCapture(0)

log_file = "people_log.csv"

def get_capacity():
    global max_cap
    user_input = entry.get()
    try:
        max_cap = int(user_input)
        root.destroy()
    except ValueError:
        messagebox.showerror("Invalid Input","Enter Valid Number")

root = tk.Tk()
root.title("Set People Capacity")
root.geometry("300x150")

tk.Label(root, text="Enter Max People Capacity:").pack(pady=5)
entry = tk.Entry(root,width = 10)
entry.pack(pady=5)

btn_submit = tk.Button(root, text="Submit", command=get_capacity)
btn_submit.pack(pady=10)

root.mainloop()

try:
    with open(log_file, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "People Count"])
except FileExistsError:
    pass  

prev_count = None  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count+=1

    results = model(frame,imgsz=320)

    if frame_count%frame_skip!=0:
        continue

    person_count = 0
    for result in results:
        for box in result.boxes:
            if box.cls == 0:  
                person_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Person", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if person_count > max_cap:
        GPIO.output(buzzer_pin, GPIO.HIGH)
        GPIO.output(rled_pin, GPIO.HIGH)
        GPIO.output(gled_pin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(buzzer_pin, GPIO.LOW)
        GPIO.output(rled_pin, GPIO.HIGH)
    else:
        GPIO.output(buzzer_pin, GPIO.LOW)
        GPIO.output(gled_pin, GPIO.HIGH)
        GPIO.output(rled_pin, GPIO.LOW)

    cv2.putText(frame, f"People Count: {person_count}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if person_count != prev_count:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, person_count])
        print(f"Logged: {timestamp}, Count: {person_count}")
        prev_count = person_count 

    cv2.imshow("People Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()