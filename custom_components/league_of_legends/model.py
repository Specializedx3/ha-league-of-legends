"""Convert match-v5 data to sensor values without Home Assistant dependencies."""
from datetime import datetime, timezone


def parse_match(match, puuid):
    info = match["info"]
    player = next(p for p in info["participants"] if p["puuid"] == puuid)
    kills, deaths, assists = (player[k] for k in ("kills", "deaths", "assists"))
    duration = info["gameDuration"]
    # Older match-v5 payloads used milliseconds and lack gameEndTimestamp.
    if "gameEndTimestamp" not in info:
        duration /= 1000
    end = info.get("gameEndTimestamp")
    if end is None:
        end = info.get("gameStartTimestamp", info["gameCreation"]) + duration * 1000
    return {
        "match_id": match["metadata"]["matchId"],
        "result": "win" if player["win"] else "loss",
        "champion": player["championName"],
        "kills": kills, "deaths": deaths, "assists": assists,
        "kda": round((kills + assists) / max(1, deaths), 2),
        "cs": player.get("totalMinionsKilled", 0) + player.get("neutralMinionsKilled", 0),
        "gold": player.get("goldEarned", 0),
        "damage": player.get("totalDamageDealtToChampions", 0),
        "vision_score": player.get("visionScore", 0),
        "duration": round(duration),
        "ended_at": datetime.fromtimestamp(end / 1000, tz=timezone.utc),
        "queue_id": info.get("queueId"),
        "game_mode": info.get("gameMode"),
        "position": player.get("teamPosition"),
    }
