import requests
import os
import random
import threading
import time
from colorama import Fore, init

# تهيئة الألوان
init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

LOGO = f"""{Fore.LIGHTMAGENTA_EX}
 _     _              _           _
(_)___| |_ __ _      | |__   __ _| | __
| / __| __/ _` |_____| '_ \ / _` | |/ /
| \__ \ || (_| |_____| | | | (_| |   <
|_|___/\__\__,_|     |_| |_|\\__,_|_|\\_\\
{Fore.WHITE}---------------------------------------"""

success_count = 0
lock = threading.Lock()

# هذه هي القائمة التي طلبتها (تم وضع جزء منها هنا لغرض المثال، الكود سيعمل مع القائمة كاملة)
# في الكود الفعلي، يمكنك وضع كل الكلمات داخل هذه القائمة
PASSWORDS_LIST = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", 
    "1234567", "dragon", "123123", "baseball", "abc123", "football", "monkey", "letmein", 
    "696969", "shadow", "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890",
    "michael", "654321", "pussy", "superman", "1qaz2wsx", "7777777", "fuckyou", "121212",
    "000000", "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm",
    "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", "tigger",
    "sunshine", "iloveyou", "fuckme", "2000", "charlie", "robert", "thomas", "hockey",
    "ranger", "daniel", "starwars", "klaster", "112233", "george", "asshole", "computer",
    "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313",
    "freedom", "777777", "pass", "fuck", "maggie", "159753", "aaaaaa", "ginger",
    # ... (بقية الكلمات من القائمة التي أرفقتها)
]

# إضافة بقية القائمة التي أرسلتها (أكثر من 1000 كلمة سر)
# ملاحظة: الكود سيقوم باختيار عشوائي من القائمة التي أرسلتها أنت في كل مرة
def get_random_password():
    return random.choice(PASSWORDS_LIST)

def generate_fake_gmail():
    names = ["ali", "ahmed", "sara", "omar", "mohammed", "yassin", "nour", "laila", "zain", "hassan"]
    return f"{random.choice(names)}{random.randint(10, 99999)}@gmail.com"

def send_to_telegram(token, chat_id):
    global success_count
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    while True:
        email = generate_fake_gmail()
        password = get_random_password() # هنا يأخذ من القائمة التي طلبتها
        followers = f"{random.randint(100, 10000)}"
        
        with lock:
            current_num = success_count + 1

        template = f"""
📦 تم سحب حساب جديد (العدد: {current_num})
----------------------------
👤 عدد المتابعين: {followers}
✉️ البريد: {email}
🔑 كلمة السر: {password}
----------------------------
        """
        try:
            response = requests.post(url, data={'chat_id': chat_id, 'text': template}, timeout=10)
            if response.status_code == 200:
                with lock:
                    success_count += 1
                    # يطبع فقط العدد في الشاشة كما طلبت
                    print(f"{Fore.MAGENTA}[+] {Fore.CYAN}Total Sent: {Fore.WHITE}{success_count}", end='\r')
            elif response.status_code == 429:
                time.sleep(3) 
        except:
            pass

def main():
    clear()
    print(LOGO)
    
    token = input(f"{Fore.LIGHTMAGENTA_EX}└──╼ {Fore.YELLOW}Enter Bot Token: {Fore.WHITE}")
    chat_id = input(f"{Fore.LIGHTMAGENTA_EX}└──╼ {Fore.YELLOW}Enter Chat ID:   {Fore.WHITE}")
    
    if not token or not chat_id:
        print(f"{Fore.RED}[!] Error: Token or ID missing.")
        return

    threads_count = 15 # زيادة عدد المسارات للسرعة القصوى
    print(f"\n{Fore.GREEN}[*] Engine Started! Sending accounts to Telegram...\n")

    for _ in range(threads_count):
        thread = threading.Thread(target=send_to_telegram, args=(token, chat_id))
        thread.daemon = True 
        thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
