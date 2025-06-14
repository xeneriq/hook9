#v1.0.0


import os
import fade
import asyncio
import aiohttp

intro = fade.pinkred(r"""
                                                                                                     _                 _     _____ 
                                                                                                    | |               | |   |  _  |
                                                                                                    | |__   ___   ___ | | __| |_| |
                                                                                                    | '_ \ / _ \ / _ \| |/ /\____ |
                                                                                                    | | | | (_) | (_) |   < .___/ /
                                                                                                    |_| |_|\___/ \___/|_|\_\\____/ 
                                                                                                                        Made by @xeneriq""")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

async def check_webhook(webhook):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(webhook) as resp:
                if resp.status != 200:
                    print("invalid webhook or error:", resp.status)
                    exit(1)
    except Exception as e:
        print("webhook check failed:", e)
        exit(1)

async def send_message(session, web, msg, username, avatar):
    while True:
        try:
            payload = {"content": msg}
            if username:
                payload["username"] = username
            if avatar:
                payload["avatar_url"] = avatar

            async with session.post(web, json=payload) as resp:
                if resp.status == 429:
                    retry_after = await resp.json()
                    wait_time = retry_after.get("retry_after", 0) / 1000
                    print(fade.purplepink(f"rate limited, retrying after {wait_time} seconds"))
                    await asyncio.sleep(wait_time)
                    continue
                elif resp.status >= 400:
                    print(fade.fire(f"failed to send message, status: {resp.status}"))
                else:
                    print(fade.purplepink(f"message sent successfully: {msg}"))
                break
        except Exception as e:
            print("failed to send message:", e)
            break

async def send_msgs_async(count, msg, web, username, avatar):
    async with aiohttp.ClientSession() as session:
        tasks = [send_message(session, web, msg, username, avatar) for _ in range(count)]
        await asyncio.gather(*tasks)

async def delete_webhook(webhook_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(webhook_url) as resp:
                if resp.status == 204:
                    print(fade.purplepink("webhook deleted successfully."))
                else:
                    print(fade.fire(f"failed to delete webhook. Status: {resp.status}"))
    except Exception as e:
        print("error deleting webhook:", e)

print(intro)
link = input("\nwebhook link: ")
asyncio.run(check_webhook(link))

print("\nwebhook verified.")
clear()

# default values
msg = "hello"
count = 1
username = ""
avatar = ""

while True:
    print(intro)
    print("""
                                                                                +---------------------------------------------------------------+
                                                                                |   1) Set message content          2) Set number of messages   |
                                                                                |   3) Set custom username          4) Set custom pfp           |
                                                                                |   5) Start sending messages       6) Delete webhook           |
                                                                                |   0) Exit                                                     |
                                                                                +---------------------------------------------------------------+""")

    choice = input("> ")

    if choice == "1":
        msg = input("message: ")
        clear()
    elif choice == "2":
        try:
            count = int(input("number of messages: "))
            clear()
        except ValueError:
            print("invalid number.")
    elif choice == "3":
        username = input("custom username: ")
        clear()
    elif choice == "4":
        avatar = input("avatar url: ")
        clear()
    elif choice == "5":
        asyncio.run(send_msgs_async(count, msg, link, username, avatar))
        clear()
    elif choice == "6":
        confirm = input("Are you sure you want to delete this webhook? (y/n): ").strip().lower()
        if confirm == "y":
            asyncio.run(delete_webhook(link))
        else:
            print("Deletion cancelled.")
        input("Press Enter to continue...")
        clear()

    elif choice == "0":
        print("exiting...")
        break
    else:
        print("invalid option.")
        clear()
