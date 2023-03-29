import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders 


def select_folder():
    # Open a file dialog to select a folder
    root = tk.Tk() 
    root.withdraw() 
    
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return
    compress_folder(folder_path)

def compress_folder(folder_path):
    # Create a zip file with the same name as the folder
    zip_path = folder_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add all files and folders in the selected folder to the zip file
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zip_file.write(os.path.join(root, file))

    # Show a message box to confirm that the folder has been compressed
    messagebox.showinfo("A pasta foi zipada com sucesso")

    # Send the compressed file via email
    sender_email = sender_entry.get()
    receiver_emails = receiver_entry.get().split(',')
    send_email(zip_path, sender_email, receiver_emails)

def send_email(zip_path, sender_email, receiver_emails):
    # Set up the email parameters
    subject = 'Compressed folder'
    body = 'Please find attached the compressed folder.'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = COMMASPACE.join(receiver_emails)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Attach the compressed file to the email message
    with open(zip_path, 'rb') as file:
        part = MIMEBase('application', 'zip')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(zip_path)}"')
        message.attach(part)

    # Send the email
    with smtplib.SMTP('smtp_server_adress', 587) as server:
        server.starttls()
        server.login(sender_email, 'smtp_server_key')
        server.sendmail(sender_email, receiver_emails, message.as_string())

    # Show a message box to confirm that the email has been sent
    messagebox.showinfo("Arqui zipados enviados com sucesso")

# Create the main window
root = tk.Tk()
root.title("Folder Compressor") 
root.geometry("320x320") 
root.maxsize(width=320, height=320) 
canvas = tk.Canvas(height=100) 
title_label = tk.Label(root, text='XML envio', font="Arial 36") 
title_label.pack(pady=5) 


# # create a PhotoImage object by specifying the file path
# image = tk.PhotoImage(file="./logo_file.png")
# label = tk.Label(root, image=image)
# label.pack()


# Create a label and an entry for the sender email
sender_label = tk.Label(root, text="Email remetente:")
sender_label.pack(pady=5) 
sender_entry = tk.Entry(root, width=40)
sender_entry.pack(pady=5) 


# Create a label and an entry for the recipient email
receiver_label = tk.Label(root, text="Email destinatário:")
receiver_label.pack(pady=5) 
receiver_entry = tk.Entry(root, width=40)
receiver_entry.pack(pady=5)

# Create a button to select a folder
select_button = tk.Button(root, text="SELECIONAR & ENVIAR", command=select_folder, width=35, height=50, bg='orange')
select_button.pack(pady=20)

# Start the main event loop
root.mainloop()
