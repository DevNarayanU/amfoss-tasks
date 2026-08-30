import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
db_path = "berry_broker.db"

initial_wallet = 500
initial_bank = 0
daily_min = 1000
daily_max = 5000

base_win_chance = 0.5
