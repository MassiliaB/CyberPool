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
from threading import Thread

log_file_path = "log/irondome.log"
logging.basicConfig(filename=log_file_path, level=logging.INFO)

def log_alert(message): # enregistre les erreurs dans les logs
    logging.info(message)

def memory_limit():
    memory_limit_bytes = 100 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

def monitor_disk_read_abuse(): # check le disk usage
    while True:
        timer = 60 
        stats = os.popen("cat /sys/block/sda/stat").read()
        stats_split = stats.split(' ')
        stats_array = list(filter(None, stats_split))

        time.sleep(timer)

        stats_2 = os.popen("cat /sys/block/sda/stat").read()
        stats_split_2 = stats_2.split(' ')
        stats_array_2 = list(filter(None, stats_split_2))
        iototal = [
        int(stats_array_2[0]) - int(stats_array[0]),
        int(stats_array_2[1]) - int(stats_array[1]),
        int(stats_array_2[2]) - int(stats_array[2]),
        int(stats_array_2[3]) - int(stats_array[3]),
        int(stats_array_2[4]) - int(stats_array[4]),
        int(stats_array_2[5]) - int(stats_array[5]),
        int(stats_array_2[6]) - int(stats_array[6]),
        int(stats_array_2[7]) - int(stats_array[7]),
        int(stats_array_2[8]) - int(stats_array[8]),
        int(stats_array_2[9]) - int(stats_array[9]),
        int(stats_array_2[10]) - int(stats_array[10])
        ]

        description = [
        "\n-----------Disk read monitoring----------\n",
        "IO stats over last " + str(timer) + " seconds \n\n",
        "read I/Os : " + str(iototal[0]),
        "read merges : " + str(iototal[1]),
        "read sectors : " + str(iototal[2]),
        "read ticks (ms) : " + str(iototal[3]),
        "write I/Os : " + str(iototal[4]),
        "write merges : " + str(iototal[5]),
        "write sectors : " + str(iototal[6]),
        "write ticks (ms) : " + str(iototal[7]),
        "in_flight : " + str(iototal[8]),
        "io_ticks (ms) : " + str(iototal[9]),
        "time_in_queue (ms) : " + str(iototal[10]),
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

def process_file(file_path):
    try:
        with open(file_path, "rb") as file:
            counters = {byte: 0 for byte in range(2 ** 8)} 
            for byte in file.read():
                counters[byte] += 1
            filesize = file.tell()
            probabilities = [counter / filesize for counter in counters.values()]
            entropy = -sum(probability * math.log2(probability) for probability in probabilities if probability > 0)
            log_alert("\n-----------Entropy monitoring----------\n")
            log_alert(f"Entropy of {os.path.basename(file_path)}: {entropy}")
    except Exception as expn:
        error_message = "\n-----------File entropy monitoring----------\n"
        error_message = error_message + f"Error processing file {file_path}: {str(expn)}\n\n{traceback.format_exc()}"
        print(error_message)
        log_alert(error_message)

def entropy_change(paths):
    try:
        while True:
            for path in paths:
                if os.path.isfile(path):
                    process_file(path)
                elif os.path.isdir(path):
                    files_in_directory = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
                    for file_path in files_in_directory:
                        process_file(file_path)
                else:
                    log_alert("\n-----------File entropy monitoring----------\n")
                    log_alert(f"Invalid path: {path}")
            time.sleep(60)
    except Exception as expn:
        error_message = "\n-----------File entropy monitoring----------\n"
        error_message = error_message + f"Error in entropy_change: {str(expn)}\n\n{traceback.format_exc()}"
        print(error_message)
        log_alert(error_message)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*', default=['$HOME'], type=str, help='Paths to files or directories.')
    args = parser.parse_args()
    paths = args.paths
    return paths

def main():
    # process = current_process()
    # print(f'Daemon process: {process.daemon}')
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\n Exiting.")
    paths = parse_arguments()

    # Create threads for monitoring functions
    disk_read_thread = Thread(target=monitor_disk_read_abuse)
    entropy_thread = Thread(target=entropy_change, args=(paths,))
    # Start the threads
    disk_read_thread.start()
    entropy_thread.start()
    # Join the threads to wait for them to finish
    disk_read_thread.join()
    entropy_thread.join()
    # monitor_crypto_activity()

if __name__ == "__main__":
    memory_limit() # Met une limite de 100 MB en utilisation de memoire (a voir si c'est correct) 
    main()
    # try: # Permet normalement de lancer le programme en daemon en fond, le silencer pour tester
    #     process = Process(target=main, daemon=True)
    #     process.start()
    #     process.join()
    # except MemoryError:
    #     error_message = '\n\nERROR: Memory limit of 100MB exceeded.'
    #     print(error_message)
    #     log_alert(error_message)
    #     sys.exit(1)
