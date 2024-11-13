import tkinter as tk
from tkinter import ttk, filedialog
import Training_with_stardist

# class FolderBrowserApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#
#         self.title("Folder Browser App with Text Box")
#         self.geometry("600x200")
#
#         # Create a label to display the selected folder path
#         self.folder_path_label = tk.Label(self, text="Selected Folder Path:")
#         self.folder_path_label.pack(pady=10)
#
#         # Create a text box to display the selected folder path
#         self.folder_path_text = tk.Text(self, height=1, wrap=tk.WORD)
#         self.folder_path_text.pack(fill=tk.X, padx=10, pady=5)
#
#         # Create a button to open the folder browser
#         self.browse_button = ttk.Button(self, text="Browse Folder", command=self.browse_folder)
#         self.browse_button.pack(pady=10)
#
#         # Create a button to get text from the text box
#         self.get_text_button = ttk.Button(self, text="Get Text", command=self.get_text)
#         self.get_text_button.pack(pady=10)
#
#
#     def browse_folder(self):
#         folder_path = filedialog.askdirectory()
#         if folder_path:
#             self.folder_path_text.delete(1.0, tk.END)
#             self.folder_path_text.insert(tk.END, folder_path)
#
#     def get_text(self):
#         folder_name = self.folder_name_text.get("1.0", tk.END).strip()
#         print("Folder Name from Text Box:", folder_name)

if __name__ == "__main__":
    # app = FolderBrowserApp()
    #app.mainloop()
    input_directory = 'X:/Users/Members/Ruthi/VideoBMR11/New ruthie project/ground_truth'
    model_name = 'stardist_oxytocin_spetial'
    dir_for_models = 'X:/Users/Members/Ruthi/VideoBMR11/New ruthie project/models'
    Training_with_stardist.Training(input_directory, model_name, dir_for_models)
