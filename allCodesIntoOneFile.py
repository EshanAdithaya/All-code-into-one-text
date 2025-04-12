import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from datetime import datetime

class CodeScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Code File Scanner")
        self.root.geometry("700x650")  # Increased height for new controls
        
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
        # Source folders selection
        self.source_frame = ttk.LabelFrame(self.main_frame, text="Source Directories (Code Files)", padding="5")
        self.source_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # List to store source directories
        self.source_directories = []
        
        # Listbox to display selected directories
        self.source_listbox = tk.Listbox(self.source_frame, width=60, height=5)
        self.source_listbox.grid(row=0, column=0, rowspan=4, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for the listbox
        self.source_scrollbar = ttk.Scrollbar(self.source_frame, orient=tk.VERTICAL, command=self.source_listbox.yview)
        self.source_scrollbar.grid(row=0, column=1, rowspan=4, sticky=(tk.N, tk.S))
        self.source_listbox['yscrollcommand'] = self.source_scrollbar.set
        
        # Buttons for source directory management
        self.add_source_button = ttk.Button(self.source_frame, text="Add Directory", command=self.add_source_directory)
        self.add_source_button.grid(row=0, column=2, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        self.add_file_button = ttk.Button(self.source_frame, text="Add File", command=self.add_source_file)
        self.add_file_button.grid(row=1, column=2, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        self.remove_source_button = ttk.Button(self.source_frame, text="Remove Selected", command=self.remove_source)
        self.remove_source_button.grid(row=2, column=2, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        self.clear_sources_button = ttk.Button(self.source_frame, text="Clear All", command=self.clear_sources)
        self.clear_sources_button.grid(row=3, column=2, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # File type selection
        self.filetype_frame = ttk.LabelFrame(self.main_frame, text="File Types to Scan", padding="5")
        self.filetype_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # File type checkboxes
        self.js_enabled = tk.BooleanVar(value=True)
        self.jsx_enabled = tk.BooleanVar(value=False)
        self.ts_enabled = tk.BooleanVar(value=True)
        self.tsx_enabled = tk.BooleanVar(value=False)
        self.json_enabled = tk.BooleanVar(value=False)
        self.py_enabled = tk.BooleanVar(value=False)
        self.html_enabled = tk.BooleanVar(value=False)
        self.css_enabled = tk.BooleanVar(value=False)
        
        # File type checkbox widgets
        self.js_check = ttk.Checkbutton(self.filetype_frame, text="JavaScript (.js)", variable=self.js_enabled)
        self.js_check.grid(row=0, column=0, padx=5, sticky=tk.W)
        
        self.jsx_check = ttk.Checkbutton(self.filetype_frame, text="React JSX (.jsx)", variable=self.jsx_enabled)
        self.jsx_check.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        self.ts_check = ttk.Checkbutton(self.filetype_frame, text="TypeScript (.ts)", variable=self.ts_enabled)
        self.ts_check.grid(row=1, column=0, padx=5, sticky=tk.W)
        
        self.tsx_check = ttk.Checkbutton(self.filetype_frame, text="React TSX (.tsx)", variable=self.tsx_enabled)
        self.tsx_check.grid(row=1, column=1, padx=5, sticky=tk.W)
        
        self.json_check = ttk.Checkbutton(self.filetype_frame, text="JSON (.json)", variable=self.json_enabled)
        self.json_check.grid(row=2, column=0, padx=5, sticky=tk.W)
        
        self.py_check = ttk.Checkbutton(self.filetype_frame, text="Python (.py)", variable=self.py_enabled)
        self.py_check.grid(row=2, column=1, padx=5, sticky=tk.W)
        
        self.html_check = ttk.Checkbutton(self.filetype_frame, text="HTML (.html, .htm)", variable=self.html_enabled)
        self.html_check.grid(row=3, column=0, padx=5, sticky=tk.W)
        
        self.css_check = ttk.Checkbutton(self.filetype_frame, text="CSS (.css)", variable=self.css_enabled)
        self.css_check.grid(row=3, column=1, padx=5, sticky=tk.W)
        
        # Exclude test files option
        self.exclude_tests = tk.BooleanVar(value=True)
        self.test_check = ttk.Checkbutton(
            self.filetype_frame, 
            text="Exclude test files (.spec.*, .test.*)", 
            variable=self.exclude_tests
        )
        self.test_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Target folder selection
        self.target_frame = ttk.LabelFrame(self.main_frame, text="Target Directory (Output Location)", padding="5")
        self.target_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.target_path = tk.StringVar()
        self.target_entry = ttk.Entry(self.target_frame, textvariable=self.target_path, width=60)
        self.target_entry.grid(row=0, column=0, padx=5)
        
        self.target_button = ttk.Button(self.target_frame, text="Browse", command=self.browse_target)
        self.target_button.grid(row=0, column=1, padx=5)
        
        # Output file name
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Output File Settings", padding="5")
        self.output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.output_name = tk.StringVar(value="codebase_export.txt")
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_name, width=60)
        self.output_entry.grid(row=0, column=0, columnspan=2, padx=5)
        
        # Status display
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Progress Log", padding="5")
        self.status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.status_text = tk.Text(self.status_frame, height=12, width=70)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for status
        self.scrollbar = ttk.Scrollbar(self.status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text['yscrollcommand'] = self.scrollbar.set
        
        # Make the main frame and status frame expandable
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(4, weight=1)
        self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.rowconfigure(0, weight=1)
        
        # Scan button
        self.scan_button = ttk.Button(self.main_frame, text="Scan Code Files", command=self.scan_files)
        self.scan_button.grid(row=5, column=0, columnspan=3, pady=10)
    
    def add_source_directory(self):
        folder_selected = filedialog.askdirectory(title="Select Source Directory (Code Files)")
        if folder_selected:
            if folder_selected not in self.source_directories:
                self.source_directories.append(folder_selected)
                self.update_source_listbox()
    
    def add_source_file(self):
        file_selected = filedialog.askopenfilename(title="Select Source File")
        if file_selected:
            if file_selected not in self.source_directories:
                self.source_directories.append(file_selected)
                self.update_source_listbox()
    
    def remove_source(self):
        selected_indices = self.source_listbox.curselection()
        if selected_indices:
            # Remove from highest index to lowest to avoid index shifting problems
            for index in sorted(selected_indices, reverse=True):
                del self.source_directories[index]
            self.update_source_listbox()
    
    def clear_sources(self):
        self.source_directories.clear()
        self.update_source_listbox()
    
    def update_source_listbox(self):
        self.source_listbox.delete(0, tk.END)
        for directory in self.source_directories:
            self.source_listbox.insert(tk.END, directory)
            
    def browse_target(self):
        folder_selected = filedialog.askdirectory(title="Select Target Directory (Output Location)")
        if folder_selected:
            self.target_path.set(folder_selected)
    
    def should_skip_directory(self, dir_path):
        # List of directories to exclude
        excluded_dirs = {'node_modules', 'dist', '.git'}
        return os.path.basename(dir_path) in excluded_dirs
    
    def get_selected_extensions(self):
        extensions = []
        
        if self.js_enabled.get():
            extensions.append('.js')
        if self.jsx_enabled.get():
            extensions.append('.jsx')
        if self.ts_enabled.get():
            extensions.append('.ts')
        if self.tsx_enabled.get():
            extensions.append('.tsx')
        if self.json_enabled.get():
            extensions.append('.json')
        if self.py_enabled.get():
            extensions.append('.py')
        if self.html_enabled.get():
            extensions.extend(['.html', '.htm'])
        if self.css_enabled.get():
            extensions.append('.css')
            
        return tuple(extensions)
    
    def get_test_exclusions(self):
        if not self.exclude_tests.get():
            return tuple()
            
        # Define test file patterns to exclude
        exclusions = ['.spec.js', '.test.js', '.spec.ts', '.test.ts', 
                     '.spec.jsx', '.test.jsx', '.spec.tsx', '.test.tsx']
        return tuple(exclusions)
    
    def process_source_path(self, source_path, file_extensions, test_exclusions):
        """Process a single source path (file or directory) and return found code files"""
        code_files = []
        
        # Check if the source path is a file or directory
        if os.path.isfile(source_path):
            # Process a single file
            file_name = os.path.basename(source_path)
            if file_name.endswith(file_extensions) and not any(file_name.endswith(test_ext) for test_ext in test_exclusions):
                # For a single file, use the parent directory as base for relative path
                parent_dir = os.path.dirname(source_path)
                relative_path = os.path.basename(source_path)
                code_files.append((relative_path, source_path))
                self.status_text.insert(tk.END, f"Found file: {relative_path}\n")
                self.status_text.see(tk.END)
                self.root.update()
        else:
            # Process a directory
            for folder_path, dirs, files in os.walk(source_path):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not self.should_skip_directory(os.path.join(folder_path, d))]
                
                for file in files:
                    if file.endswith(file_extensions) and not any(file.endswith(test_ext) for test_ext in test_exclusions):
                        file_path = os.path.join(folder_path, file)
                        relative_path = os.path.relpath(file_path, source_path)
                        code_files.append((relative_path, file_path))
                        self.status_text.insert(tk.END, f"Found: {relative_path}\n")
                        self.status_text.see(tk.END)
                        self.root.update()
        
        return code_files
            
    def scan_files(self):
        if not self.source_directories:
            messagebox.showerror("Error", "Please add at least one source directory or file!")
            return
            
        target_folder = self.target_path.get()
        output_file = self.output_name.get()
        
        # Get selected file types
        file_extensions = self.get_selected_extensions()
        test_exclusions = self.get_test_exclusions()
        
        if not target_folder:
            messagebox.showerror("Error", "Please select a target folder!")
            return
            
        if not file_extensions:
            messagebox.showerror("Error", "Please select at least one file type to scan!")
            return
            
        try:
            self.status_text.delete(1.0, tk.END)
            
            ext_description = ", ".join([ext.replace(".", "") for ext in file_extensions])
            self.status_text.insert(tk.END, f"Scanning for {ext_description} files (excluding node_modules, dist, .git)...\n")
            if test_exclusions:
                self.status_text.insert(tk.END, f"Excluding test files: {', '.join(test_exclusions)}\n")
            self.root.update()
            
            # Create output file in target directory
            output_path = os.path.join(target_folder, output_file)
            all_code_files = []
            
            # Process each source path
            for source_path in self.source_directories:
                self.status_text.insert(tk.END, f"\nProcessing source: {source_path}\n")
                self.status_text.see(tk.END)
                self.root.update()
                
                code_files = self.process_source_path(source_path, file_extensions, test_exclusions)
                all_code_files.extend([(source_path, rel_path, full_path) for rel_path, full_path in code_files])
            
            if not all_code_files:
                self.status_text.insert(tk.END, f"\nNo matching files found in the selected sources.\n")
                return
            
            # Sort files by source path and then by relative path for better organization
            all_code_files.sort(key=lambda x: (x[0], x[1]))
            
            # Write to output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Codebase Export ({ext_description} files)\n{'='*80}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Files Found: {len(all_code_files)}\n\n")
                
                current_source = None
                
                for source_path, relative_path, full_path in all_code_files:
                    # Add source header when source changes
                    if current_source != source_path:
                        current_source = source_path
                        f.write(f"\n\n{'#'*80}\n")
                        f.write(f"Source: {source_path}\n")
                        f.write(f"{'#'*80}\n")
                    
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
            self.status_text.insert(tk.END, f"Total files processed: {len(all_code_files)}\n")
            messagebox.showinfo("Success", f"Scan completed successfully!\nFound {len(all_code_files)} {ext_description} files.")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_text.insert(tk.END, f"ERROR: {str(e)}\n")

def main():
    root = tk.Tk()
    app = CodeScanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()