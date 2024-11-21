from discord.ext import commands
import json
import os

TASKS_FILE = "src/tasks.json"

# Asegurar que el archivo existe
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        json.dump({}, f)

def load_tasks():
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class TaskCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_task")
    async def add_task(self, ctx, *, task: str):
        """Agregar una nueva tarea."""
        tasks = load_tasks()
        user_id = str(ctx.author.id)
        if user_id not in tasks:
            tasks[user_id] = []
        tasks[user_id].append(task)
        save_tasks(tasks)
        await ctx.send(f"Tarea agregada: `{task}`")

    @commands.command(name="list_tasks")
    async def list_tasks(self, ctx):
        """Listar todas las tareas del usuario."""
        tasks = load_tasks()
        user_id = str(ctx.author.id)
        user_tasks = tasks.get(user_id, [])
        if user_tasks:
            tasks_str = "\n".join([f"{i + 1}. {t}" for i, t in enumerate(user_tasks)])
            await ctx.send(f"Tus tareas:\n{tasks_str}")
        else:
            await ctx.send("No tienes tareas pendientes.")

    @commands.command(name="clear_tasks")
    async def clear_tasks(self, ctx):
        """Eliminar todas las tareas del usuario."""
        tasks = load_tasks()
        user_id = str(ctx.author.id)
        if user_id in tasks:
            tasks.pop(user_id)
            save_tasks(tasks)
            await ctx.send("Todas tus tareas han sido eliminadas.")
        else:
            await ctx.send("No tienes tareas para eliminar.")

def setup_tasks(bot):
    bot.add_cog(TaskCommands(bot))
