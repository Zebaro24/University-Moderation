# University Moderation Bot 🤖

[![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-%233776AB?logo=python)](https://python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-1.7.3-%235865F2?logo=discord)](https://discordpy.readthedocs.io/)
[![Telegram Bot API](https://img.shields.io/badge/pyTelegramBotAPI-4.x-%2326A5E4?logo=telegram)](https://core.telegram.org/bots/api)

Unified moderation and utility platform for Discord and Telegram, featuring music, games, schedules, and community management.

---

## ✨ Core Features

### Cross-Platform
- 🔄 **Unified Configuration** - Single settings for both platforms
- 📝 **Centralized Logging** - Comprehensive event and error tracking
- 🗃️ **Database Integration** - PostgreSQL backend for persistent data
- 🔄 **Version Control** - Track changes and updates

### Discord-Specific
- 🎵 **Music Player** - Stream music via Lavalink
- 🎮 **Mafia Game** - Host mafia games on your server
- 👑 **Role Management** - Assign and moderate roles
- 📅 **Event Scheduling** - Create and notify about events
- 🔊 **Voice Channel Automation** - Dynamic voice channel creation
- 🌈 **RGB Decorations** - Customize server appearance
- 📊 **Activity Tracking** - Monitor user engagement

### Telegram-Specific
- 📅 **Schedule Integration** - Sync and manage events
- 🔄 **Discord Synchronization** - Cross-platform data sharing

---

## 🧰 Tech Stack

- **Core**: ![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)
- **Discord**: 
  ![discord.py](https://img.shields.io/badge/discord.py-1.7.3-5865F2?logo=discord)
  ![dislash.py](https://img.shields.io/badge/dislash.py-1.3.0-5865F2)
- **Telegram**: 
  ![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-4.0-26A5E4?logo=telegram)
- **Database**: 
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-4169E1?logo=postgresql)
  ![psycopg2](https://img.shields.io/badge/psycopg2-2.9.1-1C1C1C)
- **Music**: 
  ![Lavalink](https://img.shields.io/badge/Lavalink-3.4-1C1C1C?logo=java)
  ![wavelink](https://img.shields.io/badge/wavelink-1.3.0-1C1C1C)
- **APIs**: 
  ![Spotify](https://img.shields.io/badge/Spotify_Tekore-4.4.0-1DB954?logo=spotify)
  ![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-pyowm-1C1C1C?logo=openweathermap)
- **Web**: 
  ![FastAPI](https://img.shields.io/badge/FastAPI-0.78.0-009688?logo=fastapi)
  ![uvicorn](https://img.shields.io/badge/uvicorn-0.18.2-1C1C1C)
- **Utilities**: 
  ![scheduler](https://img.shields.io/badge/scheduler-1.1.0-1C1C1C)
  ![pytz](https://img.shields.io/badge/pytz-2022.1-1C1C1C)
  ![speedtest-cli](https://img.shields.io/badge/speedtest--cli-2.1.3-1C1C1C)
  ![xmltodict](https://img.shields.io/badge/xmltodict-0.13.0-1C1C1C)

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Java Runtime Environment (for Lavalink)

### Steps

1. **Clone repository**
   ```bash
   git clone https://github.com/Zebaro24/University-Moderation.git
   cd university-moderation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**  
   Copy `.env.example` to `.env` and fill in your details:
   ```env
   TELEGRAM_API=your_telegram_token
   DISCORD_API=your_discord_token
   DB_NAME=database_name
   DB_USER=database_user
   DB_PASSWORD=database_password
   DB_HOST=localhost
   DB_PORT=5432
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   OWM_API_KEY=your_openweathermap_key
   ```

5. **Set up Lavalink**
   - Configure `application.yml`
   - Start the server:
   ```bash
   java -jar Lavalink.jar
   ```

---

## 🚀 Launching the Bot

```bash
python worker.py
```

---

## 🗂️ Project Structure
```bash
discord_bot/          # Discord modules
├── mafia/            # Mafia game mechanics
├── music/            # Music player
├── roles/            # Role management
├── timetable/        # Schedule for Discord
telegram_bot/         # Telegram modules
├── timetable/        # Schedule for Telegram
tg_ds/                # Shared functions
timetable/            # Core schedule logic
.env                  # Environment variables
config.py             # Application configuration
database_func.py      # Database functions
main_bot_function.py  # Core bot functions
requirements.txt      # Dependencies
worker.py             # Main executable
```

---

## 🎮 Feature Highlights
| Discord Features                              | Telegram Features                                 |
|-----------------------------------------------|---------------------------------------------------|
| <img src="" alt="Features" width="500" />     | <img src="" alt="Features" width="500" />         |
| <img src="" alt="Music Player" width="500" /> | <img src="" alt="Schedule" width="500" />         |
| <img src="" alt="Mafia Game" width="500" />   | <img src="" alt="Morning greeting" width="500" /> |
| <img src="" alt="Roles" width="500" />        | <img src="" alt="Status" width="500" />           |


---

## 🛠️ API & Extensibility

### Database Functions
Use `database_func.py` for database operations:
```python
from database_func import add_event, get_events

# Add event
add_event(guild_id, "Meeting", "2023-12-31 20:00")

# Get events
events = get_events(guild_id)
```

### Adding Discord Commands
```python
from discord_bot.discord_command import register_command

@register_command(name="hello", description="Says hello")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")
```

---

## 📬 Contact
- **Developer**: Denys Shcherbatyi
- **Email**: zebaro.work@gmail.com