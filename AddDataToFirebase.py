import tkinter as tk
from tkinter import filedialog
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
        image_label.config(text=file_path)

def submit():
    name = name_entry.get()
    age = age_entry.get()
    father_name = father_name_entry.get()
    mobile_number = mobile_number_entry.get()
    image = image_label.cget("text")
    
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



root = tk.Tk()
root.title("Submit Information")

# Name
name_label = tk.Label(root, text="Name:")
name_label.pack()

name_entry = tk.Entry(root)
name_entry.pack()

# Age
age_label = tk.Label(root, text="Age:")
age_label.pack()

age_entry = tk.Entry(root)
age_entry.pack()

# Father's Name
father_name_label = tk.Label(root, text="Father's Name:")
father_name_label.pack()

father_name_entry = tk.Entry(root)
father_name_entry.pack()

# Mobile Number
mobile_number_label = tk.Label(root, text="Mobile Number:")
mobile_number_label.pack()

mobile_number_entry = tk.Entry(root)
mobile_number_entry.pack()

# Image
image_label = tk.Label(root, text="No image selected")
image_label.pack()

browse_button = tk.Button(root, text="Browse", command=browse_image)
browse_button.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
