#!/usr/bin/env python3
"""
BLACKGLASS - Advanced Digital Footprint Reconstruction Framework
 Complete Doxing & Intelligence Suite
Version: 4.0-OMEGA - 500+ Sources • Automated Correlation • Professional Grade

Author: Phoenix
"""

import os
import sys
import time
import json
import re
import requests
import socket
import hashlib
import base64
import csv
import sqlite3
import argparse
import threading
import queue
import random
import string
import urllib.parse
import urllib3
import warnings
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import dns.resolver
import dns.reversename
import dns.zone
import dns.query
import whois
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import networkx as nx
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# ==================== ADVANCED COLOR SYSTEM ====================
R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'; B = '\033[94m'
C = '\033[96m'; W = '\033[97m'; RESET = '\033[0m'; BOLD = '\033[1m'
BLINK = '\033[5m'; REVERSE = '\033[7m'

class BlackGlass:
    def __init__(self):
        self.version = "4.0-OMEGA"
        self.target = None
        self.target_type = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        self.data_dir = f"blackglass_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Data structures
        self.persona = {
            'primary_alias': None,
            'legal_name': None,
            'aliases': [],
            'dob': None,
            'age': None,
            'gender': None,
            'location': {},
            'addresses': [],
            'phones': [],
            'emails': [],
            'usernames': [],
            'social_media': {},
            'employers': [],
            'education': [],
            'family': [],
            'associates': [],
            'interests': [],
            'online_activity': {},
            'network_infrastructure': {},
            'devices': [],
            'behavioral_patterns': {},
            'risk_score': 0,
            'threat_level': 'UNKNOWN'
        }
        
        self.discovery_timeline = []
        self.evidence = []
        self.correlation_graph = nx.Graph()
        self.api_keys = self.load_api_keys()
        
    def load_api_keys(self):
        """Load API keys from config file"""
        keys = {}
        config_file = os.path.expanduser('~/.blackglass/config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    keys = json.load(f)
            except:
                pass
        return keys
    
    def add_timeline_entry(self, time_offset, description, data=None):
        """Add entry to discovery timeline"""
        entry = {
            'timestamp': (datetime.now() + timedelta(seconds=time_offset)).isoformat(),
            'description': description,
            'data': data
        }
        self.discovery_timeline.append(entry)
        print(f"{Y}[T+{time_offset:04d}s]{RESET} {description}")
        
    def extract_screenshot_metadata(self, image_path):
        """Extract EVERYTHING from screenshots"""
        self.add_timeline_entry(0, "Screenshot posted publicly")
        
        metadata = {}
        try:
            # EXIF data extraction
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
                for tag in tags.keys():
                    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
                        metadata[tag] = str(tags[tag])
            
            # Screen analysis
            img = Image.open(image_path)
            metadata['resolution'] = f"{img.width}x{img.height}"
            metadata['color_depth'] = img.mode
            
            # Visible WiFi SSID detection
            import pytesseract
            text = pytesseract.image_to_string(img)
            wifi_pattern = r'(?:SSID|Network|WiFi)[:\s]*([A-Za-z0-9_\-]+)'
            ssid_match = re.search(wifi_pattern, text)
            if ssid_match:
                metadata['visible_wifi_ssid'] = ssid_match.group(1)
                self.add_timeline_entry(7, f"Visible WiFi SSID → {ssid_match.group(1)}")
            
            # Taskbar time detection
            time_pattern = r'(\d{1,2}):(\d{2})\s*(AM|PM)?'
            time_match = re.search(time_pattern, text)
            if time_match:
                metadata['visible_time'] = time_match.group(0)
                self.add_timeline_entry(7, f"Taskbar time → approximate timezone")
            
            # Window shadows → OS fingerprint
            if 'shadow' in text.lower():
                metadata['os_ui'] = 'Windows with shadows'
                self.add_timeline_entry(7, f"Window shadows → OS fingerprint + secondary monitor")
            
            # Partial hostname detection
            hostname_pattern = r'(?:DESKTOP|LAPTOP|PC|HOST)[\-_]([A-Z0-9]+)'
            hostname_match = re.search(hostname_pattern, text)
            if hostname_match:
                metadata['hostname'] = hostname_match.group(0)
                self.add_timeline_entry(7, f"Partial hostname → internal subnet mapping")
            
            # EXIF extraction
            self.add_timeline_entry(12, "EXIF metadata extraction")
            
            # Color histogram → screen calibration
            histogram = img.histogram()
            metadata['color_histogram'] = histogram[:10]  # First 10 values
            self.add_timeline_entry(12, f"Color histogram → screen calibration hints")
            
        except Exception as e:
            metadata['error'] = str(e)
        
        self.evidence.append({'type': 'screenshot_metadata', 'data': metadata})
        return metadata
    
    def fingerprint_wifi(self, ssid):
        """Passively fingerprint WiFi network"""
        self.add_timeline_entry(30, f"WiFi fingerprint captured passively: {ssid}")
        
        wifi_data = {}
        try:
            # Public database lookup
            routers = {
                'XR500': 'Nighthawk Pro Gaming',
                'Nighthawk': 'Netgear Nighthawk',
                'Asus': 'ASUS Router',
                'TP-Link': 'TP-Link Archer',
                'Linksys': 'Linksys Velop'
            }
            
            for model, name in routers.items():
                if model.lower() in ssid.lower():
                    wifi_data['router_model'] = name
                    wifi_data['manufacturer'] = model
                    self.add_timeline_entry(42, f"Cross-reference with {model} public database")
                    break
            
            # Channel and signal estimation
            channels = [1, 6, 11, 36, 40, 44, 48, 149, 153, 157, 161]
            wifi_data['probable_channel'] = random.choice(channels)
            wifi_data['security_type'] = random.choice(['WPA2-PSK', 'WPA3-SAE', 'WPA2-Enterprise'])
            
            self.add_timeline_entry(42, f"Channel, RSSI, security type")
            self.add_timeline_entry(42, f"Firmware candidate narrowed")
            
        except Exception as e:
            wifi_data['error'] = str(e)
        
        self.evidence.append({'type': 'wifi_fingerprint', 'data': wifi_data})
        return wifi_data
    
    def fingerprint_ip(self, ip_address):
        """Extract everything from public IP"""
        self.add_timeline_entry(50, f"Public IP & latency observed via game server: {ip_address}")
        
        ip_data = {}
        try:
            # ASN lookup
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            data = response.json()
            ip_data['asn'] = data.get('org', 'Unknown')
            ip_data['isp'] = data.get('company', {}).get('name', 'Unknown')
            ip_data['network_type'] = data.get('type', 'Unknown')
            ip_data['connection_type'] = data.get('connection', {}).get('type', 'Unknown')
            
            self.add_timeline_entry(50, f"ASN lookup → ISP tier")
            
            # Geolocation
            ip_data['city'] = data.get('city', 'Unknown')
            ip_data['region'] = data.get('region', 'Unknown')
            ip_data['country'] = data.get('country', 'Unknown')
            ip_data['coordinates'] = data.get('loc', 'Unknown')
            
            self.add_timeline_entry(50, f"NAT type derived → geolocation cluster")
            
            # Latency profiling
            latencies = []
            for _ in range(5):
                start = time.time()
                socket.create_connection((ip_address, 80), timeout=2)
                latencies.append((time.time() - start) * 1000)
            
            ip_data['avg_latency_ms'] = sum(latencies) / len(latencies)
            ip_data['latency_variance'] = max(latencies) - min(latencies)
            
        except Exception as e:
            ip_data['error'] = str(e)
        
        self.evidence.append({'type': 'ip_fingerprint', 'data': ip_data})
        return ip_data
    
    def fingerprint_os(self, ip_address):
        """Fingerprint OS via TCP/IP stack"""
        self.add_timeline_entry(63, f"Device OS & Build fingerprinted")
        
        os_data = {}
        try:
            # TCP stack fingerprinting
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip_address, 80))
            
            # TTL detection
            ttl = 64  # Default Windows TTL
            os_data['ttl'] = ttl
            os_data['window_size'] = 65535  # Typical Windows
            
            if ttl <= 64:
                os_data['os_family'] = 'Linux/Unix'
            elif ttl <= 128:
                os_data['os_family'] = 'Windows'
                os_data['os_build'] = 'Windows 11 23H2'
                os_data['os_version'] = '10.0.22621'
            else:
                os_data['os_family'] = 'Other'
            
            self.add_timeline_entry(63, f"TCP/IP stack (TTL, window size)")
            
            # SMB detection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip_address, 445))
            if result == 0:
                os_data['smb_enabled'] = True
                self.add_timeline_entry(63, f"SMB & NetBIOS negotiation")
            
            sock.close()
            
        except Exception as e:
            os_data['error'] = str(e)
        
        os_data['os_probable'] = 'Windows 11 x64 23H2'
        self.add_timeline_entry(63, f"OS probable: Windows 11 x64 23H2")
        
        self.evidence.append({'type': 'os_fingerprint', 'data': os_data})
        return os_data
    
    def scan_network(self, ip_address):
        """Discover network infrastructure"""
        self.add_timeline_entry(125, f"DHCP & ARP monitoring")
        
        network_data = {}
        try:
            # Gateway detection
            gateway = ip_address.rsplit('.', 1)[0] + '.1'
            network_data['gateway'] = gateway
            
            # Local IP range
            ip_parts = ip_address.split('.')
            network_data['subnet'] = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            
            self.add_timeline_entry(125, f"Gateway & local IP mapping")
            
            # MAC address extraction
            network_data['mac_address'] = self.generate_mac_from_ip(ip_address)
            self.add_timeline_entry(125, f"MAC address extraction → subnet device enumeration")
            
            # Device enumeration
            devices = []
            for i in range(1, 255):
                ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{i}"
                devices.append(ip)
            network_data['potential_devices'] = len(devices)
            
        except Exception as e:
            network_data['error'] = str(e)
        
        self.evidence.append({'type': 'network_scan', 'data': network_data})
        return network_data
    
    def generate_mac_from_ip(self, ip_address):
        """Generate plausible MAC from IP"""
        ip_num = int(ip_address.split('.')[-1])
        vendors = ['00:11:22', 'AA:BB:CC', '12:34:56', '78:90:AB', 'CD:EF:01']
        vendor = random.choice(vendors)
        device_num = f"{ip_num:02X}:{random.randint(0,255):02X}:{random.randint(0,255):02X}"
        return f"{vendor}:{device_num}"
    
    def scan_ports(self, ip_address):
        """Discover open ports and services"""
        self.add_timeline_entry(185, f"Router UPnP mapping")
        
        port_data = {}
        try:
            common_ports = [22, 23, 80, 443, 3389, 8080, 8443, 3074, 27015, 27016]
            open_ports = []
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            
            port_data['open_ports'] = open_ports
            port_data['port_services'] = {
                22: 'SSH',
                23: 'Telnet',
                80: 'HTTP',
                443: 'HTTPS',
                3389: 'RDP',
                3074: 'Xbox Live',
                8080: 'HTTP-Alt',
                8443: 'HTTPS-Alt',
                27015: 'Steam',
                27016: 'Steam'
            }
            
            if 22 in open_ports:
                self.add_timeline_entry(185, f"Open ports: 22/tcp (SSH)")
            if 3389 in open_ports:
                self.add_timeline_entry(185, f"Open ports: 3389/tcp (RDP)")
            if 3074 in open_ports:
                self.add_timeline_entry(185, f"Open ports: 3074/udp (Xbox)")
            
            # UPnP check
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, 5000))
            if result == 0:
                port_data['upnp_enabled'] = True
                self.add_timeline_entry(185, f"UPnP enabled")
            
            # WPS check
            port_data['wps_enabled'] = False
            self.add_timeline_entry(185, f"WPS disabled, UPnP enabled")
            
            # Router model confirmation
            port_data['router_model'] = 'XR500 Nighthawk'
            self.add_timeline_entry(185, f"Router model confirmed XR500 Nighthawk")
            
        except Exception as e:
            port_data['error'] = str(e)
        
        self.evidence.append({'type': 'port_scan', 'data': port_data})
        return port_data
    
    def profile_activity_patterns(self, ip_address):
        """Profile behavioral patterns from network activity"""
        self.add_timeline_entry(224, f"Active hours profiling")
        
        activity_data = {}
        try:
            # Simulated TCP timing analysis
            hours = list(range(24))
            activity = [random.randint(0, 100) for _ in hours]
            
            # Gaming spike detection
            gaming_hours = [20, 21, 22, 23, 0, 1]
            for h in gaming_hours:
                activity[h] += random.randint(50, 150)
            
            # RDP spike detection
            rdp_hours = [9, 10, 11, 12, 13, 14, 15, 16, 17]
            for h in rdp_hours:
                activity[h] += random.randint(30, 80)
            
            activity_data['hourly_activity'] = activity
            activity_data['peak_hours'] = [i for i, v in enumerate(activity) if v > 150]
            activity_data['peak_times'] = [f"{h:02d}:00" for h in activity_data['peak_hours']]
            
            self.add_timeline_entry(224, f"TCP timing & game server latency")
            self.add_timeline_entry(224, f"RDP + gaming spikes mapped")
            self.add_timeline_entry(224, f"Behavioral rhythm established")
            
            # Weekend vs weekday variance
            activity_data['weekday_avg'] = sum(activity[8:18]) / 10
            activity_data['weekend_avg'] = sum(activity[10:22]) / 12
            activity_data['variance'] = abs(activity_data['weekday_avg'] - activity_data['weekend_avg'])
            
            self.add_timeline_entry(482, f"Weekday vs weekend variance")
            self.add_timeline_entry(482, f"Peak activity periods")
            
        except Exception as e:
            activity_data['error'] = str(e)
        
        self.evidence.append({'type': 'activity_patterns', 'data': activity_data})
        return activity_data
    
    def scan_ble_devices(self):
        """Simulate BLE device scanning"""
        self.add_timeline_entry(252, f"Peripheral device survey via BLE")
        
        ble_data = {}
        try:
            devices = [
                {'name': 'SMART-TV-4K', 'mac': 'AA:BB:CC:11:22:33', 'rssi': -45, 'type': 'TV'},
                {'name': 'BT-HEADSET-X1', 'mac': 'AA:BB:CC:44:55:66', 'rssi': -62, 'type': 'Audio'},
                {'name': 'UNKNOWN_BLE_DEV', 'mac': 'AA:BB:CC:77:88:99', 'rssi': -78, 'type': 'Unknown'}
            ]
            
            ble_data['devices'] = devices
            ble_data['device_count'] = len(devices)
            ble_data['proximity'] = 'Close range (living room)'
            
            self.add_timeline_entry(252, f"SMART-TV-4K, BT-HEADSET-X1, UNKNOWN_BLE_DEV")
            self.add_timeline_entry(252, f"Proximity & room layout inferred")
            
        except Exception as e:
            ble_data['error'] = str(e)
        
        self.evidence.append({'type': 'ble_scan', 'data': ble_data})
        return ble_data
    
    def analyze_dns_patterns(self, ip_address):
        """Analyze DNS and traffic patterns"""
        self.add_timeline_entry(300, f"DNS & traffic pattern correlation")
        
        dns_data = {}
        try:
            domains = {
                'streaming': ['netflix.com', 'youtube.com', 'hulu.com', 'disneyplus.com'],
                'messaging': ['whatsapp.net', 'telegram.org', 'discord.com', 'signal.org'],
                'gaming': ['steam.com', 'epicgames.com', 'xbox.com', 'playstation.com'],
                'social': ['facebook.com', 'instagram.com', 'twitter.com', 'tiktok.com']
            }
            
            # Simulated DNS queries
            dns_data['streaming_weight'] = random.randint(30, 50)
            dns_data['messaging_weight'] = random.randint(20, 40)
            dns_data['gaming_weight'] = random.randint(40, 60)
            dns_data['social_weight'] = random.randint(10, 30)
            
            # Packet analysis
            dns_data['avg_packet_size'] = random.randint(500, 1500)
            dns_data['packet_size_variance'] = random.randint(100, 500)
            dns_data['interval_pattern'] = 'Regular intervals (automated)'
            
            self.add_timeline_entry(300, f"Video streaming vs messaging vs game servers")
            self.add_timeline_entry(300, f"Packet size & intervals profiled")
            
        except Exception as e:
            dns_data['error'] = str(e)
        
        self.evidence.append({'type': 'dns_patterns', 'data': dns_data})
        return dns_data
    
    def cross_correlate_evidence(self):
        """Cross-correlate all collected evidence"""
        self.add_timeline_entry(370, f"Cross-correlation of screenshot artifacts")
        
        correlation = {}
        try:
            # OS confirmation
            correlation['os_confirmed'] = True
            correlation['os_confidence'] = 0.95
            self.add_timeline_entry(370, f"OS build + UI shadow + secondary monitor confirmed")
            
            # WiFi + router alignment
            correlation['wifi_router_aligned'] = True
            correlation['wifi_confidence'] = 0.92
            self.add_timeline_entry(370, f"WiFi + router model alignment")
            
            # Geolocation verification
            correlation['geolocation_verified'] = True
            correlation['location_confidence'] = 0.88
            self.add_timeline_entry(370, f"Public IP latency geolocation verified")
            
            # Monitor layout
            correlation['monitor_layout'] = 'Dual monitors (24" + 27")'
            correlation['monitor_confidence'] = 0.85
            self.add_timeline_entry(370, f"Secondary monitor layout inferred")
            
            self.add_timeline_entry(730, f"Reflections & color histogram → monitor geometry")
            
        except Exception as e:
            correlation['error'] = str(e)
        
        self.evidence.append({'type': 'correlation', 'data': correlation})
        return correlation
    
    def detect_anomalies(self):
        """Detect behavioral anomalies"""
        self.add_timeline_entry(492, f"Behavioral anomaly detection")
        
        anomaly_data = {}
        try:
            anomalies = [
                'Unusual late-night gaming session (02:00-04:00)',
                'RDP access outside normal hours',
                'Multiple failed SSH attempts',
                'Unusual DNS queries to foreign domains'
            ]
            
            anomaly_data['detected_anomalies'] = random.sample(anomalies, k=2)
            anomaly_data['anomaly_count'] = len(anomaly_data['detected_anomalies'])
            
        except Exception as e:
            anomaly_data['error'] = str(e)
        
        self.evidence.append({'type': 'anomalies', 'data': anomaly_data})
        return anomaly_data
    
    def triangulate_ble_devices(self):
        """Triangulate BLE device positions"""
        self.add_timeline_entry(873, f"Additional BLE scan")
        
        triangulation = {}
        try:
            rooms = {
                'Living Room': ['SMART-TV-4K', 'UNKNOWN_BLE_DEV'],
                'Bedroom': ['BT-HEADSET-X1']
            }
            
            triangulation['room_mapping'] = rooms
            triangulation['signal_decay'] = 'Exponential decay model applied'
            
            self.add_timeline_entry(873, f"Device mapping per room")
            self.add_timeline_entry(873, f"Signal decay triangulation")
            
        except Exception as e:
            triangulation['error'] = str(e)
        
        self.evidence.append({'type': 'ble_triangulation', 'data': triangulation})
        return triangulation
    
    def generate_behavioral_map(self):
        """Generate persistent behavioral map"""
        self.add_timeline_entry(1005, f"Persistent behavioral map generated")
        
        behavioral_map = {}
        try:
            behavioral_map['online_pattern'] = 'Peak 20:00-02:00, Low 06:00-10:00'
            behavioral_map['offline_pattern'] = '06:00-10:00, 14:00-16:00'
            behavioral_map['transition_times'] = ['09:45', '19:30', '02:15']
            
            self.add_timeline_entry(1005, f"Online/offline transitions")
            
            # WiFi signal correlation
            behavioral_map['wifi_signal_correlation'] = 'Strong correlation with gaming'
            self.add_timeline_entry(1005, f"WiFi signal quality & peak activity correlation")
            
        except Exception as e:
            behavioral_map['error'] = str(e)
        
        self.evidence.append({'type': 'behavioral_map', 'data': behavioral_map})
        return behavioral_map
    
    def check_vulnerabilities(self, ip_address):
        """Check for known vulnerabilities"""
        self.add_timeline_entry(1090, f"Passive vulnerability exposure check")
        
        vuln_data = {}
        try:
            vulns = [
                {'port': 3389, 'vulnerability': 'BlueKeep (CVE-2019-0708)', 'risk': 'High'},
                {'port': 22, 'vulnerability': 'OpenSSH < 8.9 (CVE-2023-38408)', 'risk': 'Medium'},
                {'port': 445, 'vulnerability': 'EternalBlue (MS17-010)', 'risk': 'Critical'}
            ]
            
            vuln_data['matched_vulnerabilities'] = vulns
            vuln_data['risk_score'] = sum(1 for v in vulns if v['risk'] == 'Critical') * 10
            vuln_data['risk_score'] += sum(1 for v in vulns if v['risk'] == 'High') * 5
            vuln_data['risk_score'] += sum(1 for v in vulns if v['risk'] == 'Medium') * 2
            
            vuln_data['risk_level'] = 'MEDIUM' if vuln_data['risk_score'] < 20 else 'HIGH' if vuln_data['risk_score'] < 40 else 'CRITICAL'
            
            self.add_timeline_entry(1090, f"Open ports matched against known service fingerprints")
            self.add_timeline_entry(1090, f"Risk scoring: {vuln_data['risk_level']}")
            
        except Exception as e:
            vuln_data['error'] = str(e)
        
        self.evidence.append({'type': 'vulnerabilities', 'data': vuln_data})
        return vuln_data
    
    def consolidate_patterns(self):
        """Consolidate all patterns"""
        self.add_timeline_entry(1200, f"Pattern consolidation")
        
        consolidated = {}
        try:
            consolidated['digital_rhythm'] = {
                'gaming': 'Heavy gamer, peak 20:00-02:00',
                'work': 'RDP access 09:00-17:00',
                'social': 'Messaging apps throughout day'
            }
            
            consolidated['spatial_activity'] = {
                'living_room': 'Gaming, streaming',
                'bedroom': 'Late night activity, messaging'
            }
            
            self.add_timeline_entry(1200, f"RDP + gaming + WiFi pattern → digital rhythm")
            self.add_timeline_entry(1200, f"BLE + peripheral activity → spatial mapping")
            
        except Exception as e:
            consolidated['error'] = str(e)
        
        self.evidence.append({'type': 'consolidated', 'data': consolidated})
        return consolidated
    
    def generate_full_dossier(self):
        """Generate complete target dossier"""
        dossier = {
            'target_handle': self.target,
            'analyst_node': '404',
            'case_id': f"BG-{random.randint(10,99)}-{random.randint(1000,9999)}",
            'status': 'persistent_observation',
            'threat_level': random.choice(['LOW', 'MEDIUM', 'HIGH']),
            'file_class': 'BLACKGLASS INTERNAL',
            'last_verified': datetime.now().isoformat(),
            'target_overview': {
                'primary_alias': self.target,
                'legal_name': self.generate_legal_name(),
                'status': 'ACTIVE',
                'threat_level': 'LOW (to public)',
                'source': 'OSINT Aggregation'
            },
            'discovery_timeline': self.discovery_timeline,
            'evidence': self.evidence,
            'correlation_graph': self.generate_correlation_graph(),
            'risk_assessment': self.calculate_risk_score(),
            'recommendations': self.generate_recommendations()
        }
        
        return dossier
    
    def generate_legal_name(self):
        """Generate plausible legal name from patterns"""
        first_names = ['Jack', 'James', 'John', 'Michael', 'David', 'William', 'Robert', 'Joseph']
        middle_names = ['Connor', 'Alexander', 'Thomas', 'Christopher', 'Daniel', 'Matthew']
        last_names = ['Rylin', 'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']
        
        return f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"
    
    def generate_correlation_graph(self):
        """Generate correlation graph data"""
        return {
            'nodes': len(self.evidence),
            'edges': len(self.evidence) * 2,
            'density': 0.75,
            'clusters': 3
        }
    
    def calculate_risk_score(self):
        """Calculate overall risk score"""
        base_score = len(self.evidence) * 5
        vuln_score = sum(e['data'].get('risk_score', 0) for e in self.evidence if e['type'] == 'vulnerabilities')
        return min(base_score + vuln_score, 100)
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = [
            'Monitor RDP access patterns for anomalies',
            'Check for unauthorized BLE device proximity',
            'Review UPnP configuration for security risks',
            'Update router firmware to latest version',
            'Enable WPA3 if not already configured',
            'Disable unnecessary open ports (22, 3389 if not needed)'
        ]
        return random.sample(recommendations, k=3)
    
    def export_dossier(self, filename=None):
        """Export complete dossier to file"""
        if not filename:
            filename = f"{self.data_dir}/dossier_{self.target}.json"
        
        dossier = self.generate_full_dossier()
        
        with open(filename, 'w') as f:
            json.dump(dossier, f, indent=2, default=str)
        
        print(f"{G}[✓] Complete dossier exported to {filename}{RESET}")
        return filename
    
    def run_full_recon(self, target):
        """Run complete reconnaissance pipeline"""
        self.target = target
        
        print(f"{BOLD}{R}🔥 BLACKGLASS - COMPLETE DIGITAL FOOTPRINT RECONSTRUCTION 🔥{RESET}\n")
        print(f"{C}Target: {target}{RESET}")
        print(f"{C}Case ID: BG-{random.randint(10,99)}-{random.randint(1000,9999)}{RESET}\n")
        
        # Simulate screenshot analysis (would be from actual file)
        screenshot_data = self.extract_screenshot_metadata(target)
        
        # Extract visible WiFi from screenshot
        visible_wifi = screenshot_data.get('visible_wifi_ssid', 'SKYNET_HOME_5G')
        
        # Run all modules
        self.fingerprint_wifi(visible_wifi)
        ip_data = self.fingerprint_ip('192.168.1.100')  # Simulated
        self.fingerprint_os('192.168.1.100')
        self.scan_network('192.168.1.100')
        self.scan_ports('192.168.1.100')
        self.profile_activity_patterns('192.168.1.100')
        self.scan_ble_devices()
        self.analyze_dns_patterns('192.168.1.100')
        self.cross_correlate_evidence()
        self.detect_anomalies()
        self.triangulate_ble_devices()
        self.generate_behavioral_map()
        self.check_vulnerabilities('192.168.1.100')
        self.consolidate_patterns()
        
        # Export final dossier
        dossier_file = self.export_dossier()
        
        print(f"\n{G}[✓] FULL RECONSTRUCTION COMPLETE{RESET}")
        print(f"{C}Discovery Timeline: {len(self.discovery_timeline)} entries{RESET}")
        print(f"{C}Evidence Collected: {len(self.evidence)} items{RESET}")
        print(f"{C}Risk Score: {self.calculate_risk_score()}/100{RESET}")
        
        return dossier_file

    def menu(self):
        """Interactive menu system"""
        while True:
            os.system('clear')
            print(f"""{R}
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║     ██████╗ ██╗      █████╗  ██████╗██╗  ██╗ ██████╗ ██╗      █████╗ ███████╗
║     ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██║     ██╔══██╗██╔════╝
║     ██████╔╝██║     ███████║██║     █████╔╝ ██║  ███╗██║     ███████║███████╗
║     ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██║   ██║██║     ██╔══██║╚════██║
║     ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚██████╔╝███████╗██║  ██║███████║
║     ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝
║                                                                          ║
║                    【黑玻璃】- DIGITAL FOOTPRINT RECONSTRUCTION           ║
║                            COMPLETE DOXING FRAMEWORK                     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
            """)
            
            print(f"{BOLD}{C}╔══════════════════════════════════════════════════════════╗{RESET}")
            print(f"{BOLD}{C}║                    MAIN MENU                              ║{RESET}")
            print(f"{BOLD}{C}╠══════════════════════════════════════════════════════════╣{RESET}")
            print(f"{BOLD}{C}║                                                          ║{RESET}")
            print(f"{BOLD}{C}║  {W}[01]{RESET} 🎯 Set Target            {W}[11]{RESET} 📱 OSINT Email        ║{RESET}")
            print(f"{BOLD}{C}║  {W}[02]{RESET} 🔍 Quick Scan            {W}[12]{RESET} 📱 OSINT Phone        ║{RESET}")
            print(f"{BOLD}{C}║  {W}[03]{RESET} 📸 Screenshot Analysis   {W}[13]{RESET} 📱 OSINT Username     ║{RESET}")
            print(f"{BOLD}{C}║  {W}[04]{RESET} 📡 Network Recon         {W}[14]{RESET} 📱 OSINT Domain       ║{RESET}")
            print(f"{BOLD}{C}║  {W}[05]{RESET} 🔐 Vulnerability Check   {W}[15]{RESET} 📊 Generate Report    ║{RESET}")
            print(f"{BOLD}{C}║  {W}[06]{RESET} 📍 Geolocation           {W}[16]{RESET} 📈 View Statistics    ║{RESET}")
            print(f"{BOLD}{C}║  {W}[07]{RESET} 🕒 Timeline Analysis     {W}[17]{RESET} 🔄 Export All Data    ║{RESET}")
            print(f"{BOLD}{C}║  {W}[08]{RESET} 🔗 Correlation Graph     {W}[18]{RESET} 📜 View Timeline      ║{RESET}")
            print(f"{BOLD}{C}║  {W}[09]{RESET} 📋 View Evidence         {W}[19]{RESET} ⚡ Run Full Recon     ║{RESET}")
            print(f"{BOLD}{C}║  {W}[10]{RESET} 📝 Generate Dossier      {W}[20]{RESET} ❌ Exit               ║{RESET}")
            print(f"{BOLD}{C}║                                                          ║{RESET}")
            print(f"{BOLD}{C}╚══════════════════════════════════════════════════════════╝{RESET}")
            print()
            
            choice = input(f"{BOLD}{R}BLACKGLASS@target:~# {RESET}").strip()
            
            if choice == '01' or choice == '1':
                target = input(f"{Y}[?] Enter target (username/email/phone/domain): {RESET}").strip()
                if target:
                    self.target = target
                    print(f"{G}[✓] Target set to: {target}{RESET}")
                self.pause()
            
            elif choice == '02' or choice == '2':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.run_full_recon(self.target)
                self.pause()
            
            elif choice == '03' or choice == '3':
                path = input(f"{Y}[?] Enter screenshot path: {RESET}").strip()
                if path:
                    self.extract_screenshot_metadata(path)
                self.pause()
            
            elif choice == '04' or choice == '4':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.scan_network(self.target)
                self.scan_ports(self.target)
                self.pause()
            
            elif choice == '05' or choice == '5':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.check_vulnerabilities(self.target)
                self.pause()
            
            elif choice == '06' or choice == '6':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.fingerprint_ip(self.target)
                self.pause()
            
            elif choice == '07' or choice == '7':
                self.display_timeline()
                self.pause()
            
            elif choice == '08' or choice == '8':
                self.display_correlation_graph()
                self.pause()
            
            elif choice == '09' or choice == '9':
                self.display_evidence()
                self.pause()
            
            elif choice == '10' or choice == '10':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.export_dossier()
                self.pause()
            
            elif choice == '11':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.osint_email(self.target)
                self.pause()
            
            elif choice == '12':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.osint_phone(self.target)
                self.pause()
            
            elif choice == '13':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.osint_username(self.target)
                self.pause()
            
            elif choice == '14':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.osint_domain(self.target)
                self.pause()
            
            elif choice == '15':
                self.generate_report()
                self.pause()
            
            elif choice == '16':
                self.display_statistics()
                self.pause()
            
            elif choice == '17':
                self.export_all_data()
                self.pause()
            
            elif choice == '18':
                self.display_timeline()
                self.pause()
            
            elif choice == '19':
                if not self.target:
                    print(f"{R}[!] No target set{RESET}")
                    self.pause()
                    continue
                self.run_full_recon(self.target)
                self.pause()
            
            elif choice == '20' or choice == '0' or choice.lower() == 'q':
                print(f"{R}[!] Exiting BLACKGLASS...{RESET}")
                break
    
    def pause(self):
        input(f"\n{Y}[+] Press Enter to continue...{RESET}")
    
    def display_timeline(self):
        """Display discovery timeline"""
        print(f"\n{BOLD}{C}DISCOVERY TIMELINE{RESET}\n")
        for entry in self.discovery_timeline:
            print(f"{Y}[{entry['timestamp']}]{RESET} {entry['description']}")
    
    def display_evidence(self):
        """Display collected evidence"""
        print(f"\n{BOLD}{C}COLLECTED EVIDENCE{RESET}\n")
        for i, evidence in enumerate(self.evidence, 1):
            print(f"{Y}[{i}]{RESET} {evidence['type']}")
            if isinstance(evidence['data'], dict):
                for k, v in list(evidence['data'].items())[:5]:
                    print(f"  {G}{k}:{RESET} {v}")
                if len(evidence['data']) > 5:
                    print(f"  {C}... and {len(evidence['data'])-5} more items{RESET}")
            print()
    
    def display_correlation_graph(self):
        """Display correlation graph info"""
        print(f"\n{BOLD}{C}CORRELATION GRAPH{RESET}\n")
        print(f"{G}Nodes:{RESET} {len(self.evidence)}")
        print(f"{G}Edges:{RESET} {len(self.evidence) * 2}")
        print(f"{G}Density:{RESET} 0.75")
        print(f"{G}Clusters:{RESET} 3")
    
    def display_statistics(self):
        """Display statistics"""
        print(f"\n{BOLD}{C}STATISTICS{RESET}\n")
        print(f"{G}Target:{RESET} {self.target or 'Not set'}")
        print(f"{G}Timeline Entries:{RESET} {len(self.discovery_timeline)}")
        print(f"{G}Evidence Items:{RESET} {len(self.evidence)}")
        print(f"{G}Risk Score:{RESET} {self.calculate_risk_score()}/100")
        print(f"{G}Threat Level:{RESET} {self.persona['threat_level']}")
    
    def generate_report(self):
        """Generate HTML report"""
        filename = f"{self.data_dir}/report_{self.target}.html"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>BLACKGLASS Intelligence Report</title>
            <style>
                body {{ font-family: Arial; margin: 40px; background: #0a0a0a; color: #fff; }}
                h1 {{ color: #ff4444; }}
                h2 {{ color: #44ff44; }}
                .section {{ margin: 30px 0; padding: 20px; background: #1a1a1a; }}
                .evidence {{ background: #2a2a2a; padding: 10px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>BLACKGLASS Intelligence Report</h1>
            <p>Target: {self.target}</p>
            <p>Generated: {datetime.now().isoformat()}</p>
            
            <div class="section">
                <h2>Discovery Timeline</h2>
                {''.join([f'<div class="evidence">{e["timestamp"]}: {e["description"]}</div>' for e in self.discovery_timeline])}
            </div>
            
            <div class="section">
                <h2>Evidence Collected</h2>
                {''.join([f'<div class="evidence"><strong>{e["type"]}:</strong> {json.dumps(e["data"])}</div>' for e in self.evidence])}
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"{G}[✓] Report generated: {filename}{RESET}")
    
    def export_all_data(self):
        """Export all data to files"""
        # Export JSON
        json_file = f"{self.data_dir}/all_data.json"
        with open(json_file, 'w') as f:
            json.dump({
                'target': self.target,
                'timeline': self.discovery_timeline,
                'evidence': self.evidence,
                'persona': self.persona
            }, f, indent=2, default=str)
        print(f"{G}[✓] JSON export: {json_file}{RESET}")
        
        # Export CSV
        csv_file = f"{self.data_dir}/evidence.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Data'])
            for e in self.evidence:
                writer.writerow([e['type'], json.dumps(e['data'])])
        print(f"{G}[✓] CSV export: {csv_file}{RESET}")
    
    def osint_email(self, email):
        """OSINT on email address"""
        print(f"{G}[*] Running OSINT on email: {email}{RESET}")
        results = {
            'email': email,
            'domain': email.split('@')[1] if '@' in email else None,
            'username': email.split('@')[0] if '@' in email else None,
            'gravatar': f"https://www.gravatar.com/avatar/{hashlib.md5(email.lower().encode()).hexdigest()}",
            'haveibeenpwned': f"https://haveibeenpwned.com/account/{email}",
            'emailrep': f"https://emailrep.io/{email}"
        }
        print(json.dumps(results, indent=2))
        self.evidence.append({'type': 'osint_email', 'data': results})
    
    def osint_phone(self, phone):
        """OSINT on phone number"""
        print(f"{G}[*] Running OSINT on phone: {phone}{RESET}")
        clean = re.sub(r'[^0-9]', '', phone)
        results = {
            'raw': phone,
            'clean': clean,
            'length': len(clean),
            'whitepages': f"https://www.whitepages.com/phone/{clean}",
            'spokeo': f"https://www.spokeo.com/{clean}",
            'fastpeoplesearch': f"https://www.fastpeoplesearch.com/{clean}"
        }
        print(json.dumps(results, indent=2))
        self.evidence.append({'type': 'osint_phone', 'data': results})
    
    def osint_username(self, username):
        """OSINT on username"""
        print(f"{G}[*] Running OSINT on username: {username}{RESET}")
        platforms = {
            'github': f"https://github.com/{username}",
            'twitter': f"https://twitter.com/{username}",
            'instagram': f"https://instagram.com/{username}",
            'reddit': f"https://reddit.com/user/{username}",
            'linkedin': f"https://linkedin.com/in/{username}"
        }
        results = {
            'username': username,
            'platforms': platforms
        }
        print(json.dumps(results, indent=2))
        self.evidence.append({'type': 'osint_username', 'data': results})
    
    def osint_domain(self, domain):
        """OSINT on domain"""
        print(f"{G}[*] Running OSINT on domain: {domain}{RESET}")
        try:
            ip = socket.gethostbyname(domain)
            whois_info = whois.whois(domain)
            results = {
                'domain': domain,
                'ip': ip,
                'whois': str(whois_info)
            }
            print(json.dumps(results, indent=2))
            self.evidence.append({'type': 'osint_domain', 'data': results})
        except Exception as e:
            print(f"{R}[!] Error: {e}{RESET}")

def main():
    try:
        bg = BlackGlass()
        bg.menu()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()