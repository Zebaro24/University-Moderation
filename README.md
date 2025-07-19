# University Moderation Bot 🤖

[![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
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
| <img src="https://github.com/user-attachments/assets/b5f0a6fc-ec2a-41df-8ca6-e4ccd87a353b" alt="Features" width="500" />     | <img src="https://github.com/user-attachments/assets/3bc0f30a-348b-4d1f-bd4e-5d3b2737972d" alt="Features" width="500" />         |
| <img src="https://github.com/user-attachments/assets/39285a2d-3e50-415a-9c56-5497d5452474" alt="Music Player" width="500" /> | <img src="https://github.com/user-attachments/assets/8a6910d3-a63a-45f5-85b4-d52f3c39f10b" alt="Schedule" width="500" />         |
| <img src="https://github.com/user-attachments/assets/adf8763a-23ef-4531-8c51-f75e1a2754ef" alt="Mafia Game" width="500" />   | <img src="https://github.com/user-attachments/assets/95ae7d71-6cb9-412b-9d81-d4ef86b562fb" alt="Morning greeting" width="500" /> |
| <img src="https://github.com/user-attachments/assets/300fe47e-3a98-4926-82ff-da91c5d2f9d0" alt="Roles" width="500" />        | <img src="https://github.com/user-attachments/assets/bdd0b02b-cd57-47e0-9e27-245b85b8e365" alt="Status" width="500" />           |

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
