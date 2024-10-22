import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord import app_commands
from datetime import datetime
from datetime import timedelta
import asyncio
import json
import os
import re
import emoji
import aiohttp

user_data = {}

class ViewPersistence(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=discord.Intents.all(), description="The best supporter Bot for Exchanging and Ticketing💜")

    async def setup_hook(self):
        self.add_view(ButtonToOpenExchangeTicket())  
        self.add_view(ButtonForExchangerModal())


    
open_tickets_for_Exchange = {}    

client = ViewPersistence()
bot = client

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    try:
        await asyncio.sleep(0.5)
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        print("-------------------")
    except Exception as e:
        print("Error: ", e)

    update_member_count.start()  # Starts member counting task
    check_stats.start()  # Starts stats checking
    check_ExchangerLimit.start()
"""
@client.command()
async def send(ctx):
    embed = discord.Embed(
        title="💱 Exchange Ticket System",
        description=(
            f"Welcome to our **Exchange Ticket System**! 💼\n\n"
            f"To open an Exchange Ticket, simply press the **`Exchange`** button below. "
            f"You have to wait till an Exchanger claims your Ticket.\n\n"
            f"Please note that by creating an exchange ticket, you agree to our Terms of Service in <#1285932625709498430> 📜\n"
        ),
        color=discord.Color.from_rgb(0, 255, 0),
    )

    embed.set_thumbnail(url=f"https://cdn.discordapp.com/icons/1244472690383917066/e65412e8ae2655be334f577109b88c0f.png?size=4096") 
    embed.set_footer(text="We appreciate your trust in our exchange service!")

    await ctx.send(embed=embed, view=ButtonToOpenExchangeTicket())


@bot.command()
async def send2(ctx):
    embed = discord.Embed(
        title="💱 Exchanging Info & ToS",
        description="When using our Exchange service, you agree to follow the rules outlined below.",
        color=discord.Color.from_rgb(0, 255, 0)
    )

    # Exchangers Section
    exchangers_info = (
    "Our trusted Exchangers:\n\n"
    "- <@611403629416415257>, <@929655970576089128>, and <@1168162359479644271> manage exchanges between "
    "<:PayPal:1244753696508739585> and <:Litecoin:1244753012438597703>.\n"
    "- <@611403629416415257> also handles exchanges between <:Cashapp:1244759109891391620> and both "
    "<:Litecoin:1244753012438597703> and <:PayPal:1244753696508739585>.\n"
    "- <@929655970576089128>, <@763288874663018506>, and <@1168162359479644271> specialize in exchanging "
    "<:crypto:1286420902497615882> with other <:crypto:1286420902497615882>.\n\n"
    "Additionally, users with the <@&1244735162340610058> role are also authorized to handle exchanges. "
    "Those not listed above have provided a safety deposit for extra security."
    )

    embed.add_field(name="Exchangers", value=exchangers_info, inline=False)


    rules = (
        "- If something like PayPal Limited or Cashapp Limited occurs, it's **NOT** our fault.\n"
        "- Sending LTC to the wrong address is **NOT** our fault.\n"
        "- Providing a false LTC address is **NOT** our fault.\n"
        "- Providing a false PayPal or Cashapp email/tag is **NOT** our fault.\n"
        "- You must cover the PayPal/Crypto fees; otherwise, no exchange will be processed.\n"
        "- After the ticket is complete, please vouch for the exchanger in <#1244752187155021935>. "
        "Your exchange details will be logged in <#1244752108499243008>.\n"
        "- When we exchange your <:Litecoin:1244753012438597703> for our <:PayPal:1244753696508739585>, "
        "we always send via Friends and Family (FnF). **We do not cover FnF fees**, it’s included in the amount.\n"
        "- Always send <:PayPal:1244753696508739585> via FnF, with no notes, and from PayPal balance. "
        "You must provide proof of payment via a recording or screenshot from the transaction email.\n"
        "- Failure to follow these rules will result in an exchange ban."
    )
    embed.add_field(name="Rules", value=rules, inline=False)


    fees = (
        "------------------------------------\n"
        "<:PayPal:1244753696508739585> <:ARight:1244846665039347734> <:Litecoin:1244753012438597703> (4.5% Fee)\n"
        "<:Litecoin:1244753012438597703> <:ARight:1244846665039347734> <:PayPal:1244753696508739585> (4% Fee)\n"
        "*Minimum Fee is 2$*\n"
        "------------------------------------\n"
        "<:Cashapp:1244759109891391620> <:ARight:1244846665039347734> <:Litecoin:1244753012438597703> (4.5% Fee)\n"
        "<:Cashapp:1244759109891391620> <:ARight:1244846665039347734> <:PayPal:1244753696508739585> (4% Fee)\n"
        "*Minimum Fee is 2$*\n"
        "------------------------------------\n"
        "<:Litecoin:1244753012438597703> <:ARight:1244846665039347734> <:Cashapp:1244759109891391620> (4.5% Fee)\n"
        "<:PayPal:1244753696508739585> <:ARight:1244846665039347734> <:Cashapp:1244759109891391620> (4% Fee)\n"
        "*Minimum Fee is 2$*\n"
        "------------------------------------\n"
        "<:crypto:1286420902497615882> <:ARight:1244846665039347734> <:crypto:1286420902497615882> (3% Fee)\n"
        "*Minimum Fee is 2$*\n"
        "------------------------------------\n"
        "~~Fees may change in the future.~~"
    )
    embed.add_field(name="Exchange Fees", value=fees, inline=False)

    # Footer and image (optional)
    embed.set_footer(text="By opening an exchange ticket, you agree to our Terms of Service.")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1244472690383917066/e65412e8ae2655be334f577109b88c0f.png?size=4096")

    await ctx.send(embed=embed)
"""

class ButtonToOpenExchangeTicket(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Exchange", style=discord.ButtonStyle.green, custom_id="EchangeOpenID")
    async def OpenAExchangeTicket(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(HowMuchUserWantsToExchange())

class HowMuchUserWantsToExchange(discord.ui.Modal, title="How much do you want to Exchange?"):
    Amount = discord.ui.TextInput(
        label="How much you want to Exchange?",
        placeholder="Please do only write a Number. Between 5 and 500",
        required=True,
        max_length=5,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        amount_str = self.Amount.value

       
        if not amount_str.isdigit():
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid Input",
                    description="The amount must be a number. Please enter a valid number between 5 and 1250.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

   
        amount = int(amount_str)

      
        if not (5 <= amount <= 1250):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid Range",
                    description="The number must be between 5 and 1250. Please enter a number within this range.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        if interaction.user.id not in user_data:
            user_data[interaction.user.id] = {}

        user_data[interaction.user.id]["HowMuch"] = amount

        print(user_data)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="What do you have?",
                description=f"You want to exchange **{amount}**. Please now select below this Embed what you **HAVE**.",
                color=discord.Color.from_rgb(0, 255, 0)
            ),
            view=WhatUserHas(),
            ephemeral=True
        )
        

import discord
from discord.ui import View

class WhatUserHas(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.paypal_button = discord.ui.Button(label="Paypal FnF", style=discord.ButtonStyle.blurple, custom_id="paypal_button")
        self.litecoin_button = discord.ui.Button(label="Litecoin", style=discord.ButtonStyle.blurple, custom_id="litecoin_button")
        self.cashapp_button = discord.ui.Button(label="Cashapp", style=discord.ButtonStyle.blurple, custom_id="cashapp_button")
        self.crypto_button = discord.ui.Button(label="Crypto for Crypto", style=discord.ButtonStyle.blurple, custom_id="crypto_button")
        self.add_item(self.paypal_button)
        self.add_item(self.litecoin_button)
        self.add_item(self.cashapp_button)
        self.add_item(self.crypto_button)

        self.paypal_button.callback = self.paypal_callback
        self.litecoin_button.callback = self.litecoin_callback
        self.cashapp_button.callback = self.cashapp_callback
        self.crypto_button.callback = self.crypto_callback

    async def paypal_callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data[user_id]["Have"] = "PayPal"
        self.disable_buttons(self.paypal_button, self.litecoin_button, self.cashapp_button, self.crypto_button)
        await interaction.response.edit_message(view=self)
        
        embed = discord.Embed(
            title="Selection Confirmed",
            description="You have selected **PayPal (FnF)**.",
            color=discord.Color.from_rgb(0, 255, 0)
        )
        embed.add_field(name="Next Step", value="Please select now what you **need**.", inline=False)
        
        await interaction.followup.send(embed=embed, view=AllWithoutPayPal(), ephemeral=True)
        print(user_data)

    async def litecoin_callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data[user_id]["Have"] = "Litecoin"
        self.disable_buttons(self.litecoin_button, self.paypal_button, self.cashapp_button, self.crypto_button)
        await interaction.response.edit_message(view=self)
        
        embed = discord.Embed(
            title="Selection Confirmed",
            description="You have selected **Litecoin**.",
            color=discord.Color.from_rgb(0, 255, 0)
        )
        embed.add_field(name="Next Step", value="Please select now what you **need**.", inline=False)
        embed.add_field(name="Info", value="If you want an other Crypto for PayPal/CashApp, then please continue here. After that write in Ticket what crypto coin you have.", inline=False)
        
        await interaction.followup.send(embed=embed, view=AllWithoutLitecoin(), ephemeral=True)
        print(user_data)

    async def cashapp_callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data[user_id]["Have"] = "Cashapp"
        self.disable_buttons(self.litecoin_button, self.paypal_button, self.cashapp_button, self.crypto_button)
        await interaction.response.edit_message(view=self)
        
        embed = discord.Embed(
            title="Selection Confirmed",
            description="You have selected **Cashapp**.",
            color=discord.Color.from_rgb(0, 255, 0)
        )
        embed.add_field(name="Next Step", value="Please select now what you **need**.", inline=False)
        print(user_data)
        
        await interaction.followup.send(embed=embed, view=AllWithoutCashapp(), ephemeral=True)

    async def crypto_callback(self, interaction: discord.Interaction):
        self.disable_buttons(self.litecoin_button, self.paypal_button, self.cashapp_button, self.crypto_button)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=discord.Embed(
            title="⚠️ Important: Read Carefully Before Proceeding",
            description=(
                "It's crucial that you read the following instructions **carefully** before proceeding. "
                "If you skip this, you might not know what to write in the Modal!\n\n"
                "**For the `Have` and `Need` fields**, make sure to only write one of the following "
                "cryptocurrencies based on what you have and what you need:\n\n"
                "• **Bitcoin**\n"
                "• **Ethereum**\n"
                "• **BNB**\n"
                "• **Dogecoin**\n"
                "• **USDC**\n"
                "• **USDT**\n"
                "• **Solana**\n"
                "• **Litecoin**\n\n"
                "Please write them 1:1 as stated above. If not, you wont be able to continue."
                "We have all Crypto currency in all Networks. Please after creating the Ticket write the specific Network so we both dont make anything wrong."
                "Once you understand, press the `open` button below to proceed."
                
            ),
            color=discord.Color.from_rgb(0, 255, 0))
        .set_footer(text="Make sure you double-check everything before submitting!"),
        view=OpenCryptoOnlyModal(), ephemeral=True)


    def disable_buttons(self, *buttons):
        for button in buttons:
            button.disabled = True

class OpenCryptoOnlyModal(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="open", style=discord.ButtonStyle.green, custom_id="iasjdijwds")
    async def asidjiwjd(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(CryptoOnly())

class CryptoOnly(discord.ui.Modal, title="Crypto to Crypto"):
    Have = discord.ui.TextInput(
        label="What do you have?",
        placeholder="Please write here what you have.",
        required=True,
        max_length=10,
        style=discord.TextStyle.short
    )

    Need = discord.ui.TextInput(
        label="What do you need?",
        placeholder="Please write here what you need.",
        required=True,
        max_length=10,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        have = self.Have.value
        need = self.Need.value
        if interaction.user.id in user_data:
            if have in {"Bitcoin", "Litecoin", "USDT", "USDC", "BNB", "Dogecoin", "Ethereum", "Solana"}:
                if need in {"Bitcoin", "Litecoin", "USDT", "USDC", "BNB", "Dogecoin", "Ethereum", "Solana"}:
                    if have == need:
                        await interaction.response.send_message("You can't have the same Crypto coin in Have and Need.", ephemeral=True)
                    else:
                        user_id = interaction.user.id
                        user_data[user_id]["Have"] = have
                        price_amount = user_data[user_id]["HowMuch"]
                        user_data[user_id]["Need"] = need
                        user_data[interaction.user.id]["Gets"] = f"{price_amount * CryptoToCrypto - 2:.2f}"

                        await interaction.response.send_message(embed=discord.Embed(
                            title="Confirm",
                            description=f"Before opening the Ticket, you have to confirm everything is correct. \n\nExchange amount: **{price_amount}$**\nWhat you have: **{have}**\nWhat you need: **{need}**\n\nYou will receive **${price_amount * CryptoToCrypto - 2:.2f}**\n\nPress the `confirm` Button to open a Ticket.",
                            color=discord.Color.from_rgb(0, 255, 0)
                        ), view=OpenTicketFinallyBruh(), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(
                        title="invaled",
                        description=f"You wrote something false in the `need` section. Please read the Embed above again and write the correct name.",
                        color=discord.Color.red()
                    ), ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(
                        title="invaled",
                        description=f"You wrote something false in the `have` section. Please read the Embed above again and write the correct name.",
                        color=discord.Color.red()
                    ), ephemeral=True)

                
        else:
            await interaction.response.send_message("You are not in userdata. Please restart the exchange.", ephemeral=True)



    



PayPalToLTC = 0.955
LTCToPayPal = 0.96

CaToLTC = 0.955
CaToPayPal = 0.96

LTCToCa = 0.955
PayPalToCa = 0.96


CryptoToCrypto = 0.97

class AllWithoutPayPal(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Litecoin", style=discord.ButtonStyle.blurple)
    async def Litecoinasasdwadsdwdjdijwidjwijd(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id
        user_data[user_id]["Need"] = "Litecoin"
        price_amount = user_data[user_id]["HowMuch"]
        user_data[interaction.user.id]["Gets"] = f"{price_amount*PayPalToLTC-2:.2f}"
        await interaction.response.send_message(embed=discord.Embed(
            title="Confirm",
            description=f"Before opening the Ticket, you have to confirm everything is correct. \n\nExchange amount: **{price_amount}$**\nWhat you have: **PayPal**\nWhat you need: **Litecoin**\n\nYou will receive **${price_amount*PayPalToLTC-2:.2f}**\n\nPress the `confirm` Button to open a Ticket.",
            color=discord.Color.from_rgb(0, 255, 0)
        ), view=OpenTicketFinallyBruh(), ephemeral=True)
        print(user_data)

    @discord.ui.button(label="Cashapp", style=discord.ButtonStyle.blurple)
    async def PayPalPASDkjhgfghjklkjhgfdfghji86IJWIDJI(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id
        user_data[user_id]["Need"] = "Cashapp"
        price_amount = user_data[user_id]["HowMuch"]
        user_data[interaction.user.id]["Gets"] = f"{price_amount*PayPalToCa-2:.2f}"
        await interaction.response.send_message(embed=discord.Embed(
            title="Confirm",
            description=f"Before opening the Ticket, you have to confirm everything is correct. \n\nExchange amount: **{price_amount}$**\nWhat you have: **PayPal**\nWhat you need: **Cashapp**\n\nYou will receive **${price_amount*PayPalToCa-2:.2f}**\n\nPress the `confirm` Button to open a Ticket.",
            color=discord.Color.from_rgb(0, 255, 0)
        ), view=OpenTicketFinallyBruh(), ephemeral=True)
        print(user_data)

class AllWithoutLitecoin(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Paypal FnF", style=discord.ButtonStyle.blurple)
    async def asdadsasdwadsdwhhghgfghg(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id
        user_data[user_id]["Need"] = "PayPal"
        price_amount = user_data[user_id]["HowMuch"]
        user_data[interaction.user.id]["Gets"] = f"{price_amount*LTCToPayPal-2:.2f}"
        await interaction.response.send_message(embed=discord.Embed(
            title="Confirm",
            description=f"Before opening the Ticket, you have to confirm everything is correct. \n\nExchange amount: **{price_amount}$**\nWhat you have: **Litecoin**\nWhat you need: **PayPal**\n\nYou will receive **${price_amount*LTCToPayPal-2:.2f}**\n\nPress the `confirm` Button to open a Ticket.",
            color=discord.Color.from_rgb(0, 255, 0)
        ), view=OpenTicketFinallyBruh(), ephemeral=True)
        print(user_data)


    @discord.ui.button(label="Cashapp", style=discord.ButtonStyle.blurple)
    async def PayPalPhgfhgvhgASDIJsWIDJI(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id
        user_data[user_id]["Need"] = "Cashapp"
        price_amount = user_data[user_id]["HowMuch"]
        user_data[interaction.user.id]["Gets"] = f"{price_amount*LTCToCa-2:.2f}"
        await interaction.response.send_message(embed=discord.Embed(
            title="Confirm",
            description=f"Before opening the Ticket, you have to confirm everything is correct. \n\nExchange amount: **{price_amount}$**\nWhat you have: **Litecoin**\nWhat you need: **Cashapp**\n\nYou will receive **${price_amount*LTCToCa-2:.2f}**\n\nPress the `confirm` Button to open a Ticket.",
            color=discord.Color.from_rgb(0, 255, 0)
        ), view=OpenTicketFinallyBruh(), ephemeral=True)
        print(user_data)

class AllWithoutCashapp(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Paypal FnF", style=discord.ButtonStyle.blurple)
    async def PayPalPpoijhbvcfghjkASDIJWIDJI(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id
        user_data[user_id]["Need"] = "PayPal"
        price_amount = user_data[user_id]["HowMuch"]
        user_data[interaction.user.id]["Gets"] = f"{price_amount*CaToPayPal-2:.2f}"
        await interaction.response.send_message(embed=discord.Embed(
            title="Confirm",
            description=f"Before opening the Ticket, you have to confirm everything is correct. \n\nExchange amount: **{price_amount}$**\nWhat you have: **Cashapp**\nWhat you need: **PayPal**\n\nYou will receive **${price_amount*CaToPayPal-2:.2f}**\n\nPress the `confirm` Button to open a Ticket.",
            color=discord.Color.from_rgb(0, 255, 0)
        ), view=OpenTicketFinallyBruh(), ephemeral=True)
        print(user_data)


    @discord.ui.button(label="Litecoin", style=discord.ButtonStyle.blurple)
    async def Litecoinalkjhgfghjkjuzt6754sjdijwidjwijd(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id
        user_data[user_id]["Need"] = "Litecoin"
        price_amount = user_data[user_id]["HowMuch"]
        user_data[interaction.user.id]["Gets"] = f"{price_amount*CaToLTC-2:.2f}"
        await interaction.response.send_message(embed=discord.Embed(
            title="Confirm",
            description=f"Before opening the Ticket, you have to confirm everything is correct. \n\nExchange amount: **{price_amount}$**\nWhat you have: **Cashapp**\nWhat you need: **Litecoin**\n\nYou will receive **${price_amount*CaToLTC-2:.2f}**\n\nPress the `confirm` Button to open a Ticket.",
            color=discord.Color.from_rgb(0, 255, 0)
        ), view=OpenTicketFinallyBruh(), ephemeral=True)
        print(user_data)


class OpenTicketFinallyBruh(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def pwpwoepwoepwoepweo(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id in open_tickets_for_Exchange:
            await interaction.response.send_message("You can't open a ticket since a ticket is already open. If it isn't, please ping a staff member.", ephemeral=True)
            return

        user_id = interaction.user.id
        channel_name = f"exchange-{interaction.user.name}"
        guild = interaction.guild
        category_name = "tickets"

        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            category = await guild.create_category(category_name)


        role1 = discord.utils.get(guild.roles, name="Exchanger")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True),
            role1: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=False),
        }

        ticket_channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
        open_tickets_for_Exchange[user_id] = ticket_channel.id
        await interaction.response.send_message(f"Ticket channel {ticket_channel.mention} created!", ephemeral=True)

        have = user_data[interaction.user.id].get("Have", "Not specified")
        need = user_data[interaction.user.id].get("Need", "Not specified")
        how_much = user_data[interaction.user.id].get("HowMuch", "Not specified")
        gets = user_data[interaction.user.id].get("Gets", "Not specified")

        # Calculate fees and profits
        Fees = float(how_much) - float(gets)
        YouProfit = Fees * 0.65
        WeGet = Fees * 0.35

        # Create the embed for ticket details
        embed = discord.Embed(
            title="Exchange Information",
            description=f"{interaction.user.mention} has created a ticket!\nPlease wait till an Exchanger claims this Ticket.\n\nHere are the details:",
            color=discord.Color.from_rgb(0, 255, 0)
        )

        embed.add_field(name="What User Has", value=have, inline=False)
        embed.add_field(name="What User Gets", value=need, inline=False)
        embed.add_field(name="How Much Will be Exchanged", value=f"{how_much}", inline=False)
        embed.add_field(name="How Much User Receives", value=gets, inline=False)
        embed.set_footer(text="With this ticket created, you agree to our Exchange ToS.")

        await ticket_channel.send(content=f"{interaction.user.mention}", embed=embed)

        # Add fields for profit and fees
        embed.add_field(name="How Much You Profit", value=f"{YouProfit:.2f}", inline=False)
        embed.add_field(name="How Much We Get", value=f"{WeGet:.2f}", inline=False)
        embed.set_footer(text="When claiming this Ticket, you agree to our Exchanger claiming ToS.")

        # Initialize ping_message to prevent UnboundLocalError
        ping_message = "No valid exchange pair found."

        try:
            if have == "PayPal":
                if need == "Litecoin":
                    ping_message = "<@&1286333065534247027>"
                elif need == "Cashapp":
                    ping_message = "<@&1286333117329838120>"

            elif have == "Litecoin":
                if need == "PayPal":
                    ping_message = "<@&1286333149655334985>"
                elif need == "Cashapp":
                    ping_message = "<@&1286333181384982628>"

            elif have == "Cashapp":
                if need == "PayPal":
                    ping_message = "<@&1286333241053151254>"
                elif need == "Litecoin":
                    ping_message = "<@&1286333209482887268>"

            elif have and need == "Bitcoin" or "Litecoin" or "USDT" or "USDC" or "BNB" or "Dogecoin" or "Ethereum":
                ping_message=("<@&1286702518356934717>")
        except ValueError as e:
            print(f"Error: {e}")
            ping_message = "An error occurred while processing the exchange."

        # Send ping message and embed to the claim channel
        claim_channel = client.get_channel(1286061646472679566)
        claim_view = ClaimExchangerTicket(ticket_channel_id=ticket_channel.id, have=have, need=need, how_much=how_much)
        await claim_channel.send(embed=embed, view=claim_view)
        await claim_channel.send(f"{ping_message}")


claimed_tickets = {}



class ClaimExchangerTicket(discord.ui.View):
    def __init__(self, ticket_channel_id, have, need, how_much):
        super().__init__(timeout=None)
        self.ticket_channel_id = ticket_channel_id
        self.have = have.strip()
        self.need = need.strip()
        self.how_much = float(how_much)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.green, custom_id="ClaimingExchangeTicketID")
    async def claiming_exchange_ticket(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id in claimed_tickets:
            await interaction.response.send_message(
                "You can't claim this Ticket because you already have one claimed. If you think this is false, please contact Raichi.",
                ephemeral=True
            )
            return

        guild = interaction.guild
        user = interaction.user

        name_mapping = {
            "Litecoin": "LTC",
            "PayPal": "PayPal",
            "CashApp": "CashApp",
            "Bitcoin": "BTC",
            "Ethereum": "ETH",
            "BNB": "BNB",
            "Dogecoin": "DOGE",
            "USDC": "USDC",
            "USDT": "USDT",
            "Crypto": "Crypto",
            "Solana": "SOL"
        }

        user_id_str = str(user.id)
        if user_id_str not in exchanger_limits:
            await interaction.response.send_message(
                "You are not in the exchanger limit list and cannot claim this ticket.",
                ephemeral=True
            )
            return

        user_limit = exchanger_limits[user_id_str].get("amount", 0)
        if user_limit < self.how_much:
            await interaction.response.send_message(
                f"Your exchange limit (${user_limit}) is lower than the required amount (${self.how_much}). You cannot claim this ticket.",
                ephemeral=True
            )
            return

        exchanger_role = discord.utils.get(guild.roles, name="Exchanger")
        if exchanger_role not in user.roles:
            await interaction.response.send_message("You do not have the 'Exchanger' role.", ephemeral=True)
            return

        abbreviated_have = name_mapping.get(self.have, self.have)
        abbreviated_need = name_mapping.get(self.need, self.need)

        crypto_roles = {"BTC", "ETH", "BNB", "DOGE", "LTC", "USDC", "USDT", "SOL"}

        if abbreviated_have in crypto_roles and abbreviated_need in crypto_roles:
            crypto_role = discord.utils.get(guild.roles, name="Crypto > Crypto")
            if crypto_role not in user.roles:
                await interaction.response.send_message(
                    f"You need the 'Crypto > Crypto' role to claim this ticket.", ephemeral=True)
                return
        else:
            role_name = f"{abbreviated_have} > {abbreviated_need}"
            role = discord.utils.get(guild.roles, name=role_name)
            if not role or role not in user.roles:
                await interaction.response.send_message(
                    f"You do not have the required role '{role_name}' to claim this ticket.", ephemeral=True)
                return

        button.disabled = True
        button.label = "claimed"
        await interaction.response.edit_message(view=self)

        ticket_channel = guild.get_channel(self.ticket_channel_id)
        if ticket_channel:
            claimed_tickets[interaction.user.id] = ticket_channel.id

            # Give the user permissions to view and send messages in the ticket channel
            overwrite = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            await ticket_channel.set_permissions(user, overwrite=overwrite)

            await ticket_channel.send(f"{user.mention} has claimed the ticket and will be your Exchanger.")

        await interaction.followup.send(f"You have successfully claimed the ticket in {ticket_channel.mention}.", ephemeral=True)




allowed_roles = {"PayPal > LTC", "PayPal > Cashapp", "LTC > PayPal", "LTC > Cashapp", "Cashapp > LTC", "Cashapp > PayPal", "Crypto > Crypto"}

json_file_path = "ExchangerLimit.json"

def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

with open("TotalDealt.json", "r") as f:
    total_dealt = json.load(f)


@client.tree.command(name="close", description="Closes an Exchange Ticket. Owner must approve before fully closing.")
async def ClosingExchangeTicket(interaction: discord.Interaction):
    guild = interaction.guild
    user = interaction.user

    
    exchanger_role = discord.utils.get(guild.roles, name="Exchanger")
    if exchanger_role not in user.roles:
        await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🚪 Closing Ticket Requested",
        description=f"Before closing this ticket, it **must be verified** by someone with the <@&1244473316610146404> role or higher authority.",
        color=discord.Color.from_rgb(30, 215, 96)  # A softer green
    )

    embed.add_field(
        name="🔒 Ticket Status", 
        value="**Pending Verification**", 
        inline=False
    )

    embed.add_field(
        name="👤 Required Action", 
        value="A user with the <@&1244473316610146404> role or higher needs to approve the closure.", 
        inline=False
    )

    embed.set_footer(
        text=f"Closing channel requested by {interaction.user.name} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
    )


    
    await interaction.response.send_message(embed=embed, view=VerifyClosureView(interaction.channel.id, user))
    channel = interaction.channel
    await channel.send("<@&1287115584693076040>")



class VerifyClosureView(discord.ui.View):
    def __init__(self, channel_id, closing_user):
        super().__init__(timeout=None)
        self.channel_id = channel_id  
        self.closing_user = closing_user  

    @discord.ui.button(label="Verify Closure", style=discord.ButtonStyle.green)
    async def verify_closure(self, interaction: discord.Interaction, button: discord.Button):
        allowed_user_ids = {1168162359479644271, 611403629416415257, 929655970576089128, 763288874663018506,347749441396146177}

        if interaction.user.id not in allowed_user_ids:
            await interaction.response.send_message("You are not authorized to verify this closure.", ephemeral=True)
            return

        button.disabled = True
        await interaction.response.edit_message(view=self)

        Exchanger = None
        for uid, channel_id in claimed_tickets.items():
            if channel_id == self.channel_id:
                Exchanger = uid
                break

        user_id = None
        for uid, channel_id in open_tickets_for_Exchange.items():
            if channel_id == self.channel_id:
                user_id = uid
                break

        print(user_id)
        print(Exchanger)

        if user_id is None:
            await interaction.followup.send("No user found associated with this ticket.", ephemeral=True)
            return

        try:
            amount_exchanged = float(user_data[user_id]["HowMuch"])
            user_needed = user_data[user_id]["Need"]  
            user_had = user_data[user_id]["Have"]      
        except KeyError as e:
            await interaction.followup.send(f"Couldn't find the exchange details for this user. Missing key: {e}", ephemeral=True)
            return

        # Update TotalDealt.json
        if "Dealt" not in total_dealt:
            total_dealt["Dealt"] = 0.0

        total_dealt["Dealt"] += amount_exchanged

        with open("TotalDealt.json", "w") as f:
            json.dump(total_dealt, f, indent=4)

        try:
            with open("DealtUSDAmount.json", "r") as f:
                dealt_usd_amount = json.load(f)

            if str(user_id) in dealt_usd_amount["Stats"]:  # Ensure you're using the correct user_id
                dealt_usd_amount["Stats"][str(user_id)] += amount_exchanged  # Updating by user_id
            else:
                dealt_usd_amount["Stats"][str(user_id)] = amount_exchanged  # Assign to user_id

            with open("DealtUSDAmount.json", "w") as f:
                json.dump(dealt_usd_amount, f, indent=4)
        except Exception as e:
            await interaction.followup.send(f"Error updating DealtUSDAmount.json: {e}", ephemeral=True)
            return

        # Update HowManyTimesDealt.json
        try:
            with open("HowManyTimesDealt.json", "r") as f:
                how_many_times_dealt = json.load(f)

            if str(user_id) in how_many_times_dealt["Stats"]:
                how_many_times_dealt["Stats"][str(user_id)] += 1  # Track by user_id
            else:
                how_many_times_dealt["Stats"][str(user_id)] = 1  # Assign to user_id

            with open("HowManyTimesDealt.json", "w") as f:
                json.dump(how_many_times_dealt, f, indent=4)
        except Exception as e:
            await interaction.followup.send(f"Error updating HowManyTimesDealt.json: {e}", ephemeral=True)
            return


        # Create the transcript
        transcript_file_name = f"{interaction.channel.name}.md"
        with open(transcript_file_name, 'a', encoding='utf-8') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")

                if message.attachments:
                    image_links = "\n".join(attachment.url for attachment in message.attachments)
                    f.write(f"{message.author} on {created}: Sent image(s) or Video(s):\n{image_links}\n")
                else:
                    content = replace_emojis(message.clean_content)
                    if message.edited_at:
                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                        f.write(f"{message.author} on {created}: {content} (Edited at {edited})\n")
                    else:
                        f.write(f"{message.author} on {created}: {content}\n")

            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {client.user}*\nDate Formatting: MM/DD/YY*\n*Time Zone: UTC*")

        # Log the exchange as done
        log_channel = client.get_channel(1244752108499243008)  
        embed = discord.Embed(
            title="Exchange Completed",
            color=discord.Color.green()
        )

        # Create the appropriate messages for what the user had and needed
        message1 = self.get_currency_emoji(user_had)
        message2 = self.get_currency_emoji(user_needed)

        embed.add_field(name="What User Had", value=message1, inline=True)
        embed.add_field(name="What User Needed", value=message2, inline=True)
        embed.add_field(name="Exchanged", value=f"${amount_exchanged}", inline=True)
        embed.add_field(name="Exchanged By", value=f"<@{Exchanger}>", inline=True)
        embed.add_field(name="Who got Exchanged", value=f"<@{user_id}>", inline=True)
        embed.add_field(name="Closed By", value=self.closing_user.mention, inline=True)

        await log_channel.send(embed=embed)

        log_channel_2 = client.get_channel(1244677456208855225)  
        with open(transcript_file_name, 'rb') as f:
            transcript_embed = discord.Embed(
                title="Transcript of closed Ticket",
                description="The transcript for the closed ticket is attached **above**.",
                color=discord.Color.green()
            )
            await log_channel_2.send(embed=transcript_embed, file=discord.File(f, transcript_file_name))

        if user_id in user_data:
            del user_data[user_id]  

        claimed_tickets.pop(Exchanger, None)  
        open_tickets_for_Exchange.pop(user_id, None) 

        await interaction.channel.send("The exchange has been confirmed and the ticket is now closed.")
        await interaction.channel.delete()  # Optionally delete the ticket channel

        # Clean up the transcript file
        os.remove(transcript_file_name)

        await rename_voice_channel()

        print(user_data)
        print(claimed_tickets)
        print(open_tickets_for_Exchange)


    # Verification failed button
    @discord.ui.button(label="Verification Failed", style=discord.ButtonStyle.red)
    async def verification_failed(self, interaction: discord.Interaction, button: discord.Button):
        allowed_user_ids = {1168162359479644271, 611403629416415257, 929655970576089128, 763288874663018506}

        if interaction.user.id not in allowed_user_ids:
            await interaction.response.send_message("You are not authorized to perform this action.", ephemeral=True)
            return

        button.disabled = True
        await interaction.response.edit_message(view=self)

        Exchanger = None
        for uid, channel_id in claimed_tickets.items():
            if channel_id == self.channel_id:
                Exchanger = uid
                break

        user_id = None
        for uid, channel_id in open_tickets_for_Exchange.items():
            if channel_id == self.channel_id:
                user_id = uid
                break

        if user_id is None:
            await interaction.followup.send("No user found associated with this ticket.", ephemeral=True)
            return

        # Transcript creation
        transcript_file_name = f"{interaction.channel.name}.md"
        with open(transcript_file_name, 'a', encoding='utf-8') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                
                if message.attachments:
                    image_links = "\n".join(attachment.url for attachment in message.attachments)
                    f.write(f"{message.author} on {created}: Sent image(s) or Video(s):\n{image_links}\n")
                else:
                    content = replace_emojis(message.clean_content)
                    if message.edited_at:
                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                        f.write(f"{message.author} on {created}: {content} (Edited at {edited})\n")
                    else:
                        f.write(f"{message.author} on {created}: {content}\n")

            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {client.user}*\nDate Formatting: MM/DD/YY*\n*Time Zone: UTC*")

        # Log the failed verification in log_channel_2
        log_channel_2 = client.get_channel(1244677456208855225)  
        embed = discord.Embed(
            title="Exchange Failed Verification",
            color=discord.Color.red()
        )

        embed.add_field(name="Who claimed the ticket", value=f"<@{Exchanger}>", inline=True)
        embed.add_field(name="Who opened the ticket", value=f"<@{user_id}>", inline=True)
        embed.add_field(name="Closed By", value=self.closing_user.mention, inline=True)
        
        await log_channel_2.send(embed=embed)

        # Attach the transcript
        with open(transcript_file_name, 'rb') as f:
            transcript_embed = discord.Embed(
                title="Transcript of unverified Ticket",
                description="The transcript for the unverified ticket is attached **above**.",
                color=discord.Color.red()
            )
            await log_channel_2.send(embed=transcript_embed, file=discord.File(f, transcript_file_name))

        # Remove user data, claimed tickets, and open tickets as requested
        if user_id in user_data:
            del user_data[user_id]

        claimed_tickets.pop(Exchanger, None) 
        open_tickets_for_Exchange.pop(user_id, None) 

        await interaction.channel.send("The exchange was not verified and the ticket is now closed.")
        await interaction.channel.delete()  # Optionally delete the ticket channel

        # Clean up the transcript file
        os.remove(transcript_file_name)

        await rename_voice_channel()

        print(user_data)
        print(claimed_tickets)
        print(open_tickets_for_Exchange)

    # Helper function for currency emojis
    def get_currency_emoji(self, currency):
        currency_emojis = {
            "PayPal": "<:PayPal:1244753696508739585>",
            "Litecoin": "<:Litecoin:1244753012438597703>",
            "Cashapp": "<:Cashapp:1244759109891391620>",
            "Bitcoin": "<:Bitcoin:1244816179302891580>",
            "Ethereum": "<:Ethereum:1244816751020085268>",
            "BNB": "<:BNB:1286801387786862665>",
            "Dogecoin": "<:Dogecoin:1244817004204916736>",
            "USDC": "<:USDC:1286801554535354489>",
            "USDT": "<:TetherUSD:1244817460608368671>",
            "Solana": "<:Solana:1244817279573688381>"
        }
        return currency_emojis.get(currency, "Could not find what user had.")






def replace_emojis(text):
    def replace(match):
        emoji_unicode = match.group()
        try:
            emoji_name = emoji.demojize(emoji_unicode).replace(":", "")
            if emoji_unicode.startswith("<a:"):  # Animated custom emoji
                emoji_unicode = f"\\U{emoji_name.split(':')[2]}"
            elif emoji_unicode.startswith("<:"):  # Regular custom emoji
                emoji_unicode = f"\\U{emoji_name.split(':')[1]}"
            else:
                emoji_unicode = emoji.emojize(f":{emoji_name}:", use_aliases=True)
                emoji_unicode = emoji_unicode.encode('unicode-escape').decode('utf-8')
        except:
            pass
        return emoji_unicode

    return re.sub(r"<a?:[a-zA-Z0-9_]+:[0-9]+>|:[a-zA-Z0-9_]+:", replace, text)



"""

@bot.command()
async def send3(ctx):
    embed = discord.Embed(
        title="💼 Apply to Become a SecureSwap Exchanger!",
        description=(
            "📢 **Now's your chance to join SecureSwap as an Exchanger!**\n"
            "As part of the team, you'll need to make a **Safety Deposit**. "
            "This deposit ensures that, in case of any misconduct like an `Exit Scam`, "
            "we can use the funds to reimburse affected users. Currently, we only accept **CRYPTO deposits**.\n\n"
            "🔑 **To qualify as an Exchanger, you must meet the following requirements based on the type of exchange:**"
        ),
        color=discord.Color.from_rgb(34, 139, 34)  # A nice green color
    )

    embed.add_field(
        name="🔗 **PayPal ➡️ CashApp**",
        value="• A verified PayPal account to receive funds\n• A CashApp account to send money",
        inline=False
    )

    embed.add_field(
        name="🔗 **PayPal ➡️ Litecoin (LTC)**",
        value="• A verified PayPal account\n• Litecoin balance to send funds",
        inline=False
    )

    embed.add_field(
        name="🔗 **Litecoin (LTC) ➡️ PayPal**",
        value="• A wallet to receive LTC\n• A verified PayPal account to send money (FnF, no note, PayPal balance only)",
        inline=False
    )

    embed.add_field(
        name="🔗 **Litecoin (LTC) ➡️ CashApp**",
        value="• A wallet to receive LTC\n• A CashApp account to send money",
        inline=False
    )

    embed.add_field(
        name="🔗 **CashApp ➡️ PayPal**",
        value="• A verified CashApp to receive funds\n• A verified PayPal to send money (FnF, no note, PayPal balance only)",
        inline=False
    )

    embed.add_field(
        name="🔗 **CashApp ➡️ Litecoin (LTC)**",
        value="• A verified CashApp to receive funds\n• Litecoin balance to send funds",
        inline=False
    )

    embed.add_field(
        name="🔗 **Crypto ➡️ Crypto**",
        value="• Both cryptocurrencies available as needed by the user\n\nAny false application will be directly denied and you will get an warning.",
        inline=False
    )

    embed.set_footer(text="Press the button below to apply. We will notify you via DM if you're hired!")

    await ctx.send(embed=embed, view=ButtonForExchangerModal())

"""
class ButtonForExchangerModal(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="apply", style=discord.ButtonStyle.green, custom_id="iasjdiwjdijs")
    async def kwidjsdijwidj(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(applyForEchangerModal())


class applyForEchangerModal(discord.ui.Modal, title="Apply for Exchanger"):
    WhatCanUserExchange = discord.ui.TextInput(
        label="What can you Exchange?",
        placeholder="Please write here what you can Exchange. e.g. PayPal > LTC ; LTC > CashApp ; etc...",
        required=True,
        max_length=100,
        style=discord.TextStyle.short
    )
    HowMuchDeposit = discord.ui.TextInput(
        label="How much will you Deposit?",
        placeholder="Please enter the amount (in $) you want to deposit.",
        required=True,
        max_length=100,
        style=discord.TextStyle.short
    )
    ToSAccept = discord.ui.TextInput(
        label="Do you accept our ToS?",
        placeholder="Please write 'Yes' if you agree.",
        required=True,
        max_length=3,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        Can_Exchange = self.WhatCanUserExchange.value
        Deposit = self.HowMuchDeposit.value
        ToS_Accept = self.ToSAccept.value

        # Check if deposit input is a valid number
        try:
            deposit_amount = float(Deposit)
        except ValueError:
            await interaction.response.send_message(
                "❌ Please enter a valid number for the deposit amount.", 
                ephemeral=True
            )
            return
        
       
        if ToS_Accept.lower() != "yes":
            await interaction.response.send_message(
                "❌ You must accept the ToS to proceed.",
                ephemeral=True
            )
            return

      
        channel = client.get_channel(1285934004087947277)
        embed = discord.Embed(
            title="📋 New Exchanger Application",
            description=(
                f"**User:** {interaction.user.mention}\n"
                f"**Username:** {interaction.user.name}\n"
                f"**User ID:** {interaction.user.id}\n\n"
                f"🔄 **Exchange Offer:** {Can_Exchange}\n"
                f"💰 **Deposit Amount:** ${deposit_amount:.2f}\n"
                f"✅ **ToS Accepted:** {ToS_Accept}"
            ),
            color=discord.Color.from_rgb(0, 255, 0)
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None) 
        embed.set_footer(text="SecureSwap Exchanger Application")

        await channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ Your application has been submitted. Please allow 1 to 48 hours for a response.",
            ephemeral=True
        )



    





@client.tree.command(name="answer", description="Accepts or denies someone to be an Exchanger")
@app_commands.describe(user="Select the user", result="Type 'accept' if the user is accepted, otherwise 'denied'")
async def owkadojsdskdwok(interaction: discord.Interaction, user: discord.Member, result: str):
    if interaction.user.id == 1168162359479644271: 
        if result in ["accept", "denied"]:  

            if result == "accept":
                embed = discord.Embed(
                    title="🎉 Congratulations! You've Been Accepted as an Exchanger!",
                    description=(
                        f"Hello {user.mention}, we are pleased to inform you that you've been hired as an **Exchanger** for **SecureSwap**! Before you can start Exchanging, you still have to Deposit before getting your Exchanger role!\n\n"
                        f"📜 **Please make sure to read** <#1285932625709498430> and <#1286818289351266386>**carefully** (If you cant see the Channel, its because you dont have the Exchanger role). Any violation of the ToS will result in an immediate demotion, "
                        f"and your deposit may be forfeited.\n\n"
                        f"Welcome aboard and happy exchanging!"
                    ),
                    color=discord.Color.from_rgb(0, 255, 0)
                )
                embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
                embed.set_footer(text="SecureSwap Exchanger Program")

                await interaction.response.send_message(f"✅ {user.mention} has been notified of their acceptance!", ephemeral=True)
                await user.send(embed=embed)

            elif result == "denied":
                embed = discord.Embed(
                    title="🚫 Application Denied",
                    description=(
                        f"Hello {user.mention}, we're sorry to inform you that your application to become an **Exchanger** for **SecureSwap** "
                        f"has been denied at this time.\n\n"
                        f"Please don't be discouraged! You're welcome to try again in the future."
                    ),
                    color=discord.Color.from_rgb(255, 0, 0)
                )
                embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
                embed.set_footer(text="SecureSwap Exchanger Program")

                await interaction.response.send_message(f"❌ {user.mention} has been notified of their denial.", ephemeral=True)
                await user.send(embed=embed)

        else:
            await interaction.response.send_message("❗ Please enter 'accept' or 'denied' as the result.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)



@client.tree.command(name="stats", description="View your stats or someone else's stats.")
@app_commands.describe(user="The user whose stats you want to view (optional)")
async def stats(interaction: discord.Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.user  

    file_path = "DealtUSDAmount.json"
    file_path2 = "HowManyTimesDealt.json"

    try:
        with open(file_path, 'r') as file:
            usd_data = json.load(file)
    except FileNotFoundError:
        usd_data = {'Stats': {}}

    try:
        with open(file_path2, 'r') as file:
            deals_data = json.load(file)
    except FileNotFoundError:
        deals_data = {'Stats': {}}

 
    total_usd = usd_data['Stats'].get(str(user.id), 0)
    total_deals = deals_data['Stats'].get(str(user.id), 0)

    if total_usd == 0 and total_deals == 0:
        no_stats_embed = discord.Embed(
            title=f"{user.name}'s Stats",
            description=f"⚠️ {user.mention} has no recorded stats at this time.",
            color=discord.Color.from_rgb(255, 165, 0) 
        )
        no_stats_embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=no_stats_embed)
        return

  
    stats_embed = discord.Embed(
        title=f"{user.name}'s Exchange Stats",
        color=discord.Color.from_rgb(0, 255, 0)  
    )

    stats_embed.add_field(name="💵 Total USD Value Dealt", value=f"${total_usd:.2f}", inline=True)
    stats_embed.add_field(name="📈 Deals Completed", value=str(total_deals), inline=True)

    stats_embed.set_thumbnail(url=user.display_avatar.url)

    stats_embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=stats_embed)


JOIN_CHANNEL_ID = 1244777673620848750  
LEAVE_CHANNEL_ID = 1244777691828457614

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(JOIN_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="A user joined",
            description=f"{member.mention} has joined the server!",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"User ID: {member.id}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member: discord.Member):
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="A user left",
            description=f"{member.mention} has left the server.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"User ID: {member.id}")
        await channel.send(embed=embed)


thresholds = {
    0.01: '1244735972361371808',
    100: '1244735906586296350',
    250: '1244735758552535122',
    500: '1245107081715912766',
    1000: '1287110587758805074',
    2000: "1287110786912620594"
}

def load_stats():
    with open('DealtUSDAmount.json', 'r') as file:
        data = json.load(file)
    return data['Stats']

def load_total_dealt():
    with open('TotalDealt.json', 'r') as file:
        data = json.load(file)
    return data['Dealt']

async def update_roles(user_id, amount):
    guild = bot.get_guild(1244472690383917066)  
    member = guild.get_member(user_id)

    if member:
        for threshold, role_id in thresholds.items():
            role = guild.get_role(int(role_id))
            if amount >= threshold and role not in member.roles:
                await member.add_roles(role)
            elif amount < threshold and role in member.roles:
                await member.remove_roles(role)

@tasks.loop(minutes=15)
async def check_stats():
    stats = load_stats()
    for user_id, amount in stats.items():
        if user_id is not None: 
            try:
                await update_roles(int(user_id), amount)
            except ValueError as e:
                print(f"Error converting user_id to int: {user_id}, Error: {e}")
        else:
            pass


@tasks.loop(minutes=10)
async def check_ExchangerLimit():
    with open('ExchangerLimit.json', 'r') as file:
        global exchanger_limits
        exchanger_limits = json.load(file)
    


@tasks.loop(minutes=10)
async def update_member_count():
    guild = bot.get_guild(1244472690383917066)
    if guild is None:
        print("Guild not found!")
        return

    channel = bot.get_channel(1245075969241251883)
    if channel is None:
        print("Channel not found!")
        return

    member_count = sum(1 for member in guild.members if not member.bot)
    new_name = f"Members: {member_count}"
    
    await channel.edit(name=new_name)

async def rename_voice_channel():
  
    total_dealt = load_total_dealt()
    guild = bot.get_guild(1244472690383917066)
    if guild is None:
        print("Guild not found!")
        return


    voice_channel = guild.get_channel(1244680878961987666)  
    if voice_channel is None:
        print("Voice channel not found!")
        return

    new_name = f"Exchanged: ${total_dealt}"
    await voice_channel.edit(name=new_name)


@client.tree.command(name="leaderboard", description="Shows the best 10 people who have exchanged the most")
async def leaderboard(interaction: discord.Interaction):
    stats = load_stats()

  
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    top10 = sorted_stats[:10]

   
    user_id = str(interaction.user.id)
    user_amount = stats.get(user_id, 0)

    
    rank_emojis = ["🥇", "🥈", "🥉", "🎖️", "🎖️", "🏅", "🏅", "🏅", "🏅", "🏅"]

    
    embed = discord.Embed(title="🏆 Top 10 Exchanged Amounts 🏆", color=discord.Color.gold())
    embed.set_thumbnail(url=interaction.guild.icon.url)  

   
    for rank, (uid, amount) in enumerate(top10, 1):
     
        member = interaction.guild.get_member(int(uid))
        user_mention = member.mention if member else f"User {uid}"
        emoji = rank_emojis[rank - 1] 
        embed.add_field(name=f"{emoji} #{rank}", value=f"{user_mention}: **${amount}**", inline=False)

 
    if user_id not in [uid for uid, _ in top10]:
      
        all_users_sorted = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        user_position = next((i + 1 for i, (uid, amount) in enumerate(all_users_sorted) if uid == user_id), len(all_users_sorted))
        
        embed.add_field(name="👤 Your Position", value=f"You ({interaction.user.mention}) are at position **#{user_position}** with **${user_amount}**", inline=False)

    
    embed.set_footer(text="Keep exchanging to climb the leaderboard! 🚀")

    await interaction.response.send_message(embed=embed)



            
"""
@bot.command()
async def send4(ctx):
    embed = discord.Embed(
        title="📜 Important Exchanger Rules & Guidelines",
        description=(
            "💼 **Claim Responsibly**\n"
            "When you claim a ticket, you **must** complete the exchange. Failing to do so will result in a loss of **$5** from your safety deposit. "
            "If the issue is on your end, you will lose **$3.5** from your deposit (means that if your PayPal/Cashapp/LTC does not work or you provided some false infomartion. Depending on what you did the $3.5 will be higher.). However, if the problem lies with the user, you won’t lose anything.\n\n"
            "🚨 **Exit Scam Consequences**\n"
            "In the unfortunate event of an **exit scam**, the scammed user will be compensated with your safety deposit. This ensures fairness and trust in the exchange process.\n\n"
            "💸 **Fees & Earnings**\n"
            "For each successful exchange, you keep **65%** of the fees while we get **35%**. For example, if the fees are **$10**, you get **$6.50** and we receives **$3.50**. "
            "This helps us cover hosting costs and keeps the system running smoothly, while both parties earn money.\n\n"
            "⚠️ **Penalty for Non-Payment**\n"
            "If you refuse or are unable to pay the fee which we get after completing an exchange, you will be **demoted** and only receive **30%** of your deposit back.\n\n"
            "🔒 **Stay Secure**\n"
            "Always ensure you're following the proper guidelines to avoid penalties and maintain your exchanger status!"
        ),
        color=discord.Color.red()  # Or you can use a different color depending on your theme.
    )

    embed.set_footer(text="SecureSwap Exchanger Program")
    embed.set_thumbnail(url="https://example.com/icon.png")  # Replace with an appropriate image URL
    await ctx.send(embed=embed)

"""




@bot.command()
async def leave(ctx):
    ROLE_ID = 1244735162340610058 
    user_id = ctx.author.id
    channel = ctx.channel


    role = ctx.guild.get_role(ROLE_ID)
    if role not in ctx.author.roles:
        await ctx.send(f"{ctx.author.mention}, you don't have the required role to leave this ticket.")
        return

 
    if claimed_tickets.get(user_id) == channel.id:
        if role:
        
            del claimed_tickets[user_id]
            await channel.set_permissions(role, view_channel=True, send_messages=True)
            await channel.set_permissions(ctx.author, overwrite=None)

    
            embed = discord.Embed(
                title="✅ Ticket Left Successfully",
                description=(
                    f"{ctx.author.mention} has been removed as the Exchanger. "
                    f"The `{role.name}` role now has access to this ticket."
                ),
                color=discord.Color.green(),
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(text=f"{ctx.author.name} left exchanging this ticket")
            embed.set_thumbnail(url=ctx.author.avatar.url)

            await ctx.send(content=f"<@&{ROLE_ID}>", embed=embed)
        else:
            await ctx.send("The specified role could not be found. Please check the ROLE_ID.")
    else:
    
        embed = discord.Embed(
            title="❌ Error",
            description=(
                f"{ctx.author.mention}, this is not the ticket you claimed, "
                f"or you are not the Exchanger."
            ),
            color=discord.Color.red(),
            timestamp=ctx.message.created_at,
        )
        embed.set_footer(text="Ensure you're in the correct ticket channel.")
        embed.set_thumbnail(url=ctx.author.avatar.url)

        await ctx.send(embed=embed)


@bot.command()
async def take(ctx):
    ROLE_ID = 1244735162340610058  
    user_id = ctx.author.id
    channel = ctx.channel


    role = ctx.guild.get_role(ROLE_ID)
    if role not in ctx.author.roles:
        await ctx.send(f"{ctx.author.mention}, you don't have the required role to claim this ticket.")
        return

    if channel.id in claimed_tickets.values():
        embed = discord.Embed(
            title="❌ Error",
            description=f"{ctx.author.mention}, this ticket is already claimed by someone else!",
            color=discord.Color.red(),
        )
        embed.set_footer(text="Please wait for the current exchanger to leave the ticket.")
        await ctx.send(embed=embed)
        return

    if role:
      
        claimed_tickets[user_id] = channel.id
        await channel.set_permissions(role, view_channel=False)
        await channel.set_permissions(ctx.author, view_channel=True, send_messages=True)

        embed = discord.Embed(
            title="✅ Ticket Successfully Claimed",
            description=(
                f"{ctx.author.mention} has claimed this ticket. "
                f"The `{role.name}` role no longer has access to this channel."
            ),
            color=discord.Color.green(),
            timestamp=ctx.message.created_at,
        )
        embed.set_footer(text=f"{ctx.author.name} claimed this ticket")
        embed.set_thumbnail(url=ctx.author.avatar.url)

        await ctx.send(embed=embed)
    else:
        await ctx.send("The specified role could not be found. Please check the ROLE_ID.")



@bot.command()
async def steal(ctx):
    CO_OWNER_ROLE_ID = 1244473316610146404  
    ROLE_ID = 1244735162340610058  
    user_id = ctx.author.id
    channel = ctx.channel

 
    co_owner_role = ctx.guild.get_role(CO_OWNER_ROLE_ID)
    if co_owner_role not in ctx.author.roles:
        await ctx.send(f"{ctx.author.mention}, you don't have the required role to steal this ticket.")
        return

 
    current_exchanger = None
    for uid, ch_id in claimed_tickets.items():
        if ch_id == channel.id:
            current_exchanger = uid
            break

   
    if not current_exchanger:
        embed = discord.Embed(
            title="❌ Error",
            description="This ticket is not currently claimed by anyone, so it can't be stolen. Please use `$take`.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return


    del claimed_tickets[current_exchanger]
    claimed_tickets[user_id] = channel.id

  
    role = ctx.guild.get_role(ROLE_ID)
    await channel.set_permissions(role, view_channel=False)
    await channel.set_permissions(ctx.guild.get_member(current_exchanger), view_channel=False) 
    await channel.set_permissions(ctx.author, view_channel=True, send_messages=True) 

    # Success Embed
    embed = discord.Embed(
        title="✅ Ticket Stolen Successfully",
        description=(
            f"{ctx.author.mention} has taken over this ticket! The previous exchanger has been removed."
            f"\nThe `{role.name}` role no longer has access to this channel."
        ),
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"{ctx.author.name} is now the exchanger")

    await ctx.send(embed=embed)

async def get_ltc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data["litecoin"]["usd"]

@client.tree.command(name="converter", description="Convert LTC to USD or USD to LTC")
@app_commands.describe(amount="The amount to convert. In LTC or USD")
async def converter(interaction: discord.Interaction, amount: float):
    view = ConversionView(amount)
    await interaction.response.send_message(
        "Please choose the conversion type:", view=view, ephemeral=True
    )

class ConversionView(discord.ui.View):
    def __init__(self, amount: float):
        super().__init__(timeout=None)
        self.amount = amount

    @discord.ui.button(label="LTC to USD", style=discord.ButtonStyle.primary)
    async def ltc_to_usd(self, interaction: discord.Interaction, button: discord.ui.Button):
        price = await get_ltc_price()
        converted = self.amount * price
        await interaction.response.send_message(
            f"{self.amount} LTC is approximately ${converted:.2f} USD.", ephemeral=True
        )

    @discord.ui.button(label="USD to LTC", style=discord.ButtonStyle.success)
    async def usd_to_ltc(self, interaction: discord.Interaction, button: discord.ui.Button):
        price = await get_ltc_price()
        converted = self.amount / price
        await interaction.response.send_message(
            f"${self.amount:.2f} USD is approximately {converted:.8f} LTC.", ephemeral=True
        )

@bot.command()
async def ping(ctx):
    # Bot latency in milliseconds
    latency = round(client.latency * 1000, 2)
    await ctx.send(f"Pong! 🏓 Latency: `{latency}ms`")

client.run("")  # EXCHANGE BOT FOR raichii. account.titit
