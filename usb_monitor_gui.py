import time

import usb.core
import usb.util
import logging
import tkinter as tk
from tkinter import scrolledtext

# Configure logging to save USB events to a file
logging.basicConfig(filename='usb_monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class USBMonitorGUI:
    def __init__(self):
        # Create the main Tkinter window
        self.root = tk.Tk()
        self.root.title("USB Monitor Tool")
        self.root.geometry("600x400")

        # Create a scrolled text area for displaying logs
        self.log_text = scrolledtext.ScrolledText(self.root, width=80, height=20, wrap=tk.WORD)
        self.log_text.pack(pady=10)

        # Create buttons for starting, stopping monitoring, and getting device info
        self.start_button = tk.Button(self.root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.device_info_button = tk.Button(self.root, text="Get Device Info", command=self.get_device_info)
        self.device_info_button.pack(pady=5)

        # Initialize monitoring state variable
        self.monitoring = False

    def log_usb_event(self, event_type, device):
        # Log USB events and display in the text area
        info = f"{event_type} - Vendor ID: {device.idVendor}, Product ID: {device.idProduct}, Serial Number: {device.serial_number}"
        logging.info(info)
        self.log_text.insert(tk.END, info + "\n")
        self.log_text.see(tk.END)

    def monitor_usb_events(self):
        # Continuous monitoring of USB events
        while self.monitoring:
            # Get the list of connected devices before and after a short delay
            devices_before = set([device.serial_number for device in usb.core.find(find_all=True)])
            time.sleep(1)
            devices_after = set([device.serial_number for device in usb.core.find(find_all=True)])

            # Identify new and removed devices
            new_devices = devices_after - devices_before
            removed_devices = devices_before - devices_after

            # Log and display events
            if new_devices:
                for serial_number in new_devices:
                    device = usb.core.find(serial_number=serial_number)
                    if device is not None:
                        self.log_usb_event("Device Connected", device)

            if removed_devices:
                for serial_number in removed_devices:
                    device = usb.core.find(serial_number=serial_number)
                    if device is not None:
                        self.log_usb_event("Device Removed", device)

    def start_monitoring(self):
        # Start monitoring when the button is clicked
        if not self.monitoring:
            self.monitoring = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.device_info_button.config(state=tk.DISABLED)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "Monitoring started...\n")
            self.log_text.see(tk.END)
            self.monitor_usb_events()

    def stop_monitoring(self):
        # Stop monitoring when the button is clicked
        if self.monitoring:
            self.monitoring = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.device_info_button.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, "Monitoring stopped.\n")
            self.log_text.see(tk.END)

    def get_device_info(self):
        # Fetch and display information about connected USB devices
        devices = usb.core.find(find_all=True)
        self.log_text.insert(tk.END, "\nConnected USB Devices:\n")
        if devices:
            for device in devices:
                self.log_text.insert(tk.END, f"\nVendor ID: {device.idVendor}, Product ID: {device.idProduct}\n")
                self.log_text.insert(tk.END, f"Manufacturer: {usb.util.get_string(device, device.iManufacturer)}\n")
                self.log_text.insert(tk.END, f"Product: {usb.util.get_string(device, device.iProduct)}\n")
                self.log_text.insert(tk.END, f"Serial Number: {usb.util.get_string(device, device.iSerialNumber)}\n")
        else:
            self.log_text.insert(tk.END, "No USB devices connected.\n")
        self.log_text.see(tk.END)

    def run(self):
        # Start the Tkinter main loop
        self.root.mainloop()

if __name__ == "__main__":
        # Create an instance of the USBMonitorGUI class and run the GUI
    app = USBMonitorGUI()
    app.run()