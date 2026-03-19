import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Modal, TextInput
import config
from database import DatabaseManager
from datetime import datetime, timezone
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
db = DatabaseManager()


# ─────────────────────────────────────────────
#  Modals
# ─────────────────────────────────────────────

class ServiceOrderModal(Modal, title='📝 Service Order Form'):
    service_details = TextInput(
        label='📋 Describe what you need',
        placeholder='Be as detailed as possible about your requirements...',
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=1000
    )

    budget = TextInput(
        label='💰 Your Budget',
        placeholder='e.g. $25 or willing to do invites',
        style=discord.TextStyle.short,
        required=True,
        max_length=100
    )

    timeline = TextInput(
        label='⏰ Expected Timeline',
        placeholder='e.g. 3 days, 1 week, ASAP',
        style=discord.TextStyle.short,
        required=True,
        max_length=100
    )

    additional_info = TextInput(
        label='📎 Additional Information (optional)',
        placeholder='Reference links, examples, or anything else...',
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=500
    )

    def __init__(self, service_type: str, service_data: dict):
        super().__init__()
        self.service_type = service_type
        self.service_data = service_data

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        user = interaction.user

        # Get or create ticket category
        category = discord.utils.get(guild.categories, id=config.TICKET_CATEGORY_ID)
        if not category:
            category = await guild.create_category(
                "📁 Tickets",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
            )

        # Channel permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        for role_id in config.STAFF_ROLE_IDS:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_channel = await guild.create_text_channel(
            name=f'🎫・{user.name}',
            category=category,
            overwrites=overwrites
        )

        # Save to database
        ticket_data = {
            'discord_user_id': str(user.id),
            'discord_username': str(user),
            'channel_id': str(ticket_channel.id),
            'service_type': self.service_type,
            'service_details': self.service_details.value,
            'budget': self.budget.value,
            'timeline': self.timeline.value,
            'additional_info': self.additional_info.value or 'N/A',
            'status': 'open'
        }

        db_ticket = db.create_ticket(ticket_data)

        # Staff mentions
        role_mentions = ' '.join([f'<@&{role_id}>' for role_id in config.STAFF_ROLE_IDS])

        # Build ticket embed
        svc = self.service_data
        embed = discord.Embed(
            title=f'{svc["emoji"]}  New Order — {svc["name"]}',
            color=svc.get('color', 0x5865F2),
            timestamp=datetime.now(timezone.utc)
        )

        embed.add_field(
            name='👤 Client',
            value=f'{user.mention}',
            inline=True
        )
        embed.add_field(
            name='💵 Base Price',
            value=f'**${svc["price"]}+** or **{svc["invites"]} Invites**',
            inline=True
        )
        embed.add_field(name='\u200b', value='\u200b', inline=True)

        embed.add_field(
            name='📋 Service Details',
            value=f'```\n{self.service_details.value}\n```',
            inline=False
        )
        embed.add_field(
            name='💰 Client Budget',
            value=f'`{self.budget.value}`',
            inline=True
        )
        embed.add_field(
            name='⏰ Timeline',
            value=f'`{self.timeline.value}`',
            inline=True
        )

        if self.additional_info.value:
            embed.add_field(
                name='📎 Additional Info',
                value=self.additional_info.value,
                inline=False
            )

        if db_ticket:
            embed.set_footer(text=f'Ticket #{db_ticket.get("ticket_number", "N/A")}  •  Created')

        embed.set_thumbnail(url=user.display_avatar.url)

        # Action buttons
        action_view = TicketActionsView()

        await ticket_channel.send(
            content=f'||{user.mention} {role_mentions}||',
            embed=embed,
            view=action_view
        )

        # Welcome message
        welcome_embed = discord.Embed(
            description=(
                f'Hey {user.mention}! 👋\n\n'
                f'Thanks for ordering **{svc["emoji"]} {svc["name"]}**.\n'
                f'A staff member will be with you shortly.\n\n'
                f'> 💡 *Please provide any files, references, or details while you wait!*'
            ),
            color=0x2F3136
        )
        await ticket_channel.send(embed=welcome_embed)

        # Confirmation to user
        confirm_embed = discord.Embed(
            description=f'✅ Your ticket has been created! Head over to {ticket_channel.mention}',
            color=0x57F287
        )
        await interaction.followup.send(embed=confirm_embed, ephemeral=True)


# ─────────────────────────────────────────────
#  Views & Buttons
# ─────────────────────────────────────────────

class ServiceButton(Button):
    def __init__(self, service_type: str, service_data: dict):
        super().__init__(
            label=f'{service_data["name"]}  •  ${service_data["price"]}+',
            style=discord.ButtonStyle.secondary,
            emoji=service_data.get('emoji'),
            custom_id=f'service_{service_type}',
        )
        self.service_type = service_type
        self.service_data = service_data

    async def callback(self, interaction: discord.Interaction):
        modal = ServiceOrderModal(self.service_type, self.service_data)
        await interaction.response.send_modal(modal)


class ServicePanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for service_type, service_data in config.SERVICES.items():
            self.add_item(ServiceButton(service_type, service_data))


class TicketActionsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.danger, emoji='🔒', custom_id='close_ticket')
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        channel = interaction.channel

        db.update_ticket_status(
            str(channel.id),
            'closed',
            datetime.now(timezone.utc).isoformat()
        )

        embed = discord.Embed(
            description=(
                f'🔒 **Ticket Closed**\n'
                f'Closed by {interaction.user.mention}\n\n'
                f'*This channel will be deleted in 5 seconds...*'
            ),
            color=0xED4245
        )

        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(5)

        try:
            await channel.delete()
        except Exception:
            pass


# ─────────────────────────────────────────────
#  Events
# ─────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f'╔══════════════════════════════════════════╗')
    print(f'║  ✅  Bot online as {bot.user}')
    print(f'║  🌐  Connected to {len(bot.guilds)} guild(s)')
    print(f'╚══════════════════════════════════════════╝')

    # Re-register persistent views
    bot.add_view(ServicePanelView())
    bot.add_view(TicketActionsView())

    try:
        synced = await bot.tree.sync()
        print(f'  ✅  Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'  ❌  Failed to sync commands: {e}')


# ─────────────────────────────────────────────
#  Slash Commands
# ─────────────────────────────────────────────

@bot.tree.command(name='setup-panel', description='🛒 Set up the service order panel')
@app_commands.checks.has_permissions(administrator=True)
async def setup_panel(interaction: discord.Interaction):

    # ── Build the price table as a code block ──
    header = f'{"SERVICE":<26}{"PRICE":<10}{"INVITES"}'
    separator = '─' * 46
    rows = []
    for svc in config.SERVICES.values():
        name_col = f'{svc["name"]}'
        price_col = f'${svc["price"]}+'
        invite_col = f'{svc["invites"]} Invites'
        rows.append(f'{name_col:<26}{price_col:<10}{invite_col}')

    table = f'```\n{header}\n{separator}\n' + '\n'.join(rows) + '\n```'

    embed = discord.Embed(
        title='🛒  Service Order Panel',
        description=(
            '**Welcome!** We offer premium development services.\n'
            'Click a button below to place your order.\n'
        ),
        color=0x5865F2
    )

    embed.add_field(
        name='📦  Pricing & Services',
        value=table,
        inline=False
    )

    embed.add_field(
        name='📌  How It Works',
        value=(
            '> **1.** Click a service button below\n'
            '> **2.** Fill out the quick order form\n'
            '> **3.** A private ticket channel opens for you\n'
            '> **4.** Our staff handles your order\n'
        ),
        inline=False
    )

    embed.set_footer(text='⬇️  Select a service to get started!')

    view = ServicePanelView()

    await interaction.response.send_message(embed=embed, view=view)

    confirm = discord.Embed(
        description='✅ Panel deployed successfully!',
        color=0x57F287
    )
    await interaction.followup.send(embed=confirm, ephemeral=True)


@bot.tree.command(name='tickets', description='📋 View all open tickets')
@app_commands.checks.has_permissions(manage_channels=True)
async def view_tickets(interaction: discord.Interaction):
    tickets = db.get_all_open_tickets()

    if not tickets:
        embed = discord.Embed(
            description='📭 No open tickets found.',
            color=0xFEE75C
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(
        title='📋  Open Tickets',
        description=f'**{len(tickets)}** ticket(s) currently open',
        color=0x5865F2
    )

    for ticket in tickets[:10]:
        channel = interaction.guild.get_channel(int(ticket['channel_id']))
        channel_mention = channel.mention if channel else '*(deleted)*'

        embed.add_field(
            name=f'🎫 #{ticket["ticket_number"]}  —  {ticket["service_type"]}',
            value=f'👤 <@{ticket["discord_user_id"]}>\n📌 {channel_mention}',
            inline=True
        )

    if len(tickets) > 10:
        embed.set_footer(text=f'Showing 10 of {len(tickets)} tickets')

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='my-tickets', description='🎫 View your ticket history')
async def my_tickets(interaction: discord.Interaction):
    tickets = db.get_user_tickets(str(interaction.user.id))

    if not tickets:
        embed = discord.Embed(
            description='📭 You have no tickets yet.',
            color=0xFEE75C
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(
        title='🎫  Your Tickets',
        description=f'**{len(tickets)}** total ticket(s)',
        color=0x5865F2
    )

    for ticket in tickets[:10]:
        status_emoji = '🟢' if ticket['status'] == 'open' else '🔴'
        embed.add_field(
            name=f'{status_emoji} #{ticket["ticket_number"]}  —  {ticket["service_type"]}',
            value=f'Status: `{ticket["status"]}`\nCreated: `{ticket["created_at"][:10]}`',
            inline=True
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

if __name__ == '__main__':
    if not config.DISCORD_TOKEN:
        print('❌ DISCORD_TOKEN not found in environment variables')
    else:
        bot.run(config.DISCORD_TOKEN)