import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lpl"
)

mycursor = mydb.cursor()


scorecade = json.load(open('Final/scorecard.json'))
mycursor.execute("SELECT Pname,Batting,Bowling,All_Rounder FROM player_ranking")
myresult1 = mycursor.fetchall()


# Get batting attack and bowling attack
def getBowlingAttack(team):
    bowlingAttack = 0
    count = 0
    for bowl in scorecade['Bowling']:
        if bowl['Team'] == team:
            for x in myresult1:
                if bowl['Name'] == x[0]:
                    bowlingAttack += x[2]
                    count += 1
    if (count > 0):
        return int(bowlingAttack / count)
    else:
        return 0


team1BawlingAttack = getBowlingAttack(scorecade['MatchInfo']['Team2'])
team2BawlingAttack = getBowlingAttack(scorecade['MatchInfo']['Team1'])


def getBowlingDefense(team):
    if team == scorecade['MatchInfo']['Team1']:
        return team1BawlingAttack
    else:
        return team2BawlingAttack


def getBattingAttack(team):
    battingAttack = 0
    count = 0
    for bat in scorecade['Batting']:
        if bat['Team'] == team:
            for x in myresult1:
                if bat['Name'] == x[0]:
                    battingAttack += x[1]
                    count += 1
    if (count > 0):
        return int(battingAttack / count)
    else:
        return 0


team1BattingAttack = getBattingAttack(scorecade['MatchInfo']['Team2'])
team2BattingAttack = getBattingAttack(scorecade['MatchInfo']['Team1'])



def getBattingDefense(team):
    if team == scorecade['MatchInfo']['Team1']:
        return team1BattingAttack
    else:
        return team2BattingAttack


# Database update names
for bat in scorecade['Batting']:
    isInDatabase = False
    for x in myresult1:
        if bat['Name'] == x[0]:
            isInDatabase = True

    if isInDatabase == False:
        name = bat['Name']
        batrate = 0
        batrate = 0
        alleate = 0
        sql = "INSERT INTO player_ranking (Pname,Batting,Bowling,All_Rounder) VALUES (%s,%s,%s,%s)"
        val = (name, batrate, batrate, alleate)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")

mycursor.execute("SELECT Pname,Batting,Bowling,All_Rounder FROM player_ranking")
myresult2 = mycursor.fetchall()

for bowl in scorecade['Bowling']:
    isInDatabase = False
    for x in myresult2:
        if bowl['Name'] == x[0]:
            isInDatabase = True

    if isInDatabase == False:
        name = bowl['Name']
        batrate = 0
        batrate = 0
        alleate = 0
        sql = "INSERT INTO player_ranking (Pname,Batting,Bowling,All_Rounder) VALUES (%s,%s,%s,%s)"
        val = (name, batrate, batrate, alleate)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")

# Batting update
mycursor.execute("SELECT Pname,Batting,Bowling,All_Rounder FROM player_ranking")
myresult3 = mycursor.fetchall()

for bat in scorecade['Batting']:
    name = bat['Name']
    teamTotal = bat['MatchInfo']['Total']
    winloss = bat['WinLoss']
    runs = bat['Runs']
    sr = bat['StrikeRate']
    outnotout = bat['outNotOut']
    bowlingAttack = getBowlingDefense(bat['Team'])

    print("Team 1 Bowling Attack: ", bowlingAttack)

    TodayRating = ((runs / teamTotal) * 500) + runs*2 + ((sr * runs) / 100) + (bowlingAttack * runs / 100)

    if outnotout:
        TodayRating = TodayRating + 10

    if winloss:
        TodayRating = TodayRating + 50

    if runs == 0:
        TodayRating = 0

    for x in myresult3:
        if bat['Name'] == x[0]:
            if x[1] == 0:
                NewRating = TodayRating
            else:
                # NewRating = x[1] + ((TodayRating / x[1]) - (x[1] / 1000)) * 5
                # NewRating = x[1] + ((TodayRating - x[1]) / ((TodayRating+x[1])/2)) * 100
                # NewRating = x[1] + (TodayRating - (x[1] / 2))

                if TodayRating > x[1]/2:
                    NewRating = x[1] + ((TodayRating - (x[1] / 2))/TodayRating)*100
                else:
                    NewRating = x[1] + ((TodayRating - (x[1] / 2))/x[1])*100

            if NewRating < 0:
                NewRating = 0

            if NewRating > 1000:
                NewRating = 1000

            # update table
            sql = "UPDATE player_ranking SET Batting = %s WHERE Pname = %s LIMIT 1"
            val = (NewRating, bat['Name'])

            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")

# Bowling update
mycursor.execute("SELECT Pname,Batting,Bowling,All_Rounder FROM player_ranking")
myresult4 = mycursor.fetchall()

for bowl in scorecade['Bowling']:
    name = bowl['Name']
    winloss = bowl['WinLoss']
    wickets = bowl['Wickets']
    TeamTotalWickets = bowl['MatchInfo']['Wickets']
    economy = bowl['EconomyRate']
    maidens = bowl['Maiden']
    battingngAttack = getBattingDefense(bowl['Team'])
    overs = bowl['Overs']

    print("Team 1 Batting Attack: ", battingngAttack)

    if (TeamTotalWickets == 0):
        TodayRating = ((battingngAttack * wickets / 20) + (maidens * 55) + (100 - (100 / 36) * economy))
    else:
        TodayRating = (wickets * 100) + (battingngAttack * wickets / 20) + (maidens * 20) + (
                100 - (100 / 36) * economy)

    if (TeamTotalWickets == 10):
        TodayRating = TodayRating + 20
    else:
        TodayRating = TodayRating + overs * 5

    if winloss:
        TodayRating = TodayRating + 50

    if overs == 0:
        TodayRating = 0

    for x in myresult4:
        if bowl['Name'] == x[0]:
            if x[2] == 0:
                NewRating = TodayRating
            else:
                # NewRating = x[2] + ((TodayRating / x[2]) - (x[2] / 1000)) * 5
                # NewRating = x[2] + (TodayRating-(x[2]/2))
                if TodayRating > x[2]/2:
                    NewRating = x[2] + ((TodayRating - (x[2] / 2))/TodayRating)*100
                else:
                    NewRating = x[2] + ((TodayRating - (x[2] / 2))/x[2])*100

            if NewRating < 0:
                NewRating = 0

            if NewRating > 1000:
                NewRating = 1000

            # update table
            sql = "UPDATE player_ranking SET Bowling = %s WHERE Pname = %s LIMIT 1"
            val = (NewRating, bowl['Name'])

            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")
