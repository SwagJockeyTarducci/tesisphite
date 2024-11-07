from machine import UART, Pin
import time
import urequests
import ubinascii
import libreriafingerprint as fingerprint

# Configuración del UART y el sensor AS608
uart = UART(2, baudrate=57600, tx=17, rx=16)
time.sleep(2)
sensor = fingerprint.PyFingerprint(uart)

# Set the packet size to 64 bytes for testing
sensor.setMaxPacketSize(64)  # Ensure this method is supported by your library

def capturar_y_convertir(char_buffer):
    print("Por favor, coloca tu dedo en el sensor...")
    while not sensor.readImage():
        time.sleep(2)
        print("Intentando capturar la imagen...")

    if sensor.convertImage(char_buffer):
        print("Imagen capturada y convertida correctamente.")
        time.sleep(2)
        return True
    else:
        print("Error al convertir la imagen.")
        return False

def enviar_huella_a_servidor(template):
    url = "http://192.168.2.193/TESISLAUTAROCOLLINO/TESTINGLOGIN/public/guardarhuella"
    # Reemplaza con la IP de tu PC
    headers = {'Content-Type': 'application/json'}
    data = {'template': template}

    try:
        response = urequests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Huella enviada y guardada en la base de datos.")
        else:
            print("Error al guardar la huella:", response.text)
        response.close()
    except Exception as e:
        print("Error de conexión al servidor:", e)

def comparar_y_guardar_huella():
    if not capturar_y_convertir(fingerprint.FINGERPRINT_CHARBUFFER1):
        print("Error en la captura de la huella.")
        return

    try:
        characteristics = sensor.downloadCharacteristics(fingerprint.FINGERPRINT_CHARBUFFER1)
        if characteristics:
            template = ubinascii.b2a_base64(bytes(characteristics)).decode('utf-8')
            enviar_huella_a_servidor(template)
        else:
            print("No se pudieron descargar las características de la huella.")
    except Exception as e:
        print("Error al descargar las características:", e)

# Ejecutar la función para capturar y enviar la huella
comparar_y_guardar_huella()
