import aiohttp
import asyncio
import tasksio
import os
import sys
import secrets
import colorama
from colorama import Fore

colorama.init(convert=True)

def clear():
  if sys.platform in ["linux", "linux2", "darwin32"]:
    os.system("clear")
  else:
    os.system("cls")

clear()
os.system("title Discord Password Changer - [KaramveerPlayZ#3301]")

def save_password(pwd):
  os.remove('password.txt')
  with open('password.txt', 'a+') as f:
    f.write(pwd)

def save_token(tkn):
  os.remove('token.txt')
  with open('token.txt', 'a+') as f:
    f.write(tkn)

async def check_tkn(tkn):
  async with aiohttp.ClientSession() as session:
    async with session.request(method="GET", url="https://discord.com/api/v9/users/@me", headers={"Authorization": tkn}) as response:
      if response.status in (204, 200, 201):
        pass
      else:
        print("KaramveerPlayZ#1337 | Invaild Token.")
        sys.exit()
    
token = input("[-] Enter Token: ")
password = input("[-] Enter Password: ")
delay = int(input("[-] Delay: "))

asyncio.run(check_tkn(token))

def getheaders(Toke):
  header = {
			'Authorization': Toke,
			'accept': '*/*',
			'accept-language': 'en-US',
			'connection': 'keep-alive',
			'cookie': f'__cfduid = {secrets.token_hex(43)}; __dcfduid={secrets.token_hex(32)}; locale=en-US',
			'DNT': '1',
			'origin': 'https://discord.com',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'referer': 'https://discord.com/channels/@me',
			'TE': 'Trailers',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
			'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
		}
  return header

menu = f"""[{Fore.RED}-{Fore.RESET}] Created by KaramveerPlayZ#3301, https://discord.gg/lgnop\n\n"""

clear()
print(menu)

async def change_password():
  global token, password
  new_pwd = secrets.token_hex(10)
  headers = getheaders(token)
  async with aiohttp.ClientSession() as session:
    async with session.patch(url="https://discord.com/api/v9/users/@me", headers=headers, json={"password": password, "new_password": f"{new_pwd}"}) as response:
      if response.status in (204, 200, 201):
        json = await response.json()
        ntkn = json['token']
        token = ntkn
        password = new_pwd
        save_password(new_pwd)
        save_token(ntkn)
        print(f"[-] Changed Password, New Token And Password Has Been Saved!")
      else:
        print(f"[-] Failed To Change Password, Response Status: {response.status}, Response Text: {await response.text()}")

async def startup():
  async with tasksio.TaskPool(10_000) as pool:
    while True:
      await pool.put(change_password())
      await asyncio.sleep(delay)


asyncio.run(startup())
