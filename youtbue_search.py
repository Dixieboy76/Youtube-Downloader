import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import webbrowser
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import re

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("800x550")
app.title("YouTube Search")

def open_link(event):
    try:
        index = out_put_textbox.index("@%s,%s" % (event.x, event.y))
        line_start = f"{index.split('.')[0]}.0"
        line_end = f"{index.split('.')[0]}.end"
        line_text = out_put_textbox.get(line_start, line_end)
        url = re.search(r'https?://\S+', line_text)
        if url:
            webbrowser.open_new_tab(url.group())
    except:
        pass

def search():
    query = search_entry.get()
    if not query:
        messagebox.showerror("Error", "Please enter a search query")
        return

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")  # Run in headless mode
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(options=options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        url = f"https://www.youtube.com/results?search_query={query}"
        driver.get(url)

        video_links = driver.find_elements(By.CSS_SELECTOR, 'a#video-title')
        video_titles = driver.find_elements(By.CSS_SELECTOR, 'a#video-title')

        if not video_links:
            messagebox.showinfo("No Results", "No videos found for this query")
            return

        out_put_textbox.delete(1.0, "end")  # Clear existing content

        for i in range(len(video_links)):
            # Concatenate video titles and URLs into a single string
            video_info = f"{video_titles[i].text}\n{video_links[i].get_attribute('href')}\n\n"
            # Insert concatenated string into the Text widget
            out_put_textbox.insert("end", video_info)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def clear():
    search_entry.delete(0, "end")

def save_list():
    """Save list to a file"""
    # Ask the user to select the file name and location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])

    # Check if the user cancelled the dialog
    if not file_path:
        return

    # Write the list data to the selected file
    with open(file_path, "w", encoding="utf-8") as file:
        # listbox.get() returns a tuple
        list_tuple = out_put_textbox.get(0, "end")
        for item in list_tuple:
            # Strip the newline character from each item before writing to the file
            file.write(item.strip() + "\n")

def download():
    try:
        url = link_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube video URL")
            return

        yt = YouTube(url)
        
        # Open file dialog for selecting download location
        download_path = filedialog.askdirectory()
        
        if download_path:
            stream = yt.streams.get_highest_resolution()
            stream.download(download_path)
            messagebox.showinfo("Success", "Video downloaded successfully")
        else:
            messagebox.showinfo("Cancelled", "Download cancelled by user")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def hide_download_frame():
    download_frame.pack_forget()

# def show_download_frame():
#     download_frame.pack()

def toggle_download_frame():
    if download_frame.winfo_ismapped():  # Check if the download frame is currently visible
        download_frame.pack_forget()  # If visible, hide the download frame
        app.geometry("800x550")  # Resize the window when the frame is hidden
    else:
        download_frame.pack()  # If hidden, show the download frame
        app.geometry("800x600")  # Resize the window when the frame is shown



output_frame = ctk.CTkFrame(app)
output_frame.pack(pady=(20, 0))

out_put_textbox = ctk.CTkTextbox(output_frame, width=745, height=400, wrap="word")
out_put_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
out_put_textbox.bind("<Double-1>", open_link)

search_entry = ctk.CTkEntry(app, placeholder_text="Enter your search query", width=745, height=40)
search_entry.pack(pady=10)
search_entry.bind("<Return>", lambda event: search())

button_frame = ctk.CTkFrame(app, width=545, height=50)
button_frame.pack(pady=10)

search_button = ctk.CTkButton(button_frame, text="Search", command=search)
search_button.grid(row=0, column=0, padx=10)

clear_button = ctk.CTkButton(button_frame, text="Clear Response", command=clear)
clear_button.grid(row=0, column=1, padx=10)

save_button = ctk.CTkButton(button_frame, text="Save List", command=save_list)
save_button.grid(row=0, column=2, padx=10)

quit_button = ctk.CTkButton(button_frame, text="Quit", command=app.destroy)
quit_button.grid(row=0, column=3, padx=10)

load_button = ctk.CTkButton(button_frame, text="Get Downloader", command=toggle_download_frame)
load_button.grid(row=0, column=4, padx=10)
load_button.configure(command=toggle_download_frame)

download_frame = ctk.CTkFrame(app)
download_frame.pack(pady=(5, 20))
download_frame.pack_forget()

link_entry = ctk.CTkEntry(download_frame, placeholder_text="Enter link", width=500, height=30)
link_entry.grid(row=0, column=0, padx=10, pady=10)

download_button = ctk.CTkButton(download_frame, text="Download", command=download)
download_button.grid(row=0, column=1, padx=10, pady=10)
download_button.configure(command=lambda: [hide_download_frame(), download()])


app.mainloop()
