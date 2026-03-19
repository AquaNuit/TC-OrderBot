# Troubleshooting Guide

## Common Issues and Solutions

### Bot Won't Start

**Problem**: Bot doesn't come online

**Solutions**:
1. Check if DISCORD_TOKEN is set in .env file
2. Verify token is correct from Discord Developer Portal
3. Check if all required dependencies are installed
4. Run: `pip install -r requirements.txt`

**Problem**: "Privileged intent provided is not enabled or whitelisted"

**Solutions**:
1. Go to Discord Developer Portal
2. Navigate to Bot section
3. Enable "Server Members Intent" and "Message Content Intent"
4. Save and restart bot

### Slash Commands Not Working

**Problem**: /setup-panel command not found

**Solutions**:
1. Wait 5-10 minutes after bot starts (commands need time to sync)
2. Restart bot - commands sync on startup
3. Try in a different channel
4. Check bot has "Use Slash Commands" permission

**Problem**: "Application did not respond"

**Solutions**:
1. Check bot is online and running
2. Verify bot has proper permissions in the server
3. Check console for error messages
4. Try restarting the bot

### Panel/Button Issues

**Problem**: Buttons don't work when clicked

**Solutions**:
1. Verify bot is still running
2. Check bot has permission to create channels
3. Ensure bot role is high enough in role hierarchy
4. Check TICKET_CATEGORY_ID is set (or let bot create one)

**Problem**: "Unknown interaction"

**Solutions**:
1. Bot was restarted - panel needs to be recreated
2. Delete old panel and run /setup-panel again
3. Views don't persist across bot restarts

### Ticket Creation Issues

**Problem**: Ticket channel not created

**Solutions**:
1. Check bot has "Manage Channels" permission
2. Verify TICKET_CATEGORY_ID exists (or remove it to auto-create)
3. Check bot role hierarchy (must be above roles it manages)
4. Ensure server hasn't hit channel limit (500 channels max)

**Problem**: Staff not pinged

**Solutions**:
1. Verify STAFF_ROLE_IDS in .env are correct
2. Check bot can mention the roles (role must be mentionable)
3. Try adding role IDs one at a time to identify issue
4. Format: STAFF_ROLE_IDS=123456789,987654321

### Database Issues

**Problem**: "Supabase credentials not found"

**Solutions**:
1. Check VITE_SUPABASE_URL is set in .env
2. Check VITE_SUPABASE_ANON_KEY is set in .env
3. Verify credentials are correct from Supabase dashboard
4. Ensure no extra spaces in .env file

**Problem**: Database operations failing

**Solutions**:
1. Check Supabase project is active
2. Verify table exists (check supabase/migrations/)
3. Check RLS policies are properly set
4. Review console for specific error messages

### Permission Issues

**Problem**: "Missing permissions"

**Solutions**:
1. Check bot role has required permissions:
   - Manage Channels
   - Manage Roles
   - Send Messages
   - Embed Links
   - Read Message History
2. Bot role must be higher than roles it needs to manage
3. Re-invite bot with updated permissions URL

### Other Issues

**Problem**: Ticket closes but channel doesn't delete

**Solutions**:
1. Bot needs "Manage Channels" permission
2. Check bot has permission in that specific category
3. Manual deletion is okay - database is already updated

**Problem**: Ticket numbers not showing

**Solutions**:
1. Check database connection
2. Verify migrations ran successfully
3. Check serial sequence in database

## Getting Help

If you still have issues:

1. Check the console output for error messages
2. Enable debug logging by adding to bot.py:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
3. Verify all IDs are correct (enable Developer Mode to copy IDs)
4. Test in a different server to isolate the issue
5. Check Discord API status: https://discordstatus.com

## Debugging Tips

1. Always check console output when bot starts
2. Test commands in a test server first
3. Use /my-tickets to verify database is working
4. Create a test role to test staff pinging
5. Keep bot logs for troubleshooting

## Configuration Checklist

- [ ] Bot token is valid
- [ ] Intents are enabled in Developer Portal
- [ ] Bot is invited with correct permissions
- [ ] Guild ID is correct
- [ ] Staff role IDs are correct (comma-separated)
- [ ] Supabase credentials are valid
- [ ] Dependencies are installed
- [ ] .env file exists and is properly formatted