from . import *

import contextlib
import os
import sys
import time
import asyncio
from .core.helper import time_formatter
from .load_plug import load
from telethon.errors import SessionRevokedError
from .utils import (
    join_dev,
    main_process,
)


jmubot.me.phone = None

if not jmubot.me.bot:
    jmdB.set_key("OWNER_ID", jmubot.me.id)
    jmdB.set_key("NAME", jmubot.full_name)

LOGS.info("جار تثبيت سورس KYnX ...")

try:
    LOGS.info("يتم أعداد الأعدادات")
    jmubot.loop.run_until_complete(main_process())
    LOGS.info("تم اعداد اعدادت سورس KYnX ✅")
except Exception as meo:
    LOGS.error(f"- {meo}")
    sys.exit()

jmubot.loop.create_task(join_dev())

async def load_plugins():
    load(path=["plugins/basic", "plugins/assistant", "plugins/account", "plugins/fun", "plugins/group"])

jmubot.run_in_loop(load_plugins())

LOGS.info(f"⏳ تم استغراق {time_formatter((time.time() - start_time) * 1000)} ميللي ثانية لبدء تشغيل سورس  آســaSaLـال .")

LOGS.info(
    """
    ╔══════════════════════════════════════════╗
    ║       ✅ تم تنصيب وتشغيل سورس KYnX  بنجاح             ║ 
    ║       تابع آخر التحديثات من خلال قناة @KYnX2            ║
    ╚══════════════════════════════════════════╝
    """
)

async def start_bots():
    while True:
        try:
            if asst:
                LOGS.info("🔄 محاولة تشغيل البوت المساعد...")
                await asst.start()
                LOGS.info(f"✅ تم تشغيل البوت المساعد: @{asst.me.username}")
            LOGS.info("🔄 محاولة تشغيل حساب KYnX...")
            await jmubot.start()
            await jmubot.run_until_disconnected()
        except SessionRevokedError:
            LOGS.warning("⚠️ فشل تشغيل البوت المساعد، سيتم تشغيل الحساب فقط")
            try:
                await jmubot.start()
                await jmubot.run_until_disconnected()
            except Exception as e:
                LOGS.error(f"❌ فشل تشغيل الحساب: {e}")
        except (ConnectionError, OSError) as net_err:
            LOGS.warning(f"📡 الاتصال فُقد: {net_err}")
            LOGS.info("⏳ سيتم إعادة المحاولة خلال 10 ثوانٍ...")
            await asyncio.sleep(10)
        except Exception as e:
            LOGS.error(f"🚨 خطأ غير متوقع: {e}")
            LOGS.info("🔁 سيتم إعادة المحاولة خلال 10 ثوانٍ...")
            await asyncio.sleep(10)

jmubot.loop.run_until_complete(start_bots())