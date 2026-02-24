import discord
from discord.ext import commands

# 🔥 PUT YOUR NEW RESET TOKEN HERE
import os
TOKEN = os.getenv("TOKEN")

CATEGORY_ID = 1475480122617368751
STAFF_ROLE_ID = 1475433514471260282
LOG_CHANNEL_ID = 1475475167957225555

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ================= READY =================

@bot.event
async def on_ready():
    print(f"⚡ ETHRAN SHOP ONLINE AS {bot.user}")


# ================= PANEL VIEW =================

class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Nitro Stock", emoji="⚡", style=discord.ButtonStyle.secondary)
    async def nitro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Nitro Stock")

    @discord.ui.button(label="Spawner Stock", emoji="💀", style=discord.ButtonStyle.secondary)
    async def spawner(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Spawner Stock")

    @discord.ui.button(label="Boost Stock", emoji="🚀", style=discord.ButtonStyle.secondary)
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Boost Stock")

    @discord.ui.button(label="Donut Kits", emoji="🍩", style=discord.ButtonStyle.secondary)
    async def donut(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Donut Kits")

    @discord.ui.button(label="Member Stock", emoji="👥", style=discord.ButtonStyle.secondary)
    async def member(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Member Stock")

    @discord.ui.button(label="Auto Adv", emoji="📣", style=discord.ButtonStyle.secondary)
    async def autoadv(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Auto Adv")

    @discord.ui.button(label="Elytra Stock", emoji="🪽", style=discord.ButtonStyle.secondary)
    async def elytra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Elytra Stock")

    @discord.ui.button(label="Stash Stock", emoji="📦", style=discord.ButtonStyle.secondary)
    async def stash(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Stash Stock")


# ================= CREATE TICKET =================

async def create_ticket(interaction, product):

    guild = interaction.guild
    category = guild.get_channel(CATEGORY_ID)
    staff_role = guild.get_role(STAFF_ROLE_ID)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    channel = await guild.create_text_channel(
        name=f"{product.lower().replace(' ', '-')}-{interaction.user.name}",
        category=category,
        overwrites=overwrites
    )

    description = (
        "🖤━━━━━━━━━━━━━━━━━━━━━━🖤\n"
        f"🛒 PRODUCT: **{product}**\n"
        f"👤 CLIENT: {interaction.user.mention}\n\n"
        "🔒 Secure Neon Transaction Channel\n"
        "⏳ Please wait for staff response.\n"
        "🖤━━━━━━━━━━━━━━━━━━━━━━🖤"
    )

    embed = discord.Embed(
        title="⚡ ETHRAN SHOP • NEON TICKET ⚡",
        description=description,
        color=0xff00ff
    )

    embed.set_footer(text="ETHRAN SHOP • Underground Neon System")

    await channel.send(embed=embed, view=CloseButton())

    await interaction.response.send_message(
        f"⚡ Your {product} ticket has been opened!",
        ephemeral=True
    )

    log = guild.get_channel(LOG_CHANNEL_ID)
    if log:
        await log.send(f"📩 NEW TICKET | {channel.mention} | {product} | {interaction.user}")


# ================= CLOSE BUTTON =================

class CloseButton(discord.ui.View):
    @discord.ui.button(label="Close Ticket", emoji="🔒", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.channel.send("⚠️ Closing ticket...")

        log = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log:
            await log.send(f"❌ Ticket Closed: {interaction.channel.name}")

        await interaction.channel.delete()


# ================= PANEL COMMAND =================

@bot.command()
@commands.has_permissions(administrator=True)
async def panel(ctx):

    description = (
        "⚡━━━━━━━━━━━━━━━━━━━━━━⚡\n"
        "🖤 ETHRAN SHOP • NEON BLACK MARKET 🖤\n\n"
        "⚡ Nitro Stock\n"
        "💀 Spawner Stock\n"
        "🚀 Boost Stock\n"
        "🍩 Donut Kits\n"
        "👥 Member Stock\n"
        "📣 Auto Adv\n"
        "🪽 Elytra Stock\n"
        "📦 Stash Stock\n\n"
        "🛒 Select your product below.\n"
        "⚡━━━━━━━━━━━━━━━━━━━━━━⚡"
    )

    embed = discord.Embed(
        title="🖤 ETHRAN SHOP PURCHASE PANEL 🖤",
        description=description,
        color=0xff00ff
    )

    embed.set_footer(text="ETHRAN SHOP • Powered by Neon System")
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)

    await ctx.send(embed=embed, view=TicketPanel())


bot.run(TOKEN)
