import serial
import logging

# Configure logging to write to a text file
logging.basicConfig(
    filename="serial_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


def monitor_serial_port(port, baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(
            f"Monitoring serial port {port} at {baudrate} baudrate. Press Ctrl+C to exit."
        )

        while True:
            try:
                # Read data from the serial port as binary
                data = ser.read(ser.in_waiting)

                # Print the received data as raw bytes
                if data:
                    received_data = data.hex()
                    print(f"Received data (raw bytes): {data}")
                    print(f"Received HEX data: {received_data}")

                    # Log the received data to the text file
                    logging.info(f"Received data (raw bytes): {data}")
                    logging.info(f"Received HEX data: {received_data}")

                    # bytesData = "b'\x02'b'\x06'b'\xb1'b'\x03b'\x07"
                    hex_input = "02064d0307"
                    hex_data = bytes.fromhex(hex_input)

                    ser.write(hex_data)

            except serial.SerialException as e:
                print(f"Serial port error: {e}")
                logging.error(f"Serial port error: {e}")

    except serial.SerialException as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")


if __name__ == "__main__":
    port_name = "COM5"  # Change this to the appropriate port name
    monitor_serial_port(port_name)
