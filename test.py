from youtubesearchpython import VideosSearch
import time

time_before = time.perf_counter()
gg = VideosSearch("PollmixaN - Мрак", 2)
print(gg.result()["result"][0])
print(f"Time: {time.perf_counter() - time_before}")
