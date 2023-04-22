'''
Intended to parse "decoded" files which would be present on a user's computer

How to use:
- import RioStatLib obviously
- open a Rio stat json file
- convert from json string to obj using json.loads(jsonStr)
- create StatObj with your stat json obj using the following:
	myStats = RioStatLib.StatObj(jsonObj)
- call any of the built-in methods to get some stats

- ex:
	import RioStatLib
	import json
	with open("path/to/RioStatFile.json", "r") as jsonStr:
		jsonObj = json.load(jsonStr)
		myStats = RioStatLib.StatObj(jsonObj)
		homeTeamOPS = myStats.ops(0)
		awayTeamSLG = myStats.slg(1)
		booERA = myStats.era(0, 4) # Boo in this example is the 4th character on the home team

Team args:
- arg == 0 means team0 which is the home team
- arg == 1 means team1 which is the away team
- arg == -1 or no arg provided means both teams (if function allows) (none currently accept this, but it might be added in the future)

Roster args:
- arg == 0 -> 8 for each of the 9 roster spots
- arg == -1 or no arg provided means all characters on that team (if function allows)

# teamNum: 0 == home team, 1 == away team
# rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
'''

"""note from Micah - not my script, credit to LittleCoaks & thanks for sharing it"""

# create stat obj
class StatObj:
    def __init__(this, statJson: dict):
        this.statJson = statJson


    def gameID(this):
        # returns it in int form
        return int(this.statJson["GameID"].replace(',', ''), 16)

    # should look to convert to unix or some other standard date fmt
    def date(this):
        return this.statJson["Date"]

    def isRanked(this):
        # tells if a game was a ranked game or not
        rankedStatus = this.statJson["Ranked"]
        return rankedStatus == 1

    def stadium(this):
        # returns the stadium that was played on
        return this.statJson["StadiumID"]

    def player(this, teamNum: int):
        # returns name of player
        # teamNum: 0 == home team, 1 == away team
        if teamNum == 0:
            return this.statJson["Home Player"]
        elif teamNum == 1:
            return this.statJson["Away Player"]
        else:
            this.__errorCheck_teamNum(teamNum)

    def score(this, teamNum: int):
        # returns final score of said team
        # teamNum: 0 == home team, 1 == away team
        if teamNum == 0:
            return this.statJson["Home Score"]
        elif teamNum == 1:
            return this.statJson["Away Score"]
        else:
            this.__errorCheck_teamNum(teamNum)

    def inningsTotal(this):
        # returns how many innings were selected for the game
        return this.statJson["Innings Selected"]

    def inningsPlayed(this):
        # returns how many innings were played in the game
        return this.statJson["Innings Played"]

    def isMercy(this):
        # returns if the game ended in a mercy or not
        if this.inningsTotal() - this.inningsPlayed() >= 1 and not this.wasQuit():
            return True
        else:
            return False

    def wasQuit(this):
        # returns if the same was quit out early
        if this.statJson["Quitter Team"] == "":
            return False
        else:
            return True

    def quitter(this):
        # returns the name of the quitter if the game was quit. empty string if no quitter
        return this.statJson["Quitter Team"]

    def ping(this):
        # returns average ping of the game
        return this.statJson["Average Ping"]

    def lagspikes(this):
        # returns number of lag spikes in a game
        return this.statJson["Lag Spikes"]

    def characterGameStats(this):
        # returns the full dict of character game stats as shown in the stat file
        return this.statJson["Character Game Stats"]

    def isSuperstarGame(this):
        # returns if the game has any superstar characters in it
        isStarred = False
        charStats = this.characterGameStats()
        for character in charStats:
            if charStats[character]["Superstar"] == 1:
                isStarred = True
        return isStarred

    # TODO: function that tells if no stars, stars, or mixed stars?

    # character stats
    # (this, teamNum: int, rosterNum: int):

    def characterName(this, teamNum: int, rosterNum: int = -1):
        # returns name of specified character
        # if no roster spot is provided, returns a list of characters on a given team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            charList = []
            for x in range(0, 9):
                charList.append(this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["CharID"])
            return charList
        else:
            return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["CharID"]


    def isStarred(this, teamNum: int, rosterNum: int = -1):
        # returns if a character is starred
        # if no arg, returns if any character on the team is starred
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            for x in range(0, 9):
                if this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Superstar"] == 1:
                    return True
        else:
            if this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Superstar"] == 1:
                return True
            else:
                return False


    def captain(this, teamNum: int):
        # returns name of character who is the captain
        # teamNum: 0 == home team, 1 == away team
        this.__errorCheck_teamNum(teamNum)
        captain = ""
        for character in this.characterGameStats():
            if character["Captain"] == 1 and int(character["Team"]) == teamNum:
                captain = character["CharID"]
        return captain


    def offensiveStats(this, teamNum: int, rosterNum: int = -1):
        # grabs offensive stats of a character as seen in the stat json
        # if no roster provided, returns a list of all character's offensive stats
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            oStatList = []
            for x in range(0, 9):
                oStatList.append(this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Offensive Stats"])
            return oStatList
        else:
            return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Offensive Stats"]


    def defensiveStats(this, teamNum: int, rosterNum: int = -1):
        # grabs defensive stats of a character as seen in the stat json
        # if no roster provided, returns a list of all character's defensive stats
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            dStatList = []
            for x in range(0, 9):
                dStatList.append(this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Defensive Stats"])
            return dStatList
        else:
            return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Defensive Stats"]


    def fieldingHand(this, teamNum: int, rosterNum: int):
        # returns fielding handedness of character
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum2(rosterNum)
        return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Fielding Hand"]


    def battingHand(this, teamNum: int, rosterNum: int):
        # returns batting handedness of character
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum2(rosterNum)
        return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Batting Hand"]


    # defensive stats
    def era(this, teamNum: int, rosterNum: int = -1):
        # tells the era of a character
        # if no character given, returns era of that team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        return 9 * float(this.runsAllowed(teamNum, rosterNum)) / this.inningPitched(teamNum, rosterNum)


    def battersFaced(this, teamNum: int, rosterNum: int = -1):
        # tells how many batters were faced by character
        # if no character given, returns batters faced by that team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Batters Faced"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Batters Faced"]


    def runsAllowed(this, teamNum: int, rosterNum: int = -1):
        # tells how many runs a character allowed when pitching
        # if no character given, returns runs allowed by that team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Runs Allowed"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Runs Allowed"]


    def battersWalked(this, teamNum: int, rosterNum: int = -1):
        # tells how many walks a character allowed when pitching
        # if no character given, returns walks by that team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        return this.battersWalkedBallFour(teamNum, rosterNum) + this.battersHitByPitch(teamNum, rosterNum)


    def battersWalkedBallFour(this, teamNum: int, rosterNum: int = -1):
        # returns how many times a character has walked a batter via 4 balls
        # if no character given, returns how many times the team walked via 4 balls
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Batters Walked"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Batters Walked"]


    def battersHitByPitch(this, teamNum: int, rosterNum: int = -1):
        # returns how many times a character walked a batter by hitting them by a pitch
        # if no character given, returns walked via HBP for the team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Batters Hit"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Batters Hit"]


    def hitsAllowed(this, teamNum: int, rosterNum: int = -1):
        # returns how many hits a character allowed as pitcher
        # if no character given, returns how many hits a team allowed
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Hits Allowed"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Hits Allowed"]


    def homerunsAllowed(this, teamNum: int, rosterNum: int = -1):
        # returns how many homeruns a character allowed as pitcher
        # if no character given, returns how many homeruns a team allowed
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["HRs Allowed"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["HRs Allowed"]


    def pitchesThrown(this, teamNum: int, rosterNum: int = -1):
        # returns how many pitches a character threw
        # if no character given, returns how many pitches a team threw
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Pitches Thrown"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Pitches Thrown"]


    def stamina(this, teamNum: int, rosterNum: int = -1):
        # returns final pitching stamina of a pitcher
        # if no character given, returns total stamina of a team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Stamina"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Stamina"]


    def wasPitcher(this, teamNum: int, rosterNum: int):
        # returns if a character was a pitcher
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_rosterNum2(rosterNum)
        if this.defensiveStats(teamNum, rosterNum)["Was Pitcher"] == 1:
            return True
        else:
            return False


    def strikeoutsPitched(this, teamNum: int, rosterNum: int = -1):
        # returns how many strikeouts a character pitched
        # if no character given, returns how mnany strikeouts a team pitched
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Strikeouts"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Strikeouts"]


    def starPitchesThrown(this, teamNum: int, rosterNum: int = -1):
        # returns how many star pitches a character threw
        # if no character given, returns how many star pitches a team threw
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Star Pitches Thrown"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Star Pitches Thrown"]


    def bigPlays(this, teamNum: int, rosterNum: int = -1):
        # returns how many big plays a character had
        # if no character given, returns how many big plays a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Big Plays"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Big Plays"]


    def outsPitched(this, teamNum: int, rosterNum: int = -1):
        # returns how many outs a character was pitching for
        # if no character given, returns how many outs a team pitched for
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Outs Pitched"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Outs Pitched"]


    def inningsPitched(this, teamNum: int, rosterNum: int = -1):
        # returns how many innings a character was pitching for
        # if no character given, returns how many innings a team pitched for
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        return float(this.outsPitched(teamNum, rosterNum)) / 3


    def pitchesPerPosition(this, teamNum: int, rosterNum: int):
        # returns a dict which tracks how many pitches a character was at a position for
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_rosterNum2(rosterNum)
        return this.defensiveStats(teamNum, rosterNum)["Pitches Per Position"][0]


    def outsPerPosition(this, teamNum: int, rosterNum: int):
        # returns a dict which tracks how many outs a character was at a position for
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: 0 -> 8 for each of the 9 roster spots
        this.__errorCheck_rosterNum2(rosterNum)
        return this.defensiveStats(teamNum, rosterNum)["Outs Per Position"][0]


    # offensive stats


    def atBats(this, teamNum: int, rosterNum: int = -1):
        # returns how many at bats a character had
        # if no character given, returns how many at bats a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["At Bats"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["At Bats"]


    def hits(this, teamNum: int, rosterNum: int = -1):
        # returns how many hits a character had
        # if no character given, returns how many hits a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Hits"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Hits"]


    def singles(this, teamNum: int, rosterNum: int = -1):
        # returns how many singles a character had
        # if no character given, returns how many singles a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Singles"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Singles"]


    def doubles(this, teamNum: int, rosterNum: int = -1):
        # returns how many doubles a character had
        # if no character given, returns how many doubles a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Doubles"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Doubles"]


    def triples(this, teamNum: int, rosterNum: int = -1):
        # returns how many triples a character had
        # if no character given, returns how many triples a teams had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Triples"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Triples"]


    def homeruns(this, teamNum: int, rosterNum: int = -1):
        # returns how many homeruns a character had
        # if no character given, returns how many homeruns a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Homeruns"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Homeruns"]


    def buntsLanded(this, teamNum: int, rosterNum: int = -1):
        # returns how many successful bunts a character had
        # if no character given, returns how many successful bunts a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Successful Bunts"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Successful Bunts"]


    def sacFlys(this, teamNum: int, rosterNum: int = -1):
        # returns how many sac flys a character had
        # if no character given, returns how many sac flys a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Sac Flys"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Sac Flys"]


    def strikeouts(this, teamNum: int, rosterNum: int = -1):
        # returns how many times a character struck out when batting
        # if no character given, returns how many times a team struck out when batting
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Strikeouts"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Strikeouts"]


    def walks(this, teamNum: int, rosterNum: int):
        # returns how many times a character was walked when batting
        # if no character given, returns how many times a team was walked when batting
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        return this.walksBallFour(teamNum, rosterNum) + this.walksHitByPitch(teamNum, rosterNum)


    def walksBallFour(this, teamNum: int, rosterNum: int = -1):
        # returns how many times a character was walked via 4 balls when batting
        # if no character given, returns how many times a team was walked via 4 balls when batting
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Walks (4 Balls)"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Walks (4 Balls)"]


    def walksHitByPitch(this, teamNum: int, rosterNum:int = -1):
        # returns how many times a character was walked via hit by pitch when batting
        # if no character given, returns how many times a team was walked via hit by pitch when batting
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Walks (Hit)"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Walks (Hit)"]


    def rbi(this, teamNum: int, rosterNum: int = -1):
        # returns how many RBI's a character had
        # if no character given, returns how many RBI's a team had
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["RBI"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["RBI"]


    def basesStolen(this, teamNum: int, rosterNum: int = -1):
        # returns how many times a character successfully stole a base
        # if no character given, returns how many times a team successfully stole a base
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Bases Stolen"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Bases Stolen"]


    def starHitsUsed(this, teamNum: int, rosterNum: int = -1):
        # returns how many star hits a character used
        # if no character given, returns how many star hits a team used
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Star Hits"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Star Hits"]




    # complicated stats


    def battingAvg(this, teamNum: int, rosterNum: int = -1):
        # returns the batting average of a character
        # if no character given, returns the batting average of a team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        nAtBats = this.atBats(teamNum, rosterNum)
        nHits = this.hits(teamNum, rosterNum)
        nWalks = this.walks(teamNum, rosterNum)
        return float(nHits) / float(nAtBats - nWalks)


    def obp(this, teamNum: int, rosterNum: int = -1):
        # returns the on base percentage of a character
        # if no character given, returns the on base percentage of a team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        nAtBats = this.atBats(teamNum, rosterNum)
        nHits = this.hits(teamNum, rosterNum)
        nWalks = this.walks(teamNum, rosterNum)
        return float(nHits + nWalks) / float(nAtBats)


    def slg(this, teamNum: int, rosterNum: int = -1):
        # returns the SLG of a character
        # if no character given, returns the SLG of a team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        nAtBats = this.atBats(teamNum, rosterNum)
        nSingles = this.singles(teamNum, rosterNum)
        nDoubles = this.doubles(teamNum, rosterNum)
        nTriples = this.triples(teamNum, rosterNum)
        nHomeruns = this.homeruns(teamNum, rosterNum)
        nWalks = this.walks(teamNum, rosterNum)
        return float(nSingles + nDoubles*2 + nTriples*3 + nHomeruns*4) / float(nAtBats - nWalks)


    def ops(this, teamNum: int, rosterNum: int = -1):
        # returns the OPS of a character
        # if no character given, returns the OPS of a team
        # teamNum: 0 == home team, 1 == away team
        # rosterNum: optional (no arg == all characters on team), 0 -> 8 for each of the 9 roster spots
        return this.obp(teamNum, rosterNum) + this.slg(teamNum, rosterNum)


    # event stats
    # these all probably involve looping through all the events
    def events(this):
        # returns the list of events in a game
        return this.statJson['Events']


    def eventFinal(this):
        # returns the number of the last event
        eventList = this.events()
        return eventList[-1]["Event Num"]


    def eventByNum(this, eventNum: int):
        # returns a single event specified by its number
        # if event is less than 0 or greater than the highest event, returns the last event
        eventList = this.events()
        finalEvent = this.eventFinal()
        if eventNum < 0 or eventNum > finalEvent:
            return finalEvent
        for event in eventList:
            if event["Event Num"] == eventNum:
                return event
        return {} # empty dict if no matching event found, which should be impossible anyway

    # TODO:
    # - add method for getting every stat from an event dict
    # - add methods that go through each event

    # manual exception handling stuff
    def __errorCheck_teamNum(this, teamNum: int):
        # tells if the teamNum is invalid
        if teamNum != 0 and teamNum != 1:
            raise Exception(f'Invalid team arg {teamNum}. Function only accepts team args of 0 (home team) or 1 (away team).')


    def __errorCheck_rosterNum(this, rosterNum: int):
        # tells if rosterNum is invalid. allows -1 arg
        if rosterNum < -1 or rosterNum > 8:
            raise Exception(f'Invalid roster arg {rosterNum}. Function only accepts roster args of from 0 to 8.')


    def __errorCheck_rosterNum2(this, rosterNum: int):
        # tells if rosterNum is invalid. does not allow -1 arg
        if rosterNum < 0 or rosterNum > 8:
            raise Exception(f'Invalid roster arg {rosterNum}. Function only accepts roster args of from 0 to 8.')
    

    '''
    {
      "Event Num": 0,
      "Inning": 1,
      "Half Inning": 0,
      "Away Score": 0,
      "Home Score": 0,
      "Balls": 0,
      "Strikes": 0,
      "Outs": 0,
      "Star Chance": 0,
      "Away Stars": 4,
      "Home Stars": 3,
      "Chemistry Links on Base": 0,
      "Pitcher Roster Loc": 2,
      "Batter Roster Loc": 0,
      "RBI": 0,
      "Result of AB": "Out",
      "Runner Batter": {
        "Runner Roster Loc": 0,
        "Runner Char Id": "Paragoomba",
        "Runner Initial Base": 0,
        "Out Type": "Tag",
        "Out Location": 0,
        "Steal": "None",
        "Runner Result Base": 255
      },
      "Pitch": {
        "Pitcher Team Id": 0,
        "Pitcher Char Id": "Mario",
        "Pitch Type": "Curve",
        "Charge Type": "N/A",
        "Star Pitch": 0,
        "Pitch Speed": 130,
        "DB": 1,
        "Pitch Result": "Contact",
        "Contact": {
          "Type of Swing": "Bunt",
          "Type of Contact": "Perfect",
          "Charge Power Up": 0,
          "Charge Power Down": 0,
          "Star Swing Five-Star": 0,
          "Input Direction": "None",
          "Frame Of Swing Upon Contact": 0,
          "Ball Angle": "571",
          "Ball Vertical Power": "27",
          "Ball Horizontal Power": "31",
          "Ball Velocity - X": 0.0991619,
          "Ball Velocity - Y": 0.00641787,
          "Ball Velocity - Z": 0.118957,
          "Ball Landing Position - X": 2.85452,
          "Ball Landing Position - Y": 0.185372,
          "Ball Landing Position - Z": 3.82766,
          "Ball Position Upon Contact - X": -2.3,
          "Ball Position Upon Contact - Z": -0.6,
          "Batter Position Upon Contact - X": 0,
          "Batter Position Upon Contact - Z": 0,
          "Multi-out": 0,
          "Contact Result - Primary": "Fair",
          "Contact Result - Secondary": "foul",
          "First Fielder": {
            "Fielder Roster Location": 4,
            "Fielder Position": "1B",
            "Fielder Character": "Koopa(G)",
            "Fielder Action": "Unable to Decode. Invalid Value (247).",
            "Fielder Swap": 188,
            "Fielder Position - X": 7.9392,
            "Fielder Position - Y": 9.73028,
            "Fielder Position - Z": -0,
            "Fielder Bobble": "None"
          }
        }
      }
    }
    '''
