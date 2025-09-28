import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess # Komut satırı komutlarını çalıştırmak için

# Video çözünürlük seçenekleri
video_resolution_options = {
    "4K (2160p)": "3840:2160",
    "1440p": "2560:1440", 
    "1080p": "1920:1080",
    "720p": "1280:720",
    "480p": "854:480"
}

# Fotoğraf çözünürlük seçenekleri (MP)
photo_resolution_options = {
    "12MP (4000x3000)": "4000:3000",
    "8MP (3264x2448)": "3264:2448",
    "5MP (2592x1944)": "2592:1944",
    "3MP (2048x1536)": "2048:1536",
    "2MP (1600x1200)": "1600:1200"
}

# Varsayılan seçenekler
current_resolution_options = video_resolution_options
current_file_type = 'video'

def select_video():
    filepath = filedialog.askopenfilename(
        title="Dosya Seçin (Video/Fotoğraf)",
        filetypes=(
            ("Video Dosyaları", "*.mp4 *.avi *.mkv *.mov *.wmv"), 
            ("Fotoğraf Dosyaları", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("Tüm Dosyalar", "*.*")
        )
    )
    if filepath:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, filepath)
        
        # Dosya türünü belirle ve çözünürlük seçeneklerini güncelle
        update_resolution_options(filepath)

def update_resolution_options(filepath):
    global current_resolution_options, current_file_type
    
    # Dosya uzantısından türü belirle
    import os
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
        current_file_type = 'photo'
        current_resolution_options = photo_resolution_options
        # Widget'ların var olup olmadığını kontrol et
        if 'resolution_var' in globals():
            resolution_var.set("5MP (2592x1944)")  # Varsayılan fotoğraf çözünürlüğü
        if 'label_resolution' in globals():
            label_resolution.config(text="Hedef Çözünürlük (MP):")
        if 'btn_upscale' in globals():
            btn_upscale.config(text="Fotoğraf Çözünürlüğünü Yükselt")
    else:
        current_file_type = 'video'
        current_resolution_options = video_resolution_options
        # Widget'ların var olup olmadığını kontrol et
        if 'resolution_var' in globals():
            resolution_var.set("1080p")  # Varsayılan video çözünürlüğü
        if 'label_resolution' in globals():
            label_resolution.config(text="Hedef Çözünürlük:")
        if 'btn_upscale' in globals():
            btn_upscale.config(text="Video Çözünürlüğünü Yükselt")
    
    # ComboBox'u güncelle
    if 'resolution_combo' in globals():
        resolution_combo['values'] = list(current_resolution_options.keys())

def upscale_video():
    input_path = entry_input.get()
    if not input_path:
        file_type_text = "fotoğraf" if current_file_type == 'photo' else "video"
        messagebox.showerror("Hata", f"Lütfen bir {file_type_text} dosyası seçin.")
        return

    # Seçilen çözünürlüğü al
    selected_resolution_name = resolution_var.get()
    selected_resolution_value = current_resolution_options[selected_resolution_name]

    # Uygun dosya uzantısını belirle
    if current_file_type == 'photo':
        default_ext = ".jpg"
        file_types = (("JPEG Fotoğraf", "*.jpg"), ("PNG Fotoğraf", "*.png"))
    else:
        default_ext = ".mp4"
        file_types = (("MP4 Video", "*.mp4"),)
    
    output_path = filedialog.asksaveasfilename(
        title=f"Yükseltilmiş {current_file_type.title()}'u Kaydet",
        defaultextension=default_ext,
        filetypes=file_types
    )
    if not output_path:
        return

    if current_file_type == 'photo':
        # Fotoğraf işleme
        command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={selected_resolution_value}:flags=lanczos',
            '-q:v', '2',  # Yüksek kalite için
            output_path
        ]
        process_type = "Fotoğraf"
    else:
        # Video işleme
        command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={selected_resolution_value}:flags=lanczos',
            '-c:v', 'libx264',
            '-preset', 'slow',
            '-crf', '18',
            output_path
        ]
        process_type = "Video"

    try:
        # Komutu çalıştır ve tamamlanmasını bekle
        messagebox.showinfo("Başlatıldı", f"{process_type} {selected_resolution_name} çözünürlüğe yükseltme işlemi başladı. Bu işlem uzun sürebilir...")
        subprocess.run(command, check=True)
        messagebox.showinfo("Başarılı", f"{process_type} başarıyla şuraya kaydedildi: {output_path}")
    except FileNotFoundError:
        messagebox.showerror("Hata", "FFmpeg bulunamadı. Lütfen sisteminize kurup PATH'e eklediğinizden emin olun.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hata", f"FFmpeg hatası oluştu: {e}")


# Arayüzü oluşturma
root = tk.Tk()
root.title("Video & Fotoğraf Yükseltici")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Girdi yolu için etiket ve giriş kutusu
label_input = tk.Label(frame, text="Giriş Dosyası (Video/Fotoğraf):")
label_input.pack()
entry_input = tk.Entry(frame, width=50)
entry_input.pack()
btn_select = tk.Button(frame, text="Dosya Seç", command=select_video)
btn_select.pack(pady=5)

# Çözünürlük seçimi
label_resolution = tk.Label(frame, text="Hedef Çözünürlük:")
label_resolution.pack(pady=(10, 5))

resolution_var = tk.StringVar(value="1080p")  # Varsayılan değer
resolution_combo = ttk.Combobox(frame, textvariable=resolution_var, values=list(current_resolution_options.keys()), state="readonly")
resolution_combo.pack(pady=5)

# Yükseltme butonu
btn_upscale = tk.Button(frame, text="Çözünürlüğü Yükselt", command=upscale_video, bg="green", fg="white")
btn_upscale.pack(pady=20)

root.mainloop()


