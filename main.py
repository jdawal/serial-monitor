import serial


def monitor_serial_port(port, baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(
            f"Monitoring serial port {port} at {baudrate} baudrate. Press Ctrl+C to exit."
        )

        while True:
            # Read data from the serial port
            data = ser.readline().decode("utf-8").strip()

            # Print the received data
            if data:
                print(f"Received data: {data}")

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")


if __name__ == "__main__":
    port_name = "COM4"  # Change this to the appropriate port name
    monitor_serial_port(port_name)
