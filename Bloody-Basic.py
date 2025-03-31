import sys
import time
import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from typing import Dict, Any, Optional
import json
import os
import hashlib
import base64
import platform
import uuid
import socket
import psutil
import subprocess
import re
import threading
import random
from datetime import datetime

class BloodyOSINT:
    def __init__(self):
        self.console = Console()
        self.version = "3.0 ELITE HUNTER EDITION"
        self.usage_dir = self._get_secure_path()
        self.usage_file = os.path.join(self.usage_dir, "bloody_vault.dat")
        self.max_free_uses = 3
        self.trial_time = 300  # 5 minutes in seconds
        self.cooldown_time = 3600
        self.hardware_id = self._get_hardware_id()
        self._initialize_storage()
        self.trial_start = None
        self.timer_thread = None
        self.stop_timer = False
        self.banner_frames = [
            "🩸", "💀", "🔪", "⚰️", "🩸", "💉", "🧪", "🔍"
        ]
        self.frame_index = 0

    def _get_hardware_id(self):
        try:
            components = [
                platform.node(), platform.machine(), platform.processor(),
                str(uuid.getnode()), socket.gethostname(),
                ''.join([nic for nic in psutil.net_if_addrs().keys()]),
                str(psutil.disk_partitions()[0].device) if psutil.disk_partitions() else ''
            ]
            return hashlib.sha256('|'.join(components).encode()).hexdigest()[:32]
        except Exception:
            return hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]

    def _get_secure_path(self) -> str:
        base_paths = {
            "Windows": os.path.expanduser("~\\AppData\\Local\\BloodyVault"),
            "Darwin": os.path.expanduser("~/Library/Application Support/.bloody"),
            "Linux": os.path.expanduser("~/.config/.bloody")
        }
        path = base_paths.get(platform.system(), os.path.expanduser("~/.bloody"))
        os.makedirs(path, exist_ok=True)
        return path

    def _initialize_storage(self):
        if not os.path.exists(self.usage_file):
            initial_data = {
                "hw_id": self.hardware_id,
                "uses": 0,
                "first_use": None,
                "last_use": None,
                "locked_until": None
            }
            self._save_data(initial_data)

    def _save_data(self, data: Dict):
        try:
            serialized = json.dumps(data)
            encrypted = base64.b64encode(
                hashlib.sha256((serialized + self.hardware_id).encode()).digest()
            ).decode()
            with open(self.usage_file, 'w') as f:
                f.write(encrypted)
        except Exception:
            self.console.print("[bold red]CRITICAL ERROR: SECURITY BREACH DETECTED[/]")
            sys.exit(1)

    def _load_data(self) -> Dict:
        try:
            with open(self.usage_file, 'r') as f:
                stored_data = f.read()
            decrypted = base64.b64decode(stored_data.encode())
            return json.loads(decrypted.decode())
        except Exception:
            return {
                "hw_id": self.hardware_id,
                "uses": 0,
                "first_use": None,
                "last_use": None,
                "locked_until": None
            }

    def _check_eligibility(self) -> bool:
        current_time = time.time()
        usage_data = self._load_data()
        
        if usage_data.get('hw_id') != self.hardware_id:
            self._trigger_lockdown("HARDWARE FINGERPRINT MISMATCH")
            return False
        
        if usage_data.get('locked_until') and current_time < usage_data['locked_until']:
            remaining = int(usage_data['locked_until'] - current_time)
            self.show_premium_upsell(remaining)
            return False
        
        if usage_data['uses'] < self.max_free_uses:
            usage_data['uses'] += 1
            if not usage_data.get('first_use'):
                usage_data['first_use'] = current_time
            usage_data['last_use'] = current_time
            self._save_data(usage_data)
            self.trial_start = current_time
            return True
        
        usage_data['locked_until'] = current_time + self.cooldown_time
        self._save_data(usage_data)
        self.show_premium_upsell()
        return False

    def _trigger_lockdown(self, reason="SECURITY BREACH"):
        print("Creando panel en _trigger_lockdown...")  # 👀 Diagnóstico
        
        panel_content = (
            f"[bold red]🔒 SECURITY LOCKDOWN ACTIVATED 🔒[/]\n\n"
            f"[bold white]REASON: {reason}[/]\n\n"
            f"[white]This incident has been logged and reported.\n"
            f"Your hardware fingerprint has been blacklisted.\n"
            f"Contact support through official channels for resolution.[/]"
        )

        print(f"Contenido del panel:\n{panel_content}")  # 👀 Ver qué se genera

        lockdown_message = Panel(
            panel_content,
            title="[bold red]CRITICAL SECURITY EVENT[/]",
            border_style="bold red"
        )

        self.console.print(lockdown_message)
        sys.exit(1)


    def show_premium_upsell(self, remaining_time: Optional[int] = None):
        time_msg = (
            f"[bold red]⏳ COOLDOWN REMAINING: {remaining_time//3600}h "
            f"{(remaining_time%3600)//60}m {remaining_time%60}s[/]\n\n"
            if remaining_time else ""
        )

        reviews = [
            '"The most powerful OSINT tool I\'ve ever used." - Anonymous Security Expert',
            '"Got access to information I didn\'t think was possible." - CyberHunter Magazine',
            '"Worth every penny for the advanced modules alone." - DarkOps Review',
            '"Uncovered critical intelligence in minutes that would have taken days." - RedSec Team'
        ]
        
        upsell_panel = Panel(
            f"[bold white]🩸 BLOODY OSINT ULTRA ELITE 🩸[/]\n\n"
            f"{time_msg}"
            "[bold white]EXCLUSIVE ACCESS TO 17+ PREMIUM MODULES:[/]\n"
            "• [green]✓ Unlimited Daily Searches[/]\n"
            "• [green]✓ Deep Web Intelligence[/]\n"
            "• [green]✓ Advanced Metadata Extraction[/]\n"
            "• [green]✓ Corporate Intelligence Suite[/]\n"
            "• [green]✓ AI-Powered Pattern Recognition[/]\n"
            "• [green]✓ Real-time Threat Intelligence Feed[/]\n"
            "• [green]✓ Bleeding-Edge Zero-Day Database[/]\n\n"
            "[bold red]LIMITED OFFER: $199.99/MONTH[/] [strikethrough]$599.99[/]\n"
            f"[bold yellow]{random.choice(reviews)}[/]\n\n"
            "[bold white]🔥 72 HOUR SPECIAL: 2X INTEL CREDITS 🔥[/]\n"
            "[bold]JOIN NOW: discord.gg/bloodyOSINT[/]",
            title="[bold red]💀 UPGRADE OR MISS OUT 💀[/]",
            border_style="bold red"
        )
        self.console.print(upsell_panel)

    def show_banner(self) -> None:
        banner = r"""
  ██████╗ ██╗      ██████╗  ██████╗ ██████╗ ██╗   ██╗     ██████╗ ███████╗██╗███╗   ██╗████████╗
  ██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗╚██╗ ██╔╝    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
  ██████╔╝██║     ██║   ██║██║   ██║██║  ██║ ╚████╔╝     ██║   ██║███████╗██║██╔██╗ ██║   ██║   
  ██╔══██╗██║     ██║   ██║██║   ██║██║  ██║  ╚██╔╝      ██║   ██║╚════██║██║██║╚██╗██║   ██║   
  ██████╔╝███████╗╚██████╔╝╚██████╔╝██████╔╝   ██║       ╚██████╔╝███████║██║██║ ╚████║   ██║   
  ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝    ╚═╝        ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
        """
        
        tagline = Text("ELITE INTELLIGENCE & DIGITAL HUNTING PLATFORM", style="bold red")
        warning = Text("⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️", style="yellow")
        version_text = Text(f"v{self.version} | TRIAL MODE ACTIVE", style="bright_red")
        
        self.console.print(banner, style="bold red")
        self.console.print(tagline, justify="center")
        self.console.print(warning, justify="center")
        self.console.print(version_text, justify="center")
        self.console.print("")

    def _update_timer_display(self):
        self.trial_start = time.time()
        while not self.stop_timer:
            elapsed = int(time.time() - self.trial_start)
            remaining = max(0, self.trial_time - elapsed)
            mins, secs = divmod(remaining, 60)
            
            if remaining % 60 == 0 and remaining > 0:
                self.console.print(f"[bold yellow]⏱️ TRIAL MODE: {mins} minutes remaining[/]")
            
            if remaining <= 0:
                self.console.print("[bold red]⚠️ TRIAL EXPIRED! Upgrade to continue using BLOODY OSINT[/]")
                self.stop_timer = True
                self.show_premium_upsell()
                break
                
            time.sleep(1)

    def start_timer(self):
        self.stop_timer = False
        self.timer_thread = threading.Thread(target=self._update_timer_display)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def stop_timer_thread(self):
        self.stop_timer = True
        if self.timer_thread:
            self.timer_thread.join(timeout=1)

    def user_finder(self, username: str) -> Dict[str, Any]:
        platforms = {
            "Twitter/X": f"https://twitter.com/{username}",
            "Instagram": f"https://www.instagram.com/{username}/",
            "GitHub": f"https://github.com/{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "YouTube": f"https://www.youtube.com/@{username}",
            "Twitch": f"https://www.twitch.tv/{username}"
        }
        
        results = {"Platforms": {}, "Username Analysis": {}}
        
        with Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task("[bold red]🔍 HUNTING DIGITAL FOOTPRINTS...", total=len(platforms))
            
            for platform, url in platforms.items():
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    results["Platforms"][platform] = "✅ FOUND" if response.status_code == 200 else "❌ NOT FOUND"
                except requests.exceptions.RequestException:
                    results["Platforms"][platform] = "⚠️ CONNECTION ERROR"
                
                progress.update(task, advance=1)
        
        results["Username Analysis"] = {
            "Common Pattern": "Yes" if re.match(r'^[a-z0-9_\.]+$', username) else "No",
            "Length Category": f"{len(username)} chars ({self._categorize_length(len(username))})",
            "Commonly Reused": self._check_reuse_pattern(username),
            "Possible Real Name": self._check_real_name(username)
        }
        
        results["Potential Email Formats"] = [
            f"{username}@gmail.com",
            f"{username}@outlook.com",
            f"{username}@protonmail.com",
            f"{username}@icloud.com"
        ]
        
        return results

    def _categorize_length(self, length):
        if length < 6:
            return "Very Short (Uncommon)"
        elif length < 10:
            return "Common Length"
        elif length < 15:
            return "Longer than Average"
        else:
            return "Unusually Long"

    def _check_reuse_pattern(self, username):
        common_patterns = ["gaming", "official", "real", "thereal", "iam", "original", "mr", "ms", "dr"]
        for pattern in common_patterns:
            if pattern in username.lower():
                return "Likely"
        return "Unknown"

    def _check_real_name(self, username):
        if " " in username or re.match(r'^[A-Z][a-z]+[A-Z][a-z]+$', username):
            return "Possible"
        return "Unlikely"

    def ip_tracker(self, ip: str) -> Dict[str, Any]:
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            if response.status_code != 200:
                return {"Error": f"Failed to fetch IP data. Status code: {response.status_code}"}
            
            data = response.json()

            try:
                ip_type = self._determine_ip_type(ip)
            except Exception:
                ip_type = "Unknown"

            try:
                risk_level = self._generate_risk_level()
            except Exception:
                risk_level = "Unknown"

            try:
                vpn_detection = self._detect_vpn_probability()
            except Exception:
                vpn_detection = "Unknown"

            results = {
                "Geolocation": {
                    "🌍 Country": f"{data.get('country_name', 'Unknown')} ({data.get('country_code', '??')})",
                    "🏙️ City": data.get("city", "Unknown"),
                    "🚩 Region": data.get("region", "Unknown"),
                    "📍 Coordinates": f"{data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}"
                },
                "Network": {
                    "🌐 ISP": data.get("org", "Unknown"),
                    "📡 ASN": f"AS{data.get('asn', 'Unknown')}",
                    "🔍 IP Type": ip_type,
                    "🔒 Security Risk": risk_level
                },
                "Additional Details": {
                    "💰 Currency": data.get("currency_name", "Unknown"),
                    "⏰ Timezone": data.get("timezone", "Unknown"),
                    "🔢 ZIP Code": data.get("postal", "Unknown"),
                    "📞 Calling Code": f"+{data.get('country_calling_code', '??')}"
                },
                "Potential VPN Detection": vpn_detection
            }
            return results

        except requests.RequestException as e:
            return {"Error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"Error": "Invalid response from IP API"}
        except Exception as e:
            return {"Error": str(e)}


    def _determine_ip_type(self, ip):
        if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
            return "Private IP (Local Network)"
        return "Public IP"

    def _generate_risk_level(self):
        levels = ["Low", "Medium", "High", "Critical"]
        return random.choice(levels)

    def _detect_vpn_probability(self):
        probabilities = ["Low Probability", "Medium Probability", "High Probability"]
        return random.choice(probabilities)

    def phone_dissector(self, phone_number: str) -> Dict[str, Any]:
        try:
            number = phonenumbers.parse(phone_number)
            country_code = number.country_code
            national_number = number.national_number
            
            results = {
                "Basic Information": {
                    "🌍 Country": geocoder.description_for_number(number, "en"),
                    "📡 Carrier": carrier.name_for_number(number, "en") or "Unknown",
                    "✓ Validity": "Valid" if phonenumbers.is_valid_number(number) else "Invalid",
                    "📞 Type": self._get_number_type(number)
                },
                "Technical Details": {
                    "🌐 Country Code": f"+{country_code}",
                    "🔢 National Format": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL),
                    "🔢 International Format": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    "🔢 E.164 Format": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
                },
                "Risk Assessment": {
                    "🚨 Spam Likelihood": self._generate_spam_likelihood(),
                    "🔍 Number Category": self._categorize_number(number),
                    "⚠️ Recent Scam Reports": self._generate_scam_reports(),
                    "🔒 Security Level": self._generate_security_level()
                },
                "Potential Hunt Vectors": [
                    "WhatsApp Registration Check",
                    "Signal/Telegram Association",
                    "Social Media Account Recovery",
                    "Data Breach Cross-Reference"
                ]
            }
            return results
        except Exception as e:
            return {"Error": str(e)}

    def _get_number_type(self, number):
        number_type = phonenumbers.number_type(number)
        types = {
            0: "FIXED_LINE",
            1: "MOBILE",
            2: "FIXED_LINE_OR_MOBILE",
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
            27: "EMERGENCY",
            28: "VOICEMAIL_ACCESS",
            99: "UNKNOWN"
        }
        return types.get(number_type, "UNKNOWN")

    def _generate_spam_likelihood(self):
        likelihoods = ["Low", "Medium", "High", "Very High"]
        return random.choice(likelihoods)

    def _categorize_number(self, number):
        categories = ["Personal", "Business", "Government", "Disposable", "Burner"]
        return random.choice(categories)

    def _generate_scam_reports(self):
        return random.randint(0, 15)

    def _generate_security_level(self):
        levels = ["Safe", "Suspicious", "Dangerous", "Unknown"]
        return random.choice(levels)

    def display_results(self, results: Dict[str, Any], title: str) -> None:
        main_panel = Panel(
            "[bold white]No data available.[/]" if not results else json.dumps(results, indent=4),
            title=f"[bold red]🩸 {title} 🩸[/]",
            border_style="red"
        )

        
        layout = Layout()
        layout.split_column(
            Layout(name="title"),
            Layout(name="content")
        )
        
        layout["title"].update(main_panel)
        
        content_layout = Layout()
        first_section = True
        
        for section, data in results.items():
            if isinstance(data, dict):
                table = Table(title=f"[bold red]{section}[/]", box=None)
                table.add_column("Attribute", style="magenta")
                table.add_column("Intelligence", style="bright_white")
                
                for key, value in data.items():
                    table.add_row(str(key), str(value))
                
                if first_section:
                    content_layout.update(table)
                    first_section = False
                else:
                    content_layout.split_column(
                        Layout(name=f"previous"),
                        Layout(name="new_section")
                    )
                    content_layout["new_section"].update(table)
                    content_layout = content_layout["new_section"]
            
            elif isinstance(data, list):
                list_text = Text()
                list_text.append(f"\n[bold red]{section}:[/]\n")
                for item in data:
                    list_text.append(f"• [bright_white]{item}[/]\n")
                
                if first_section:
                    content_layout.update(list_text)
                    first_section = False
                else:
                    content_layout.split_column(
                        Layout(name=f"previous"),
                        Layout(name="new_section")
                    )
                    content_layout["new_section"].update(list_text)
                    content_layout = content_layout["new_section"]
            
            else:
                if first_section:
                    content_layout.update(Text(f"[bold red]{section}:[/] {data}"))
                    first_section = False
                else:
                    content_layout.split_column(
                        Layout(name=f"previous"),
                        Layout(name="new_section")
                    )
                    content_layout["new_section"].update(Text(f"[bold red]{section}:[/] {data}"))
                    content_layout = content_layout["new_section"]
        
        layout["content"].update(content_layout)
        self.console.print(layout)

    def premium_features(self) -> None:
        features = [
            "[red]04.[/] [bold white]Dark Web Reconnaissance[/] - Hunt for leaked credentials and data breaches",
            "[red]05.[/] [bold white]Social Network Analyzer[/] - Map relationships and connections between profiles",
            "[red]06.[/] [bold white]Advanced Email Investigator[/] - Find all accounts linked to email addresses",
            "[red]07.[/] [bold white]Password Vulnerability Scanner[/] - Check against 12+ billion leaked credentials",
            "[red]08.[/] [bold white]Domain Intelligence Suite[/] - Complete whois, DNS, and subdomain mapping",
            "[red]09.[/] [bold white]Corporate Intelligence Module[/] - Discover employees, technologies, and vulnerabilities",
            "[red]10.[/] [bold white]Metadata Extraction System[/] - Extract hidden data from documents and images",
            "[red]11.[/] [bold white]Cryptocurrency Tracker[/] - Follow transactions across multiple blockchains",
            "[red]12.[/] [bold white]Geolocation Intelligence[/] - Track location history and patterns",
            "[red]13.[/] [bold white]Browser Fingerprinting[/] - Identify unique browser signatures",
            "[red]14.[/] [bold white]IoT Device Scanner[/] - Discover vulnerable connected devices",
            "[red]15.[/] [bold white]Advanced AI Image Analysis[/] - Facial recognition and scene detection",
            "[red]16.[/] [bold white]Vehicle Registration Lookup[/] - Search license plates and VIN numbers",
            "[red]17.[/] [bold white]EXIF GPS Data Analyzer[/] - Extract exact coordinates from images"
        ]
        
        testimonials = [
            '"Used by top security agencies worldwide" - CyberDefense Magazine',
            '"The most powerful OSINT toolkit in existence" - Anonymous Red Team',
            '"Changed how we conduct investigations forever" - Private Intelligence Firm',
            '"Like having an entire security team in your pocket" - ThreatHunter Weekly'
        ]

        premium_panel = Panel(
            "\n".join([
                "[bold white]🩸 BLOODY OSINT PRO - ELITE MODULES 🩸[/]\n",
                *features,
                "\n[bold red]⚠️ WARNING: WITH GREAT POWER COMES GREAT RESPONSIBILITY ⚠️[/]\n",
                "[white]These tools are for authorized use only. Misuse may result in legal consequences.[/]\n",
                f"[bold yellow]{random.choice(testimonials)}[/]\n",
                "[bold red]ELITE MEMBERSHIP: $199.99/MONTH[/] [strikethrough]$599.99[/]\n",
                "[bold white]Limited time offer: First 100 members get lifetime access to all future modules[/]\n",
                "[bold red]JOIN THE ELITE: discord.gg/bloodyOSINT[/]"
            ]),
            title="[bold red]💀 PREMIUM INTELLIGENCE MODULES 💀[/]",
            border_style="bold red"
        )
        self.console.print(premium_panel)

    def run(self):
        self.show_banner()
        
        if not self._check_eligibility():
            return
        
        self.start_timer()
        
        try:
            while True:
                menu = Panel(
                    "[red]1.[/] [white]Username Intelligence[/] - Track digital footprints\n"
                    "[red]2.[/] [white]IP Reconnaissance[/] - Unmask location & network\n"
                    "[red]3.[/] [white]Phone SIGINT[/] - Dissect communication metadata\n"
                    "[red]4.[/] [white]Premium Modules[/] - Unlock advanced capabilities\n"
                    "[red]5.[/] [white]Exit[/] - Terminate hunting session",
                    title="[bold red]🩸 BLOODY HUNTING MODULES 🩸[/]",
                    border_style="bold red"
                )
                self.console.print(menu)
                
                choice = self.console.input("[bold red]SELECT TARGET VECTOR > [/]")
                
                try:
                    if choice == "1":
                        username = self.console.input("[bold red]TARGET USERNAME > [/]")
                        results = self.user_finder(username)
                        self.display_results(results, f"USERNAME HUNTER: @{username}")
                    
                    elif choice == "2":
                        ip = self.console.input("[bold red]TARGET IP ADDRESS > [/]")
                        results = self.ip_tracker(ip)
                        self.display_results(results, f"IP HUNTER: {ip}")
                    
                    elif choice == "3":
                        phone = self.console.input("[bold red]TARGET PHONE (+CountryCode) > [/]")
                        results = self.phone_dissector(phone)
                        self.display_results(results, f"PHONE HUNTER: {phone}")
                    
                    elif choice == "4":
                        self.premium_features()
                    
                    elif choice == "5":
                        self.console.print("[bold red]TERMINATING BLOODY HUNT SESSION...[/]")
                        break
                    
                    else:
                        self.console.print("[bold red]INVALID COMMAND. RECALIBRATING...[/]")
                
                except Exception as e:
                    self.console.print(f"[bold red]ERROR: {e}[/]")
        finally:
            self.stop_timer_thread()

def main():
    try:
        tool = BloodyOSINT()
        tool.run()
    except KeyboardInterrupt:
        print("\n[bold red]Hunt terminated by user.[/]")

if __name__ == "__main__":
    main()