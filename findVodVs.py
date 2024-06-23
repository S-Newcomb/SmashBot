import sys
from pytube import YouTube, Playlist

# Initial dictionary with primary characters, values are alternate names
smash_ultimate_chars = {
    "Mario": [],
    "Donkey Kong": ["DK"],
    "Link": [],
    "Samus": [],
    "Yoshi": [],
    "Kirby": [],
    "Fox": [],
    "Pikachu": [],
    "Luigi": [],
    "Ness": [],
    "Captain Falcon": [],
    "Jigglypuff": [],
    "Peach": ["Daisy"],
    "Bowser": [],
    "Ice Climbers": [],
    "Sheik": [],
    "Zelda": [],
    "Dr. Mario": [],
    "Pichu": [],
    "Falco": [],
    "Marth": [],
    "Lucina": [],
    "Young Link": [],
    "Ganondorf": [],
    "Mewtwo": [],
    "Roy": [],
    "Chrom": [],
    "Mr. Game and Watch": ["GnW", "Game and Watch"],
    "Meta Knight": ["MetaKnight", "Meta-Knight", "MK"],
    "Pit": [],
    "Zero Suit": [],
    "Wario": [],
    "Snake": [],
    "Ike": [],
    "Pokemon Trainer": ["PT"],
    "Diddy Kong": [],
    "Lucas": [],
    "Sonic": [],
    "King Dedede": ["D3"],
    "Olimar": ["Alph"],
    "Lucario": [],
    "Rob": ["ROB", "R.O.B."],
    "Toon Link": [],
    "Wolf": [],
    "Villager": [],
    "Mega Man": ["MegaMan", "Megaman"],
    "Wii Fit": [],
    "Rosalina and Luma": ["Rosalina"],
    "Little Mac": [],
    "Greninja": [],
    "Palutena": [],
    "Pac-Man": ["PacMan", "Pac"],
    "Robin": [],
    "Shulk": [],
    "Bowser Jr.": ["Bowser Jr", "Larry"],
    "Duck Hunt": [],
    "Ryu": [],
    "Ken": [],
    "Cloud": [],
    "Corrin": [],
    "Bayonetta": [],
    "Inkling": [],
    "Ridley": [],
    "Belmont": ["Simon", "Richter"],
    "King K. Rool": ["Krool"],
    "Isabelle": [],
    "Incineroar": [],
    "Piranha Plant": ["Plant"],
    "Joker": [],
    "Hero": ["hero"],
    "Banjo": [],
    "Terry": [],
    "Byleth": [],
    "Min Min": [],
    "Steve": [],
    "Sephiroth": [],
    "Aegis": ["Pyra/Mythra", "Pyra", "Mythra", "PyraMythra"],
    "Kazuya": [],
    "Sora": [],
    "Mii Brawler": ["Brawler"],
    "Mii Swordfighter": ["Swordfighter"],
    "Mii Gunner": ["Gunner"],
    "Uncategorized": []
}

def addVideo(charName, video, vodDict):
    found = False
    for primary, alts in smash_ultimate_chars.items():
        if charName == primary or charName in alts:
            vodDict[primary].append(video)
            found = True
            break

    if not found:
        vodDict["Uncategorized"].append(video)

#TODO: Add player vs player capability (i.e pull all vods vs DCA)
#Expects video title to contain Player1 (Char1) ... Player2 (char2)
def get_vods_vs_char(playlistURL, charName, playerName = ""):
    playlist = Playlist(playlistURL)
    eligibleVods = []

    for video in playlist.videos:
        title = video.title
        url = video.watch_url
        #print(title + " | " + url)


        #remove player name and char from str if player is specified
        valid = True
        if playerName != "":
            start = title.find(playerName)
            end = title.find(")", start)
            trim = title[:start] + title[end + 1:]
            title = trim
            if start == -1 or end == -1:
                valid = False
        
        #vod contains char
        if valid and title.find(charName) != -1:
            eligibleVods.append(video)
    
    for vod in eligibleVods:
        print(vod.title + " | " + vod.watch_url)
    
    return eligibleVods

def get_all_vods(playlistURL, playerName = ""):
    #dictionary containing [key:charName, value: list of videos]
    vodDict = {char: [] for char in smash_ultimate_chars.keys()}
    playlist = Playlist(playlistURL)

    for video in playlist.videos:
        title = video.title

        #remove player name and char from str if player is specified
        start = title.find(playerName)
        end = title.find(")", start)
        trim = title[:start] + title[end + 1:]
        title = trim

        charName = title[title.find("(") + 1 : title.find(")")]

        #Handle special case where multiple chars i.e AC (Joker/Snake) or (Joker, Snake)
        dualCharacter = charName.find("/")
        if dualCharacter == -1:
            dualCharacter = charName.find(",")
        if (dualCharacter != -1 and "Pyra" not in charName):
            char1 = charName[:dualCharacter].strip()
            char2 = charName[dualCharacter + 1:].strip()                
            addVideo(char1, video, vodDict)
            addVideo(char2, video, vodDict)

        else:
            addVideo(charName, video, vodDict)

    return vodDict

myVods =  "https://www.youtube.com/playlist?list=PL0idm2uMQWS99jtrqZZGeshQL1NlMMnb7"
topVods = "https://www.youtube.com/playlist?list=PL0idm2uMQWS9UTUs1us-1uo0dDgYFomZf"

def main():
    get_all_vods(myVods, "Pawp")

#main()