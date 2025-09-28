from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
import subprocess
import os
from threading import Thread

__version__ = "1.0"

class FileChooserPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        
        layout = BoxLayout(orientation='vertical')
        
        # Dosya seçici
        self.filechooser = FileChooserListView()
        self.filechooser.filters = ['*.mp4', '*.avi', '*.mkv', '*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
        layout.add_widget(self.filechooser)
        
        # Butonlar
        button_layout = BoxLayout(size_hint_y=None, height='48dp')
        
        select_btn = Button(text='Seç')
        select_btn.bind(on_press=self.select_file)
        
        cancel_btn = Button(text='İptal')
        cancel_btn.bind(on_press=self.dismiss)
        
        button_layout.add_widget(select_btn)
        button_layout.add_widget(cancel_btn)
        layout.add_widget(button_layout)
        
        self.content = layout
        self.title = 'Dosya Seç (Video/Fotoğraf)'
        self.size_hint = (0.9, 0.9)
    
    def select_file(self, instance):
        if self.filechooser.selection:
            self.callback(self.filechooser.selection[0])
        self.dismiss()

class SaveFilePopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        
        layout = BoxLayout(orientation='vertical')
        
        # Dosya seçici (klasör seçimi için)
        self.filechooser = FileChooserListView()
        self.filechooser.dirselect = True
        layout.add_widget(self.filechooser)
        
        # Dosya adı girişi
        self.filename_input = TextInput(
            hint_text='Dosya adını girin (örn: output.mp4 veya output.jpg)',
            size_hint_y=None,
            height='48dp',
            text='output.mp4'
        )
        layout.add_widget(self.filename_input)
        
        # Butonlar
        button_layout = BoxLayout(size_hint_y=None, height='48dp')
        
        save_btn = Button(text='Kaydet')
        save_btn.bind(on_press=self.save_file)
        
        cancel_btn = Button(text='İptal')
        cancel_btn.bind(on_press=self.dismiss)
        
        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)
        layout.add_widget(button_layout)
        
        self.content = layout
        self.title = 'Kaydetme Konumu Seç'
        self.size_hint = (0.9, 0.9)
    
    def save_file(self, instance):
        if self.filechooser.path and self.filename_input.text:
            full_path = os.path.join(self.filechooser.path, self.filename_input.text)
            self.callback(full_path)
        self.dismiss()

class MessagePopup(Popup):
    def __init__(self, title, message, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        
        label = Label(text=message, text_size=(None, None))
        layout.add_widget(label)
        
        ok_btn = Button(text='Tamam', size_hint_y=None, height='48dp')
        ok_btn.bind(on_press=self.dismiss)
        layout.add_widget(ok_btn)
        
        self.content = layout
        self.title = title
        self.size_hint = (0.8, 0.4)

class VideoUploaderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Video çözünürlük seçenekleri
        self.video_resolution_options = {
            '4K (2160p)': '3840:2160',
            '1440p': '2560:1440', 
            '1080p': '1920:1080',
            '720p': '1280:720',
            '480p': '854:480'
        }
        
        # Fotoğraf çözünürlük seçenekleri (MP)
        self.photo_resolution_options = {
            '12MP (4000x3000)': '4000:3000',
            '8MP (3264x2448)': '3264:2448',
            '5MP (2592x1944)': '2592:1944',
            '3MP (2048x1536)': '2048:1536',
            '2MP (1600x1200)': '1600:1200'
        }
        self.selected_resolution = '1920:1080'  # Varsayılan 1080p
        self.selected_resolution_name = '1080p'
        self.current_file_type = 'video'  # 'video' veya 'photo'
        self.current_resolution_options = self.video_resolution_options
    
    def build(self):
        # Ana layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Başlık
        title = Label(
            text='Video & Fotoğraf Yükseltici',
            size_hint_y=None,
            height='48dp',
            font_size='20sp'
        )
        main_layout.add_widget(title)
        
        # Giriş dosyası seçimi
        input_label = Label(
            text='Giriş Dosyası (Video/Fotoğraf):',
            size_hint_y=None,
            height='32dp'
        )
        main_layout.add_widget(input_label)
        
        self.input_text = TextInput(
            hint_text='Seçilen dosya (video/fotoğraf) burada görünecek',
            readonly=True,
            size_hint_y=None,
            height='48dp'
        )
        main_layout.add_widget(self.input_text)
        
        select_btn = Button(
            text='Video Seç',
            size_hint_y=None,
            height='48dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        select_btn.bind(on_press=self.select_video)
        main_layout.add_widget(select_btn)
        
        # Çözünürlük seçimi
        resolution_label = Label(
            text='Hedef Çözünürlük:',
            size_hint_y=None,
            height='32dp'
        )
        main_layout.add_widget(resolution_label)
        
        # Çözünürlük butonları
        self.resolution_grid = GridLayout(cols=3, size_hint_y=None, height='100dp', spacing=5)
        
        self.resolution_buttons = {}
        self.update_resolution_buttons()
        
        main_layout.add_widget(self.resolution_grid)
        
        # Seçilen çözünürlük göstergesi
        self.resolution_status = Label(
            text=f'Seçilen çözünürlük: {self.selected_resolution_name}',
            size_hint_y=None,
            height='32dp'
        )
        main_layout.add_widget(self.resolution_status)
        
        # Boşluk
        main_layout.add_widget(Label(size_hint_y=None, height='20dp'))
        
        # Yükseltme butonu
        self.upscale_btn = Button(
            text=f'Çözünürlüğü Yükselt ({self.selected_resolution_name})',
            size_hint_y=None,
            height='60dp',
            background_color=(0, 0.8, 0, 1),
            font_size='16sp'
        )
        self.upscale_btn.bind(on_press=self.upscale_video)
        main_layout.add_widget(self.upscale_btn)
        
        # Durum etiketi
        self.status_label = Label(
            text='Video seçin ve yükseltme işlemini başlatın',
            size_hint_y=None,
            height='32dp'
        )
        main_layout.add_widget(self.status_label)
        
        return main_layout
    
    def update_resolution_buttons(self):
        # Önceki butonları temizle
        self.resolution_grid.clear_widgets()
        self.resolution_buttons = {}
        
        # Yeni butonları ekle
        for res_name, res_value in self.current_resolution_options.items():
            btn = Button(
                text=res_name,
                background_color=(0.3, 0.3, 0.3, 1) if res_name != self.selected_resolution_name else (0, 0.8, 0, 1)
            )
            btn.bind(on_press=lambda x, name=res_name, value=res_value: self.select_resolution(name, value))
            self.resolution_buttons[res_name] = btn
            self.resolution_grid.add_widget(btn)
    
    def detect_file_type(self, filepath):
        # Dosya uzantısından türü belirle
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']:
            return 'video'
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
            return 'photo'
        return 'unknown'
    
    def select_resolution(self, res_name, res_value):
        # Önceki seçimi sıfırla
        for name, btn in self.resolution_buttons.items():
            btn.background_color = (0.3, 0.3, 0.3, 1)
        
        # Yeni seçimi vurgula
        self.resolution_buttons[res_name].background_color = (0, 0.8, 0, 1)
        
        # Seçili çözünürlüğü güncelle
        self.selected_resolution = res_value
        self.selected_resolution_name = res_name
        
        # UI'yi güncelle
        file_type_text = 'Video' if self.current_file_type == 'video' else 'Fotoğraf'
        self.resolution_status.text = f'Seçilen çözünürlük: {self.selected_resolution_name}'
        self.upscale_btn.text = f'{file_type_text} Çözünürlüğünü Yükselt ({self.selected_resolution_name})'
    
    def select_video(self, instance):
        popup = FileChooserPopup(self.on_video_selected)
        popup.open()
    
    def on_video_selected(self, filepath):
        self.input_text.text = filepath
        
        # Dosya türünü belirle
        self.current_file_type = self.detect_file_type(filepath)
        
        # Çözünürlük seçeneklerini güncelle
        if self.current_file_type == 'photo':
            self.current_resolution_options = self.photo_resolution_options
            self.selected_resolution = '2592:1944'  # 5MP varsayılan
            self.selected_resolution_name = '5MP (2592x1944)'
        else:
            self.current_resolution_options = self.video_resolution_options
            self.selected_resolution = '1920:1080'  # 1080p varsayılan
            self.selected_resolution_name = '1080p'
        
        # UI'yi güncelle
        self.update_resolution_buttons()
        file_type_text = 'Fotoğraf' if self.current_file_type == 'photo' else 'Video'
        self.status_label.text = f'Seçilen {file_type_text.lower()}: {os.path.basename(filepath)}'
        self.resolution_status.text = f'Seçilen çözünürlük: {self.selected_resolution_name}'
        self.upscale_btn.text = f'{file_type_text} Çözünürlüğünü Yükselt ({self.selected_resolution_name})'
    
    def upscale_video(self, instance):
        input_path = self.input_text.text
        if not input_path:
            file_type_text = 'Fotoğraf' if self.current_file_type == 'photo' else 'Video'
            popup = MessagePopup('Hata', f'Lütfen bir {file_type_text.lower()} dosyası seçin.')
            popup.open()
            return
        
        # Kaydetme konumu seç
        save_popup = SaveFilePopup(self.on_save_location_selected)
        save_popup.open()
    
    def on_save_location_selected(self, output_path):
        input_path = self.input_text.text
        
        # Yükseltme işlemini arka planda başlat
        self.upscale_btn.disabled = True
        file_type_text = 'Fotoğraf' if self.current_file_type == 'photo' else 'Video'
        self.status_label.text = f'{file_type_text} yükseltme işlemi başladı. Lütfen bekleyin...'
        
        if self.current_file_type == 'photo':
            thread = Thread(target=self.run_photo_upscale, args=(input_path, output_path))
        else:
            thread = Thread(target=self.run_ffmpeg, args=(input_path, output_path))
        
        thread.daemon = True
        thread.start()
    
    def run_ffmpeg(self, input_path, output_path):
        command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={self.selected_resolution}:flags=lanczos',
            '-c:v', 'libx264',
            '-preset', 'slow',
            '-crf', '18',
            output_path
        ]
        
        try:
            subprocess.run(command, check=True)
            self.show_success_message(output_path)
        except FileNotFoundError:
            self.show_error_message('FFmpeg bulunamadı. Lütfen sisteminize kurup PATH\'e eklediğinizden emin olun.')
        except subprocess.CalledProcessError as e:
            self.show_error_message(f'FFmpeg hatası oluştu: {e}')
        finally:
            # UI güncellemelerini ana thread'de yap
            from kivy.clock import Clock
            Clock.schedule_once(self.reset_ui, 0)
    
    def run_photo_upscale(self, input_path, output_path):
        # FFmpeg ile fotoğraf yükseltme
        command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={self.selected_resolution}:flags=lanczos',
            '-q:v', '2',  # Yüksek kalite için
            output_path
        ]
        
        try:
            subprocess.run(command, check=True)
            self.show_success_message(output_path)
        except FileNotFoundError:
            self.show_error_message('FFmpeg bulunamadı. Lütfen sisteminize kurup PATH\'e eklediğinizden emin olun.')
        except subprocess.CalledProcessError as e:
            self.show_error_message(f'FFmpeg hatası oluştu: {e}')
        finally:
            # UI güncellemelerini ana thread'de yap
            from kivy.clock import Clock
            Clock.schedule_once(self.reset_ui, 0)
    
    def show_success_message(self, output_path):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._show_success_popup(output_path), 0)
    
    def show_error_message(self, message):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._show_error_popup(message), 0)
    
    def _show_success_popup(self, output_path):
        file_type_text = 'Fotoğraf' if self.current_file_type == 'photo' else 'Video'
        popup = MessagePopup('Başarılı', f'{file_type_text} başarıyla şuraya kaydedildi:\n{output_path}')
        popup.open()
    
    def _show_error_popup(self, message):
        popup = MessagePopup('Hata', message)
        popup.open()
    
    def reset_ui(self, dt):
        self.upscale_btn.disabled = False
        self.status_label.text = 'İşlem tamamlandı'

if __name__ == '__main__':
    VideoUploaderApp().run()
