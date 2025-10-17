import requests
import random
import string
import threading
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

class fishdis:
    def __init__(self):
        self.session = requests.Session()
        self.found_users = []
        self.rate_limit_delay = 1.0
        self.attempts = 0
        self.success_rate = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/'
        }
        self.language = "english"
        
    def set_language(self, lang):
        self.language = lang
        
    def t(self, key):
        translations = {
            "english": {
                "banner": """
    ╔══════════════════════════════════════════════╗
    ║           DISCORD USERNAME FISHING v1.0      ║
    ║           [MADE BY GozBlox (F4X]              ║
    ╚══════════════════════════════════════════════╝
                """,
                "main_menu_1": "Hunt Usernames",
                "main_menu_2": "Languages", 
                "main_menu_0": "Exit",
                "select_option": "Select option",
                "username_length": "Username length (3-32)",
                "username_quantity": "Number of usernames (1-1000)",
                "invalid_length": "[-] Length must be between 3-32",
                "invalid_quantity": "[-] Quantity must be 1-1000",
                "invalid_input": "[-] Invalid input",
                "invalid_choice": "[-] Invalid choice",
                "hunting_start": "[+] Hunting {quantity} usernames with {length} chars...",
                "success_found": "[SUCCESS] Available: {username}",
                "hunt_completed": "[+] Completed! Found {count}/{total} usernames",
                "success_rate": "[+] Success rate: {rate}%",
                "post_hunt_title": "POST-HUNT MENU",
                "post_hunt_found": "Found: {count} usernames",
                "post_hunt_1": "Copy all usernames",
                "post_hunt_2": "Return to main menu", 
                "post_hunt_0": "Exit program",
                "copy_success": "[+] All usernames copied!",
                "copy_manual": "[+] Copy usernames manually",
                "no_usernames": "[-] No usernames found!",
                "returning_main": "[+] Returning to main menu...",
                "thank_you": "[+] Thank you!",
                "language_menu": "Choose language:",
                "lang_1": "English",
                "lang_2": "العربية",
                "lang_success": "[+] Language changed!",
                "low_success_warning": "[!] Warning: Low success rate for {length} chars!",
                "recommend_length": "[!] Recommend: 4-8 chars for better results"
            },
            "arabic": {
                "banner": """
    ╔══════════════════════════════════════════════╗
    ║           صياد يوزرات الديسكورد v4.0        ║
    ║           [الاداة مصنوعه من طرف GozBlox (F4X)]            ║
    ╚══════════════════════════════════════════════╝
                """,
                "main_menu_1": "صيد اليوزرات",
                "main_menu_2": "اللغات",
                "main_menu_0": "خروج", 
                "select_option": "اختر الخيار",
                "username_length": "كم حرف فاليوزر (3-32)",
                "username_quantity": "كم اسم تبي (1-1000)",
                "invalid_length": "[-] عدد الحروف يجب أن يكون بين 3 و 32",
                "invalid_quantity": "[-] عدد الأسماء يجب أن يكون بين 1 و 1000",
                "invalid_input": "[-] مدخل غير صحيح",
                "invalid_choice": "[-] خيار غير صحيح",
                "hunting_start": "[+] بدء الصيد لـ {quantity} يوزر بـ {length} حرف...",
                "success_found": "[تم بنجاح] {username}",
                "hunt_completed": "[+] اكتمل الصيد! تم العثور على {count} من {total}",
                "success_rate": "[+] نسبة النجاح: {rate}%",
                "post_hunt_title": "قائمة ما بعد الصيد",
                "post_hunt_found": "تم العثور على: {count} يوزر",
                "post_hunt_1": "نسخ كل اليوزرات",
                "post_hunt_2": "العودة للقائمة الرئيسية",
                "post_hunt_0": "إغلاق البرنامج", 
                "copy_success": "[+] تم نسخ جميع اليوزرات!",
                "copy_manual": "[+] نسخ اليوزرات يدوياً",
                "no_usernames": "[-] لم يتم العثور على يوزرات!",
                "returning_main": "[+] العودة للقائمة الرئيسية...",
                "thank_you": "[+] شكراً لك!",
                "language_menu": "اختر اللغة:",
                "lang_1": "English",
                "lang_2": "العربية",
                "lang_success": "[+] تم تغيير اللغة!",
                "low_success_warning": "[!] تحذير: نسبة نجاح قليلة لـ {length} حرف!",
                "recommend_length": "[!] نوصي: 4-8 أحرف لنتائج أفضل"
            }
        }
        return translations[self.language][key]
    
    def check_length_success_rate(self, length):
        """تقدير نسبة النجاح بناءً على طول اليوزر"""
        success_rates = {
            3: 0.1,   # 0.1% نجاح
            4: 1.0,   # 1% نجاح  
            5: 5.0,   # 5% نجاح
            6: 15.0,  # 15% نجاح
            7: 30.0,  # 30% نجاح
            8: 50.0,  # 50% نجاح
        }
        return success_rates.get(length, 60.0)  # أكثر من 8 أحرف = 60%+ نجاح
    
    def generate_smart_username(self, length):
        """توليد يوزرات ذكية باحتمالية نجاح أعلى"""
        # استخدام أنماط شائعة
        patterns = [
            string.ascii_lowercase,
            string.ascii_lowercase + string.digits,
            string.ascii_lowercase + '_',
            string.ascii_lowercase + string.digits + '_'
        ]
        
        chars = random.choice(patterns)
        return ''.join(random.choice(chars) for _ in range(length))
    
    def check_username_availability(self, username):
        """التحقق من اليوزر مع معالجة أفضل للمعدل"""
        try:
            url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
            payload = {"username": username}
            
            response = self.session.post(
                url, 
                json=payload,
                headers=self.headers, 
                timeout=10
            )
            
            self.attempts += 1
            
            if response.status_code == 200:
                data = response.json()
                return data.get('taken') == False, username
            elif response.status_code == 429:
                time.sleep(1.5)
                return False, username
            else:
                return False, username
                
        except Exception:
            return False, username
    
    def mass_username_hunt(self, username_length, quantity):
        """صيد اليوزرات بإصدار فائق السرعة"""
        print(self.t("hunting_start").format(quantity=quantity, length=username_length))
        
        # تحذير إذا كان الطول قصير
        success_rate = self.check_length_success_rate(username_length)
        if success_rate < 5.0:
            print(self.t("low_success_warning").format(length=username_length))
            print(self.t("recommend_length"))
        
        self.found_users = []
        self.attempts = 0
        
        start_time = time.time()
        
        def hunt_batch(batch_size=50):
            """صيد مجموعة من اليوزرات"""
            batch_results = []
            for _ in range(batch_size):
                if len(self.found_users) >= quantity:
                    break
                    
                username = self.generate_smart_username(username_length)
                available, checked_username = self.check_username_availability(username)
                
                if available:
                    batch_results.append(checked_username)
                    print(self.t("success_found").format(username=checked_username))
                
                time.sleep(random.uniform(0.5, 1.5))  # تقليل التأخير
            
            return batch_results
        
        # استخدام 4 خيوط بدلاً من 2
        with ThreadPoolExecutor(max_workers=4) as executor:
            while len(self.found_users) < quantity and self.attempts < quantity * 20:
                future = executor.submit(hunt_batch, 25)
                batch_results = future.result()
                self.found_users.extend(batch_results)
                
                # حفظ اليوزرات فوراً
                for user in batch_results:
                    self.save_username(user)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # إحصائيات
        success_rate = (len(self.found_users) / self.attempts * 100) if self.attempts > 0 else 0
        
        print(self.t("hunt_completed").format(count=len(self.found_users), total=quantity))
        print(self.t("success_rate").format(rate=round(success_rate, 2)))
        print(f"[+] Time taken: {round(total_time, 2)} seconds")
        print(f"[+] Total attempts: {self.attempts}")
        
        self.post_hunt_menu()
    
    def save_username(self, username):
        """حفظ اليوزرات"""
        try:
            with open("available_usernames.txt", "a", encoding="utf-8") as file:
                file.write(username + "\n")
        except Exception:
            pass
    
    def copy_all_usernames(self):
        """نسخ اليوزرات"""
        if not self.found_users:
            print(self.t("no_usernames"))
            return
        
        usernames_text = "\n".join(self.found_users)
        
        try:
            import pyperclip
            pyperclip.copy(usernames_text)
            print(self.t("copy_success"))
        except ImportError:
            print("\n" + "="*50)
            print("COPY USERNAMES:")
            print("="*50)
            print(usernames_text)
            print("="*50)
            print(self.t("copy_manual"))
        
        input("\nPress enter to continue...")
    
    def post_hunt_menu(self):
        """قائمة ما بعد الصيد"""
        while True:
            print("\n" + "="*40)
            print(self.t("post_hunt_title"))
            print("="*40)
            print(self.t("post_hunt_found").format(count=len(self.found_users)))
            print("[1]", self.t("post_hunt_1"))
            print("[2]", self.t("post_hunt_2"))
            print("[0]", self.t("post_hunt_0"))
            print("="*40)
            
            choice = input(f"\n{self.t('select_option')}: ").strip()
            
            if choice == "1":
                self.copy_all_usernames()
                break
            elif choice == "2":
                print("\n" + self.t("returning_main"))
                break
            elif choice == "0":
                print("\n" + self.t("thank_you"))
                sys.exit(0)
            else:
                print(self.t("invalid_choice"))
    
    def language_menu(self):
        """قائمة اللغات"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.t("banner"))
            print("\n" + self.t("language_menu"))
            print("[1]", self.t("lang_1"))
            print("[2]", self.t("lang_2"))
            print("[0]", self.t("main_menu_0"))
            
            choice = input(f"\n{self.t('select_option')}: ").strip()
            
            if choice == "1":
                self.set_language("english")
                print(self.t("lang_success"))
                input("\nPress enter to continue...")
                break
            elif choice == "2":
                self.set_language("arabic")
                print(self.t("lang_success"))
                input("\nاضغط انتر للمتابعة...")
                break
            elif choice == "0":
                break
            else:
                print(self.t("invalid_choice"))
                input("\nPress enter to continue...")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    hunter = fishdis()
    
    while True:
        clear_screen()
        print(hunter.t("banner"))
        print("[1]", hunter.t("main_menu_1"))
        print("[2]", hunter.t("main_menu_2"))
        print("[0]", hunter.t("main_menu_0"))
        
        choice = input(f"\n{hunter.t('select_option')}: ").strip()
        
        if choice == "1":
            try:
                length = int(input(hunter.t("username_length") + ": "))
                quantity = int(input(hunter.t("username_quantity") + ": "))
                
                if length < 3 or length > 32:  # تغيير من 2 إلى 3
                    print(hunter.t("invalid_length"))
                    input("\nPress enter to continue...")
                    continue
                
                if quantity <= 0 or quantity > 1000:
                    print(hunter.t("invalid_quantity"))
                    input("\nPress enter to continue...")
                    continue
                
                hunter.mass_username_hunt(length, quantity)
                
            except ValueError:
                print(hunter.t("invalid_input"))
                input("\nPress enter to continue...")
                
        elif choice == "2":
            hunter.language_menu()
                
        elif choice == "0":
            print("\n" + hunter.t("thank_you"))
            break
            
        else:
            print(hunter.t("invalid_choice"))
            input("\nPress enter to continue...")

if __name__ == "__main__":
    main()