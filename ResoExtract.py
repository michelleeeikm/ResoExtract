import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pefile

class ResoExtractApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ResoExtract - EXE Resource Extractor")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.selected_file = None
        self.output_folder = tk.StringVar(value=os.getcwd())
        
        # Layout
        self.create_widgets()
        
    def create_widgets(self):
        # File Selection
        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text="Selected EXE:").pack(side=tk.LEFT, padx=(0, 5))
        self.file_label = ttk.Label(file_frame, text="None", anchor="w", width=50)
        self.file_label.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)
        
        # Output Folder Selection
        output_frame = ttk.Frame(self.root)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output Folder:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(output_frame, textvariable=self.output_folder, width=50).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(output_frame, text="Change", command=self.browse_folder).pack(side=tk.LEFT)
        
        # Treeview for Resources
        self.tree = ttk.Treeview(self.root, columns=("Type", "Size"), show="tree headings")
        self.tree.heading("#0", text="Resource")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size (bytes)")
        self.tree.column("#0", width=300)
        self.tree.column("Type", width=150)
        self.tree.column("Size", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Extract Selected", command=self.extract_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Extract All", command=self.extract_all).pack(side=tk.LEFT)
        
    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if file:
            self.selected_file = file
            self.file_label.config(text=os.path.basename(file))
            self.load_resources()
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)
            
    def load_resources(self):
        if not self.selected_file:
            return
        try:
            pe = pefile.PE(self.selected_file)
            self.tree.delete(*self.tree.get_children())
            for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                self.add_resource_to_tree(entry)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load resources: {e}")
            
    def add_resource_to_tree(self, entry, parent=""):
        name = entry.name.string.decode() if entry.name else f"ID_{entry.id}"
        node = self.tree.insert(parent, "end", text=name, values=("Folder" if entry.struct.DataIsDirectory else "File", ""))
        if entry.struct.DataIsDirectory:
            for subentry in entry.directory.entries:
                self.add_resource_to_tree(subentry, node)
                
    def extract_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No resource selected!")
            return
        messagebox.showinfo("Info", "Feature under development!")
        
    def extract_all(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "No EXE file loaded!")
            return
        messagebox.showinfo("Info", "Feature under development!")
        
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResoExtractApp(root)
    root.mainloop()
