import os
import resource
import sys
import logging
from multiprocessing import current_process, Process
import time
import traceback
from cryptodetector import CryptoDetector, Output, Options, Logger, FileLister
from cryptodetector.exceptions import CryptoDetectorError
import cantera as ct
import numpy as np

path = "$HOME"
log_file_path = "/var/log/irondome/irondome.log"
logging.basicConfig(filename=log_file_path, level=logging.INFO)

def log_alert(message): # enregistre les erreurs dans les logs
    logging.info(message)

def memory_limit():
    memory_limit_bytes = 100 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

def monitor_disk_read_abuse(): # check le disk usage
    timer = 5 
    disk_stats = os.popen("cat /sys/block/sda/stat").read()
    disk_stats_split = disk_stats.split(' ')
    disk_stats_array = list(filter(None, disk_stats_split))

    time.sleep(timer)

    disk_stats_2 = os.popen("cat /sys/block/sda/stat").read()
    disk_stats_split_2 = disk_stats_2.split(' ')
    disk_stats_array_2 = list(filter(None, disk_stats_split_2))

    disk_reads_diff = int(disk_stats_array_2[0]) - int(disk_stats_array[0])

    if disk_reads_diff > 100:  # Adjust the threshold as needed
        alert_message = "Disk read abuse detected!"
        print(alert_message)
        log_alert(alert_message)

def monitor_crypto_activity(): # check l'activité intensive crypto
    try:
        log_output_directory = None
        options = Options(CryptoDetector.VERSION).read_all_options()
        if "log" in options and options["log"]:
            log_output_directory = options["output"]
        crypto_detector = CryptoDetector(options)
        crypto_detector.scan()

        if crypto_detector.results.intensive_activity_detected():
            alert_message = "Intensive use of cryptographic activity detected!"
            print(alert_message)
            log_alert(alert_message)

    except CryptoDetectorError as expn:
        error_message = f"CryptoDetectorError: {str(expn)}"
        print(error_message)
        log_alert(error_message)
        if log_output_directory:
            Logger.write_log_files(log_output_directory)
        FileLister.cleanup_all_tmp_files()
    except KeyboardInterrupt:
        FileLister.cleanup_all_tmp_files()
        raise
    except Exception as expn:
        error_message = f"Unhandled exception: {str(expn)}\n\n{traceback.format_exc()}"
        print(error_message)
        log_alert(error_message)
        if log_output_directory:
            Logger.write_log_files(log_output_directory)
        FileLister.cleanup_all_tmp_files()

def entropy_change(): # verifie l'entropy d'un fichier
    try:
        file = "your_file_name_here.cti"
        gas1 = ct.Solution(file)
        alert_message = f'Entropy change detected: {gas1}'
        print(alert_message)
        log_alert(alert_message)
    except Exception as expn:
        error_message = f"Error in entropy_change: {str(expn)}\n\n{traceback.format_exc()}"
        print(error_message)
        log_alert(error_message)

def main():
    process = current_process()
    print(f'Daemon process: {process.daemon}')
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\n Exiting.")
    monitor_disk_read_abuse()
    monitor_crypto_activity()
    entropy_change()

if __name__ == "__main__":
    memory_limit() # Met une limite de 100 MB en utilisation de memoire (a voir si c'est correct) 
    try: # Permet normalement de lancer le programme en daemon en fond, le silencer pour tester
        process = Process(target=main, daemon=True)
        process.start()
        process.join()
    except MemoryError:
        error_message = '\n\nERROR: Memory limit of 100MB exceeded.'
        print(error_message)
        log_alert(error_message)
        sys.exit(1)
