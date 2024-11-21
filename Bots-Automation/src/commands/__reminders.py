from discord.ext import commands, tasks
import asyncio
import sqlite3
from utils.database import DB_FILE

class ReminderCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()

    @commands.command(name="reminder")
    async def set_reminder(self, ctx, time: int, *, message: str):
        """Establece un recordatorio."""
        user_id = str(ctx.author.id)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO reminders (user_id, message, time) VALUES (?, ?, ?)",
                       (user_id, message, time))
        conn.commit()
        conn.close()

        await ctx.send(f"✅ Recordatorio configurado: `{message}` en {time} segundos.")

    @tasks.loop(seconds=10)
    async def check_reminders(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT id, user_id, message, time FROM reminders")
        reminders = cursor.fetchall()

        for reminder in reminders:
            reminder_id, user_id, message, time = reminder
            if time <= 0:
                user = await self.bot.fetch_user(int(user_id))
                await user.send(f"🔔 Recordatorio: {message}")

                cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
            else:
                cursor.execute("UPDATE reminders SET time = time - 10 WHERE id = ?", (reminder_id,))

        conn.commit()
        conn.close()

def setup_reminders(bot):
    bot.add_cog(ReminderCommands(bot))
