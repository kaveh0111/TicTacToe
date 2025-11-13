import tkinter as tk

class App(tk.Tk):
    def __init__(self, target=50):
        super().__init__()
        self.title("Loop demo")
        self.count, self.target = 0, target
        self.running, self.stopped = True, False

        self.lbl = tk.Label(self, text="count: 0"); self.lbl.pack(padx=10, pady=10)
        tk.Button(self, text="Pause",  command=self.pause).pack(side="left", padx=5)
        tk.Button(self, text="Resume", command=self.resume).pack(side="left", padx=5)
        tk.Button(self, text="Stop",   command=self.stop).pack(side="left", padx=5)

        self.step_loop()  # kick off

    def pause(self):  self.running = False
    def resume(self): self.running = True
    def stop(self):   self.stopped = True

    def step_loop(self):
        if not self.stopped and self.count < self.target:
            if self.running:
                # one small, interruptible unit of work
                self.count += 1
                self.lbl.config(text=f"count: {self.count}")
            # reschedule quickly; keeps UI responsive and allows pausing
            self.after(50, self.step_loop)
        else:
            self.lbl.config(text="done")

if __name__ == "__main__":
    App().mainloop()
