# Lift-elevator-simulation
🚀 Elevator Simulation (Python + Tkinter)

A fully functional Animated Elevator (Lift) Simulation built using Python and Tkinter.
This project demonstrates how core data structures (Queue, Stack, Linked List) can be used to simulate a real-world elevator system with scheduling algorithms.

📌 Project Overview

This simulation models a lift inside a building with 8 floors (0–7).
The elevator processes requests using the SCAN algorithm (also known as the Elevator Scheduling Algorithm).
The lift moves up and down with smooth animation, and supports:

Adding floor requests

Upward and downward request queues

Step-by-step movement animation

Request history tracking using a stack

Route logging using a linked list

Automatic or manual processing of tasks

🧠 Data Structures Used

The main purpose of this project is to demonstrate how Data Structures can be applied in real-world simulations.

⭐ 1. Up Queue (Ascending Priority Queue)

Type: Sorted List (acts as a Queue)
Used For: Requests above the current floor.

Example:

self.up_queue = sorted(set(self.up_queue))


📌 Why this DS?

Requests must be served in the smallest-to-largest order while going up.

Sorted list ensures nearest floor above is served first.

Works like a min-priority queue.

⭐ 2. Down Queue (Descending Priority Queue)

Type: Sorted List (descending order)
Used For: Requests below the current floor.

self.down_queue = sorted(set(self.down_queue), reverse=True)


📌 Why this DS?

When moving down, elevator must serve the closest lower floor first.

Sorted list (reverse) acts like a max-priority queue.

⭐ 3. History Stack

Type: Python List (LIFO)
Used For: Storing order of requests, last-request-first view.

self.history_stack.append(request)


📌 Why a Stack?

Perfect for showing recent requests first.

Useful in debugging & for viewing the request pattern.

Stack is a classic DS to represent backtracking and user request trace.

⭐ 4. Route Log (Linked List Behavior)

Type: Python List
Used For: Storing the entire movement path of the elevator.

self.route_log.append(floor)


📌 Why Linked List style?

Every movement step is appended sequentially.

Behaves like a singly linked list where each node represents a movement event.

Excellent for simulation histories and traversal outputs.

⭐ 5. State Variables (Part of Simulation DS)

Along with DS above, the simulation uses:

current_floor

direction (1 = up, -1 = down)

target_floor

These maintain elevator state and help run the scheduling algorithm correctly.

🔄 Scheduling Algorithm (SCAN / Elevator Algorithm)

SCAN algorithm ensures:

Elevator completes all requests in current direction

Then reverses direction

Prevents unnecessary movement

Minimizes waiting time

Typical behavior:

If going down from 7 with requests [5, 2]:
It goes 7 → 5 → 2 (correct order)

If going up from 2 with [4, 6]:
It goes 2 → 4 → 6

The DS used (sorted queues) helps achieve this behavior cleanly.

🎨 GUI + Animation

The GUI uses:

Tkinter Canvas

A rectangle representing the elevator

Smooth pixel-by-pixel animation

Buttons for interaction

Real-time text logs

Example animation logic:

self.canvas.move(self.lift, 0, step)
self.root.after(25, move)

📂 Folder Structure
/elevator-simulation
│── animated_elevator.py
│── README.md
│── requirements.txt  (optional)
│── screenshots/      (optional)
└── assets/            (optional)

▶️ How to Run
python animated_elevator.py


Python 3.8+ recommended.
Tkinter is required (pre-installed with Python on Windows & Linux).

🧪 Example Features

✔ Add Request: Adds a floor into Up/Down queue
✔ Process Next: Runs SCAN and moves lift
✔ Auto Process: Serves all pending requests
✔ Show Status: Displays queues and current floor
✔ Show Request History: Uses Stack
✔ Show Route Log: Uses Linked List

🎓 Why This Project Is Excellent for BTech / MCA / Diploma

Uses multiple data structures in a real-world scenario

Shows algorithmic decision-making (SCAN)

Includes GUI + animation, which impresses evaluators

Perfect for OOP + DS + Python subjects

Very viva-friendly

⭐ Future Enhancements

You can extend the project by adding:

Multiple elevators

Door opening animation

Load balancing

Up/Down call buttons on each floor

Saving logs to a file

Sound effects
