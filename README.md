# League of Legends for Home Assistant

Track the latest League of Legends match for multiple players in Home Assistant. View match results, champions, kills, deaths, assists, KDA, CS, gold, damage, vision score, and game duration. Stats update every five minutes.

## Install with HACS

You need HACS installed in Home Assistant and a Riot API key from the [Riot Developer Portal](https://developer.riotgames.com/).

1. Open **HACS** in Home Assistant.
2. Open the **three-dot menu → Custom repositories**.
3. Paste the URL of this GitHub repository, select **Integration**, and click **Add**.
4. Find **League of Legends** in HACS and download it.
5. Restart Home Assistant.

## Add a player

1. Go to **Settings → Devices & services → Add integration**.
2. Search for **League of Legends**.
3. Enter the player's Riot ID in two separate fields. For `Player#EUW`, enter `Player` as the **Game name** and `EUW` as the **Tagline**, without `#`.
4. Select the region and enter your **Riot API key**.
5. Complete the setup. The player's device and sensors appear under **Devices & services**.

| Region | Servers |
| --- | --- |
| `europe` | EUW, EUNE, TR, RU |
| `americas` | NA, BR, LAN, LAS |
| `asia` | KR, JP |
| `sea` | OCE and Southeast Asia |

To track more players, repeat **Add integration → League of Legends** for each player. Every player gets a separate device and sensors. You can use the same API key for multiple players; enter it for each player.

## Show stats on your dashboard

Open your dashboard, select **Edit dashboard → Add card → Entities**, and choose the sensors belonging to the player's device. Add a separate card for each player if desired.

## Renew your API key

Riot development API keys expire after 24 hours. If Home Assistant asks you to reauthenticate, generate a new key in the [Riot Developer Portal](https://developer.riotgames.com/) and enter it in the reauthentication dialog. If several players share that key, update every affected integration entry.

Stats can take a few minutes to appear after a match. Players without a match history show unknown values until a match is available.

---

League of Legends for Home Assistant is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
