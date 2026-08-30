import discord
from discord.ext import commands
import random
import config
from db import get_connection, get_user

def setup(bot):




    @bot.command(name="bounty")
    async def bounty(ctx,target:discord.Member=None):
        member = target or ctx.author
        user = get_user(member.id)
        total_bounty = user['wallet'] + user['bank']

        embed = discord.Embed(title=f"Bounty: {member.display_name}")
        embed.add_field(name=" Wallet",value=f"{user['wallet']:,}", inline=True)
        embed.add_field(name=" Bank",value=f"{user['bank']:,}", inline=True)
        embed.add_field(name=" Overall Bounty",value=f"{total_bounty:,}", inline=True)
        await ctx.send(embed=embed)

    @bot.command(name="setsail")
    @commands.cooldown(1,86400,commands.BucketType.user)
    async def setsail(ctx):
        get_user(ctx.author.id)
        reward = random.randint(config.daily_min,config.daily_max)
        conn = get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute("select id from inventory where user_id = ? and item_id='gluttony' and qty>0",(ctx.author.id,))
            buff = cursor.fetchone()
            if buff:
                reward = int(reward * 1.5)
                cursor.execute("update inventory set qty=qty-1 where id = ?",(buff['id'],))
                cursor.execute("delete from inventory where qty<=0")
            conn.execute("update users set wallet=wallet+? where user_id = ?", (reward, ctx.author.id))
            conn.execute("insert into history (user_id,action,amount) values (?,'setsail',?)", (ctx.author.id, reward))
        conn.close()
        await ctx.send(f" {ctx.author.mention} set sail and earned {reward:,} coins! ")

    @setsail.error
    async def setsail_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            hour=int(error.retry_after//3600)
            minutes=int((error.retry_after%3600)//60)
            await ctx.send(f" Cooldown going on ! Try again in '{hour}h {minutes}m'.")
    @bot.command(name="trade")
    async def trade(ctx, recipient: discord.Member, amount:int):
        if recipient.id == ctx.author.id or recipient.bot or amount<=0:
            await ctx.send(" Invalid recipient or amount")
            return

        sender = get_user(ctx.author.id)
        get_user(recipient.id)

        if sender['wallet'] <amount:
            await ctx.send(" Insufficient wallet funds.")
            return

        conn = get_connection()

        with conn:
            conn.execute("update users set wallet=wallet-? where user_id=?", (amount, ctx.author.id))
            conn.execute("update users set wallet=wallet+? where user_id=?",(amount, recipient.id))
            conn.execute("insert into history (user_id, end_id, action, amount) values (?, ?, 'trade', ?)", (ctx.author.id, recipient.id, amount))
        conn.close()

        await ctx.send(f" Transferred **{amount:,}** to {recipient.mention}")


    @bot.command(name="raid")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def raid(ctx, target: discord.Member):
        if target.id == ctx.author.id or target.bot:
            await ctx.send(" Invalid raid target ")
            return
        get_user(ctx.author.id)
        victim=get_user(target.id)

        if victim['wallet']<100:
            await ctx.send(f"  {target.display_name} has insufficient raidable berries");
            return

        conn=get_connection()
        with conn:
            cursor=conn.cursor()
            cursor.execute("select id from inventory where user_id=? and item_id in('shield', 'Straw hat') and qty>0", (target.id,))
            shield=cursor.fetchone()
            if shield:
                cursor.execute("update inventory set qty=qty-1 where id =?", (shield['id'],))
                cursor.execute("delete form inventory where qty <=0")
                conn.close()
                await ctx.send(f" {target.mention}'s shield protected them from raid!")
                return
            if random.random()<=config.base_win_chance:
                stolen=max(1,int(victim['wallet']*0.20))
                conn.execute("update users set wallet=wallet-? where user_id=?", (stolen, target.id))
                conn.execute("update users set wallet=wallet+? where user_id=?", (stolen, ctx.author.id))
                conn.execute("insert into history (user_id, end_id, action, amount) values (?, ?, 'raid_win', ?)", (ctx.author.id, target.id, stolen))
                msg= f"  Raid success!! Got **{stolen:,}** from {target.mention}"
            else:
                penalty=min(500,max(50, int(victim['wallet']*0.05)))
                conn.execute("update users set wallet=max(0, wallet-?) where user_id=?", (penalty, ctx.author.id))
                conn.execute("update users set wallet=wallet+? where user_id=?",(penalty, target.id))
                conn.execute("insert into history (user_id, end_id, action, amount) values (?, ?, 'raid_loss', ?)",(ctx.author.id, target.id, penalty))
                msg= f" Raid failed! you lost **{penalty:,}** retreating from {target.mention}"
        conn.close()
        await ctx.send(msg)

    @raid.error
    async def raid_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = int(error.retry_after // 60)
            await ctx.send(f" Rest your crew. Try again in `{minutes}` minutes.")

    @bot.command(name="worstgeneration")
    async def worstgeneration(ctx):
        conn= get_connection()
        cursor=conn.cursor()
        cursor.execute("select user_id, (wallet+bank) as total from users order by total desc limit 5")
        top_users=cursor.fetchall()
        conn.close()
        lines=[]
        for i, row in enumerate(top_users,1):
            user_id=row['user_id']
            total=row['total']
            lines.append(f"**#{i} <@{user_id}>** - {total:,}")
        embed=discord.Embed(title="the worst generation ",description="\n".join(lines) or "No entries yet",color=discord.Color.red())
        await ctx.send(embed=embed)

    @bot.command(name="history")
    async def history(ctx):
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("select action, amount, timestamp from history where user_id=? order by id desc limit 5", (ctx.author.id,))
        records=cursor.fetchall()
        conn.close()

        if not records:
            await ctx.send(" No transactions")
            return

        lines=[]
        for r in records:
            action=r['action']
            amount=r['amount']
            time=r['timestamp']
            lines.append(f" '{action}': **{amount:,}** ({time})")
        embed=discord.Embed(title=f"Ledger history: {ctx.author.display_name}", description="\n".join(lines), color=discord.Color.blue())
        await ctx.send(embed=embed)

