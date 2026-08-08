# 🎛️ StreamDeck Casero con ESP32 (10 Botones)

Este proyecto permite construir un **StreamDeck físico de 10 botones** económico utilizando un microcontrolador **ESP32** y un panel de control en **Python (CustomTkinter)** para Windows.

Permite controlar el volumen del sistema, silenciar/desmutear el micrófono de Windows, controlar reproducción multimedia y enviar teclas virtuales de función (`F13` a `F20`) para vincular atajos directos en **OBS Studio**.

---

## 🚀 Características

* **🔊 Control de Audio en Windows:** Subir/bajar volumen, fijar niveles exactos (50%, 100%) y Mute/Unmute general.
* **🎙️ Mute de Micrófono General:** Silencia o reactiva el micrófono del sistema nativamente a nivel de Windows.
* **🎥 Integración con OBS Studio:** Envía teclas especiales (`F13` a `F20`) para  atajos de cambio de escena, inicio/fin de grabación o silenciar fuentes.
* **⌨️ Atajos de Teclado Personalizados:** Configura combinaciones de teclas (ej. `ctrl+shift+r`) o lanzadores de aplicaciones (`.exe`).
* **🎨 Interfaz Gráfica Moderna:** Panel de control en modo oscuro construido con `CustomTkinter`.
* **🔌 Detección Automática de COM:** Reconexión por puerto serie tras desconexiones físicas.

---

## 🛠️ Requisitos de Hardware

1. **ESP32** (NodeMCU ESP32 o similar).
2. **10 Pulsadores/Botones** (push buttons).
3. Cable USB a Micro-USB/USB-C (para transmisión de datos).
4. Cables de conexión (Jumper wires).

### 🔌 Esquema de Conexión (GPIO)

Cada botón se conecta entre el pin GPIO indicado y el pin **GND** común del ESP32 (utiliza las resistencias PULLUP internas de la placa):

* **Botón 1:** GPIO 12
* **Botón 2:** GPIO 13
* **Botón 3:** GPIO 14
* **Botón 4:** GPIO 27
* **Botón 5:** GPIO 26
* **Botón 6:** GPIO 25
* **Botón 7:** GPIO 33
* **Botón 8:** GPIO 32
* **Botón 9:** GPIO 15
* **Botón 10:** GPIO 23

---

## 💻 Instalación del Software

### 1. 🤖 Cargar el Firmware al ESP32
1. Abre el IDE de Arduino.
2. Carga el código contenido en `streamdeck_esp32.ino`.
3. Selecciona la placa **ESP32 Dev Module** y el puerto COM asignado.
4. Sube el programa a la placa.

### 2. 🐍 Configurar la Aplicación Python
1. Clona o descarga este repositorio.
2. Instala las dependencias necesarias ejecutando:
   ```cmd
   pip install -r requirements.txt

### 3. ▶️ Ejecuta la aplicación de escritorio en modo de desarrollo
1. Instala en
   ```cmd 
	 python streamdeck_app.py 

### 4. 📦 Crear el Ejecutable (.exe)
Si deseas generar la aplicación independiente para usarla sin abrir la consola de comandos 
python -m PyInstaller --noconsole --onefile --collect-all customtkinter streamdeck_app.py
El ejecutable listo para usar se generará dentro de la carpeta dist/

### 5. 🎬Configuración en OBS Studio
1. Abre el panel de control de la app Python y asigna funciones Tecla F13 a Tecla F20 a los botones deseados
2. Abre OBS Studio → Ajustes → Atajos
3. Selecciona la acción deseada (ej. Iniciar grabación) y presiona el botón físico correspondiente en el StreamDeck. OBS reconocerá  la tecla de asignada.
