import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime
from openpyxl import load_workbook
import csv

# Define the MAAS questions 
questions = [
    " میتوانم بعضی از هیجانات را تجربه کنم درحالی که نسبت به آنها آگاه نباشم و بعداً این آگاهی را پیدا کنم.",
    "بسیاري از کارها را به دلیل بی دقتی، عدم توجه و یا فکر کردن به مسائل دیگر از قلم می اندازم.",
    "تمرکز بر روي آنچه در حال حاضر برایم اتفاق میافتد مشکل است.",
    "تمایل دارم براي رسیدن به جایی با سرعت حرکت کنم بدون اینکه در طول راه به آنچه اتفاق میافتد توجه داشته باشم.",
    "تمایل ندارم به تنش ها و یا ناراحتی هاي جسمی ساده توجه کنم، مگر اینکه شدت ناراحتی توجه مرا جلب کند.",
    "نام افراد را تقریباً هر زمان که میخواهم در اولین برخورد به کار ببرم، فراموش میکنم.",
    "به نظر میرسد به صورت خودکار و بدون اینکه از آنچه انجام میدهم آگاهی داشته باشم کارهایم را انجام میدهم.",
    "با عجله سراغ فعالیت هایم میروم، بدون اینکه واقعاً به آنها توجه داشته باشم.",
    "آنچنان غرق در هدف میشوم که تمرکز خود را در اقدام براي رسیدن به آن از دست میدهم.",
    "کارها یا وظایفام را به صورت خودکار و بدون اینکه از آنها آگاهی داشته باشم انجام میدهم.",
    "خودم را در حالی که به حرف هاي کسی گوش میدهم و در همان زمان کار دیگري انجام میدهم، میبینم.",
    "به طور ناخواسته به جایی میروم که بعداً از اینکه آنجا رفته ام، تعجب میکنم.",
    "در مورد آینده یا گذشته پریشانی و اشتغال فکري دارم.",
    "کارهایی را بدون اینکه به آنها توجهی داشته باشم انجام میدهم.",
    "غذا (میان وعده) میخورم بدون اینکه از آنچه میخورم، آگاهی داشته باشم."
]


# Response options
options = [
    "1 = تقریبا همیشه",
    "2 = خیلی زیاد",
    "3 = تا حدی زیاد",
    "4 = تا حدی کم",
    "5 = خیلی کم",
    "6 = تقریبا هرگز"
]

responses = [None] * 15
current_question = 0

def save_data(participant_id, responses, total_score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [participant_id, timestamp] + responses + [total_score]
    
    file_path = "MAAS_Responses.csv"
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            headers = ["Participant ID", "Timestamp"] + [f"Q{i}" for i in range(1, 16)] + ["Total Score"]
            writer.writerow(headers)
        
        writer.writerow(data)

def calculate_score(responses):
    total = 0
    for idx, response in enumerate(responses, start=1):
        score = int(response)
        total += score
    #total = total /15
    return total

def submit():
    participant_id = entry_id.get().strip()
    if not participant_id:
        messagebox.showwarning("Input Error", "Please enter Participant ID.")
        return
    if None in responses:
        messagebox.showwarning("Input Error", "Please answer all 15 questions.")
        return
    total_score = calculate_score(responses)
    save_data(participant_id, responses, total_score)
    messagebox.showinfo("Success", f"Responses saved successfully!\nTotal Score: {total_score}")
    root.destroy()

def select_option(value):
    global current_question
    responses[current_question] = value
    btn_next.config(state="normal")
    
def display_question(q_num):
    lbl_question.config(text=f"Q{q_num+1}: {questions[q_num]}")
    selected_option.set(responses[q_num] if responses[q_num] else 0)
    btn_back.config(state="normal" if q_num > 0 else "disabled")
    btn_next.config(state="normal" if responses[q_num] else "disabled")
    submit_btn.config(state="normal" if all(responses) else "disabled")

def back_question():
    global current_question
    current_question -= 1
    display_question(current_question)

def next_question():
    global current_question
    if selected_option.get() == 0:
        messagebox.showwarning("Input Error", "Please select an option before proceeding.")
        return
    if current_question < len(questions) - 1:  # Check if it's not the last question
        current_question += 1
        display_question(current_question)
    else:
        btn_next.config(state="disabled")  # Disable Next button on the last question
        submit_btn.config(state="normal")  

root = tk.Tk()
root.title("MAAS Mindful Attention Awareness Scale")
root.geometry("700x400")

frame_id = tk.Frame(root)
frame_id.pack(pady=10)

lbl_id = tk.Label(frame_id, text="Participant ID:", font=("Arial", 12))
lbl_id.pack(side="left", padx=5)

entry_id = tk.Entry(frame_id, font=("Arial", 12))
entry_id.pack(side="left", padx=5)

frame_question = tk.Frame(root)
frame_question.pack(pady=20)

lbl_question = tk.Label(frame_question, text=f"Q1: {questions[0]}", wraplength=600, justify="left", font=("Arial", 12))
lbl_question.pack()

frame_options = tk.Frame(root)
frame_options.pack(pady=10)

selected_option = tk.IntVar()

radio_buttons = []
for option in options:
    rb = tk.Radiobutton(frame_options, text=option, variable=selected_option, value=options.index(option)+1, font=("Arial", 12), command=lambda: select_option(selected_option.get()))
    rb.pack(anchor="w")
    radio_buttons.append(rb)

# Back and Next Buttons Frame
frame_nav = tk.Frame(root)
frame_nav.pack(pady=10)

btn_back = tk.Button(frame_nav, text="Back", command=back_question, font=("Arial", 12), state="disabled")
btn_back.pack(side="left", padx=10)

btn_next = tk.Button(frame_nav, text="Next", command=next_question, font=("Arial", 12))
btn_next.pack(side="left", padx=10)

submit_btn = tk.Button(root, text="Submit", command=submit, font=("Arial", 12), state="disabled")
submit_btn.pack(pady=10)

display_question(current_question)

root.mainloop()
