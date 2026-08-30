import discord
from discord.ext import commands
import aiohttp
import random
from db import get_connection, get_user

def feature_setup(bot):

    @bot.command(name="shop")
    async def shop(ctx):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("select * from items")
        items = cursor.fetchall()
        conn.close()

        embed = discord.Embed(title="Shop", description="Available items for purchase:")
        for item in items:
            embed.add_field(name=f"{item['name']} - {item['cost']} coins", value=item['description'], inline=False)
        await ctx.send(embed=embed)

    @bot.command(name="buy")
    async def buy(ctx,*,item_id:str):
        item_id = item_id.strip()
        user = get_user(ctx.author.id)
        conn = get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute("select * from items where item_id = ?", (item_id,))
            item = cursor.fetchone()

            if not item:
                conn.close()
                await ctx.send("Item does not exist.")
                return
            if user['wallet'] < item['cost']:
                conn.close()
                await ctx.send(f"You do not have enough coins to buy this item.")
                return
            new_wallet = user['wallet'] - item['cost']
            conn.execute("update users set wallet = ? where user_id = ?", (new_wallet, ctx.author.id))
            
            cursor.execute("select * from inventory where user_id = ? and item_id = ?", (ctx.author.id, item_id))
            item_exists = cursor.fetchone()
            if item_exists:
                cursor.execute("update inventory set qty = qty+1 where id = ?", (item_exists['id'],))
            else:
                cursor.execute("insert into inventory (user_id, item_id, qty) values (?, ?, 1)", (ctx.author.id, item_id))
            conn.execute("insert into history (user_id,action,amount) values (?,'buy',?)", (ctx.author.id, item['cost']))
        conn.close()

        await ctx.send(f" Purchase done !! for {item['name']} for {item['cost']} coins. Your new wallet balance is {new_wallet} coins.")


    @bot.command(name="inventory")
    async def inventory(ctx):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        select i.name, i.description, inv.qty from inventory inv
        join items i on inv.item_id = i.item_id
        where inv.user_id = ? and inv.qty > 0""",(ctx.author.id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await ctx.send("Your inventory is empty.")
            return

        embed = discord.Embed(title=f"{ctx.author.name}'s inventory")
        for row in rows:
            embed.add_field(name=f"{row['name']} (x{row['qty']})", value=row['description'], inline=False)
        await ctx.send(embed=embed)

        @bot.command(name='logpose')
        async def logpose(ctx):
            url="https://api.api-onepiece.com/v2/fruits/en"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5) as resp:
                        if resp.status == 200:
                            fruits = await resp.json()
                            item = random.choice(fruits)
                            embed = discord.Embed(title="Log Pose: Devil Fruit")
                            embed.add_field(name="Name", value=item.get("name", "Unknown"), inline=True)
                            embed.add_field(name="Type", value=item.get("type", "Unknown"), inline=True)
                            embed.add_field(name="Description", value=item.get("description", "A ****** fruit"), inline=False)
                            await ctx.send(embed=embed)
                            return
            except Exception as e:
                pass

        
