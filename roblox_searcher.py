import requests
import sys

# =========================
#   ROBLOX SEARCHER
# =========================

BANNER = r"""
 ____        _               _
|  _ \ ___  | |__   _____  _| | _____  __
| |_) / _ \ | '_ \ / _ \ \/ / |/ / _ \/ /
|  _ <  __/ | |_) | (_) >  <|   <  __/ /
|_| \_\___| |_.__/ \___/_/\_\_|\_\___/_/
                 
        ROBLOX SEARCHER v1.0
"""

def get_user(username):
    url = "https://users.roblox.com/v1/usernames/users"

    data = {
        "usernames": [username],
        "excludeBannedUsers": False
    }

    response = requests.post(url, json=data, timeout=10)
    response.raise_for_status()

    users = response.json().get("data", [])

    if not users:
        return None

    return users[0]


def get_details(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


def main():
    print(BANNER)

    if len(sys.argv) < 2:
        username = input("Pseudo Roblox : ").strip()
    else:
        username = sys.argv[1]

    if not username:
        print("❌ Aucun pseudo indiqué.")
        return

    print(f"\n🔎 Recherche de : {username}...\n")

    try:
        user = get_user(username)

        if user is None:
            print("❌ Utilisateur introuvable.")
            return

        user_id = user["id"]
        details = get_details(user_id)

        print("════════════════════════════════")
        print("        INFORMATIONS PUBLIQUES")
        print("════════════════════════════════")

        print(f"👤 Username       : {user.get('name', 'N/A')}")
        print(f"🏷️ Display Name   : {user.get('displayName', 'N/A')}")
        print(f"🆔 User ID        : {user_id}")
        print(f"📅 Créé le        : {details.get('created', 'N/A')}")
        print(f"🚫 Banni          : {details.get('isBanned', 'N/A')}")

        print("\n🔗 Profil Roblox :")
        print(f"https://www.roblox.com/users/{user_id}/profile")

        print("\n════════════════════════════════")
        print("Recherche terminée ✅")
        print("════════════════════════════════")

    except requests.exceptions.RequestException as error:
        print(f"\n❌ Erreur réseau : {error}")

    except Exception as error:
        print(f"\n❌ Erreur : {error}")


if __name__ == "__main__":
    main()