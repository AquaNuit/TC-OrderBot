import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))
PANEL_CHANNEL_ID = int(os.getenv('PANEL_CHANNEL_ID', 0))
TICKET_CATEGORY_ID = int(os.getenv('TICKET_CATEGORY_ID', 0))

# Parse staff role IDs
STAFF_ROLE_IDS = [
    int(role_id.strip())
    for role_id in os.getenv('STAFF_ROLE_IDS', '').split(',')
    if role_id.strip()
]

# Service Configuration
SERVICES = {
    'scripts_tech_support': {
        'name': 'Scripts & Tech Support',
        'price': 5,
        'invites': 3,
        'emoji': '🛠️',
        'description': 'Custom scripts, automation & tech help',
        'color': 0x3498DB,
    },
    'discord_servers': {
        'name': 'Discord Servers',
        'price': 10,
        'invites': 5,
        'emoji': '🌐',
        'description': 'Professional server setup & config',
        'color': 0x9B59B6,
    },
    'discord_bots': {
        'name': 'Discord Bots',
        'price': 20,
        'invites': 10,
        'emoji': '🤖',
        'description': 'Custom bots tailored to your server',
        'color': 0x2ECC71,
    },
    'websites': {
        'name': 'Websites',
        'price': 25,
        'invites': 15,
        'emoji': '🌍',
        'description': 'Modern responsive websites & web apps',
        'color': 0xE67E22,
    },
    'android_apps': {
        'name': 'Android Apps (.apk)',
        'price': 50,
        'invites': 20,
        'emoji': '📱',
        'description': 'Native Android applications as APK',
        'color': 0xE74C3C,
    },
    'desktop_apps': {
        'name': 'Desktop Apps (.exe)',
        'price': 70,
        'invites': 25,
        'emoji': '💻',
        'description': 'Windows desktop applications as EXE',
        'color': 0x1ABC9C,
    },
}