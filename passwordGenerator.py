import tkinter as tk
from tkinter import ttk, filedialog
import string
import itertools
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Variable Length Password Generator")
        self.root.geometry("500x700")
        
        # Variables for toggles
        self.lowercase_var = tk.BooleanVar()
        self.uppercase_var = tk.BooleanVar()
        self.numbers_var = tk.BooleanVar()
        self.symbols_var = tk.BooleanVar()
        self.max_length_var = tk.StringVar(value="3")
        self.limit_var = tk.StringVar(value="")  # Optional limit
        self.save_path = tk.StringVar()
        
        # Bind variables to update method
        for var in (self.lowercase_var, self.uppercase_var, 
                   self.numbers_var, self.symbols_var, self.max_length_var):
            var.trace('w', self.update_possible_combinations)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Character options frame
        options_frame = ttk.LabelFrame(self.root, text="Character Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Checkbutton(options_frame, text="Numbers (0-9)", variable=self.numbers_var).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.lowercase_var).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.uppercase_var).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Symbols (!@#$%^&*)", variable=self.symbols_var).pack(anchor="w")
        
        # Length frame
        length_frame = ttk.LabelFrame(self.root, text="Maximum Password Length", padding=10)
        length_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(length_frame, text="Max Length:").pack(anchor="w")
        length_entry = ttk.Entry(length_frame, textvariable=self.max_length_var, width=10)
        length_entry.pack(anchor="w")
        
        # Optional limit frame
        limit_frame = ttk.LabelFrame(self.root, text="Optional Generation Limit", padding=10)
        limit_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(limit_frame, text="Limit (leave empty for all combinations):").pack(anchor="w")
        ttk.Entry(limit_frame, textvariable=self.limit_var, width=20).pack(anchor="w")
        
        # Combinations info frame
        self.combinations_frame = ttk.LabelFrame(self.root, text="Generation Information", padding=10)
        self.combinations_frame.pack(fill="x", padx=10, pady=5)
        
        self.char_pool_label = ttk.Label(self.combinations_frame, text="Character Pool: ")
        self.char_pool_label.pack(anchor="w")
        
        self.total_combinations_label = ttk.Label(self.combinations_frame, text="Total Possible Combinations: 0")
        self.total_combinations_label.pack(anchor="w")
        
        self.example_label = ttk.Label(self.combinations_frame, text="Example Range: ")
        self.example_label.pack(anchor="w")
        
        # Save location frame
        save_frame = ttk.LabelFrame(self.root, text="Save Location", padding=10)
        save_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(save_frame, textvariable=self.save_path, width=30).pack(side="left", padx=5)
        ttk.Button(save_frame, text="Browse", command=self.browse_location).pack(side="left")
        
        # Generate button
        ttk.Button(self.root, text="Generate Passwords", command=self.generate_passwords).pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=5)
        
        # Initial update
        self.update_possible_combinations()
    
    def get_character_pool(self):
        chars = ""
        if self.numbers_var.get():
            chars += string.digits
        if self.lowercase_var.get():
            chars += string.ascii_lowercase
        if self.uppercase_var.get():
            chars += string.ascii_uppercase
        if self.symbols_var.get():
            chars += "!@#$%^&*"
        return ''.join(sorted(chars))
    
    def calculate_total_combinations(self, char_pool, max_length):
        total = 0
        for length in range(1, max_length + 1):
            total += len(char_pool) ** length
        return total
    
    def update_possible_combinations(self, *args):
        char_pool = self.get_character_pool()
        try:
            max_length = int(self.max_length_var.get())
            total_combinations = self.calculate_total_combinations(char_pool, max_length) if char_pool else 0
            
            # Update labels
            self.char_pool_label.config(text=f"Character Pool: {char_pool}")
            self.total_combinations_label.config(
                text=f"Total Possible Combinations: {total_combinations:,}")
            
            # Show example range
            if char_pool:
                examples = []
                for length in range(1, max_length + 1):
                    first = char_pool[0] * length
                    last = char_pool[-1] * length
                    examples.append(f"Length {length}: {first} to {last}")
                self.example_label.config(text="Example Ranges:\n" + "\n".join(examples))
            else:
                self.example_label.config(text="Example Range: N/A")
                
        except ValueError:
            self.total_combinations_label.config(text="Please enter valid length")
    
    def browse_location(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.save_path.set(filename)
    
    def generate_passwords(self):
        if not self.save_path.get():
            self.status_label.config(text="Please select save location first!")
            return
        
        char_pool = self.get_character_pool()
        if not char_pool:
            self.status_label.config(text="Please select at least one character type!")
            return
        
        try:
            max_length = int(self.max_length_var.get())
            if max_length < 1:
                self.status_label.config(text="Length must be at least 1!")
                return
        except ValueError:
            self.status_label.config(text="Please enter valid length!")
            return
        
        # Get limit if specified
        try:
            limit = int(self.limit_var.get()) if self.limit_var.get() else None
        except ValueError:
            self.status_label.config(text="Please enter valid limit or leave empty!")
            return
        
        total_combinations = self.calculate_total_combinations(char_pool, max_length)
        if limit:
            total_combinations = min(limit, total_combinations)
        
        self.status_label.config(text=f"Generating {total_combinations:,} passwords...")
        self.root.update()
        
        try:
            with open(self.save_path.get(), 'w') as f:
                generated = 0
                batch_size = 1000  # Write in batches to improve performance
                current_batch = []
                
                # Generate for each length from 1 to max_length
                for current_length in range(1, max_length + 1):
                    for combo in itertools.product(char_pool, repeat=current_length):
                        if limit and generated >= limit:
                            break
                        
                        password = ''.join(combo)
                        current_batch.append(password)
                        generated += 1
                        
                        # Write batch and update progress
                        if len(current_batch) >= batch_size:
                            f.write('\n'.join(current_batch) + '\n')
                            current_batch = []
                            progress = (generated / total_combinations) * 100
                            self.progress_var.set(progress)
                            self.status_label.config(text=f"Generated {generated:,} of {total_combinations:,}")
                            self.root.update()
                    
                    if limit and generated >= limit:
                        break
                
                # Write any remaining passwords
                if current_batch:
                    f.write('\n'.join(current_batch) + '\n')
                
                self.status_label.config(text=f"Successfully generated {generated:,} passwords!")
                self.progress_var.set(100)
                
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()