import os
import socket
from concurrent.futures import ThreadPoolExecutor
import time
from colorama import Fore, Style, init

# Colorama'yı başlat
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_valid_ip(ip):
    parts = ip.split('.')
    return (len(parts) == 4 and all(part.isdigit() and 0 <= int(part) < 256 for part in parts))

def is_valid_port(port):
    return 1 <= port <= 65535

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                return f"{Fore.GREEN}Port {port} açık{Style.RESET_ALL}"
            else:
                if result in [111, 10061]:
                    return f"{Fore.RED}Port {port} kapalı{Style.RESET_ALL}"
                else:
                    return f"{Fore.YELLOW}Port {port} filtreli veya erişilemiyor{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}Bir hata oluştu: {e}{Style.RESET_ALL}"

def port_scanner(ip, ports):
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        
        for i, future in enumerate(futures):
            result = future.result()
            results.append(result)
            # İlerleme yüzdesini hesapla ve terminal başlığını güncelle
            percent_complete = (i + 1) / len(ports) * 100
            os.system(f'title Tarama İlerleme: %{percent_complete:.2f}')  # Windows için
            print(result)

    end_time = time.time()
    duration = end_time - start_time
    print(f"{Fore.CYAN}Tarama tamamlandı. Toplam süre: {duration:.2f} saniye{Style.RESET_ALL}")

    return results, duration

def save_results_to_file(results, duration, ip):
    filename = f"port_scan_results_{ip.replace('.', '_')}.txt"
    with open(filename, 'w') as file:
        file.write(f"Port Tarama Sonuçları: {ip}\n")
        file.write(f"Toplam Süre: {duration:.2f} saniye\n\n")
        for result in results:
            file.write(result + '\n')
    print(f"{Fore.GREEN}Sonuçlar '{filename}' dosyasına kaydedildi.{Style.RESET_ALL}")
    input("\n" + Fore.YELLOW + "Tekrardan Ana Menüye Dönmek İçin 'Enter' Tuşuna Basın...")
    clear_screen()

def main_menu():
    print(Fore.BLUE+"""
    ____             __                  
   / __ \____  _____/ /_                 
  / /_/ / __ \/ ___/ __/                 
 / ____/ /_/ / /  / /_                   
/_/____\____/_/   \__/                   
  / ___/_________ _____  ____  ___  _____
  \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 ___/ / /__/ /_/ / / / / / / /  __/ /    
/____/\___/\__,_/_/ /_/_/ /_/\___/_/\n"""+ Style.RESET_ALL)
    
    print("[1] Belirli bir port taraması")
    print("[2] En çok kullanılan portlar taraması")
    print("[3] İki port arasındaki tarama")
    print("[4] Tüm portları taraması")
    print("[5] Çıkış")

if __name__ == "__main__":
    clear_screen()

    while True:
        main_menu()
        choice = input("Seçiminizi yapın (1-5): ")

        if choice == '1':
            clear_screen()
            target_ip = input("Tarama yapılacak IP adresini girin (örneğin, 127.0.0.1): ")
            if not is_valid_ip(target_ip):
                print(f"{Fore.RED}Geçersiz IP adresi. Lütfen doğru bir IP girin.{Style.RESET_ALL}")
                continue
            port = int(input("Tarayacağınız portu girin (1-65535): "))
            if not is_valid_port(port):
                print(f"{Fore.RED}Geçersiz port numarası. Lütfen 1 ile 65535 arasında bir değer girin.{Style.RESET_ALL}")
                continue
            clear_screen()
            print(f"{Fore.CYAN}Port {port} taranıyor...{Style.RESET_ALL}")
            result = scan_port(target_ip, port)
            print(result)

        elif choice == '2':
            clear_screen()
            target_ip = input("Tarama yapılacak IP adresini girin (örneğin, 127.0.0.1): ")
            if not is_valid_ip(target_ip):
                print(f"{Fore.RED}Geçersiz IP adresi. Lütfen doğru bir IP girin.{Style.RESET_ALL}")
                continue
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306]
            clear_screen()
            print(f"{Fore.CYAN}En çok kullanılan portlar taranıyor: {common_ports}{Style.RESET_ALL}")
            results, duration = port_scanner(target_ip, common_ports)
            save_results_to_file(results, duration, target_ip)

        elif choice == '3':
            clear_screen()
            target_ip = input("Tarama yapılacak IP adresini girin (örneğin, 127.0.0.1): ")
            if not is_valid_ip(target_ip):
                print(f"{Fore.RED}Geçersiz IP adresi. Lütfen doğru bir IP girin.{Style.RESET_ALL}")
                continue
            clear_screen()
            start_port = int(input("Başlangıç portunu girin (1-65535): "))
            end_port = int(input("Bitiş portunu girin (1-65535): "))
            if not (is_valid_port(start_port) and is_valid_port(end_port)):
                print(f"{Fore.RED}Geçersiz port numarası. Lütfen 1 ile 65535 arasında bir değer girin.{Style.RESET_ALL}")
                continue
            results, duration = port_scanner(target_ip, range(start_port, end_port + 1))
            save_results_to_file(results, duration, target_ip)

        elif choice == '4':
            clear_screen()
            target_ip = input("Tarama yapılacak IP adresini girin (örneğin, 127.0.0.1): ")
            if not is_valid_ip(target_ip):
                print(f"{Fore.RED}Geçersiz IP adresi. Lütfen doğru bir IP girin.{Style.RESET_ALL}")
                continue
            clear_screen()
            results, duration = port_scanner(target_ip, range(1, 65536))
            save_results_to_file(results, duration, target_ip)

        elif choice == '5':
            clear_screen()
            print(f"{Fore.GREEN}Çıkılıyor...{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}Geçersiz seçim, lütfen tekrar deneyin.{Style.RESET_ALL}")
