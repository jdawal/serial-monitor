import serial
import tkinter as tk
from tkinter import ttk


def calculate_nmea_checksum(sentence):
    data = sentence[1:-3]
    checksum = ord(data[0])
    for char in data[1:]:
        checksum ^= ord(char)
    return format(checksum, "02X")


def send_serial_message(ser, user_input, output_text):
    if user_input:
        hex_data = bytes.fromhex(user_input)
        checksum = calculate_nmea_checksum(hex_data.decode("utf-8"))
        complete_message = f"${user_input}*{checksum}\r\n"
        ser.write(complete_message.encode("utf-8"))
        output_text.insert(tk.END, f"Sent message: {complete_message}\n")


def monitor_serial_data(ser, output_text):
    while True:
        received_data = ser.readline().decode("utf-8").strip()
        if "GNGLL" in received_data:
            output_text.insert(tk.END, f"Received data: {received_data}\n")
        output_text.update_idletasks()


def monitor_and_respond_gui(port, baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)

        # Create the main window
        window = tk.Tk()
        window.title("Serial Monitor")

        # Create and pack widgets
        label = ttk.Label(window, text="Enter a hex message:")
        label.pack(pady=10)

        input_entry = ttk.Entry(window)
        input_entry.pack(pady=10)

        send_button = ttk.Button(window, text="Send", command=lambda: on_send_button())
        send_button.pack(pady=10)

        output_text = tk.Text(window, height=10, width=50)
        output_text.pack(pady=10)

        # Start a separate thread to continuously monitor serial data
        import threading

        thread = threading.Thread(target=lambda: monitor_serial_data(ser, output_text))
        thread.daemon = True
        thread.start()

        def on_send_button():
            user_input = input_entry.get()
            send_serial_message(ser, user_input, output_text)

        window.mainloop()

    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")


if __name__ == "__main__":
    port_name = "COM4"  # Change this to the appropriate port name
    monitor_and_respond_gui(port_name)
