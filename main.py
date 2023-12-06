import serial
import os
import time
import configparser
import logging

# Configure logging to write to a text file
logging.basicConfig(
    filename="serial_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


# Read config function
def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


# Setup logger
def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


# MAIN FUNCTION TO MONITOR SERIAL
def monitor_serial_port(port, baudrate=9600, log_folder="C:\\logs", log_interval=10):
    try:
        # Ensure the logs folder exists
        os.makedirs(log_folder, exist_ok=True)

        ser = serial.Serial(port, baudrate, timeout=1)
        logging.info(
            f"Monitoring serial port {port} at {baudrate} baudrate. Press Ctrl+C to exit."
        )

        while True:
            # Read raw bytes from the serial port
            data = ser.read(ser.in_waiting)

            # Print the decoded UTF-8 representation of the raw bytes
            if data:
                try:
                    decoded_data = data.decode("utf-8")
                    hex_data = data.hex()
                    logging.info(f"Received data: {decoded_data}, Hex: {hex_data}")
                except UnicodeDecodeError as decode_error:
                    logging.error(f"Error decoding data: {decode_error}")

            # Log data to a text file based on the specified interval
            if time.time() % log_interval == 0:
                log_serial_data(decoded_data, log_folder)

    except serial.SerialException as e:
        logging.error(f"Error: {e}")
    except KeyboardInterrupt:
        logging.info("\nMonitoring stopped.")
    finally:
        if ser.is_open:
            ser.close()
            logging.info("Serial port closed.")


def log_serial_data(data, log_folder):
    log_file_path = os.path.join(log_folder, "serial_log.txt")
    with open(log_file_path, "a") as file:
        file.write(f"{time.ctime()}: {data}\n")


if __name__ == "__main__":
    setup_logger()
    config = read_config()
    serial_port = config.get("SerialConfig", "port")
    serial_baudrate = config.getint("SerialConfig", "baudrate")

    log_folder = config.get("LogConfig", "folder")
    log_interval = config.getint("LogConfig", "interval")

    monitor_serial_port(serial_port, serial_baudrate, log_folder, log_interval)
