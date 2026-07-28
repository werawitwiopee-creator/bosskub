import discord
from discord.ext import commands, tasks
import subprocess
import os
import asyncio
import aiohttp
import io
import wave
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ===== SETTINGS =====
TOKEN = "MTUzMDc5MTY4MDEyOTYzNDM1NA.GKRTqj.BPR6ZuowKeaNydDH6g36suXuh979XmVZRfGgcY"

PREFIX = ">"
TEMP_DIR = "./temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

AUTO_LOGGER_CHANNEL_ID = 1531140438285615206  # channel to start logging automatically on boot

# ===== GLOBAL STATE & CONSTANTS (เพิ่มส่วนที่ขาดหายไป) =====
logger_channels = {}     # {channel_id: last_seen_asset_id}
tracked_artists = set()  # รายชื่อ artist ที่ต้องการดักจับ
sent_asset_ids = set()   # กันส่งเพลงซ้ำ
logged_songs = []        # ประวัติเพลงที่เจอ
caught_count = 0
bot_ready_init = False

# Roblox Endpoints & Headers
ROBLOX_API_URL = "https://apis.roblox.com/toolbox-service/v1/marketplace/30?limit=30"
ROBLOX_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ===== ROBLOX COOKIES =====
ROBLOX_COOKIES = {
    ".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoEEAQYASIbCgRkdWlkEhM0Njc2MTA4ODA2MTEyNjY0MDMzIhUKBXVuYW1lEgxDR0dHX1BSSk9PT08iEQoDdWlkEgoxNjk3MzkwNjk3KAM.VIx351nBfev6pyT9dpryLMzdY8CYRub-QKRvK58_KbwCuTQLubeTNTHQzXl46C1jC8Jyd67_24lh89HH5yGVEGhNWcfvMWrKwvu-HFkz6-KuQepHeAqvvkOy3x4ACufcnMc-fYZfNL4emFqKw5Ki1PBFh1ftGBO217RiLf-TNGhcSrqeiLH_pL-XyqMon-mBvU_mh7icgIQEbw3hgfmqxJaaXFAVDo47fp2QOP_417CGexsCsp_XqqApvcjsNTk7NNI25oBbExPxbqZ5wpD7_VY0oCaf2rRCtA0aQ4YOhB3Bc9swKmD2gMmJjinhYERDe0vRuXWfKQx4ZPEv3QSm9I81jRLbT3DnZ0m6un7FbPK6kRTeOqfXhQIHe0KaZOL1JGps_8MMqacSA3bpGmj6DQ9aYK6lpcy0up5-a24fAi6gXNKQLFWnO3mpdsz39y_m-Pu7c-XvH_yczeeM3RHKK38Kpd_4KoBOHRC0BHhtm-qb434oa99NOzTtk-C_Gs3yGNh18_2s2avOHbDMUyZ24M2WJY0dPNztYJQSC_Bd4GYMKRSPLD1ts3CLpB0IOFysgVPlD-s8oDK89AIbTuMQJqXdzwom3878mxtccTJ0SGdHTkfQoaZx0_x08JVFS5IMXSAJxHJ7-c9fyNseA5pctbmEZWLFd0XUku_EfMvzpzYK_1K7Uq7GSt38xLApFs8KAahoq5GJdGIrHXg5dSUhj0godh7cufTHI1zAdtStAlYU9YiTp4UnuFyu80_N75tB25M4ptCCcWyhaw1yWSAFWm6uLrSoJg6g_YCjtwFiaVVEe4YvvziwJV-SA0O9o1uQOkzlrxAllTff3U33KEpqKviDM7Va-G15Ff2QzcAbXVMACopKVNysQQdm3GjcoxpY3pf2sNbh1Fa_p3k-HBmVh4p_1RU8RUfyndgyHWwXx-M.8VVhhl78q4OvgTLLQcvAhVBnYxY"
}

# ===== HELPERS =====

async def fetch_asset_thumbnail(asset_id: int) -> str:
    url = f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&size=420x420&format=Png&isCircular=false"
    try:
        async with aiohttp.ClientSession(cookies=ROBLOX_COOKIES) as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return ""
                data  = await resp.json()
                items = data.get("data", [])
                if items:
                    return items[0].get("imageUrl", "")
    except Exception:
        pass
    return ""


async def fetch_latest_audios() -> list[dict]:
    try:
        async with aiohttp.ClientSession(cookies=ROBLOX_COOKIES) as session:
            async with session.get(
                ROBLOX_API_URL,
                headers=ROBLOX_HEADERS,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                return data.get("data", [])
    except Exception:
        return []


async def fetch_audio_details(asset_ids: list[int]) -> dict:
    if not asset_ids:
        return {}
    ids_param = ",".join(str(i) for i in asset_ids)
    url = f"https://apis.roblox.com/toolbox-service/v1/items/details?assetIds={ids_param}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=ROBLOX_HEADERS,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status != 200:
                    return {}
                data   = await resp.json()
                result = {}
                for entry in data.get("data", []):
                    asset = entry.get("asset", {})
                    aid   = asset.get("id")
                    if not aid:
                        continue
                    audio   = asset.get("audioDetails") or {}
                    creator = entry.get("artist") or {}
                    result[aid] = {
                        "name":     asset.get("name", "Unknown"),
                        "creator":  creator.get("name", "Unknown"),
                        "genre":    audio.get("musicGenre") or audio.get("genre") or "All",
                        "duration": audio.get("duration", 0),
                        "artist":   audio.get("artist", ""),
                    }
                return result
    except Exception:
        return {}


async def download_roblox_ogg(asset_id: int, out_path: str) -> bool:
    url = f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=ROBLOX_HEADERS,
                timeout=aiohttp.ClientTimeout(total=20),
                allow_redirects=True
            ) as resp:
                if resp.status != 200:
                    return False
                content = await resp.read()
                with open(out_path, "wb") as f:
                    f.write(content)
                return True
    except Exception:
        return False


async def convert_to_ogg(input_path: str, output_path: str) -> bool:
    loop   = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-codec:a", "libvorbis", "-q:a", "5", output_path],
        capture_output=True
    ))
    return result.returncode == 0


async def get_peak_db(path: str) -> str:
    try:
        loop   = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: subprocess.run(
            ["ffmpeg", "-i", path, "-filter:a", "volumedetect", "-f", "null", "/dev/null"],
            capture_output=True, text=True
        ))
        for line in result.stderr.splitlines():
            if "max_volume" in line:
                return line.split("max_volume:")[-1].strip()
    except Exception:
        pass
    return "N/A"


async def get_loudness_peak(path: str) -> tuple[str, str]:
    """Returns (integrated_loudness_LUFS, true_peak_dBFS) using ffmpeg loudnorm."""
    try:
        loop   = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: subprocess.run(
            ["ffmpeg", "-i", path, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
            capture_output=True, text=True
        ))
        stderr = result.stderr
        json_start = stderr.rfind("{")
        json_end   = stderr.rfind("}")
        if json_start != -1 and json_end != -1:
            import json as _json
            data = _json.loads(stderr[json_start:json_end + 1])
            lufs = data.get("input_i", "N/A")
            peak = data.get("input_tp", "N/A")
            lufs_str = f"{float(lufs):.2f} LUFS" if lufs not in (None, "N/A") else "N/A"
            peak_str = f"{float(peak):.2f} dBFS" if peak not in (None, "N/A") else "N/A"
            return lufs_str, peak_str
    except Exception:
        pass
    return "N/A", "N/A"


async def get_audio_format(path: str) -> tuple[str, str]:
    """Returns (codec_name_upper, sample_rate_label) e.g. ('VORBIS', '48kHz')."""
    try:
        loop   = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=codec_name,sample_rate",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True
        ))
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        codec = lines[0].upper() if len(lines) > 0 else "OGG"
        rate  = f"{int(lines[1]) // 1000}kHz" if len(lines) > 1 else "N/A"
        return codec, rate
    except Exception:
        return "OGG", "N/A"


async def get_file_duration(path: str) -> float:
    """Returns duration in seconds read directly from the downloaded file via ffprobe."""
    try:
        loop   = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True
        ))
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def _build_waveform_png(wav_path: str) -> io.BytesIO | None:
    """CPU-heavy part (numpy + matplotlib). Meant to run inside an executor."""
    with wave.open(wav_path, "rb") as wf:
        n_ch  = wf.getnchannels()
        raw   = wf.readframes(wf.getnframes())
        all_s = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

    if len(all_s) == 0:
        return None

    left  = all_s[0::2] if n_ch >= 2 else all_s
    right = all_s[1::2] if n_ch >= 2 else all_s

    def prep(ch):
        step  = max(1, len(ch) // 3000)
        ch    = ch[::step]
        chunk = max(1, len(ch) // 300)
        env   = np.array([np.sqrt(np.mean(ch[i:i+chunk]**2))
                           for i in range(0, len(ch), chunk)])
        return ch, env, np.linspace(0, len(ch), len(env))

    l_s, l_env, l_ex = prep(left)
    r_s, r_env, r_ex = prep(right)

    WAVE_COLOR, BG_COLOR = "#FFFFFF", "none"
    fig, (ax_l, ax_r) = plt.subplots(2, 1, figsize=(9, 4.2), dpi=110,
                                      gridspec_kw={"hspace": 0.06})
    fig.patch.set_facecolor(BG_COLOR)
    fig.patch.set_alpha(0)
    for ax, samples, env, env_x in [(ax_l, l_s, l_env, l_ex), (ax_r, r_s, r_env, r_ex)]:
        ax.set_facecolor(BG_COLOR)
        ax.fill_between(env_x, env, -env, color=WAVE_COLOR, alpha=0.18, linewidth=0)
        ax.plot(np.arange(len(samples)), samples,
                color=WAVE_COLOR, linewidth=0.55, alpha=0.85, solid_capstyle="round")
        ax.axhline(0, color=WAVE_COLOR, linewidth=0.4, alpha=0.3)
        threshold = np.percentile(np.abs(samples), 99.7)
        peaks = np.where(np.abs(samples) >= threshold)[0]
        if len(peaks):
            ax.scatter(peaks, samples[peaks], color=WAVE_COLOR, s=1.2, alpha=0.6, linewidths=0)
        ax.set_xlim(0, len(samples))
        ax.set_ylim(-1.05, 1.05)
        ax.axis("off")

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=110,
                bbox_inches="tight", pad_inches=0, facecolor=BG_COLOR)
    plt.close(fig)
    buf.seek(0)
    return buf


async def generate_waveform(ogg_path: str) -> discord.File | None:
    wav_path = ogg_path + "_wv.wav"
    loop = asyncio.get_event_loop()
    try:
        r = await loop.run_in_executor(None, lambda: subprocess.run(
            ["ffmpeg", "-y", "-i", ogg_path, "-ar", "22050", "-ac", "2", wav_path],
            capture_output=True
        ))
        if r.returncode != 0 or not os.path.exists(wav_path):
            return None

        buf = await loop.run_in_executor(None, _build_waveform_png, wav_path)
        if buf is None:
            return None
        return discord.File(buf, filename="waveform.png")
    except Exception:
        return None
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)


async def _send_audio(channel, asset_id, name, display_name, genre, duration_s, asset_url):
    notify_msg = await channel.send("# 🔎 พบเพลงใหม่กำลังโหลดครับลูกพี่")

    ogg_filename  = f"{asset_id}.ogg"
    raw_path      = os.path.join(TEMP_DIR, f"rbx_{asset_id}_raw")
    ogg_path      = os.path.join(TEMP_DIR, ogg_filename)
    file_size_str = "0.00 MB"
    peak_db       = "-0.0 dB"
    ogg_file      = None

    try:
        if await download_roblox_ogg(asset_id, raw_path):
            if await convert_to_ogg(raw_path, ogg_path) and os.path.exists(ogg_path):
                size_bytes    = os.path.getsize(ogg_path)
                file_size_str = f"{size_bytes / (1024*1024):.2f} MB"
                peak_db       = await get_peak_db(ogg_path)
                if size_bytes <= 25 * 1024 * 1024:
                    ogg_file = discord.File(ogg_path, filename=ogg_filename)
    except Exception:
        pass

    waveform_file = await generate_waveform(ogg_path) if os.path.exists(ogg_path) else None
    thumb_url     = await fetch_asset_thumbnail(asset_id)

    # Loudness / true peak / format, matching the reference layout
    loudness_str, peak_str = "N/A", "N/A"
    codec, sample_rate     = "OGG", "N/A"
    if os.path.exists(ogg_path):
        loudness_str, peak_str = await get_loudness_peak(ogg_path)
        codec, sample_rate     = await get_audio_format(ogg_path)
        file_duration           = await get_file_duration(ogg_path)
        if file_duration > 0:
            duration_s = file_duration

    mins, secs   = divmod(int(duration_s or 0), 60)
    duration_fmt = f"{mins:02d}:{secs:02d}"

    embed = discord.Embed(
        title="<:emoji_1:1531714251947774034> Audio Discovered",
        description=f"**{name}** by {display_name}",
        color=discord.Color.from_rgb(255, 255, 255),
    )
    embed.add_field(name="Audio ID",  value=f"{asset_id}",      inline=False)
    embed.add_field(name="Duration",  value=duration_fmt,        inline=False)
    embed.add_field(name="Genre",     value=genre,               inline=False)
    embed.add_field(name="Type",      value="Distrokid",         inline=False)
    embed.add_field(name="Format",    value=f"{codec} {sample_rate}", inline=False)
    embed.add_field(name="Size",      value=file_size_str,       inline=False)
    embed.add_field(name="Loudness",  value=loudness_str,        inline=False)
    embed.add_field(name="Peak",      value=peak_str,            inline=False)
    embed.add_field(name="Links",     value=f"[View on Roblox]({asset_url})", inline=False)

    if thumb_url:
        embed.set_thumbnail(url=thumb_url)
    if waveform_file:
        embed.set_image(url="attachment://waveform.png")
    embed.set_footer(
        text="@191",
        icon_url="https://cdn.discordapp.com/emojis/1531714969362497797.png"
    )

    try:
        await notify_msg.delete()
        files = [f for f in [ogg_file, waveform_file] if f]
        if files:
            await channel.send(files=files, embed=embed)
        else:
            await channel.send(embed=embed)
    except Exception:
        pass
    finally:
        for p in [raw_path, ogg_path]:
            if os.path.exists(p):
                os.remove(p)


# ===== POLL LOOP =====

@tasks.loop(seconds=30)
async def roblox_audio_poll():
    global caught_count, sent_asset_ids
    if not logger_channels:
        return
    try:
        audios = await fetch_latest_audios()
        if not audios:
            return

        for channel_id, last_seen_id in list(logger_channels.items()):
            channel = bot.get_channel(channel_id)
            if channel is None:
                del logger_channels[channel_id]
                continue

            # กรองเฉพาะเพลงที่ id ใหม่กว่า last_seen_id และยังไม่เคยส่ง
            new_items = [
                a for a in audios
                if int(a.get("id", 0)) > last_seen_id
                and int(a.get("id", 0)) not in sent_asset_ids
            ]
            if not new_items:
                continue

            # อัปเดต last_seen_id ไปที่ id สูงสุดที่เจอในรอบนี้
            logger_channels[channel_id] = max(int(a.get("id", 0)) for a in new_items)

            ids         = [int(a.get("id", 0)) for a in new_items]
            details_map = await fetch_audio_details(ids)

            for item in reversed(new_items):  # reversed = เรียงเก่าสุดไปใหม่สุด
                asset_id = int(item.get("id", 0))

                # double-check ซ้ำอีกครั้ง (กรณี race condition)
                if asset_id in sent_asset_ids:
                    print(f"[⏭ SKIP DUP] ID: {asset_id}")
                    continue

                detail       = details_map.get(asset_id, {})
                name         = detail.get("name", "Unknown")
                creator      = detail.get("creator", "Unknown")
                artist       = detail.get("artist", "")
                genre        = detail.get("genre", "All")
                duration_s   = detail.get("duration", 0)
                display_name = artist if artist else creator
                asset_url    = f"https://www.roblox.com/library/{asset_id}"

                if tracked_artists and display_name.lower() not in tracked_artists:
                    continue

                # บันทึกว่าส่งแล้ว — ทำก่อน _send_audio เพื่อกัน race condition
                sent_asset_ids.add(asset_id)

                # จำกัดขนาด set ไม่ให้บวม (เก็บแค่ 2000 id ล่าสุด)
                if len(sent_asset_ids) > 2000:
                    oldest = sorted(sent_asset_ids)[:500]
                    for oid in oldest:
                        sent_asset_ids.discard(oid)

                logged_songs.append({
                    "id": asset_id, "name": name,
                    "creator": display_name, "duration": duration_s,
                    "genre": genre, "url": asset_url,
                })

                caught_count += 1
                print(f"[⚡ CAUGHT] {caught_count} -> {name} by {display_name} (ID: {asset_id})")

                await _send_audio(channel, asset_id, name, display_name, genre, duration_s, asset_url)
                await asyncio.sleep(0.2)
    except Exception as e:
        print(f"Polling error: {e}")


# ===== AUTO-START ON BOOT =====

@bot.event
async def on_ready():
    global bot_ready_init
    print(f"✅ Bot ready as {bot.user}")
    
    # ป้องกันการทำงานซ้ำเมื่อ on_ready ถูกเรียกหลายครั้ง
    if bot_ready_init:
        print("ℹ️  on_ready เรียกแล้ว ข้ามการตั้งค่า auto-logger")
        return
    
    bot_ready_init = True
    
    # เตรียม auto-logger
    try:
        channel = bot.get_channel(AUTO_LOGGER_CHANNEL_ID)
        if channel is None:
            print(f"⚠️  ไม่พบ channel {AUTO_LOGGER_CHANNEL_ID} ข้ามการเปิด auto-logger")
            return
        
        print(f"🔍 กำลังดึงข้อมูล Roblox audio...")
        audios = await fetch_latest_audios()
        
        if not audios:
            print(f"⚠️  ดึงข้อมูล Roblox ไม่ได้")
            return
        
        newest_id = max(int(a.get("id", 0)) for a in audios)
        logger_channels[AUTO_LOGGER_CHANNEL_ID] = newest_id
        print(f"✅ เปิด Auto-Logger ใน channel {AUTO_LOGGER_CHANNEL_ID}")
        print(f"   → ดักเพลงใหม่ที่ ID: {newest_id} ขึ้นไป")
        
        # เริ่ม polling loop
        if not roblox_audio_poll.is_running():
            roblox_audio_poll.start()
            print("✅ เริ่ม Polling Loop (ตรวจทุก 30 วินาที)")
        
        # ส่ง notification ไป channel
        await channel.send(embed=discord.Embed(
            title="✅ Auto-Logger เปิดแล้ว",
            description=f"Bot กำลังดักเพลงใหม่จาก Roblox Audio Library\n\n"
                       f"📊 ตรวจสอบทุก 30 วินาที\n"
                       f"🔍 ดักจาก ID: `{newest_id}`",
            color=discord.Color.green()
        ))
        
    except Exception as e:
        print(f"❌ on_ready error: {e}")
        import traceback
        traceback.print_exc()


# ===== COMMANDS =====

@bot.command(name="logger")
async def start_logger(ctx):
    channel_id = ctx.channel.id
    if channel_id in logger_channels:
        await ctx.send(".")
        return

    wait_msg = await ctx.send(".")

    audios = await fetch_latest_audios()
    if not audios:
        return

    newest_id = max(int(a.get("id", 0)) for a in audios)
    logger_channels[channel_id] = newest_id  # Start tracking only new audio from now on

    if not roblox_audio_poll.is_running():
        roblox_audio_poll.start()

    # Preview only the single latest song at the moment the command was run
    preview_items = [a for a in audios if int(a.get("id", 0)) == newest_id][:1]
    preview_ids   = [int(a.get("id", 0)) for a in preview_items]
    details_map   = await fetch_audio_details(preview_ids)

    for item in preview_items:
        asset_id     = int(item.get("id", 0))
        detail       = details_map.get(asset_id, {})
        name         = detail.get("name", "Unknown")
        creator      = detail.get("creator", "Unknown")
        artist       = detail.get("artist", "")
        genre        = detail.get("genre", "All")
        duration_s   = detail.get("duration", 0)
        display_name = artist if artist else creator
        asset_url    = f"https://www.roblox.com/library/{asset_id}"

        # บันทึกว่า preview เพลงนี้ส่งไปแล้ว → poll loop จะไม่ส่งซ้ำ
        sent_asset_ids.add(asset_id)

        await _send_audio(ctx.channel, asset_id, name, display_name, genre, duration_s, asset_url)
        await asyncio.sleep(0.5)

    # หลัง preview เสร็จ — อัปเดต last_seen_id ให้ตรงกับ newest_id
    logger_channels[channel_id] = newest_id


@bot.command(name="unlogger")
async def stop_logger(ctx):
    channel_id = ctx.channel.id
    if channel_id not in logger_channels:
        await ctx.send(".")
        return
    del logger_channels[channel_id]
    if not logger_channels and roblox_audio_poll.is_running():
        roblox_audio_poll.stop()
    await ctx.send(".")


@bot.command(name="artist")
async def add_artist(ctx, *, name: str = None):
    if name is None:
        if tracked_artists:
            await ctx.send(embed=discord.Embed(
                title="🎤 Artist ที่กำลังดักอยู่",
                description="\n".join(f"• `{a}`" for a in sorted(tracked_artists)),
                color=discord.Color.blurple()
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title="🎤 ยังไม่ได้ set artist ครับ",
                description=f"ใช้ `{PREFIX}artist <ชื่อ>` เพื่อเพิ่ม\nถ้าไม่ set จะดักทุกเพลงจาก DistroKid",
                color=discord.Color.blurple()
            ))
        return
    tracked_artists.add(name.lower())
    await ctx.send(embed=discord.Embed(
        title="✅ เพิ่ม Artist แล้วครับ",
        description=f"จะดักเพลงของ `{name}` ด้วยครับ",
        color=discord.Color.green()
    ))


@bot.command(name="removeartist")
async def remove_artist(ctx, *, name: str = None):
    if name is None:
        await ctx.send(embed=discord.Embed(
            title="❌ ใส่ชื่อ artist ด้วยครับ",
            description=f"ใช้ `{PREFIX}removeartist <ชื่อ>`",
            color=discord.Color.red()
        ))
        return
    if name.lower() in tracked_artists:
        tracked_artists.discard(name.lower())
        await ctx.send(embed=discord.Embed(
            title="🗑️ เอา Artist ออกแล้วครับ",
            description=f"ไม่ดักเพลงของ `{name}` แล้วครับ",
            color=discord.Color.orange()
        ))
    else:
        await ctx.send(embed=discord.Embed(
            title="⚠️ ไม่พบ Artist นี้ในลิสต์ครับ",
            description=f"`{name}` ไม่ได้อยู่ในลิสต์",
            color=discord.Color.orange()
        ))


bot.run(TOKEN)
