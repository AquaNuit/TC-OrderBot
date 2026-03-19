# Quick Start Guide

## Step 1: Create Discord Bot

1. Visit https://discord.com/developers/applications
2. Click "New Application"
3. Go to "Bot" tab > "Add Bot"
4. Enable "Server Members Intent" and "Message Content Intent"
5. Copy the bot token

## Step 2: Invite Bot

1. Go to OAuth2 > URL Generator
2. Select: `bot` + `applications.commands`
3. Permissions: Manage Channels, Manage Roles, Send Messages, Embed Links
4. Use generated URL to invite bot

## Step 3: Get IDs (Enable Developer Mode in Discord first)

Right-click and copy ID for:
- Your server
- Panel channel
- Ticket category (optional)
- Staff roles

## Step 4: Install & Configure

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your values
```

## Step 5: Run

```bash
python bot.py
```

## Step 6: Setup Panel

In Discord, type: `/setup-panel`

This creates the service order panel with buttons.

## That's it!

Users can now click buttons to create service orders!