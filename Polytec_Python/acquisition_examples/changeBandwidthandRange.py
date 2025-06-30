
#changeBandwidthandRange
#examles/Python/acquisition examples/interactive_bandwidth_and_range_selection.py参照

import logging
import sys

from polytec.io.device_command import DeviceCommand
from polytec.io.device_communication import DeviceCommunication
from polytec.io.device_type import DeviceType
from polytec.io.item_list import ItemList


# [bandwidth_selection]
def changeBandwidth(device_communication, new_bandwidth):
    bandwidth_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Bandwidth)
    if len(new_bandwidth) > 0:
        bandwidth_list.set_current_item(new_bandwidth)
    # [bandwidth_selection]


# [range_selection]
def changeRange(device_communication, new_range):
    range_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Range)
    if len(new_range) > 0:
        range_list.set_current_item(new_range)
    # [range_selection]



# [run]
def run(address, new_bandwidth="1 kHz", new_range="10 mm/s"):
    try:
        device_communication = DeviceCommunication(address)
        changeBandwidth(device_communication, new_bandwidth)
        changeRange(device_communication, new_range)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [run]


if __name__ == "__main__":
    ip_address = "192.168.137.1"
    device_communication = DeviceCommunication(ip_address)

    bandwidth_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Bandwidth)
    available_bandwidths = bandwidth_list.available_items()
    print(f"Available bandwidths: {', '.join(available_bandwidths)}")
    if len(available_bandwidths) > 1:
        new_bandwidth = input(f"New bandwidth [{bandwidth_list.current_item()}]: ").strip()

    range_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Range)
    available_ranges = range_list.available_items()
    print(f"Available Velocity ranges: {', '.join(available_ranges)}")
    if len(available_ranges) > 1:
        new_range = input(f"New Velocity range [{range_list.current_item()}]: ").strip()
    
    run(ip_address, new_bandwidth, new_range)
