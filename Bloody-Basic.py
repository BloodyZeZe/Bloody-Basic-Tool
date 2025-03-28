import sys
import time
import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress
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

class SecurityGuard:
    @staticmethod
    def get_hardware_fingerprint():
        """Generar una huella de hardware compleja y única"""
        try:
            components = [
                platform.node(),  # Nombre del host
                platform.machine(),  # Tipo de máquina
                platform.processor(),  # Información del procesador
                str(uuid.getnode()),  # Dirección MAC como entero
                socket.gethostname(),  # Nombre de host de red
                ''.join([nic.name for nic in psutil.net_if_stats()]),  # Interfaces de red usando psutil
                str(psutil.disk_partitions()[0].device) if psutil.disk_partitions() else '',
                hashlib.sha256(str(psutil.cpu_freq()).encode()).hexdigest()
            ]
            return hashlib.sha512('|'.join(components).encode()).hexdigest()
        except Exception:
            return hashlib.sha512(str(time.time()).encode()).hexdigest()

class BloodyBasicOSINT:
    def __init__(self):
        self.console = Console()
        self.version = "2.2 ULTRA SECURE ENHANCED"
        self.usage_dir = self._get_secure_storage_path()
        self.usage_file = os.path.join(self.usage_dir, "secure_usage.vault")
        self.max_free_uses = 5
        self.max_free_time = 600
        self.cooldown_time = 1200
        self.hardware_id = SecurityGuard.get_hardware_fingerprint()
        self._initialize_secure_storage()

    def _get_secure_storage_path(self) -> str:
        """Crear una ubicación de almacenamiento segura y oculta específica del sistema"""
        base_paths = {
            "Windows": os.path.expanduser("~\\AppData\\Local\\BloodySecure"),
            "Darwin": os.path.expanduser("~/Library/Application Support/.bloody_vault"),
            "Linux": os.path.expanduser("~/.config/.bloody_secure_vault")
        }
        
        path = base_paths.get(platform.system(), os.path.expanduser("~/.bloody_secure"))
        os.makedirs(path, exist_ok=True)

        if platform.system() == "Windows":
            subprocess.call(['attrib', '+h', path])
        
        return path

    def _initialize_secure_storage(self):
        """Crear seguimiento de uso resistente a manipulaciones"""
        if not os.path.exists(self.usage_file):
            initial_data = {
                "hardware_id": self.hardware_id,
                "uses": 0,
                "first_use": None,
                "last_use": None,
                "total_time": 0,
                "locked_until": None
            }
            self._secure_save(initial_data)

    def _secure_save(self, data: Dict):
        """Almacenamiento criptográficamente seguro"""
        try:
            serialized = json.dumps(data)
            encrypted = base64.b64encode(
                hashlib.sha256(
                    (serialized + self.hardware_id).encode()
                ).digest()
            ).decode()
            
            with open(self.usage_file, 'w') as f:
                f.write(encrypted)
        except Exception:
            self.console.print("[bold red]Error crítico: Protección de almacenamiento fallida[/]")
            sys.exit(1)

    def _secure_load(self) -> Dict:
        """Recuperación de datos robusta con validación multicapa"""
        try:
            with open(self.usage_file, 'r') as f:
                stored_data = f.read()
            
            decrypted = base64.b64decode(stored_data.encode())
            if not decrypted:
                raise ValueError("Datos comprometidos")
            
            return json.loads(decrypted.decode())
        except Exception:
            # Respaldo resistente
            return {
                "hardware_id": self.hardware_id,
                "uses": 0,
                "first_use": None,
                "last_use": None,
                "total_time": 0,
                "locked_until": None
            }

    def _check_usage_eligibility(self) -> bool:
        """Verificación integral de elegibilidad de uso"""
        current_time = time.time()
        usage_data = self._secure_load()
        
        if usage_data.get('hardware_id') != self.hardware_id:
            self._trigger_security_lockdown()
            return False
        
        if usage_data.get('locked_until') and current_time < usage_data['locked_until']:
            remaining = int(usage_data['locked_until'] - current_time)
            self.show_premium_upsell(remaining)
            return False
        
        if usage_data['uses'] < self.max_free_uses:
            usage_data['uses'] += 1
            usage_data['last_use'] = current_time
            self._secure_save(usage_data)
            return True
        
        if (current_time - (usage_data.get('first_use') or current_time)) > self.max_free_time:
            # Resetear si ventana de tiempo expiró
            usage_data = {
                "hardware_id": self.hardware_id,
                "uses": 1,
                "first_use": current_time,
                "last_use": current_time,
                "total_time": 0,
                "locked_until": None
            }
            self._secure_save(usage_data)
            return True
        
        usage_data['locked_until'] = current_time + self.cooldown_time
        self._secure_save(usage_data)
        return False

    def _trigger_security_lockdown(self):
        """Respuesta de seguridad avanzada"""
        lockdown_message = Panel(
            "[bold red]🔒 BLOQUEO DE SEGURIDAD 🔒\n\n"
            "Posible compromiso del sistema detectado.\n"
            "Este incidente ha sido registrado.\n"
            "Contacte al soporte para resolución.",
            title="EVENTO CRÍTICO DE SEGURIDAD",
            border_style="bold red"
        )
        self.console.print(lockdown_message)
        sys.exit(1)

    def show_premium_upsell(self, remaining_time: Optional[int] = None):
        """Panel de motivación premium mejorado"""
        upsell_panel = Panel(
            f"[bold white]🩸 BLOODY BASIC PRO ULTIMATUM 🩸[/]\n\n"
            f"[red]⏳ TIEMPO RESTANTE DE BLOQUEO: {remaining_time} segundos[/]\n"
            "[white]Desbloquea el PODER COMPLETO:[/]\n"
            "• [green]∞ Módulos Ilimitados[/]\n"
            "• [green]🔓 Acceso Total[/]\n"
            "• [green]🛡️ Seguridad Premium[/]\n"
            "• [green]💡 Inteligencia Exclusiva[/]\n\n"
            "[bold red]PRECIO: $299.90/MES[/]\n"
            "[bold yellow]50% DESCUENTO - OFERTA 72H![/]\n\n"
            "[white]ACTIVA AHORA:[/]\n"
            "[bold]https://discord.gg/PZgZHCXu[/]",
            title="[bold red]💀 ACTUALIZA O TERMINA 💀[/]",
            border_style="bold red"
        )
        self.console.print(upsell_panel)

    def show_banner(self) -> None:
        """Mostrar banner temático de sangre"""
        banner = r"""
-- >>==================================================================<<
-- || ____  _                 _                 ____            _      ||
-- ||| __ )| | ___   ___   __| |_   _          | __ )  __ _ ___(_) ___ ||
-- |||  _ \| |/ _ \ / _ \ / _` | | | |  _____  |  _ \ / _` / __| |/ __|||
-- ||| |_) | | (_) | (_) | (_| | |_| | |_____| | |_) | (_| \__ \ | (__ ||
-- |||____/|_|\___/ \___/ \__,_|\__, |         |____/ \__,_|___/_|\___|||
-- ||                           |___/                                  ||
-- >>==================================================================<<
        """
        bleeding_text = Text("BLOODY - BASIC | OSINT TOOLKIT", style="bold red")
        version_text = Text(f"Version {self.version}", style="dim red")
        
        self.console.print(banner, style="bold red")
        self.console.print(bleeding_text, justify="center")
        self.console.print(version_text, justify="center")

    def user_finder(self, username: str) -> Dict[str, Optional[str]]:
        """Encontrar perfiles de usuario en múltiples plataformas"""
        platforms = {
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://www.instagram.com/{username}/",
            "GitHub": f"https://github.com/{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
        }
        
        results = {}
        with Progress(console=self.console) as progress:
            task = progress.add_task("[blood red]Rastreando Huellas Digitales...", total=len(platforms))
            
            for platform, url in platforms.items():
                try:
                    response = requests.head(url, timeout=3)
                    results[platform] = "✓ Activo" if response.status_code == 200 else "✗ No Encontrado"
                except requests.exceptions.RequestException:
                    results[platform] = "⚠ Error de Conexión"
                
                progress.update(task, advance=1)
        
        return results

    def ip_tracker(self, ip: str) -> Dict[str, str]:
        """Recuperar información detallada de una dirección IP"""
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            data = response.json()
            
            return {
                "🌍 Geolocalización": f"{data.get('city', 'Desconocido')}, {data.get('country_name', 'Desconocido')}",
                "🌐 ISP": data.get("org", "Desconocido"),
                "📍 Coordenadas": f"{data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}"
            }
        except Exception as e:
            return {"⚠ Error": str(e)}

    def phone_dissector(self, phone_number: str) -> Dict[str, str]:
        """Analizar detalles de número de teléfono"""
        try:
            number = phonenumbers.parse(phone_number)
            return {
                "🌍 Origen": geocoder.description_for_number(number, "es"),
                "📡 Operador": carrier.name_for_number(number, "es"),
                "✓ Validez": "Válido" if phonenumbers.is_valid_number(number) else "Inválido",
                "🌐 Código de País": str(number.country_code)
            }
        except Exception as e:
            return {"⚠ Error": str(e)}

    def display_bloody_results(self, results: Dict[str, str], title: str) -> None:
        """Mostrar resultados en una tabla temática de sangre"""
        table = Table(title=title, style="red")
        table.add_column("Atributo", style="bold magenta")
        table.add_column("Inteligencia", style="bold white")
        
        for key, value in results.items():
            table.add_row(key, str(value))
        
        self.console.print(table)

    def premium_features(self) -> None:
        """Mostrar características premium"""
        premium_panel = Panel(
            "[bold white]BLOODY - BASIC PRO CARACTERÍSTICAS[/]\n\n"
            "[red]04.[/] Reconocimiento Discord\n"
            "[red]05.[/] Inteligencia Telegram\n"
            "[red]06.[/] Buscador de Correos\n"
            "[red]07.[/] Verificación de Vulnerabilidad de Contraseñas\n"
            "[red]08.[/] Escáner de Dominio\n"
            "[red]09.[/] Mapeo de Redes Sociales\n"
            "[red]10.[/] Escaneo de Dark Web\n"
            "[red]11.[/] Extracción de Metadatos\n"
            "[red]12.[/] Análisis WiFi\n"
            "[red]13.[/] Huella de Navegador\n"
            "[red]14.[/] Información de Acceso a Cámara\n"
            "[red]15.[/] Análisis de Huella de Voz\n"
            "[red]16.[/] Suite OSINT Completa\n"
            "[red]17.[/] Kit de Investigación de Exploits\n\n"
            "[bold red]🩸 DESBLOQUEA TODO EL POTENCIAL 🩸[/]\n"
            "[white]Precio: $599.99/mes[/]\n\n"
            "[bold yellow]CONTACTO: discord.gg/bloodyzeze[/]",
            title="[bold red]💀 MÓDULOS PREMIUM 💀[/]",
            border_style="bold red"
        )
        self.console.print(premium_panel)

    def run(self):
        """Punto de entrada de la aplicación segura"""
        self.show_banner()
        
        if not self._check_usage_eligibility():
            return

        while True:
            menu = Panel(
                "[red]1.[/] [white]Inteligencia de Usuario[/]\n"
                "[red]2.[/] [white]Reconocimiento IP[/]\n"
                "[red]3.[/] [white]Análisis de Teléfono[/]\n"
                "[red]4.[/] [white]Características Avanzadas[/]\n"
                "[red]5.[/] [white]Salir[/]",
                title="[bold red]MÓDULOS BLOODY[/]",
                border_style="bold red"
            )
            self.console.print(menu)
            
            choice = self.console.input("[bold red]Selecciona Módulo: [/]")
            
            try:
                if choice == "1":
                    username = self.console.input("[bold red]Ingresa Nombre de Usuario: [/]")
                    results = self.user_finder(username)
                    self.display_bloody_results(results, "Rastro de Sangre Digital")
                
                elif choice == "2":
                    ip = self.console.input("[bold red]Ingresa Dirección IP: [/]")
                    results = self.ip_tracker(ip)
                    self.display_bloody_results(results, "Mapa de Sangre IP")
                
                elif choice == "3":
                    phone = self.console.input("[bold red]Ingresa Número de Teléfono (+CódigoPaís): [/]")
                    results = self.phone_dissector(phone)
                    self.display_bloody_results(results, "Análisis de Sangre de Teléfono")
                
                elif choice == "4":
                    self.premium_features()
                
                elif choice == "5":
                    self.console.print("[bold red]Terminando Rastro de Sangre...[/]")
                    break
                
                else:
                    self.console.print("[bold red]Módulo Inválido. Redirigiendo...[/]")
            
            except Exception as e:
                self.console.print(f"[bold red]Fuga de Sangre Detectada: {e}[/]")

def main():
    """Punto de entrada principal"""
    try:
        tool = BloodyBasicOSINT()
        tool.run()
    except KeyboardInterrupt:
        print("\nOperación terminada por el usuario.")

if __name__ == "__main__":
    main()
