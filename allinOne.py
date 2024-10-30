import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import time

class CodeExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Extractor")
        self.root.geometry("600x400")
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.file_extensions = {
            '.js', '.jsx', '.ts', '.tsx',  # JavaScript/TypeScript
            '.css', '.scss', '.sass', '.less',  # Stylesheets
            '.html', '.htm',  # HTML
            '.py',  # Python
            '.java',  # Java
            '.cpp', '.c', '.h', '.hpp',  # C/C++
            '.php',  # PHP
            '.rb',  # Ruby
            '.go',  # Go
            '.rs',  # Rust
            '.swift',  # Swift
            '.kt', '.kts',  # Kotlin
            '.cs',  # C#
            '.vue', '.svelte',  # Web frameworks
            '.xml', '.json', '.yaml', '.yml',  # Data formats
            '.sql',  # SQL
            '.sh', '.bash',  # Shell scripts
            '.md', '.mdx'  # Documentation
        }
        self.create_ui()
        self.total_files = 0
        self.processed_files = 0
        
    def create_ui(self):
        tk.Label(self.root, text="Source Folder:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.source_path, width=50).pack()
        tk.Button(self.root, text="Browse", command=self.browse_source).pack(pady=5)
        
        tk.Label(self.root, text="Destination File:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.dest_path, width=50).pack()
        tk.Button(self.root, text="Browse", command=self.browse_dest).pack(pady=5)
        
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(self.root, text="Ready")
        self.status_label.pack(pady=5)
        
        tk.Button(self.root, text="Start Extraction", command=self.start_extraction).pack(pady=20)
        
        self.log_text = tk.Text(self.root, height=10, width=50)
        self.log_text.pack(pady=10)
        
    def browse_source(self):
        folder = filedialog.askdirectory()
        self.source_path.set(folder)
        
    def browse_dest(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        self.dest_path.set(file)
        
    def update_progress(self, file_path):
        self.processed_files += 1
        progress = (self.processed_files / self.total_files) * 100
        self.progress['value'] = progress
        self.status_label.config(text=f"Processing: {file_path}")
        self.log_text.insert(tk.END, f"Processed: {file_path}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def count_files(self, path):
        count = 0
        for root, _, files in os.walk(path):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    count += 1
        return count
    
    def extract_code(self, source_path, dest_file):
        self.total_files = self.count_files(source_path)
        self.processed_files = 0
        self.progress['value'] = 0
        
        with open(dest_file, 'w', encoding='utf-8') as output:
            for root, _, files in os.walk(source_path):
                for file in files:
                    if any(file.endswith(ext) for ext in self.file_extensions):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, source_path)
                        
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            output.write(f"\n{'='*80}\n")
                            output.write(f"File: {rel_path}\n")
                            output.write(f"{'='*80}\n\n")
                            output.write(content)
                            output.write("\n\n")
                            
                            self.update_progress(rel_path)
                            time.sleep(0.1)
                            
                        except Exception as e:
                            self.log_text.insert(tk.END, f"Error processing {rel_path}: {str(e)}\n")
                            
        self.status_label.config(text="Extraction Complete!")
        
    def start_extraction(self):
        source = self.source_path.get()
        dest = self.dest_path.get()
        
        if not source or not dest:
            messagebox.showerror("Error", "Please select source folder and destination file")
            return
            
        self.extract_code(source, dest)

def main():
    root = tk.Tk()
    app = CodeExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()