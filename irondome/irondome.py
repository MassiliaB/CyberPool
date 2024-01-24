import os
import resource
import sys
import logging
from multiprocessing import current_process, Process
import time
import traceback
import argparse
# from cryptodetector import CryptoDetector, Output, Options, Logger, FileLister
# from cryptodetector.exceptions import CryptoDetectorError
import cantera as ct
import numpy as np
import math
from threading import Thread, Event

log_file_path = "log/irondome.log"
initial_disk_state = None
initial_entropy_state = None
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_alert(message): # enregistre les erreurs dans les logs
    logging.info(message)

def memory_limit():
    memory_limit_bytes = 100 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

def get_disk_state(): # Etat actuel du disque
    stats = os.popen("cat /sys/block/sda/stat").read()
    stats_split = stats.split(' ')
    return list(filter(None, stats_split))    

def monitor_disk_read_abuse(): # check le disk usage
    global initial_disk_state
    if initial_disk_state is None:
        initial_disk_state = get_disk_state()

    current_disk_state = get_disk_state()
    if current_disk_state != initial_disk_state:
        description = [
        "\n-----------Disk read monitoring----------\n",
        "IO stats over last 60 seconds \n\n",
        "read I/Os : " + str(current_disk_state[0]),
        "read merges : " + str(current_disk_state[1]),
        "read sectors : " + str(current_disk_state[2]),
        "read ticks (ms) : " + str(current_disk_state[3]),
        "write I/Os : " + str(current_disk_state[4]),
        "write merges : " + str(current_disk_state[5]),
        "write sectors : " + str(current_disk_state[6]),
        "write ticks (ms) : " + str(current_disk_state[7]),
        "in_flight : " + str(current_disk_state[8]),
        "io_ticks (ms) : " + str(current_disk_state[9]),
        "time_in_queue (ms) : " + str(current_disk_state[10]),
        "\n---------------------\n"
        ]
        for d in description:
            log_alert(d)

# def monitor_crypto_activity(): # check l'activité intensive crypto
#     try:
#         log_output_directory = None
#         options = Options(CryptoDetector.VERSION).read_all_options()
#         if "log" in options and options["log"]:
#             log_output_directory = options["output"]
#         crypto_detector = CryptoDetector(options)
#         crypto_detector.scan()

#         if crypto_detector.results.intensive_activity_detected():
#             alert_message = "Intensive use of cryptographic activity detected!"
#             print(alert_message)
#             log_alert(alert_message)

#     except CryptoDetectorError as expn:
#         error_message = f"CryptoDetectorError: {str(expn)}"
#         print(error_message)
#         log_alert(error_message)
#         if log_output_directory:
#             Logger.write_log_files(log_output_directory)
#         FileLister.cleanup_all_tmp_files()
#     except KeyboardInterrupt:
#         FileLister.cleanup_all_tmp_files()
#         raise
#     except Exception as expn:
#         error_message = f"Unhandled exception: {str(expn)}\n\n{traceback.format_exc()}"
#         print(error_message)
#         log_alert(error_message)
#         if log_output_directory:
#             Logger.write_log_files(log_output_directory)
#         FileLister.cleanup_all_tmp_files()

def get_file_entropy(file_path): # l'entropie d'un fichier
    with open(file_path, "rb") as file:
        counters = {byte: 0 for byte in range(2 ** 8)} 
        for byte in file.read():
            counters[byte] += 1
        filesize = file.tell()
        probabilities = [counter / filesize for counter in counters.values()]
        entropy = -sum(probability * math.log2(probability) for probability in probabilities if probability > 0)
        return entropy

def get_entropy_state(paths): # l'etat actuel de l'entropie
    entropy_values = []
    for path in paths:
        if os.path.isfile(path):
            entropy_values.append(get_file_entropy(path))
        elif os.path.isdir(path):
            files_in_directory = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
            for file_path in files_in_directory:
                entropy_values.append(get_file_entropy(file_path))
    return entropy_values

def monitor_entropy(paths):
    global initial_entropy_state
    if initial_entropy_state is None:
        initial_entropy_state = get_entropy_state(paths)

    current_entropy_state = get_entropy_state(paths)
    if current_entropy_state != initial_entropy_state:
        log_alert("\n-----------Entropy monitoring----------\n")
        for idx, entropy_value in enumerate(current_entropy_state, start=1):
            log_alert(f"Entropy of file {idx}: {entropy_value}")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*', default=['/home/kali/CyberPool'], type=str, help='Paths to files or directories.')
    args = parser.parse_args()
    paths = args.paths
    return paths

def main():
    # process = current_process()
    # print(f'Daemon process: {process.daemon}')
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\n Exiting.")
    paths = parse_arguments()
    while True:
        monitor_disk_read_abuse()
        monitor_entropy(paths)
        time.sleep(60)
    # monitor_crypto_activity()

if __name__ == "__main__":
    memory_limit() # Met une limite de 100 MB en utilisation de memoire (a voir si c'est correct) 
    try: # Permet normalement de lancer le programme en daemon en fond, le silencer pour tester
        main()
    #     process = Process(target=main, daemon=True)
    #     process.start()
    #     process.join()
    except MemoryError:
        error_message = '\n\nERROR: Memory limit of 100MB exceeded.'
        print(error_message)
        log_alert(error_message)
        sys.exit(1)
