import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import math

class TSXFileSplitter:
    def __init__(self, root):
        self.root = root
        self.root.title("TSX File Splitter")
        self.root.geometry("700x500")
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Source file selection
        self.source_frame = ttk.LabelFrame(self.main_frame, text="Source TSX Index File", padding="5")
        self.source_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.source_path = tk.StringVar()
        self.source_entry = ttk.Entry(self.source_frame, textvariable=self.source_path, width=60)
        self.source_entry.grid(row=0, column=0, padx=5)
        
        self.source_button = ttk.Button(self.source_frame, text="Browse", command=self.browse_source)
        self.source_button.grid(row=0, column=1, padx=5)
        
        # Number of pieces input
        self.pieces_frame = ttk.LabelFrame(self.main_frame, text="Split Settings", padding="5")
        self.pieces_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.pieces_frame, text="Number of pieces:").grid(row=0, column=0, padx=5)
        self.pieces_var = tk.StringVar(value="2")
        self.pieces_entry = ttk.Entry(self.pieces_frame, textvariable=self.pieces_var, width=10)
        self.pieces_entry.grid(row=0, column=1, padx=5)
        
        # Output directory selection
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Output Directory", padding="5")
        self.output_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path, width=60)
        self.output_entry.grid(row=0, column=0, padx=5)
        
        self.output_button = ttk.Button(self.output_frame, text="Browse", command=self.browse_output)
        self.output_button.grid(row=0, column=1, padx=5)
        
        # Status display
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Progress Log", padding="5")
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.status_text = tk.Text(self.status_frame, height=15, width=70)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for status
        self.scrollbar = ttk.Scrollbar(self.status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text['yscrollcommand'] = self.scrollbar.set
        
        # Split button
        self.split_button = ttk.Button(self.main_frame, text="Split File", command=self.split_file)
        self.split_button.grid(row=4, column=0, columnspan=2, pady=10)
        
    def browse_source(self):
        file_selected = filedialog.askopenfilename(
            title="Select TSX Index File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_selected:
            self.source_path.set(file_selected)
            # Set default output directory to source file directory
            self.output_path.set(os.path.dirname(file_selected))
            
    def browse_output(self):
        folder_selected = filedialog.askdirectory(title="Select Output Directory")
        if folder_selected:
            self.output_path.set(folder_selected)
            
    def split_file(self):
        try:
            source_file = self.source_path.get()
            output_dir = self.output_path.get()
            num_pieces = int(self.pieces_var.get())
            
            if not source_file or not output_dir:
                messagebox.showerror("Error", "Please select source file and output directory!")
                return
                
            if num_pieces < 2:
                messagebox.showerror("Error", "Number of pieces must be at least 2!")
                return
            
            # Read the source file and split into file sections
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content by file sections
            file_sections = content.split("\nFile: ")
            header = file_sections[0]  # Get the header section
            file_sections = file_sections[1:]  # Remove header from sections
            
            if not file_sections:
                messagebox.showerror("Error", "No file sections found in the source file!")
                return
            
            # Calculate sections per file
            total_sections = len(file_sections)
            sections_per_file = math.ceil(total_sections / num_pieces)
            
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Total TSX files found: {total_sections}\n")
            self.status_text.insert(tk.END, f"Splitting into {num_pieces} pieces...\n\n")
            
            # Create split files
            base_name = os.path.splitext(os.path.basename(source_file))[0]
            
            for i in range(num_pieces):
                start_idx = i * sections_per_file
                end_idx = min((i + 1) * sections_per_file, total_sections)
                
                if start_idx >= total_sections:
                    break
                
                output_file = os.path.join(output_dir, f"{base_name}_part{i+1}.txt")
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    # Write header to each file
                    f.write(header)
                    f.write(f"\nPart {i+1} of {num_pieces}\n")
                    f.write(f"Contains files {start_idx + 1} to {end_idx} of {total_sections}\n\n")
                    
                    # Write file sections
                    for section in file_sections[start_idx:end_idx]:
                        f.write("\nFile: " + section)
                
                self.status_text.insert(tk.END, f"Created: {os.path.basename(output_file)}\n")
                self.status_text.insert(tk.END, f"Contains {end_idx - start_idx} files\n\n")
                self.root.update()
            
            self.status_text.insert(tk.END, "\nSplit completed successfully!")
            messagebox.showinfo("Success", f"File split into {num_pieces} pieces successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter a valid number for pieces!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = TSXFileSplitter(root)
    root.mainloop()

if __name__ == "__main__":
    main()