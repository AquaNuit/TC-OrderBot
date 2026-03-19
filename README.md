# Discord Service Ticket Bot

A professional Discord bot for managing service orders through a ticket system. Perfect for servers offering paid services like app development, web design, bot creation, and more.

## Features

- **Interactive Service Panel**: Beautiful embed with buttons for each service
- **Modal Forms**: Collects detailed information about service requests
- **Automatic Ticket Creation**: Creates private channels for each order
- **Role Pinging**: Automatically notifies staff when new tickets are created
- **Database Integration**: All tickets are stored in Supabase for tracking
- **Ticket Management**: Close tickets with a single button click
- **Command System**: View all open tickets and user ticket history

## Setup Instructions

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Enable these Privileged Gateway Intents:
   - Server Members Intent
   - Message Content Intent
5. Copy your bot token

### 2. Invite Bot to Your Server

1. Go to OAuth2 > URL Generator
2. Select scopes: `bot` and `applications.commands`
3. Select bot permissions:
   - Manage Channels
   - Manage Roles
   - Send Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands
4. Copy the generated URL and open it to invite the bot

### 3. Get Discord IDs

Enable Developer Mode in Discord (Settings > Advanced > Developer Mode)

Then right-click to copy IDs for:
- Your server (Guild ID)
- Channel where you want the panel (Panel Channel ID)
- Category for tickets (optional - bot can create one)
- Staff roles that should be pinged

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```env
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_server_id
PANEL_CHANNEL_ID=channel_id_for_panel
TICKET_CATEGORY_ID=category_id_for_tickets
STAFF_ROLE_IDS=role_id_1,role_id_2
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_key
```

### 6. Customize Services

Edit `config.py` to modify the available services, prices, and descriptions:

```python
SERVICES = {
    'your_service': {
        'name': 'Your Service Name',
        'price': 10,
        'description': 'Service description'
    }
}
```

### 7. Run the Bot

```bash
python bot.py
```

## Bot Commands

### Admin Commands

- `/setup-panel` - Creates the service order panel with buttons (Requires: Administrator)
- `/tickets` - View all open tickets (Requires: Manage Channels)

### User Commands

- `/my-tickets` - View your personal ticket history

## How It Works

1. **User clicks a service button** on the panel
2. **Modal form appears** asking for:
   - Service details
   - Budget
   - Timeline
   - Additional information
3. **Bot creates a private ticket channel** with:
   - User access
   - Staff role access
   - Detailed order information
4. **Staff gets pinged** and can assist the user
5. **Ticket is closed** using the Close Ticket button

## Database Schema

The bot stores all tickets in Supabase with the following information:
- Ticket number (auto-incremented)
- Discord user information
- Channel ID
- Service type and details
- Budget and timeline
- Status (open/closed)
- Timestamps

## Customization

### Add More Services

Edit `config.py` and add new services to the `SERVICES` dictionary.

### Change Embed Colors

Edit `bot.py` and modify the `discord.Color` values in the embed creation.

### Modify Form Questions

Edit the `ServiceOrderModal` class in `bot.py` to change or add form fields.

## Support

For issues or questions, please create a ticket in your Discord server or contact the developer.

## License

This project is provided as-is for personal and commercial use.