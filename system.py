import psutil
import platform
from datetime import datetime
import subprocess
import GPUtil
from tabulate import tabulate
import re
import uuid
from savloc import temp
import os

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def info():
    fileloc = os.path.join(temp(),"sys_info.txt")
    with open(fileloc,'w') as f:
#general details
        f.write("="*40 + "System Information" + "="*40)
        uname = platform.uname()
    # traverse the info
        Id = subprocess.Popen(['systeminfo'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        line = []
        while Id.poll() is None:
            text = (Id.stdout.readline().decode('utf-8').strip())
            if text not in line:
                line.append(text)
        new = []
        
    # arrange the string into clear info
        for item in line:
            new.append(str(item.split("\r")[:-1]))
            f.write("\n" + item)
        

        f.write("\n" +f"System: {uname.system}")
        f.write("\n" +f"Node Name: {uname.node}")
        f.write("\n" +f"Release: {uname.release}")
        f.write("\n" +f"Version: {uname.version}")
        f.write("\n" +f"Machine: {uname.machine}")
        f.write("\n" +f"Processor: {uname.processor}")
    
        f.write("\n" +"="*44 + "Boot Time" + "="*45)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        f.write("\n" +f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

# let's f.write CPU information
        f.write("\n" +"="*45 + "CPU Info" + "="*45)
    # number of cores
        f.write("\n" +"Physical cores:" + str(psutil.cpu_count(logical=False)))
        f.write("\n" +"Total cores:" + str(psutil.cpu_count(logical=True)))
    # CPU frequencies
        cpufreq = psutil.cpu_freq()
        f.write("\n" +f"Max Frequency: {cpufreq.max:.2f}Mhz")
        f.write("\n" +f"Min Frequency: {cpufreq.min:.2f}Mhz")
        f.write("\n" +f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
        f.write("\n" +"CPU Usage Per Core:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            f.write("\n" +f"Core {i}: {percentage}%")
        f.write("\n" +f"Total CPU Usage: {psutil.cpu_percent()}%")

        f.write("\n" +"="*40 + "GPU Details" + "="*40)
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            # get the GPU id
            gpu_id = gpu.id
            # name of GPU
            gpu_name = gpu.name
            # get % percentage of GPU usage of that GPU
            gpu_load = f"{gpu.load*100}%"
            # get free memory in MB format
            gpu_free_memory = f"{gpu.memoryFree}MB"
            # get used memory
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            # get total memory
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            # get GPU temperature in Celsius
            gpu_temperature = f"{gpu.temperature} °C"
            gpu_uuid = gpu.uuid
            list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature, gpu_uuid
            ))

        f.write("\n" +tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                        "temperature", "uuid")))

# Memory Information
        f.write("\n" +"="*40 + "Memory Information" + "="*40)
    # get the memory details
        svmem = psutil.virtual_memory()
        f.write("\n" +f"Total: {get_size(svmem.total)}")
        f.write("\n" +f"Available: {get_size(svmem.available)}")
        f.write("\n" +f"Used: {get_size(svmem.used)}")
        f.write("\n" +f"Percentage: {svmem.percent}%")
        f.write("\n" +"="*47 + "SWAP" + "="*47)
    # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        f.write("\n" +f"Total: {get_size(swap.total)}")
        f.write("\n" +f"Free: {get_size(swap.free)}")
        f.write("\n" +f"Used: {get_size(swap.used)}")
        f.write("\n" +f"Percentage: {swap.percent}%")

    # Disk Information
        f.write("\n" +"="*41 + "Disk Information" + "="*41)
        f.write("\n" +"Partitions and Usage:")
    # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            f.write("\n" +f"=== Device: {partition.device} ===")
            f.write("\n" +f"  Mountpoint: {partition.mountpoint}")
            f.write("\n" +f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            f.write("\n" +f"  Total Size: {get_size(partition_usage.total)}")
            f.write("\n" +f"  Used: {get_size(partition_usage.used)}")
            f.write("\n" +f"  Free: {get_size(partition_usage.free)}")
            f.write("\n" +f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        f.write("\n" +f"Total read: {get_size(disk_io.read_bytes)}")
        f.write("\n" +f"Total write: {get_size(disk_io.write_bytes)}")

# Network information
        f.write("\n" +"="*39 + "Network Information" + "="*40)
    # get all network interfaces (virtual and physical)
        f.write("\n" +"Mac Address - >" + ':'.join(re.findall('..', '%012x' % uuid.getnode())))
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                f.write("\n" +f"=== Interface: {interface_name} ===")
                if str(address.family) == 'AddressFamily.AF_INET':
                    f.write("\n" +f"  IP Address: {address.address}")
                    f.write("\n" +f"  Netmask: {address.netmask}")
                    f.write("\n" +f"  Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    f.write("\n" +f"  MAC Address: {address.address}")
                    f.write("\n" +f"  Netmask: {address.netmask}")
                    f.write("\n" +f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
        net_io = psutil.net_io_counters()
        f.write("\n" +f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        f.write("\n" +f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
        f.close()

info()


