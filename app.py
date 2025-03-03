import requests
import hashlib
import uuid
import random
import string
import time
import threading
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

banner = Panel(
    "[bold yellow]PYEUL SPAMSHARE & TOKEN GENERATOR[/bold yellow]", 
    width=60, 
    title="[bold cyan]SPAMSHARE Bot[/bold cyan]", 
    border_style="blue",
    expand=False
)
console.print(banner)

# Function to generate a random string
def random_string(length):
    characters = string.ascii_lowercase + "0123456789"
    return ''.join(random.choice(characters) for _ in range(length))

# Function to encode signature for Facebook login request
def encode_sig(data):
    sorted_data = {k: data[k] for k in sorted(data)}
    data_str = ''.join(f"{key}={value}" for key, value in sorted_data.items())
    return hashlib.md5((data_str + '62f8ce9f74b12f84c123cc23437a4a32').encode()).hexdigest()

# Function to generate a Facebook access token with session handling
def generate_token(email, password, proxy=None):
    session = requests.Session()
    
    # Add proxy support if provided
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})

    device_id = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    random_str = random_string(24)

    # Facebook login request parameters
    form = {
        'adid': adid,
        'email': email,
        'password': password,
        'format': 'json',
        'device_id': device_id,
        'cpl': 'true',
        'family_device_id': device_id,
        'locale': 'en_US',
        'client_country_code': 'US',
        'credentials_type': 'device_based_login_password',
        'generate_session_cookies': '1',
        'generate_analytics_claim': '1',
        'generate_machine_id': '1',
        'source': 'login',
        'machine_id': random_str,
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
    }

    form['sig'] = encode_sig(form)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; SM-G960F Build/PPR1.180610.011)'
    }

    url = 'https://b-graph.facebook.com/auth/login'

    try:
        response = session.post(url, data=form, headers=headers)
        data = response.json()

        if 'access_token' in data:
            console.print(f"[green]Login successful! Token generated.[/green]")
            return data['access_token']
        
        elif 'error' in data:
            error_message = data['error'].get('message', 'Unknown error')
            console.print(f"[red]Login failed: {error_message}[/red]")

            if "checkpoint" in error_message.lower():
                console.print("[yellow]Account requires verification! Try logging in manually.[/yellow]")

            return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request failed: {e}[/red]")
        return None

# Function to share a post using the generated token
def share_post(token, share_url, share_count):
    url = "https://graph.facebook.com/me/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "link": share_url,
        "privacy": '{"value":"SELF"}',
        "no_story": "true",
        "published": "false",
        "access_token": token
    }

    for i in range(1, share_count * 2 + 1):
        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            post_id = response_data.get("id", None)

            if post_id:
                console.print(f"[bold cyan]({i}/{share_count * 2})[/bold cyan] [green]Post shared successfully!")
            else:
                console.print(f"[red]({i}/{share_count * 2}) Failed: {response_data}")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Failed: {e}")
        time.sleep(0.1)

# Function for single token spam sharing
def spam_share_single():
    token = input("Enter your Facebook access token: ").strip()
    if not token.startswith("EAAAA"):
        console.print("[red]Invalid token format!")
        return
    share_url = input("Enter your post link: ").strip()
    share_count = int(input("Enter Share Count: ").strip())
    share_post(token, share_url, share_count)

# Function for multiple account spam sharing
def spam_share_multiple():
    tokens = input("Paste your tokens (comma separated): ").strip().split(',')
    share_url = input("Enter your post link: ").strip()
    share_count = int(input("Enter Share Count per account: ").strip())

    threads = [threading.Thread(target=share_post, args=(token, share_url, share_count)) for token in tokens]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

# Main menu function
def main_menu():
    while True:
        console.print(Panel("""  
[1] Generate Token  
[2] Multi-Account Spam Share  
[3] Single Token Share  
[4] Exit  
""", width=60, style="bold bright_white"))

        choice = input("Select an option: ").strip()

        if choice == "1":
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            use_proxy = input("Use proxy? (y/n): ").strip().lower()
            proxy = input("Enter proxy (if any): ").strip() if use_proxy == "y" else None

            token = generate_token(email, password, proxy)
            if token:
                console.print(f"\n[+] Generated Token: {token}\n")
            else:
                console.print("[red]Token generation failed!")

        elif choice == "2":
            spam_share_multiple()

        elif choice == "3":
            spam_share_single()

        elif choice == "4":
            console.print("[red]Exiting... Goodbye!")
            break

        else:
            console.print("[red]Invalid choice!")

# Run the main menu
if __name__ == '__main__':
    main_menu()
