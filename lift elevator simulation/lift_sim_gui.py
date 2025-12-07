import tkinter as tk
from tkinter import ttk, messagebox


class Elevator:
    def __init__(self):
        self.current_floor = 0
        self.up_queue = []       # ascending sorted unique floors > current
        self.down_queue = []     # descending sorted unique floors < current
        self.history_stack = []
        self.route_log = [0]
        self.direction = 1       # start by going up by default (1 = up, -1 = down)

    # -----------------------------------------
    # ADD REQUEST
    # -----------------------------------------
    def add_request(self, floor):
        if floor == self.current_floor:
            # immediate service (could be logged)
            self.history_stack.append(floor)
            return f"Already at floor {floor} (served)."

        self.history_stack.append(floor)

        if floor > self.current_floor:
            if floor not in self.up_queue:
                self.up_queue.append(floor)
                self.up_queue = sorted(self.up_queue)
        else:
            if floor not in self.down_queue:
                self.down_queue.append(floor)
                self.down_queue = sorted(self.down_queue, reverse=True)

        # Optionally set direction toward the nearest request if currently idle
        if not self.up_queue and not self.down_queue:
            self.direction = 1
        else:
            # If elevator is idle and new request is only on one side, prefer that side
            if not self.up_queue:
                self.direction = -1
            elif not self.down_queue:
                self.direction = 1

        return f"Request {floor} added."

    # -----------------------------------------
    # GET NEXT REQUEST (SCAN-aware)
    # -----------------------------------------
    def get_next_request(self):
        """
        Choose next floor using SCAN:
        - If there are requests in current direction, pick the closest in that direction.
        - Else reverse direction and pick closest there.
        - Return None if no requests.
        """
        if not (self.up_queue or self.down_queue):
            return None

        # If current direction is UP
        if self.direction == 1:
            # pick smallest up request > current_floor
            ups_above = [f for f in self.up_queue if f > self.current_floor]
            if ups_above:
                next_floor = ups_above[0]
                self.up_queue.remove(next_floor)
                return next_floor
            # no ups ahead -> try downs (reverse)
            downs_below = [f for f in self.down_queue if f < self.current_floor]
            if downs_below:
                # reverse direction
                self.direction = -1
                next_floor = downs_below[0]  # down_queue sorted descending, 0 is largest below current
                self.down_queue.remove(next_floor)
                return next_floor
            # special cases: maybe up_queue has values <= current_floor (edge); handle generically
            if self.up_queue:
                # choose the nearest (could be below) by absolute distance
                nearest = min(self.up_queue, key=lambda x: abs(x - self.current_floor))
                self.up_queue.remove(nearest)
                # set direction towards it
                self.direction = 1 if nearest > self.current_floor else -1
                return nearest

        # If current direction is DOWN
        if self.direction == -1:
            downs_below = [f for f in self.down_queue if f < self.current_floor]
            if downs_below:
                next_floor = downs_below[0]
                self.down_queue.remove(next_floor)
                return next_floor
            # no downs ahead -> try ups (reverse)
            ups_above = [f for f in self.up_queue if f > self.current_floor]
            if ups_above:
                self.direction = 1
                next_floor = ups_above[0]
                self.up_queue.remove(next_floor)
                return next_floor
            # fallback: pick nearest in down_queue if any
            if self.down_queue:
                nearest = min(self.down_queue, key=lambda x: abs(x - self.current_floor))
                self.down_queue.remove(nearest)
                self.direction = 1 if nearest > self.current_floor else -1
                return nearest

        return None


# ============================================================
#                GUI + CANVAS ANIMATED LIFT
# ============================================================
class ElevatorGUI:
    FLOOR_COUNT = 8
    FLOOR_HEIGHT = 70
    CANVAS_HEIGHT = FLOOR_COUNT * FLOOR_HEIGHT + 20
    LIFT_SPEED = 10  # pixels per frame

    def __init__(self):
        self.ev = Elevator()

        self.root = tk.Tk()
        self.root.title("Animated Elevator Simulation (Fixed SCAN logic)")
        width = 900
        height = self.CANVAS_HEIGHT + 40
        self.root.geometry(f"{width}x{height}")

        self.setup_ui()
        self.draw_building()
        self.root.mainloop()

    # -------------------------------------------------------
    # GUI Setup
    # -------------------------------------------------------
    def setup_ui(self):
        left = ttk.Frame(self.root, padding=8)
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Enter Floor (0–7):").pack(anchor="w")
        self.floor_entry = ttk.Entry(left, width=10)
        self.floor_entry.pack(pady=6, anchor="w")

        ttk.Button(left, text="Add Request", command=self.add_request_gui).pack(fill="x", pady=4)
        ttk.Button(left, text="Process Next Request", command=self.process_gui).pack(fill="x", pady=4)
        ttk.Button(left, text="Auto-Process All", command=self.auto_process_all).pack(fill="x", pady=4)
        ttk.Button(left, text="Show Status", command=self.status_gui).pack(fill="x", pady=4)
        ttk.Button(left, text="Show Request History", command=self.history_gui).pack(fill="x", pady=4)
        ttk.Button(left, text="Show Route Log", command=self.route_gui).pack(fill="x", pady=4)

        # Output box
        self.output = tk.Text(left, width=45, height=20, state="disabled")
        self.output.pack(pady=8)

        # Canvas (animation area)
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side="right", padx=10)
        self.canvas = tk.Canvas(canvas_frame, width=400, height=self.CANVAS_HEIGHT, bg="white")
        self.canvas.pack()

    # -------------------------------------------------------
    # Drawing building + lift
    # -------------------------------------------------------
    def draw_building(self):
        self.canvas.delete("all")
        # Draw floors top->bottom
        for i in range(self.FLOOR_COUNT):
            y = 10 + i * self.FLOOR_HEIGHT
            self.canvas.create_rectangle(50, y, 350, y + self.FLOOR_HEIGHT, outline="gray")
            floor_label = self.FLOOR_COUNT - 1 - i
            self.canvas.create_text(30, y + self.FLOOR_HEIGHT / 2, text=f"F{floor_label}", font=("Arial", 10))

        # Lift rectangle placed at current floor
        self.lift_width = 80
        self.lift_height = 50
        self._place_lift_on_canvas(self.ev.current_floor, instant=True)

    def _y_for_floor(self, floor):
        # convert floor number (0..F-1) to canvas y (top coordinate)
        row = self.FLOOR_COUNT - 1 - floor
        return 10 + row * self.FLOOR_HEIGHT + (self.FLOOR_HEIGHT - self.lift_height) / 2

    def _place_lift_on_canvas(self, floor, instant=False):
        x_left = 120
        y_top = self._y_for_floor(floor)
        x_right = x_left + self.lift_width
        y_bottom = y_top + self.lift_height
        if hasattr(self, "lift"):
            if instant:
                self.canvas.coords(self.lift, x_left, y_top, x_right, y_bottom)
                self.canvas.coords(self.lift_text, x_left + self.lift_width / 2, y_top + self.lift_height / 2)
            else:
                self.canvas.coords(self.lift, x_left, y_top, x_right, y_bottom)
                self.canvas.coords(self.lift_text, x_left + self.lift_width / 2, y_top + self.lift_height / 2)
        else:
            self.lift = self.canvas.create_rectangle(x_left, y_top, x_right, y_bottom,
                                                     fill="lightblue", outline="black", width=2)
            self.lift_text = self.canvas.create_text(x_left + self.lift_width / 2,
                                                     y_top + self.lift_height / 2,
                                                     text=str(floor), font=("Arial", 12, "bold"))

    # -------------------------------------------------------
    # GUI Button Handlers
    # -------------------------------------------------------
    def add_request_gui(self):
        try:
            floor = int(self.floor_entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid floor number (0–7).")
            return

        if floor < 0 or floor >= self.FLOOR_COUNT:
            messagebox.showerror("Error", "Floor out of range (0–7).")
            return

        msg = self.ev.add_request(floor)
        self.write_output(msg)
        self.update_lift_text()

    def process_gui(self):
        next_floor = self.ev.get_next_request()

        if next_floor is None:
            self.write_output("No pending requests.")
            return

        self.write_output(f"Processing request → {next_floor} (direction={'Up' if self.ev.direction==1 else 'Down'})")
        self.animate_elevator(next_floor)

    def auto_process_all(self):
        # sequentially process all requests with animation
        if not (self.ev.up_queue or self.ev.down_queue):
            self.write_output("No pending requests to auto-process.")
            return

        def step_process():
            nxt = self.ev.get_next_request()
            if nxt is None:
                self.write_output("All requests processed.")
                return
            self.write_output(f"Processing → {nxt}")
            # animate and schedule next step after animation finishes
            self.animate_elevator(nxt, callback=lambda: self.root.after(300, step_process))

        step_process()

    def status_gui(self):
        msg = (
            f"Elevator at floor: {self.ev.current_floor}\n"
            f"Direction: {'Up' if self.ev.direction==1 else 'Down'}\n"
            f"UP Queue: {self.ev.up_queue}\n"
            f"DOWN Queue: {self.ev.down_queue}\n"
        )
        self.write_output(msg)

    def history_gui(self):
        if not self.ev.history_stack:
            self.write_output("History empty.")
            return
        self.write_output("History (latest first): " + " ".join(map(str, reversed(self.ev.history_stack))))

    def route_gui(self):
        self.write_output("Route Taken: " + " → ".join(map(str, self.ev.route_log)))

    # -------------------------------------------------------
    def write_output(self, text):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n\n")
        self.output.config(state="disabled")
        self.output.see("end")

    # -------------------------------------------------------
    # Animation of Lift Movement
    # -------------------------------------------------------
    def animate_elevator(self, target_floor, callback=None):
        # compute pixel coords
        target_y = self._y_for_floor(target_floor)
        current_coords = self.canvas.coords(self.lift)
        current_y = current_coords[1]

        step = -self.LIFT_SPEED if target_y < current_y else self.LIFT_SPEED

        def move():
            nonlocal current_y
            # check completion condition
            if (step < 0 and current_y <= target_y) or (step > 0 and current_y >= target_y):
                # snap to exact position
                self._place_lift_on_canvas(target_floor, instant=True)
                self.ev.current_floor = target_floor
                self.ev.route_log.append(target_floor)
                self.canvas.itemconfigure(self.lift_text, text=str(target_floor))
                self.write_output(f"Reached floor {target_floor}")
                if callback:
                    callback()
                return

            self.canvas.move(self.lift, 0, step)
            self.canvas.move(self.lift_text, 0, step)
            current_y += step
            self.root.after(25, move)

        move()

    def update_lift_text(self):
        # update number on lift
        try:
            self.canvas.itemconfigure(self.lift_text, text=str(self.ev.current_floor))
        except Exception:
            pass


# Run GUI
if __name__ == "__main__":
    ElevatorGUI()
