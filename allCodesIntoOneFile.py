import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from datetime import datetime

class CodeScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Code File Scanner")
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
        # Source folder selection
        self.source_frame = ttk.LabelFrame(self.main_frame, text="Source Directory (Code Files)", padding="5")
        self.source_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.source_path = tk.StringVar()
        self.source_entry = ttk.Entry(self.source_frame, textvariable=self.source_path, width=60)
        self.source_entry.grid(row=0, column=0, padx=5)
        
        self.source_button = ttk.Button(self.source_frame, text="Browse", command=self.browse_source)
        self.source_button.grid(row=0, column=1, padx=5)
        
        # File type mode selection
        self.mode_frame = ttk.LabelFrame(self.main_frame, text="File Type Selection", padding="5")
        self.mode_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.jsx_mode = tk.BooleanVar(value=False)
        self.mode_switch = ttk.Checkbutton(
            self.mode_frame, 
            text="JSX Mode (ON: scan JS/JSX files, OFF: scan TS/JS files)", 
            variable=self.jsx_mode,
            command=self.update_file_mode_label
        )
        self.mode_switch.grid(row=0, column=0, padx=5, sticky=tk.W)
        
        self.file_mode_label = ttk.Label(self.mode_frame, text="Current mode: TS/JS files")
        self.file_mode_label.grid(row=1, column=0, padx=5, sticky=tk.W)
        
        # Target folder selection
        self.target_frame = ttk.LabelFrame(self.main_frame, text="Target Directory (Output Location)", padding="5")
        self.target_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.target_path = tk.StringVar()
        self.target_entry = ttk.Entry(self.target_frame, textvariable=self.target_path, width=60)
        self.target_entry.grid(row=0, column=0, padx=5)
        
        self.target_button = ttk.Button(self.target_frame, text="Browse", command=self.browse_target)
        self.target_button.grid(row=0, column=1, padx=5)
        
        # Output file name
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Output File Settings", padding="5")
        self.output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.output_name = tk.StringVar(value="codebase_export.txt")
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_name, width=60)
        self.output_entry.grid(row=0, column=0, columnspan=2, padx=5)
        
        # Status display
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Progress Log", padding="5")
        self.status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.status_text = tk.Text(self.status_frame, height=15, width=70)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for status
        self.scrollbar = ttk.Scrollbar(self.status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text['yscrollcommand'] = self.scrollbar.set
        
        # Scan button
        self.scan_button = ttk.Button(self.main_frame, text="Scan Code Files", command=self.scan_files)
        self.scan_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    def update_file_mode_label(self):
        if self.jsx_mode.get():
            self.file_mode_label.config(text="Current mode: JS/JSX files")
        else:
            self.file_mode_label.config(text="Current mode: TS/JS files")
        
    def browse_source(self):
        folder_selected = filedialog.askdirectory(title="Select Source Directory (Code Files)")
        if folder_selected:
            self.source_path.set(folder_selected)
            
    def browse_target(self):
        folder_selected = filedialog.askdirectory(title="Select Target Directory (Output Location)")
        if folder_selected:
            self.target_path.set(folder_selected)
    
    def should_skip_directory(self, dir_path):
        # List of directories to exclude
        excluded_dirs = {'node_modules', 'dist', '.git'}
        return os.path.basename(dir_path) in excluded_dirs
            
    def scan_files(self):
        source_folder = self.source_path.get()
        target_folder = self.target_path.get()
        output_file = self.output_name.get()
        jsx_mode = self.jsx_mode.get()
        
        if not source_folder or not target_folder:
            messagebox.showerror("Error", "Please select both source and target folders!")
            return
            
        try:
            self.status_text.delete(1.0, tk.END)
            
            # Set file extensions based on mode
            if jsx_mode:
                file_extensions = ('.js', '.jsx')
                test_exclusions = ('.spec.js', '.test.js')
                mode_description = "JS/JSX"
            else:
                file_extensions = ('.ts', '.js')
                test_exclusions = ('.d.ts', '.spec.ts', '.test.ts', '.spec.js', '.test.js')
                mode_description = "TS/JS"
                
            self.status_text.insert(tk.END, f"Scanning for {mode_description} files (excluding node_modules, dist, .git)...\n")
            self.root.update()
            
            # Create output file in target directory
            output_path = os.path.join(target_folder, output_file)
            code_files = []
            
            # Walk through directory
            for folder_path, dirs, files in os.walk(source_folder):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not self.should_skip_directory(os.path.join(folder_path, d))]
                
                for file in files:
                    if file.endswith(file_extensions) and not file.endswith(test_exclusions):
                        file_path = os.path.join(folder_path, file)
                        relative_path = os.path.relpath(file_path, source_folder)
                        code_files.append((relative_path, file_path))
                        self.status_text.insert(tk.END, f"Found: {relative_path}\n")
                        self.status_text.see(tk.END)
                        self.root.update()
            
            if not code_files:
                self.status_text.insert(tk.END, f"\nNo {mode_description} files found in the selected directory (excluding node_modules, dist, .git).\n")
                return
            
            # Sort files by path for better organization
            code_files.sort(key=lambda x: x[0])
            
            # Write to output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Codebase Export ({mode_description} files)\n{'='*80}\n")
                f.write(f"Source Directory: {source_folder}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Files Found: {len(code_files)}\n\n")
                
                for relative_path, full_path in code_files:
                    f.write(f"\n\n{'='*80}\n")
                    f.write(f"File: {relative_path}\n")
                    f.write(f"{'='*80}\n\n")
                    try:
                        with open(full_path, 'r', encoding='utf-8') as code_file:
                            content = code_file.read()
                            f.write(f"{content}\n")
                    except Exception as e:
                        f.write(f"Error reading file: {str(e)}\n")
            
            self.status_text.insert(tk.END, f"\nDone! Output file created at:\n{output_path}\n")
            self.status_text.insert(tk.END, f"Total files processed: {len(code_files)}\n")
            messagebox.showinfo("Success", f"Scan completed successfully!\nFound {len(code_files)} {mode_description} files.")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_text.insert(tk.END, f"ERROR: {str(e)}\n")

def main():
    root = tk.Tk()
    app = CodeScanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()