import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime

# the ACS-20 questions and reverse scoring
questions = [
    " وقتی صداهایی در اطراف وجود دارد برایم خیلی سخت است که روی یک کار دشوار تمرکز کنم",
    "وقتی نیاز به تمرکز و حل یک مسئله دارم، در تمرکز حواس با مشکل مواجه می‌شوم.",
    "وقتی خیلی سخت مشغول کار هستم به دلیل اتفاقاتی که در اطرافم می‌گذرد همچنان حواسم پرت می‌شود.",
    "تمركز من حتی اگر صدای موسیقی در اتاق و اطرافم باشد، خوب است.",
    "وقتی‌که تمرکز می‌کنم می‌توانم توجه ام را متمرکز کنم و ازآنچه در اطرافم می‌گذرد اطلاعی نداشته باشم.",
    "وقتی‌که مشغول مطالعه کتاب با درس خواندن هستم صحبت‌های دیگران که در اتاق من هستند خیلی راحت حواسم را پرت می‌کند.",
    "وقتی‌که سعی می‌کنم بر روی کاری تمرکز کنم در تفکیک کردن افکار مزاحم از موضوع کارم مشکل‌دارم.",
    "وقتی‌که در مورد موضوعی هیجان‌زده می‌شوم تمرکز کردن برایم سخت می‌شود.",
    "وقتی‌که متمرکز می‌شوم احساس گرسنگی و تشنگی را نادیده می‌گیرم.",
    "جابجا کردن توجه از یک کار به کار دیگر، برایم راحت است.",
    "مدت‌زمانی طول می‌کشد تا مشغول یک کار جدیدی شوم.",
    "برای من دشوار است که در طول سخنرانی به‌طور هم‌زمان گوش کنم و یادداشت بردارم.",
    "در صورت نیاز می‌توانم خیلی سریع به موضوع جدیدی علاقه‌مند شوم.",
    "وقتی‌که مشغول صحبت با تلفن هستم نوشتن و یا خواندن برایم آسان است.",
    "شرکت در دو مکالمه هم‌زمان برایم سخت است.",
    "رسیدن به ایده‌های جدید در مدت‌زمان کوتاه برایم سخت است.",
    "بعد از متوقف شدن و با پرت شدن حواسم، می‌توانم به‌راحتی توجهم را به کاری که مشغولش بودم بازگردانم.",
    "وقتی‌که افکار مزاحم به سراغ من می‌آیند توجه نکردن به آن‌ها، برایم کار آسانی است.",
    "جابه‌جا شدن بین دو فعالیت متفاوت برایم آسان است.",
    "برایم سخت است که نحوه تفکرم نسبت به یک موضوع را تغییر دهم یا به همان موضوع از زاویه دیگری نگاه کنم."
]

# Items with reverse scoring
reverse_scored_items = [1, 2, 3, 6, 7, 8, 9, 11, 12, 15, 16, 20]

options = [
    "1 = تقريبا هيچ وقت",
    "2 = برخي اوقات",
    "3 = اکثر اوقات",
    "4 = هميشه"
]

# Initialize responses list with None to track unanswered questions
responses = [None] * 20
current_question = 0

def save_data(participant_id, responses, total_score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [participant_id, timestamp] + responses + [total_score]
    
    file_path = "ACS20_Responses.csv"
    
    if not os.path.exists(file_path):
        headers = ["Participant ID", "Timestamp"] + [f"Q{i}" for i in range(1, 21)] + ["Total Score"]
        df = pd.DataFrame([data], columns=headers)
        df.to_csv(file_path, index=False)
    else:
        df = pd.DataFrame([data])
        df.to_csv(file_path, mode='a', header=False, index=False)

def calculate_score(responses):
    total = 0
    for idx, response in enumerate(responses, start=1):
        score = int(response)
        if idx in reverse_scored_items:
            score = 5 - score  # Reverse scoring
        total += score
    return total

def submit():
    participant_id = entry_id.get().strip()
    if not participant_id:
        messagebox.showwarning("Input Error", "Please enter Participant ID.")
        return
    if None in responses:
        messagebox.showwarning("Input Error", "Please answer all 20 questions.")
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
        btn_next.config(state="disabled")  
        submit_btn.config(state="normal")  

# Initialize main window
root = tk.Tk()
root.title("ACS-20 Attention Control Scale")
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
