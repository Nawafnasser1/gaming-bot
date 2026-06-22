import discord
from discord.ext import commands
import os
try:
    from dotenv import load_dotenv
    load_dotenv()  # يعمل محلياً عبر ملف .env
except ImportError:
    pass  # على Discloud لا نحتاج dotenv

# Enable necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# ---------- Persistent Buttons ----------

class GenderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ولد 👨", style=discord.ButtonStyle.blurple, custom_id="role_boy")
    async def boy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name="👨 | ولد")
        if role:
            girl_role = discord.utils.get(guild.roles, name="👩 | بنت")
            if girl_role in interaction.user.roles:
                await interaction.user.remove_roles(girl_role)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم إضافة رتبة {role.mention} لك وفتح السيرفر!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ الرتبة غير موجودة، تواصل مع الإدارة.", ephemeral=True)

    @discord.ui.button(label="بنت 👩", style=discord.ButtonStyle.red, custom_id="role_girl")
    async def girl_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name="👩 | بنت")
        if role:
            boy_role = discord.utils.get(guild.roles, name="👨 | ولد")
            if boy_role in interaction.user.roles:
                await interaction.user.remove_roles(boy_role)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم إضافة رتبة {role.mention} لك وفتح السيرفر!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ الرتبة غير موجودة، تواصل مع الإدارة.", ephemeral=True)


class DeviceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_device_role(self, interaction: discord.Interaction, role_name: str):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f"❌ تمت إزالة رتبة {role.mention}.", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ تمت إضافة رتبة {role.mention}!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ الرتبة غير موجودة.", ephemeral=True)

    @discord.ui.button(label="💻 PC", style=discord.ButtonStyle.secondary, custom_id="role_pc")
    async def pc_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_device_role(interaction, "💻 | PC")

    @discord.ui.button(label="🎮 PlayStation", style=discord.ButtonStyle.secondary, custom_id="role_ps")
    async def ps_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_device_role(interaction, "🎮 | PlayStation")

    @discord.ui.button(label="💚 Xbox", style=discord.ButtonStyle.secondary, custom_id="role_xbox")
    async def xbox_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_device_role(interaction, "💚 | Xbox")

    @discord.ui.button(label="📱 Mobile", style=discord.ButtonStyle.secondary, custom_id="role_mobile")
    async def mobile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_device_role(interaction, "📱 | Mobile")


# ---------- Bot Setup ----------

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    bot.add_view(GenderView())
    bot.add_view(DeviceView())
    print(f"✅ البوت يعمل الآن: {bot.user.name} ({bot.user.id})")

# ---------- Welcome Event ----------

@bot.event
async def on_member_join(member):
    # أرسل رسالة ترحيب في قناة الترحيب
    welcome_channel = discord.utils.get(member.guild.text_channels, name="الترحيب-والقوانين")
    role_channel = discord.utils.get(member.guild.text_channels, name="تحديد-الرتب")

    if welcome_channel:
        role_mention = role_channel.mention if role_channel else "#تحديد-الرتب"
        await welcome_channel.send(
            f"👋 أهلاً وسهلاً بك يا {member.mention}! 🎮\n"
            f"نورت السيرفر! توجه إلى {role_mention} لاختيار رتبتك وجهازك لفتح بقية القنوات. نتمنى لك وقتاً ممتعاً! 🎉"
        )

# ---------- Token ----------
# التوكن يُقرأ من ملف .env أو من متغيرات البيئة في منصة الاستضافة
BOT_TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ خطأ: لم يتم العثور على BOT_TOKEN. تأكد من وجود ملف .env")
    else:
        bot.run(BOT_TOKEN)
