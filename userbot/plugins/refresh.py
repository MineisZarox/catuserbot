#By @IrisZarox
import os
import heroku3
import shutil as sl
from ..Config import Config
from ..utils import load_module, load_plugins, remove_plugin as rem
from . import catub, edit_delete, edit_or_reply, UPSTREAM_REPO_URL

plugin_category = "tools"

z, y, x, w, v, = UPSTREAM_REPO_URL.split("/")
branch = Config.UPSTREAM_REPO_BRANCH or "master"
# =================================================
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
# =================================================


# =================================================
repo = os.environ.get("EXTERNAL_PLUGIN_REPO")
token = os.environ.get("GITHUB_ACCESS_TOKEN")
a, b, c, username, d, = repo.split("/")
ppr = c + "/" + username + "/"  + d
if token:
    plug_repo = f"https://{username}:{token}@{ppr}.git"
else:
    plug_repo = repo
# =================================================
    
@catub.cat_cmd(
    pattern="refresh(?:\s|$)([\s\S]*)",
    command=("refresh", plugin_category),
    info={
        "header": "To refresh external plugin with repository.",
        "description": "Reinstall external plugins from external plugin repository.",
        "usage": "{tr}refresh",
    },
)

async def refesh(event):
    "To refresh ext_plugins"
    plugin = event.pattern_match.group(1)
    if plugin:
        try:
            try:
                rem(plugin)
            except:
                return await edit_or_reply(event, f"`No such plugin exist as {plugin}.py`")
            os.remove(f"userbot/ext_plugins/{plugin}.py")
            os.system(f"git clone {plug_repo}")
            os.system(f"mv 'Plugins/ext_plugins/{plugin}.py' 'userbot/ext_plugins'")
            sl.rmtree("Plugins")
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            await load_module(plugin, "userbot/ext_plugins")
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            await edit_or_reply(event,  f"`Refreshed {plugin} successfully.`")
        except Exception as e:
            LOGS.error(f"{e}")
            return await edit_or_reply(event,  f"`Error:: {e}`")
    else:
        try:
            k = os.listdir("userbot/ext_plugins")
            res = [sub.replace('.py', '') for sub in k]
            for i in res:
                rem(i)
            await edit_or_reply(event, f"`Cloning to {d}...`")
            sl.rmtree("userbot/ext_plugins")
            os.system(f"git clone {plug_repo}")
            os.system("mv 'Plugins/ext_plugins' 'userbot'")
            sl.rmtree("Plugins")
            await edit_or_reply(event, f"`Installing external plugins...`")
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            await load_plugins("ext_plugins")
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            plug = 0
            dir = os.listdir("userbot/ext_plugins")
            for file in dir:
                plug+=1
            try:
                Heroku = heroku3.from_key(HEROKU_API_KEY)
                app = Heroku.app(HEROKU_APP_NAME)
                data = app.get_log()
                await edit_or_reply(event, data, deflink=True, linktext=f"`Refreshed all {plug} external plugins successfully:`")
            except BaseException:
                return await edit_or_reply(event, "`Refreshed all external plugins successfully`")
        except Exception as e:
            LOGS.error(f"{e}")
            return await edit_or_reply(event,  f"`Error: {e}`")
