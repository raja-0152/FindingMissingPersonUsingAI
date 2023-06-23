import tkinter as tk
from tkinter import filedialog
import customtkinter
import pyrebase
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com",
    "serviceAccount": "path/to/serviceAccount.json"
}

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-storage-bucket.appspot.com'
})

bucket = storage.bucket()

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if file_path:
        image_path_label.configure(text=file_path)

def submit():
    name = name_entry.get()
    age = age_entry.get()
    father_name = father_name_entry.get()
    mobile_number = mobile_number_entry.get()
    image = image_path_label.cget("text")
    
    # Upload image to Firebase Storage
    storage.child("Images/" + name + ".png").put(image)

    # Save data to Firebase Realtime Database
    data = {
        name:{
            "name": name,
            "age": age,
            "father_name": father_name,
            "contact_no": mobile_number,
            "last_seen_time": "2022-12-11 00:54:34",
            "location": "Vadakal, Sriperumbudur"
        }
    }
    for key, value in data.items():
        database.child("Victims/" + key).set(value)

    print("Data submitted successfully!")

    # File path and name for the downloaded image
    local_folder = "c:/Images/"
    local_file_name = name  # Specify the desired file name
    filename = f'{local_file_name}.png'

    # Download the image from Firebase Storage
    blob = bucket.blob(f"Images/{filename}")
    blob.download_to_filename(local_folder + filename)

    print("Image downloaded successfully!")



window = customtkinter.CTk()
window.title("Submit Information")
window.geometry("600x400")
window.configure(bg="#262d37")

# Create form labels and entries

name_label = customtkinter.CTkLabel(master=window, text='Name', width=80, height=25, text_color='black', fg_color=('black', 'white'), corner_radius=8)
name_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
name_entry = customtkinter.CTkEntry(master=window, placeholder_text='Name', width=180, height=25, border_width=2, corner_radius=10)
name_entry.place(relx=0.55, rely=0.3, anchor=tk.CENTER)

age_label = customtkinter.CTkLabel(master=window, text='Age', width=80, height=25, text_color='black', fg_color=('black', 'white'), corner_radius=8)
age_label.place(relx=0.3, rely=0.39, anchor=tk.CENTER)
age_entry = customtkinter.CTkEntry(master=window, placeholder_text='Age', width=180, height=25, border_width=2, corner_radius=10)
age_entry.place(relx=0.55, rely=0.39, anchor=tk.CENTER)

father_name_label = customtkinter.CTkLabel(master=window, text='Father', width=80, height=25, text_color='black', fg_color=('black', 'white'), corner_radius=8)
father_name_label.place(relx=0.3, rely=0.48, anchor=tk.CENTER)
father_name_entry = customtkinter.CTkEntry(master=window, placeholder_text='Father Name', width=180, height=25, border_width=2, corner_radius=10)
father_name_entry.place(relx=0.55, rely=0.48, anchor=tk.CENTER)

mobile_number_label = customtkinter.CTkLabel(master=window, text='Mobile No.', width=80, height=25, text_color='black', fg_color=('black', 'white'), corner_radius=8)
mobile_number_label.place(relx=0.3, rely=0.57, anchor=tk.CENTER)
mobile_number_entry = customtkinter.CTkEntry(master=window, placeholder_text='Mobile No.', width=180, height=25, border_width=2, corner_radius=10)
mobile_number_entry.place(relx=0.55, rely=0.57, anchor=tk.CENTER)

# Create image selection button and label
image_select_button = customtkinter.CTkButton(master=window, width=80, height=32, border_width=0, corner_radius=8, text="Select Image", command=browse_image)
image_select_button.place(relx=0.5, rely=0.73, anchor=tk.CENTER)
image_path_label = customtkinter.CTkLabel(master=window, text='No Image Selected!', text_color='grey')
image_path_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

# Create submit button
submit_button = customtkinter.CTkButton(master=window, width=80, height=32, border_width=0, corner_radius=8, text="Submit", command=submit)
submit_button.place(relx=0.5, rely=0.83, anchor=tk.CENTER)

# Start the GUI event loop
window.mainloop()
