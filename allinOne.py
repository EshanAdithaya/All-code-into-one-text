import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import time
import math

class CodeExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Extractor")
        self.root.geometry("700x500")
        
        # Constants for Claude compatibility
        self.CLAUDE_TOKEN_LIMIT = 200000  # Approximately 200k tokens
        self.CHARS_PER_TOKEN = 4  # Approximate characters per token
        self.MAX_CHARS_PER_FILE = self.CLAUDE_TOKEN_LIMIT * self.CHARS_PER_TOKEN
        
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
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Source selection
        source_frame = ttk.LabelFrame(main_frame, text="Source Selection", padding="5")
        source_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(source_frame, textvariable=self.source_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(source_frame, text="Browse Source", command=self.browse_source).pack(side=tk.LEFT, padx=5)
        
        # Destination selection
        dest_frame = ttk.LabelFrame(main_frame, text="Destination Selection", padding="5")
        dest_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(dest_frame, textvariable=self.dest_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(dest_frame, text="Browse Destination", command=self.browse_dest).pack(side=tk.LEFT, padx=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        # Start button
        ttk.Button(main_frame, text="Start Extraction", command=self.start_extraction).pack(pady=5)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Add scrollbar to log
        log_scroll = ttk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, width=50, yscrollcommand=log_scroll.set)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
    def browse_source(self):
        folder = filedialog.askdirectory()
        self.source_path.set(folder)
        
    def browse_dest(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        self.dest_path.set(file)
        
    def update_progress(self, message):
        self.processed_files += 1
        progress = (self.processed_files / self.total_files) * 100
        self.progress['value'] = progress
        self.status_label.config(text=message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def count_files(self, path):
        count = 0
        for root, _, files in os.walk(path):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    count += 1
        return count
    
    def get_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        header = f"\n{'='*80}\nFile: {file_path}\n{'='*80}\n\n"
        return header + content + "\n\n"
    
    def extract_code(self, source_path, dest_file):
        self.total_files = self.count_files(source_path)
        self.processed_files = 0
        self.progress['value'] = 0
        
        # Collect all file paths and their contents
        files_to_process = []
        for root, _, files in os.walk(source_path):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, source_path)
                    try:
                        content = self.get_file_content(full_path)
                        files_to_process.append((rel_path, content))
                    except Exception as e:
                        self.log_text.insert(tk.END, f"Error reading {rel_path}: {str(e)}\n")
        
        # Split into multiple files if needed
        current_file_num = 1
        current_content = ""
        current_size = 0
        
        base_path, ext = os.path.splitext(dest_file)
        
        for file_path, content in files_to_process:
            content_size = len(content)
            
            # If adding this file would exceed limit, save current content and start new file
            if current_size + content_size > self.MAX_CHARS_PER_FILE and current_content:
                output_path = f"{base_path}_part{current_file_num}{ext}"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(current_content)
                self.update_progress(f"Saved part {current_file_num} to {output_path}")
                current_file_num += 1
                current_content = ""
                current_size = 0
            
            current_content += content
            current_size += content_size
            self.update_progress(f"Processed: {file_path}")
        
        # Save any remaining content
        if current_content:
            output_path = f"{base_path}_part{current_file_num}{ext}" if current_file_num > 1 else dest_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(current_content)
            self.update_progress(f"Saved {output_path}")
        
        self.status_label.config(text="Extraction Complete!")
        if current_file_num > 1:
            messagebox.showinfo("Complete", 
                f"Extraction completed!\nContent was split into {current_file_num} files due to Claude's token limit.")
        
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