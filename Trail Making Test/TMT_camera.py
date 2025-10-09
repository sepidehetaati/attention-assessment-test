from tkinter import *
import datetime
import time
import threading
import cv2  
import math
import pandas as pd
import matplotlib.pyplot as plt
import os

class VideoRecorder:
    def __init__(self, filename, fps=30.0, resolution=(640, 480), img_folder=""):
        self.filename = filename
        self.fps = fps
        self.resolution = resolution
        self.recording = False
        self.out = None
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.img_folder = img_folder
        self.frame_count = 0

        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.filename, fourcc, self.fps, self.resolution)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.thread = threading.Thread(target=self.record)
            self.thread.start()
            print(f"Started recording: {self.filename}")

    def record(self):
        while self.recording:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)
                # cv2.imwrite(f'{self.filename}.png', frame)
                img_filename = os.path.join(self.img_folder, f"frame_{self.frame_count:04d}.jpg")
                cv2.imwrite(img_filename, frame)
                self.frame_count += 1
            else:
                print("Failed to grab frame")
                break
            # Small sleep to prevent high CPU usage
            time.sleep(1 / self.fps)

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.thread.join()
            self.out.release()
            print(f"Stopped recording: {self.filename}")

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

class Subject:
    def __init__(self):
        self.info = Label(root, text="'Esc' to exit at any time")
        self.info.pack()
        self.frame = Frame(root, bd=2, relief=GROOVE)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        id_label = Label(self.frame, text="Id")
        id_label.grid(row=0, column=0, sticky=E)
        self.id = Entry(self.frame)
        self.id.insert(END, 'test')
        self.id.grid(row=0, column=1)

        gender_label = Label(self.frame, text="Gender")
        gender_label.grid(row=1, column=0, sticky=E)
        self.gender = Entry(self.frame)
        self.gender.insert(END, 'F')
        self.gender.grid(row=1, column=1)

        age_label = Label(self.frame, text="Age")
        age_label.grid(row=2, column=0, sticky=E)
        self.age = Entry(self.frame)
        self.age.insert(END, '20')
        self.age.grid(row=2, column=1)

        trail_label = Label(self.frame, text="Trail")
        trail_label.grid(row=3, column=0, sticky=E)
        self.trail = Entry(self.frame)
        self.trail.insert(END, 'default')
        self.trail.grid(row=3, column=1)

        condition_label = Label(self.frame, text="Condition")
        condition_label.grid(row=4, column=0, sticky=E)
        self.condition = Entry(self.frame)
        self.condition.insert(END, '0')
        self.condition.grid(row=4, column=1)

        submit_button = Button(self.frame, text="Submit")
        submit_button.bind('<ButtonPress-1>', self.submit)
        submit_button.grid(columnspan=2)
        submit_button.focus_set()

    def submit(self, event):
        global level, node_pos_i, trail_input, recorder
        level = 0
        node_pos_i = 0
        self.ID = self.id.get()
        self.GENDER = self.gender.get()
        self.AGE = self.age.get()
        self.CONDITION = self.condition.get()
        self.DATE = datetime.datetime.now().strftime("%Y-%m-%d")
        self.trail_input = self.trail.get()
        os.makedirs(f'./{self.ID}', exist_ok=True)
        self.frame.destroy()
        self.info.destroy()
        with open(f'./{self.ID}/{self.ID}.csv', "w") as F:
            F.write("Id,Gender,Age,Date,Trail,Condition,Level,Tag,Time,Correct\n")
        read_trail_input(self.trail_input)
        reset_canvas()
        message(messages[level])

class Node:
    def __init__(self, x, y, tag):
        self.circle = canvas.create_oval(x, y, x + node_size, y + node_size, width=1, fill="white")
        self.content = canvas.create_text(x + node_size / 2, y + node_size / 2, fill="black",
                                          font="Times " + str(int(node_size * 0.4)), text=tag)
        self.tag = tag

        canvas.tag_bind(self.circle, '<ButtonPress-1>', self.register)
        canvas.tag_bind(self.content, '<ButtonPress-1>', self.register)

    def register(self, event):
        global node_i, last_click_time
        expected_now = node_sequence[level][node_i]
        current_time = time.time()  

        if last_click_time is None:  
            time_elapsed = 0
        else:
            time_elapsed = current_time - last_click_time  

        last_click_time = current_time 

        if self.tag == expected_now:
            x, y = event.x, event.y
            if canvas.old_coords:
                x1, y1 = canvas.old_coords

                angle = math.atan2(y - y1, x - x1)
                offset_x = (node_size / 2) * math.cos(angle)
                offset_y = (node_size / 2) * math.sin(angle)
                #canvas.create_line(x1 + offset_x, y1 + offset_y, x - offset_x, y - offset_y, fill="green")

            canvas.old_coords = x, y
            canvas.itemconfig(self.circle, outline="green", width=2)  

            with open(f'./{S.ID}/{S.ID}.csv', "a") as F:
                F.write(f"{S.ID},{S.GENDER},{S.AGE},{S.DATE},{S.trail_input},{S.CONDITION},{level},{self.tag},{time_elapsed},{1}\n")

            node_i += 1
        else:
            with open(f'./{S.ID}/{S.ID}.csv', "a") as F:
                F.write(f"{S.ID},{S.GENDER},{S.AGE},{S.DATE},{S.trail_input},{S.CONDITION},{level},{self.tag},{time_elapsed},{0}\n")

        if node_i == len(node_sequence[level]):
            next_level()

def close(event):
    if recorder:
        recorder.stop_recording()
        recorder.release()
    root.destroy()

def read_trail_input(NAME):
    global container_size, node_size, node_sequence, messages, end_message, node_sequence_pos
    with open('cfg/'+NAME) as f:
        lines = f.read().splitlines()
        container_size = [int(lines[0]), int(lines[1])]
        node_size = int(lines[2])
        n_levels = int(lines[3])

        node_sequence = []
        for l in lines[4:4 + n_levels]:
            node_sequence.append(l.split(" "))

        messages = []
        for l in lines[4 + n_levels:4 + 2 * n_levels]:
            messages.append(l.replace('\\n', '\n'))

        end_message = lines[4 + 2 * n_levels].replace('\\n', '\n')

        node_sequence_pos = []
        for l in lines[4 + 2 * n_levels + 2:]:
            node_sequence_pos.append(list(map(int, l.split(" "))))

def place_container():
    midW = root.winfo_screenwidth()/2
    midH = root.winfo_screenheight()/2
    x0 = midW - container_size[0]/2
    y0 = midH - container_size[1]/2
    x1 = midW + container_size[0]/2
    y1 = midH + container_size[1]/2
    canvas.create_rectangle(x0, y0, x1, y1)

def place_nodes():
    global node_pos_i
    for i, tag in enumerate(node_sequence[level]):
        x = node_sequence_pos[node_pos_i][0]
        y = node_sequence_pos[node_pos_i][1]
        node_instance = Node(x, y, tag)

        if i == 0:
            canvas.create_text(x + node_size / 2, y - node_size / 2, fill="black", font="Times 12 bold", text="Start")

        if i == len(node_sequence[level]) - 1:
            canvas.create_text(x + node_size / 2, y - node_size / 2, fill="black", font="Times 12 bold", text="End")

        node_pos_i += 1

def reset_canvas():
    global canvas
    canvas = Canvas(root)
    canvas.delete("all")
    canvas.config(background="white")
    canvas.focus_set()
    canvas.pack(fill='both', expand=True)

def message(msg):
    canvas.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight()/2, fill="black", font="Times 16",
                       justify=CENTER, text=msg)
    canvas.bind('<space>', start)

def start(event):
    global node_i, start_time, last_click_time, recorder
    canvas.unbind('<space>')
    canvas.delete("all")
    node_i = 0
    last_click_time = None
    place_container()
    place_nodes()
    canvas.old_coords = None
    start_time = time.time()

    trial_folder = f'./{S.ID}/trial_{level}'
    os.makedirs(trial_folder, exist_ok=True)

    img_folder = os.path.join(trial_folder, "frames")
    os.makedirs(img_folder, exist_ok=True)

    # Initialize and start video recording
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"{trial_folder}/{S.ID}_trial_{level}_{timestamp}.avi"
    recorder = VideoRecorder(video_filename, fps=30.0, resolution=(640, 480), img_folder=img_folder)
    recorder.start_recording()

    canvas.bind('<Motion>', track_mouse_movement)
    canvas.bind('<ButtonPress-1>', track_mouse_click)

trial_mouse_data = {}
recorder = None  # Initialize recorder variable
last_click_time = None

def track_mouse_movement(event):
    trial_mouse_data.setdefault(level, []).append({'x': event.x, 'y': event.y, 'time': time.time(), 'type': 'move'})

def track_mouse_click(event):
    trial_mouse_data.setdefault(level, []).append({'x': event.x, 'y': event.y, 'time': time.time(), 'type': 'click'})

def save_mouse_data(level):
    trial_folder = f'./{S.ID}/trial_{level}'
    mouse_data_file = f"{trial_folder}/mouse_data.xlsx"
    df = pd.DataFrame(trial_mouse_data[level])
    df.to_excel(mouse_data_file, index=False)
    print(f"Mouse data for trial {level} saved to {mouse_data_file}")

def plot_and_save_mouse_path(level):
    trial_folder = f'./{S.ID}/trial_{level}'
    x = [data['x'] for data in trial_mouse_data[level]]
    y = [data['y'] for data in trial_mouse_data[level]]
    clicks_x = [data['x'] for data in trial_mouse_data[level] if data['type'] == 'click']
    clicks_y = [data['y'] for data in trial_mouse_data[level] if data['type'] == 'click']

    # Ensure node positions are correctly sliced for each level
    start_pos = sum(len(seq) for seq in node_sequence[:level])
    end_pos = start_pos + len(node_sequence[level])
    node_positions = node_sequence_pos[start_pos:end_pos]

    node_x = [pos[0] + node_size / 2 for pos in node_positions]
    node_y = [pos[1] + node_size / 2 for pos in node_positions]

    plt.figure(figsize=(10, 8))
    plt.plot(x, y, linestyle='-', color='b', label='Movement')
    plt.scatter(clicks_x, clicks_y, color='r', label='Clicks')
    plt.scatter(node_x, node_y, color='w', label='Nodes', marker='o', s=50)  

    for i, (nx, ny) in enumerate(zip(node_x, node_y)):
        plt.text(nx, ny, node_sequence[level][i], fontsize=18, ha='center', va='center', color='black')

    if x and y:  
        plt.scatter(x[0], y[0], color='magenta', label='Start', s=50, edgecolors='black', marker='o')  # Start position
        plt.text(x[0], y[0], 'Start', fontsize=12, ha='right', va='bottom', color='magenta')

        plt.scatter(x[-1], y[-1], color='magenta', label='End', s=50, edgecolors='black', marker='o')  # End position
        plt.text(x[-1], y[-1], 'End', fontsize=12, ha='right', va='top', color='magenta')

    plt.title(f'Trial {level} Mouse Path')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.savefig(f"{trial_folder}/mouse_path.png")
    plt.close()  # Close the plot to free memory

def next_level():
    global level, recorder
    # Stop video recording for the current trial
    if recorder:
        recorder.stop_recording()
        recorder = None

    save_mouse_data(level)  
    plot_and_save_mouse_path(level)  

    level += 1
    if level == len(node_sequence):
        canvas.destroy()
        reset_canvas()
        message(end_message)
        canvas.unbind('<space>')
        canvas.bind('<space>', close)
    else:
        canvas.destroy()
        reset_canvas()
        message(messages[level])

def leave_to_questionnaire(event):
    if recorder:
        recorder.stop_recording()
        recorder.release()
    root.destroy()	

# Initialize Tkinter root
root = Tk()
root.title("TMT")
root.attributes('-fullscreen', True)

root.bind('<Escape>', close)

# Initialize subject information
S = Subject()

root.mainloop()
