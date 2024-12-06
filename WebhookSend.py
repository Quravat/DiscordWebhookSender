import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

def send_message(url, message, username, avatar_url):
    """Sends a message to the Discord webhook and prints status with color."""
    payload = {
        'content': message,
        'username': username if username else 'Webhook Bot',
        'avatar_url': avatar_url if avatar_url else ''
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Message sent successfully to {url}")
        else:
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Failed to send message. Status code: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Exception occurred: {e}")
        return str(e)

def send_messages_to_webhook(url, message, username, avatar_url, count=1):
    """Sends multiple messages to the Discord webhook using multi-threading."""
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting to send {count} messages to {url}")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_message, url, message, username, avatar_url) for _ in range(count)]
        
        for future in futures:
            status_code = future.result()
            if isinstance(status_code, int) and status_code != 200:
                print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Non-success status code received: {status_code}")

if __name__ == "__main__":
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Welcome to Discord Webhook Messenger!")
    webhook_url = input(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} Enter the Discord webhook URL: ")
    message = input(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} Enter the message to send: ")
    username = input(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} Enter the username (optional): ")
    avatar_url = input(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} Enter the avatar URL (optional): ")
    try:
        count = int(input(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} Enter the number of messages to send (e.g., 1): "))
    except ValueError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid input for message count. Please enter a valid number.")
        exit(1)

    send_messages_to_webhook(webhook_url, message, username, avatar_url, count=count)
