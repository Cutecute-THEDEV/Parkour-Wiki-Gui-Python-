import os
import sys
import json
import tkinter as tk
from tkinter import ttk
from pynput import keyboard
from cryptography.fernet import Fernet


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

ENCRYPTION_KEY = b"3oix7usglUIRJZ2uHUk0Q2oT856V-SJ1ZHB72OAIqx0="


# ---------------------------------------------------------------------
# Starter parkour encyclopedia
# Add more guides by copying one of these dictionaries.
# ---------------------------------------------------------------------

BUILT_IN_GUIDES = [
    {
        "category": "Basics",
        "title": "Single-Block Sprint Jump",
        "difficulty": "Beginner",
        "color": "#48d597",
        "steps": [
            "Stand close to the edge of the starting block.",
            "Hold W and begin sprinting.",
            "Jump shortly before leaving the edge.",
            "Keep holding W during the jump.",
            "Aim for the center of the target block."
        ],
        "tips": [
            "Do not jump too early.",
            "Keep sprint held until you land.",
            "Avoid changing direction in the air."
        ]
    },
    {
        "category": "Basics",
        "title": "Two-Block Jump",
        "difficulty": "Beginner",
        "color": "#48d597",
        "steps": [
            "Line up directly with the target.",
            "Start sprinting in a straight line.",
            "Jump close to the edge.",
            "Hold W while airborne.",
            "Land near the middle of the target."
        ],
        "tips": [
            "Keep the target near the center of your screen.",
            "Straight jumps are easier than diagonal jumps."
        ]
    },
    {
        "category": "Neos",
        "title": "Single-Block Neo",
        "difficulty": "Intermediate",
        "color": "#ffc857",
        "steps": [
            "Stand at the edge beside the corner.",
            "Face the outside corner of the target block.",
            "Start sprinting toward the edge.",
            "Jump instantly as you leave the edge.",
            "Hold W plus A or D toward the corner.",
            "Wrap your camera around the corner.",
            "Keep the target block near the center of your screen.",
            "Release the sideways key after clearing the corner."
        ],
        "tips": [
            "Use A for a left-side neo.",
            "Use D for a right-side neo.",
            "Jumping too early makes you hit the side.",
            "Jumping too late makes you miss the corner.",
            "Turn your camera smoothly instead of making a huge flick."
        ]
    },
    {
        "category": "Neos",
        "title": "Double Neo",
        "difficulty": "Advanced",
        "color": "#ff8066",
        "steps": [
            "Complete the first neo normally.",
            "Land near the correct edge of the first block.",
            "Keep your sprint momentum.",
            "Immediately line up with the next corner.",
            "Jump from the edge of the first landing block.",
            "Use the opposite strafe direction if necessary.",
            "Wrap your camera around the second corner.",
            "Center your view before landing."
        ],
        "tips": [
            "Practice both neos separately first.",
            "Do not spend too long adjusting between jumps.",
            "The first landing must be properly positioned."
        ]
    },
    {
        "category": "Neos",
        "title": "Triple Neo",
        "difficulty": "Expert",
        "color": "#ff4f68",
        "steps": [
            "Build sprint momentum before the first neo.",
            "Jump around the first corner.",
            "Land close to the next launch edge.",
            "Immediately jump around the second corner.",
            "Keep your camera movement controlled.",
            "Repeat the movement for the third corner.",
            "Aim for the final platform before the last turn."
        ],
        "tips": [
            "Do not stop sprinting between jumps.",
            "Use the same camera rhythm for every corner.",
            "Practice the sequence slowly before attempting full speed."
        ]
    },
    {
        "category": "Sprint Jumps",
        "title": "Four-Block Sprint Jump",
        "difficulty": "Advanced",
        "color": "#ff8066",
        "steps": [
            "Get a full sprint before reaching the edge.",
            "Aim directly at the target.",
            "Jump at the last possible moment.",
            "Hold W throughout the jump.",
            "Keep sprint active.",
            "Avoid turning your camera.",
            "Land near the middle of the target."
        ],
        "tips": [
            "Jumping early reduces your horizontal distance.",
            "A clean straight line is the most consistent setup.",
            "Do not accidentally release sprint."
        ]
    },
    {
        "category": "Sprint Jumps",
        "title": "Diagonal Sprint Jump",
        "difficulty": "Intermediate",
        "color": "#ffc857",
        "steps": [
            "Stand diagonally from the target.",
            "Hold W and A or W and D.",
            "Begin sprinting before reaching the edge.",
            "Jump near the edge of the block.",
            "Keep the target in your peripheral vision.",
            "Correct your direction gently during the jump."
        ],
        "tips": [
            "Do not turn too sharply.",
            "Use small camera adjustments.",
            "Practice both diagonal directions."
        ]
    },
    {
        "category": "Head Hitters",
        "title": "Basic Head-Hitter",
        "difficulty": "Intermediate",
        "color": "#ffc857",
        "steps": [
            "Sprint toward the low ceiling.",
            "Jump shortly before reaching it.",
            "Allow your head to hit the ceiling.",
            "Keep holding W after the collision.",
            "Aim for the far side of the target platform."
        ],
        "tips": [
            "Jumping too early loses momentum.",
            "The ceiling must be low enough to stop your jump.",
            "Keep sprint held throughout the setup."
        ]
    },
    {
        "category": "Head Hitters",
        "title": "Head-Hitter Neo",
        "difficulty": "Advanced",
        "color": "#ff8066",
        "steps": [
            "Approach the low ceiling while sprinting.",
            "Jump into the ceiling near the edge.",
            "Hold W and strafe toward the target corner.",
            "Turn your camera around the corner.",
            "Keep your crosshair on the landing block.",
            "Continue holding forward after clearing the corner."
        ],
        "tips": [
            "The head hit should happen before the corner.",
            "Do not turn the camera too early.",
            "Practice the head-hitter and neo separately first."
        ]
    },
    {
        "category": "Corner Jumps",
        "title": "Corner Wrap",
        "difficulty": "Intermediate",
        "color": "#ffc857",
        "steps": [
            "Approach the corner at sprint speed.",
            "Jump as you reach the edge.",
            "Hold W and strafe toward the corner.",
            "Turn your camera around the corner.",
            "Keep the target platform visible.",
            "Stop turning once the target is directly in front of you."
        ],
        "tips": [
            "Use a smooth camera turn.",
            "Aim slightly beyond the corner during takeoff.",
            "Practice clockwise and counterclockwise versions."
        ]
    },
    {
        "category": "Ladders",
        "title": "Ladder Catch",
        "difficulty": "Advanced",
        "color": "#ff8066",
        "steps": [
            "Jump toward the ladder.",
            "Aim your crosshair at the ladder surface.",
            "Hold the movement key toward the wall.",
            "Press sneak as you approach the ladder.",
            "Grab the ladder before falling."
        ],
        "tips": [
            "Start with a large ladder target.",
            "Do not look away from the ladder.",
            "Practice from a short distance first."
        ]
    },
    {
        "category": "Slime",
        "title": "Slime Bounce Transfer",
        "difficulty": "Advanced",
        "color": "#ff8066",
        "steps": [
            "Land near the center of the slime block.",
            "Keep your camera aimed at the next platform.",
            "Hold forward during the bounce.",
            "Use air strafing to adjust your path.",
            "Prepare to release movement when landing."
        ],
        "tips": [
            "Avoid landing on the slime edge.",
            "Practice the bounce without a target first.",
            "Keep your landing camera stable."
        ]
    },
    {
        "category": "Movement",
        "title": "Momentum Preservation",
        "difficulty": "Technique",
        "color": "#6cb6ff",
        "steps": [
            "Begin sprinting before reaching the edge.",
            "Keep forward input held.",
            "Do not press the opposite movement direction.",
            "Use small air-strafing corrections.",
            "Continue moving forward after landing."
        ],
        "tips": [
            "Stopping sprint before takeoff makes jumps shorter.",
            "Smooth movement is more consistent than rapid key presses.",
            "Land near the middle when setting up another jump."
        ]
    },
    {
        "category": "Movement",
        "title": "Air-Strafe Correction",
        "difficulty": "Technique",
        "color": "#6cb6ff",
        "steps": [
            "Jump while moving forward.",
            "Move your camera slightly toward the target.",
            "Press A or D briefly to adjust your path.",
            "Do not hold the sideways key for the entire jump.",
            "Center your camera before landing."
        ],
        "tips": [
            "Small corrections are safer than constant strafing.",
            "Practice with wide platforms before using neos."
        ]
    },
    {
        "category": "Practice",
        "title": "Ten-Attempt Consistency Drill",
        "difficulty": "Practice",
        "color": "#b187ff",
        "steps": [
            "Choose one jump.",
            "Attempt it ten times without changing the setup.",
            "Record how many attempts succeed.",
            "Change only the jump timing.",
            "Repeat another ten attempts.",
            "Keep the timing with the best success rate."
        ],
        "tips": [
            "Consistency matters more than one lucky completion.",
            "Practice left and right versions separately.",
            "Do not change sensitivity and timing at the same time."
        ]
    },
     {
        "category": "Neos",
        "title": "Triple Neo",
        "difficulty": "Advanced",
        "color": "#ff6b6b",
        "steps": [
            "Stand at the edge beside the first corner.",
            "Face the outside corner of the first target block.",
            "Start sprinting toward the edge.",
            "Jump as you leave the edge and hold W plus A or D.",
            "Wrap your camera around the first corner.",
            "Keep your movement controlled as you clear the first neo.",
            "Immediately line up with the second corner.",
            "Continue sprinting and jump toward the second neo.",
            "Hold W plus A or D and smoothly wrap around the 			second corner.",
            "Adjust your camera toward the final target while maintaining momentum.",
            "Clear the third corner and release the sideways key.",
            "Center your movement over the final block and land."
        ],
        "tips": [
            "Triple neos require consistent timing on all three corners.",
            "Use A for left-side neos and D for right-side neos.",
            "Avoid overcorrecting your camera after each corner.",
            "Keep your crosshair near the next corner before committing to the jump.",
            "Preserve as much horizontal momentum as possible between neos.",
            "Practice each neo individually before attempting all three in a row.",
            "Small camera adjustments are safer than sudden flicks.",
            "Missing the first neo usually means the approach angle was wrong; missing later neos often comes from losing momentum or alignment."
        ]
    },

]


# ---------------------------------------------------------------------
# File and encryption functions
# ---------------------------------------------------------------------

def application_folder():
    """Return the folder containing the script or compiled EXE."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(__file__))


def encrypted_guides_path():
    return os.path.join(application_folder(), "guides.enc")


def load_guides():
    """
    Load encrypted guides.

    On the first run, the built-in guides are encrypted and saved
    to guides.enc. Later runs load the encrypted copy.
    """
    path = encrypted_guides_path()
    cipher = Fernet(ENCRYPTION_KEY)

    if not os.path.exists(path):
        raw_data = json.dumps(
            BUILT_IN_GUIDES,
            indent=2
        ).encode("utf-8")

        encrypted_data = cipher.encrypt(raw_data)

        with open(path, "wb") as file:
            file.write(encrypted_data)

        return BUILT_IN_GUIDES

    try:
        with open(path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode("utf-8"))

    except Exception:
        # If the encrypted file is corrupted, recreate it.
        raw_data = json.dumps(BUILT_IN_GUIDES).encode("utf-8")
        encrypted_data = cipher.encrypt(raw_data)

        with open(path, "wb") as file:
            file.write(encrypted_data)

        return BUILT_IN_GUIDES


# ---------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------

class MinecraftParkourGUI:
    def __init__(self, guides):
        self.guides = guides
        self.visible = False
        self.current_category = "All"
        self.search_text = ""

        self.root = tk.Tk()
        self.root.title("Minecraft Parkour Encyclopedia")
        self.root.geometry("950x700+80+60")
        self.root.minsize(720, 500)
        self.root.configure(bg="#101218")
        self.root.attributes("-topmost", True)

        self.setup_styles()
        self.create_gui()
        self.root.withdraw()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Dark.Vertical.TScrollbar",
            background="#303748",
            troughcolor="#151923",
            bordercolor="#151923",
            arrowcolor="#ffffff"
        )

        style.configure(
            "Category.TButton",
            background="#202532",
            foreground="#c7ccd8",
            padding=(14, 10),
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.map(
            "Category.TButton",
            background=[
                ("active", "#39445a"),
                ("pressed", "#4b5872")
            ],
            foreground=[
                ("active", "white")
            ]
        )

    def create_gui(self):
        # Header
        header = tk.Frame(self.root, bg="#191d29", height=84)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="⟡  PARKOUR ENCYCLOPEDIA",
            bg="#191d29",
            fg="#75e6b1",
            font=("Segoe UI", 21, "bold")
        )
        title.pack(side="left", padx=24)

        subtitle = tk.Label(
            header,
            text="P to hide/show  •  ESC to hide",
            bg="#191d29",
            fg="#8d95a8",
            font=("Segoe UI", 9)
        )
        subtitle.pack(side="left", padx=8)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.search_changed)

        search = tk.Entry(
            header,
            textvariable=self.search_var,
            bg="#292f3d",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 10),
            width=25
        )
        search.pack(side="right", padx=(5, 12), pady=25)

        search_label = tk.Label(
            header,
            text="Search:",
            bg="#191d29",
            fg="#aeb5c5",
            font=("Segoe UI", 10)
        )
        search_label.pack(side="right")

        close_button = tk.Button(
            header,
            text="×",
            command=self.hide,
            bg="#191d29",
            fg="#aeb5c5",
            activebackground="#d94f5c",
            activeforeground="white",
            borderwidth=0,
            font=("Segoe UI", 20),
            width=2
        )
        close_button.pack(side="right", padx=5)

        # Body
        body = tk.Frame(self.root, bg="#101218")
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg="#151923", width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        category_title = tk.Label(
            sidebar,
            text="CATEGORIES",
            bg="#151923",
            fg="#687187",
            font=("Segoe UI", 9, "bold")
        )
        category_title.pack(anchor="w", padx=18, pady=(22, 12))

        categories = ["All"] + sorted({
            guide["category"] for guide in self.guides
        })

        for category in categories:
            button = ttk.Button(
                sidebar,
                text=category,
                style="Category.TButton",
                command=lambda name=category: self.select_category(name)
            )
            button.pack(fill="x", padx=10, pady=3)

        info = tk.Label(
            sidebar,
            text=(
                "\nControls\n"
                "P  Show/hide GUI\n"
                "ESC  Hide GUI\n"
                "Mouse wheel  Scroll\n\n"
                f"{len(self.guides)} guides loaded"
            ),
            justify="left",
            bg="#151923",
            fg="#727b90",
            font=("Segoe UI", 9)
        )
        info.pack(anchor="w", padx=18, side="bottom", pady=20)

        # Scrollable content
        content_area = tk.Frame(body, bg="#101218")
        content_area.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(
            content_area,
            bg="#101218",
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            content_area,
            orient="vertical",
            command=self.canvas.yview,
            style="Dark.Vertical.TScrollbar"
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.cards_frame = tk.Frame(self.canvas, bg="#101218")

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.cards_frame,
            anchor="nw"
        )

        self.cards_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )
        )

        self.canvas.bind_all("<MouseWheel>", self.scroll)

        self.display_guides()

    def search_changed(self, *args):
        self.search_text = self.search_var.get().lower().strip()
        self.display_guides()

    def select_category(self, category):
        self.current_category = category
        self.canvas.yview_moveto(0)
        self.display_guides()

    def get_filtered_guides(self):
        results = []

        for guide in self.guides:
            category_match = (
                self.current_category == "All"
                or guide["category"] == self.current_category
            )

            searchable_text = " ".join([
                guide["title"],
                guide["category"],
                guide["difficulty"],
                " ".join(guide["steps"]),
                " ".join(guide["tips"])
            ]).lower()

            search_match = (
                not self.search_text
                or self.search_text in searchable_text
            )

            if category_match and search_match:
                results.append(guide)

        return results

    def display_guides(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        results = self.get_filtered_guides()

        heading_text = self.current_category
        if self.search_text:
            heading_text += f'  /  "{self.search_text}"'

        heading = tk.Label(
            self.cards_frame,
            text=heading_text,
            bg="#101218",
            fg="white",
            font=("Segoe UI", 23, "bold")
        )
        heading.pack(anchor="w", padx=28, pady=(25, 2))

        count_label = tk.Label(
            self.cards_frame,
            text=f"{len(results)} guide(s)",
            bg="#101218",
            fg="#778096",
            font=("Segoe UI", 10)
        )
        count_label.pack(anchor="w", padx=30, pady=(0, 18))

        if not results:
            empty = tk.Label(
                self.cards_frame,
                text="No guides match your search.",
                bg="#101218",
                fg="#aeb5c5",
                font=("Segoe UI", 13)
            )
            empty.pack(anchor="w", padx=30, pady=30)
            return

        for guide in results:
            self.create_card(guide)

    def create_card(self, guide):
        card = tk.Frame(
            self.cards_frame,
            bg="#1b202c",
            highlightbackground="#2e3545",
            highlightthickness=1
        )
        card.pack(fill="x", padx=25, pady=9)

        stripe = tk.Frame(
            card,
            bg=guide["color"],
            height=4
        )
        stripe.pack(fill="x")

        title_row = tk.Frame(card, bg="#1b202c")
        title_row.pack(fill="x", padx=18, pady=(14, 6))

        title = tk.Label(
            title_row,
            text=guide["title"],
            bg="#1b202c",
            fg="#f1f3f7",
            font=("Segoe UI", 15, "bold")
        )
        title.pack(side="left")

        difficulty = tk.Label(
            title_row,
            text=guide["difficulty"].upper(),
            bg=guide["color"],
            fg="#101218",
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=3
        )
        difficulty.pack(side="right")

        category = tk.Label(
            card,
            text=guide["category"],
            bg="#1b202c",
            fg="#7d879c",
            font=("Segoe UI", 9)
        )
        category.pack(anchor="w", padx=20, pady=(0, 8))

        how_to = tk.Label(
            card,
            text="HOW TO DO IT",
            bg="#1b202c",
            fg=guide["color"],
            font=("Segoe UI", 9, "bold")
        )
        how_to.pack(anchor="w", padx=20, pady=(4, 4))

        for number, step in enumerate(guide["steps"], start=1):
            row = tk.Frame(card, bg="#1b202c")
            row.pack(fill="x", padx=20, pady=2)

            number_label = tk.Label(
                row,
                text=f"{number:02}",
                bg="#1b202c",
                fg=guide["color"],
                font=("Consolas", 10, "bold"),
                width=3,
                anchor="w"
            )
            number_label.pack(side="left")

            step_label = tk.Label(
                row,
                text=step,
                bg="#1b202c",
                fg="#d1d6e0",
                font=("Segoe UI", 10),
                anchor="w",
                justify="left",
                wraplength=680
            )
            step_label.pack(side="left", fill="x", expand=True)

        tips_title = tk.Label(
            card,
            text="TIPS",
            bg="#1b202c",
            fg="#8c96aa",
            font=("Segoe UI", 9, "bold")
        )
        tips_title.pack(anchor="w", padx=20, pady=(14, 3))

        for tip in guide["tips"]:
            tip_label = tk.Label(
                card,
                text=f"• {tip}",
                bg="#1b202c",
                fg="#929bad",
                font=("Segoe UI", 9),
                anchor="w",
                justify="left",
                wraplength=700
            )
            tip_label.pack(anchor="w", padx=25, pady=1)

        tk.Frame(card, bg="#1b202c", height=13).pack()

    def scroll(self, event):
        if self.visible:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def show(self):
        self.visible = True
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        self.root.lift()

    def hide(self):
        self.visible = False
        self.root.withdraw()

    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.show()


# ---------------------------------------------------------------------
# Global keyboard controls
# ---------------------------------------------------------------------

def start_keyboard_listener(app):
    def on_press(key):
        try:
            if key.char.lower() == "p":
                app.root.after(0, app.toggle)

        except AttributeError:
            if key == keyboard.Key.esc:
                app.root.after(0, app.hide)

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()


# ---------------------------------------------------------------------
# Start program
# ---------------------------------------------------------------------

def main():
    guides = load_guides()

    app = MinecraftParkourGUI(guides)
    start_keyboard_listener(app)

    print("Minecraft parkour encyclopedia is running.")
    print("Press P to show or hide the GUI.")
    print("Press Ctrl+C in this window to stop it.")

    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        app.root.destroy()


if __name__ == "__main__":
    main()
