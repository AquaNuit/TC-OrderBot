# Project Structure

```
discord-ticket-bot/
│
├── bot.py                 # Main bot file with all commands and functionality
├── config.py              # Configuration and service definitions
├── database.py            # Supabase database connection and queries
├── requirements.txt       # Python dependencies
│
├── .env                   # Environment variables (not in git)
├── .env.example           # Example environment file
├── .gitignore            # Git ignore rules
│
├── README.md             # Complete documentation
├── QUICKSTART.md         # Quick setup guide
├── FEATURES.md           # Feature overview
├── PROJECT_STRUCTURE.md  # This file
│
└── supabase/
    └── migrations/       # Database migration files
```

## File Descriptions

### Core Files

**bot.py** (Main Application)
- Discord bot initialization
- ServiceOrderModal class (form for collecting order details)
- ServiceButton and ServicePanelView classes (interactive UI)
- CloseTicketView class (ticket closing functionality)
- Bot commands: /setup-panel, /tickets, /my-tickets
- Event handlers

**config.py** (Configuration)
- Environment variable loading
- Discord configuration (token, IDs, roles)
- Supabase configuration
- Service definitions (customizable)

**database.py** (Database Layer)
- DatabaseManager class
- Supabase client initialization
- CRUD operations for tickets
- Query methods

### Configuration Files

**.env** (Environment Variables)
- Discord bot token
- Server and channel IDs
- Role IDs for staff
- Supabase credentials

**requirements.txt** (Dependencies)
- discord.py (Discord API wrapper)
- python-dotenv (environment variables)
- supabase (database client)

### Documentation Files

**README.md** - Complete setup and usage guide
**QUICKSTART.md** - Quick 6-step setup
**FEATURES.md** - Detailed feature list
**PROJECT_STRUCTURE.md** - This file

### Database

**supabase/migrations/** - Database schema migrations
- Tickets table definition
- Row Level Security policies
- Indexes for performance

## Key Components

### 1. Modal Form System
Location: `bot.py` - ServiceOrderModal class
- Collects user input through Discord modals
- 4 input fields (3 required, 1 optional)
- Validates and processes submissions

### 2. Ticket Creation
Location: `bot.py` - ServiceOrderModal.on_submit method
- Creates private channel
- Sets permissions
- Sends formatted embed
- Saves to database
- Pings staff roles

### 3. Database Operations
Location: `database.py`
- create_ticket() - Store new tickets
- get_ticket_by_channel_id() - Retrieve ticket data
- update_ticket_status() - Update ticket state
- get_user_tickets() - User ticket history
- get_all_open_tickets() - Staff ticket list

### 4. Service Configuration
Location: `config.py` - SERVICES dictionary
- Easily add/remove services
- Define names, prices, descriptions
- No code changes needed for new services

## Customization Points

1. **Add Services**: Edit SERVICES in config.py
2. **Change Form Fields**: Modify ServiceOrderModal in bot.py
3. **Adjust Embed Colors**: Update discord.Color values in bot.py
4. **Modify Permissions**: Edit overwrites in ticket creation
5. **Change Close Delay**: Modify asyncio.sleep duration

## Flow Diagram

```
User clicks service button
    ↓
Modal form appears
    ↓
User fills and submits
    ↓
Bot creates ticket channel
    ↓
Bot saves to database
    ↓
Bot pings staff roles
    ↓
Staff assists user
    ↓
Close button clicked
    ↓
Database updated
    ↓
Channel deleted
```