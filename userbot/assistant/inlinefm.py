
import asyncio
import io
import os
import shutil
import time
from pathlib import Path

from userbot import catub

from telethon import events, Button
from telethon import CallbackQuery
from ..Config import Config
from ..core import check_owner
from ..helpers.utils import _catutils, _format
from . import humanbytes


CC = []
PATH = []#using list method for some reason
thumb_image_path = os.path.join("./temp", "zarza.jpg")

# freaking selector
def add_s(msg, num: int):
    fmsg = ""
    msgs = msg.splitlines()
    leng = len(msgs)
    if num == 0:
        kiwi = leng-1
        msgs[kiwi] = msgs[kiwi] + " ⭕️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    elif num == leng:
        kiwi = 1
        msgs[kiwi] = msgs[kiwi] + " ⭕️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    else:
        kiwi = num
        msgs[kiwi] = msgs[kiwi] + " ⭕️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    buttons = [[
        Button.inline(f"D", data=f"rem_{msgs[kiwi]}|{kiwi}"),
        Button.inline(f"X", data=f"cut_{msgs[kiwi]}|{kiwi}"),
        Button.inline(f"C", data=f"copy_{msgs[kiwi]}|{kiwi}"),
        Button.inline(f"V", data=f"paste_{kiwi}")],
        [Button.inline(f"⬅️", data=f"back"),
        Button.inline(f"⬆️", data=f"up_{kiwi}"),
        Button.inline(f"⬇️", data=f"down_{kiwi}"),
        Button.inline(f"➡️", data=f"forth_{msgs[kiwi]}")]
    ]
    return fmsg, buttons


def get_manager(path, num: int):
    if os.path.isdir(path):
        msg = "Folders and Files in `{}` :\n".format(path)
        lists = sorted(os.listdir(path))
        files = ""
        folders = ""
        for contents in sorted(lists):
            zpath = os.path.join(path, contents)
            if not os.path.isdir(zpath):
                size = os.stat(zpath).st_size
                if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += f"🎧`{contents}`\n"
                if str(contents).endswith((".opus")):
                    files += f"🎤`{contents}`\n"
                elif str(contents).endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += f"🎬`{contents}`\n"
                elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += f"📚`{contents}`\n"
                elif str(contents).endswith((".py")):
                    files += f"🐍`{contents}`\n"
                elif str(contents).endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")
                ):
                    files += f"🏞`{contents}`\n"
                else:
                    files += f"📔`{contents}`\n"
            else:
                folders += f"📂`{contents}`\n"
        msg = msg + folders + files if files or folders else f"{msg}__empty path__"
        PATH.clear()
        PATH.append(path)
        msgs = add_s(msg, int(num))
    else:
        size = os.stat(path).st_size
        msg = "The details of given file :\n"
        if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎧"
        if str(path).endswith((".opus")):
            mode = "🎤"
        elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎬"
        elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "📚"
        elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🏞"
        elif str(path).endswith((".py")):
            mode = "🐍"
        else:
            mode = "📔"
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location :** `{path}`\n"
        msg += f"**icon :** `{mode}`\n"
        msg += f"**Size :** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"
        buttons = [[
            Button.inline(f"Rem", data=f"rem_File|{num}"),
            Button.inline(f"Send", data=f"send_"),
            Button.inline(f"X", data=f"cut_File|{num}"),
            Button.inline(f"C", data=f"copy_File{num}"),],
            [Button.inline(f"⬅️", data=f"back"),
            Button.inline(f"⬆️", data=f"up_File"),
            Button.inline(f"⬇️", data=f"down_File"),
            Button.inline(f"➡️", data=f"forth_File")]
        ]
        PATH.clear()
        PATH.append(path)
        msgs = (msg, buttons)
    return msgs

#BACK
@catub.tgbot.on(CallbackQuery(pattern="back"))
@check_owner
async def back(event):
    path = PATH[0]
    paths = path.split("/")
    if paths[-1] == "":
        paths.pop()
        paths.pop()
    else:
        paths.pop()
    npath = ""
    for ii in paths:
        npath += f"{ii}/"
    num = 1
    msg, buttons = get_manager(npath, num)
    await asyncio.sleep(1)
    await event.edit(msg, buttons=buttons)

#UP
@catub.tgbot.on(CallbackQuery(pattern="up_(.*)"))
@check_owner
async def up(event):
    num = (event.pattern_match.group(1).decode("UTF-8"))
    if num == "File":
        await event.answer("Its a File dummy!", alert=True)
    else:
        num1 = int(num) - 1
        path = PATH[0]
        msg, buttons = get_manager(path, num1)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)

#DOWN
@catub.tgbot.on(CallbackQuery(pattern="down_(.*)"))
@check_owner
async def down(event):
    num= (event.pattern_match.group(1).decode("UTF-8"))
    if num == "File":
        await event.answer("Its a file dummy!", alert=True)
    else:
        path = PATH[0]
        num1 = int(num) + 1
        msg, buttons = get_manager(path, num1)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)
    
#FORTH
@catub.tgbot.on(CallbackQuery(pattern="forth_(.*)"))
@check_owner
async def forth(event):
    npath = (event.pattern_match.group(1).decode("UTF-8"))
    if npath == "File":
        await event.answer("Its a file dummy!", alert=True)
    else:
        path = PATH[0]
        npath = npath[2:-4]
        rpath = f"{path}/{npath}"
        num = 1
        msg, buttons = get_manager(rpath, num)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)

#REMOVE
@catub.tgbot.on(CallbackQuery(pattern="rem_(.*)"))
@check_owner
async def remove(event):
    fn, num = (event.pattern_match.group(1).decode("UTF-8")).split("|", 1)
    path = PATH[0]
    if fn == "File":
        paths = path.split("/")
        if paths[-1] == "":
            paths.pop()
            paths.pop()
        else:
            paths.pop()
        npath = ""
        for ii in paths:
            npath += f"{ii}/"
        rpath = path
    else:
        n_path = fn[2:-4]
        rpath = f"{path}/{n_path}"
        npath = path
    msg, buttons = get_manager(npath, num)
    await asyncio.sleep(1)
    await event.edit(msg, buttons=buttons)
    await _catutils.runcmd(f"rm -rf '{rpath}'")
    await event.answer(f"{rpath} removed successfully...")

#SEND
#using ub log grp cuz callbackuery event do not give chat id (in b)
@catub.tgbot.on(CallbackQuery(pattern="send"))
@check_owner
async def send(event):
    path = PATH[0]
    await catub.send_file(Config.PRIVATE_GROUP_BOT_API_ID, file=path, thumb=thumb_image_path if os.path.exists(thumb_image_path) else None)
    await event.answer(f"File {path} sent successfully...")        

#CUT
@catub.tgbot.on(CallbackQuery(pattern="cut_(.*)"))
@check_owner
async def cut(event):
    f, n = (event.pattern_match.group(1).decode("UTF-8")).split("|", 1)
    if CC:
        return await event.answer(f"Paste {CC[1]} first")
    else:
        if f == "File":
            npath = PATH[0]
            paths = npath.split("/")
            if paths[-1] == "":
                paths.pop()
                paths.pop()
            else:
                paths.pop()
            path = ""
            for ii in paths:
                path += f"{ii}/"
            CC.append("cut")
            CC.append(npath)
            await event.answer(f"Moving {npath} ...")
        else:
            path = PATH[0]
            npath = f[2:-4]
            rpath = f"{path}/{npath}"
            CC.append("cut")
            CC.append(rpath)
            await event.answer(f"Moving {rpath} ...")
        msg, buttons = get_manager(path, n)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)

#COPY
@catub.tgbot.on(CallbackQuery(pattern="copy_(.*)"))
@check_owner
async def copy(event):
    f, n = (event.pattern_match.group(1).decode("UTF-8")).split("|", 1)
    if CC:
        return await event.answer(f"Paste {CC[1]} first")
    else:
        if f == "File":
            npath = PATH[0]
            paths = npath.split("/")
            if paths[-1] == "":
                paths.pop()
                paths.pop()
            else:
                paths.pop()
            path = ""
            for ii in paths:
                path += f"{ii}/"
            CC.append("copy")
            CC.append(npath)
            await event.answer(f"Copying {path} ...")
        else:
            path = PATH[0]
            npath = f[2:-4]
            rpath = f"{path}/{npath}"
            CC.append("copy")
            CC.append(rpath)
            await event.answer(f"Copying {rpath} ...")
        msg, buttons = get_manager(path, n)
        await asyncio.sleep(1) 
        await event.edit(msg, buttons=buttons)

#PASTE
@catub.tgbot.on(CallbackQuery(pattern="paste_(.*)"))
@check_owner
async def paste(event):
    n = (event.pattern_match.group(1).decode("UTF-8"))
    path = PATH[0]
    if CC:
        if CC[0] == "cut":
            cmd = f"mv '{CC[1]}' '{path}'"
        else:
            cmd = f"cp '{CC[1]}' '{path}'"
        await _catutils.runcmd(cmd)
        msg, buttons = get_manager(path, n)
        await event.edit(msg, buttons=buttons)
        CC.clear
    else:
        await event.answer("You aint copied anything to paste")

@catub.tgbot.on(events.InlineQuery)
async def lsinline(event):

    if event.query.user_id == Config.OWNER_ID or event.query.user_id in Config.SUDO_USERS:
        try:
            ls, path_ = (event.text).split(" ", 1)
            path = Path(path_) if path_ else os.getcwd()
        except:
            ls = event.text
            path = os.getcwd()
        if "ls" in ls:
            print(ls)
            if not os.path.exists(path):
                return
            num = 1
            msg, buttons = get_manager(path, num)
            result = []
            result.append(await event.builder.article(
                title="Inline FM",
                description="Inline file manager",
                text=msg,
                buttons=buttons))
            await event.answer(result)
