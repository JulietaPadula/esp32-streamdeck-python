import ctypes
import json
import os
import subprocess
import threading
import time
import customtkinter as ctk
import pyautogui
import serial
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config_deck.json"


# --- FUNCIONES DE AUDIO Y MICRÓFONO NATIVAS ---
def adjust_volume(change_pct):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        current_vol = volume.GetMasterVolumeLevelScalar()
        new_vol = max(0.0, min(1.0, current_vol + (change_pct / 100.0)))
        volume.SetMasterVolumeLevelScalar(new_vol, None)
    except Exception as e:
        print(f"Error de volumen: {e}")


def set_volume_exact(pct):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(pct / 100.0, None)
    except Exception as e:
        print(f"Error fijando volumen: {e}")


def toggle_microphone_mute():
    try:
        devices = AudioUtilities.GetMicrophone()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        current_mute = volume.GetMute()
        volume.SetMute(not current_mute, None)
    except Exception as e:
        print(f"Error muteando microfono: {e}")


# --- CATÁLOGO DE ACCIONES Y HOTKEYS ---
ACCIONES_ESPECIALES = {
    "Subir Volumen (+10%)": "VOL_UP",
    "Bajar Volumen (-10%)": "VOL_DOWN",
    "Volumen al 50%": "VOL_50",
    "Volumen al 100%": "VOL_100",
    "Mute / Unmute Audio PC": "ACTION_MUTE",
    "Mute / Unmute Microfono": "MUTE_MIC",
    "Play / Pausa Música": "MEDIA_PLAY_PAUSE",
    "Siguiente Canción": "MEDIA_NEXT",
    "Canción Anterior": "MEDIA_PREV",
    "Captura de Pantalla": "SCREENSHOT",
    "Tecla F13 (OBS / Hotkey)": "HOTKEY_F13",
    "Tecla F14 (OBS / Hotkey)": "HOTKEY_F14",
    "Tecla F15 (OBS / Hotkey)": "HOTKEY_F15",
    "Tecla F16 (OBS / Hotkey)": "HOTKEY_F16",
    "Tecla F17 (OBS / Hotkey)": "HOTKEY_F17",
    "Tecla F18 (OBS / Hotkey)": "HOTKEY_F18",
    "Tecla F19 (OBS / Hotkey)": "HOTKEY_F19",
    "Tecla F20 (OBS / Hotkey)": "HOTKEY_F20",
    "Atajo Personalizado (Hotkey)...": "CUSTOM_HOTKEY",
}


class StreamDeckApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("StreamDeck 10 Botones - Panel de Control")
        self.geometry("680x680")
        self.resizable(False, False)

        self.config_data = self.load_config()
        self.is_running = True

        self.setup_ui()
        self.start_serial_listener()

    def load_config(self):
        default_apps = {
            f"BUTTON{i}": "Mute / Unmute Audio PC" for i in range(1, 11)
        }
        default_apps["BUTTON1"] = "Subir Volumen (+10%)"
        default_apps["BUTTON2"] = "Bajar Volumen (-10%)"
        default_apps["BUTTON3"] = "Mute / Unmute Microfono"
        default_apps["BUTTON4"] = "Tecla F13 (OBS / Hotkey)"

        default = {"COM_PORT": "COM3", "apps": default_apps}

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return default
        return default

    def save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, indent=4)

    def setup_ui(self):
        title_label = ctk.CTkLabel(
            self,
            text="🎛️ StreamDeck ESP32 (10 Botones)",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(pady=(15, 5))

        com_frame = ctk.CTkFrame(self)
        com_frame.pack(fill="x", padx=20, pady=5)

        com_label = ctk.CTkLabel(com_frame, text="Puerto COM:")
        com_label.pack(side="left", padx=10, pady=8)

        self.com_entry = ctk.CTkEntry(com_frame, width=80)
        self.com_entry.insert(0, self.config_data.get("COM_PORT", "COM3"))
        self.com_entry.pack(side="left", padx=5)

        btn_save_com = ctk.CTkButton(
            com_frame,
            text="Guardar COM",
            width=90,
            command=self.update_com_port,
        )
        btn_save_com.pack(side="left", padx=10)

        self.buttons_frame = ctk.CTkScrollableFrame(
            self, width=620, height=470, label_text="Mapeo de Pines / Botones"
        )
        self.buttons_frame.pack(pady=10)

        self.widget_map = {}
        for i in range(1, 11):
            btn_id = f"BUTTON{i}"
            self.create_button_row(btn_id)

        self.status_label = ctk.CTkLabel(
            self,
            text="Estado: Iniciando...",
            text_color="gray",
            font=ctk.CTkFont(size=12),
        )
        self.status_label.pack(side="bottom", pady=8)

    def create_button_row(self, btn_id):
        row_frame = ctk.CTkFrame(self.buttons_frame)
        row_frame.pack(fill="x", pady=4, padx=5)

        lbl = ctk.CTkLabel(
            row_frame,
            text=f"{btn_id}:",
            width=75,
            font=ctk.CTkFont(weight="bold"),
        )
        lbl.pack(side="left", padx=5)

        val_actual = self.config_data["apps"].get(btn_id, "")

        options = list(ACCIONES_ESPECIALES.keys()) + [
            "Abrir Programa (.exe)..."
        ]
        combo = ctk.CTkOptionMenu(
            row_frame,
            values=options,
            width=230,
            command=lambda choice, b=btn_id: self.on_option_selected(choice, b),
        )
        combo.pack(side="left", padx=5)

        if val_actual in ACCIONES_ESPECIALES:
            combo.set(val_actual)
        else:
            combo.set("Abrir Programa (.exe)...")

        path_entry = ctk.CTkEntry(
            row_frame, width=220, placeholder_text="Acción, atajo o .exe"
        )
        path_entry.insert(0, val_actual)
        path_entry.pack(side="left", padx=5)

        self.widget_map[btn_id] = {"combo": combo, "entry": path_entry}

    def on_option_selected(self, choice, btn_id):
        entry = self.widget_map[btn_id]["entry"]
        if choice == "Abrir Programa (.exe)...":
            file_path = ctk.filedialog.askopenfilename(
                title="Seleccionar Ejecutable",
                filetypes=[("Ejecutables", "*.exe"), ("Todos", "*.*")],
            )
            if file_path:
                entry.delete(0, "end")
                entry.insert(0, file_path)
                self.config_data["apps"][btn_id] = file_path
                self.save_config()
        elif choice == "Atajo Personalizado (Hotkey)...":
            dialog = ctk.CTkInputDialog(
                text="Ingresa la combinación (ejemplo: ctrl+shift+r o alt+f10):",
                title="Atajo de Teclado",
            )
            shortcut = dialog.get_input()
            if shortcut:
                entry.delete(0, "end")
                entry.insert(0, shortcut.strip().lower())
                self.config_data["apps"][btn_id] = shortcut.strip().lower()
                self.save_config()
        else:
            entry.delete(0, "end")
            entry.insert(0, choice)
            self.config_data["apps"][btn_id] = choice
            self.save_config()

    def update_com_port(self):
        new_com = self.com_entry.get().strip()
        self.config_data["COM_PORT"] = new_com
        self.save_config()
        self.status_label.configure(
            text=f"COM actualizado a {new_com}.", text_color="yellow"
        )

    def start_serial_listener(self):
        threading.Thread(target=self.listen_serial, daemon=True).start()

    def listen_serial(self):
        while self.is_running:
            com = self.config_data.get("COM_PORT", "COM3")
            try:
                ser = serial.Serial(com, 115200, timeout=1)
                self.status_label.configure(
                    text=f"Conectado a ESP32 en {com}", text_color="green"
                )
                while self.is_running:
                    msg = ser.readline().decode(errors="ignore").strip()
                    if msg:
                        self.ejecutar_accion(msg)
                    time.sleep(0.02)
            except Exception:
                self.status_label.configure(
                    text=f"Buscando ESP32 en {com}...", text_color="orange"
                )
                time.sleep(2)

    def ejecutar_accion(self, btn_id):
        if btn_id not in self.config_data["apps"]:
            return

        target = self.config_data["apps"][btn_id]

        if target in ACCIONES_ESPECIALES:
            code = ACCIONES_ESPECIALES[target]
            if code == "VOL_UP":
                adjust_volume(10)
            elif code == "VOL_DOWN":
                adjust_volume(-10)
            elif code == "VOL_50":
                set_volume_exact(50)
            elif code == "VOL_100":
                set_volume_exact(100)
            elif code == "ACTION_MUTE":
                pyautogui.press("volumemute")
            elif code == "MUTE_MIC":
                toggle_microphone_mute()
            elif code == "MEDIA_PLAY_PAUSE":
                pyautogui.press("playpause")
            elif code == "MEDIA_NEXT":
                pyautogui.press("nexttrack")
            elif code == "MEDIA_PREV":
                pyautogui.press("prevtrack")
            elif code == "SCREENSHOT":
                pyautogui.hotkey("win", "shift", "s")
            elif code.startswith("HOTKEY_"):
                key_name = code.replace("HOTKEY_", "").lower()  # f13, f14...
                pyautogui.press(key_name)

        elif "+" in target:
            # Atajo personalizado como 'ctrl+shift+r'
            keys = [k.strip() for k in target.split("+")]
            pyautogui.hotkey(*keys)

        elif os.path.exists(target):
            subprocess.Popen([target])


if __name__ == "__main__":
    app = StreamDeckApp()
    app.mainloop()