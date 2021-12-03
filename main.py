import urllib.request
import json

BASE = "search_player_all"
RESULT = "queryResults"
SIZE = "totalSize"
PLAYER_DATA = "row"
QUERY = 'query'
COLLECT = 'collect'
DATATYPES = 'datatypes'
SUBQUERY = 'squery'
EXIT = 'exit'

squery = "".split()

def endpoint(player):
    return urllib.request.urlopen("http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='" + player + "%25'").read()

def menu():
    
    print("Welcome, when querying and collecting, space each parameter after the command and it will process each sequentially")
    squery = []
    while True: 
        print("'squery' - filters a query by data type")
        print("'query' - Query Player (by Last Name)")
        print("'collect' - Collects a data type for all players (e.g. collect weight -> Cespedes,220)")
        print("'datatypes' - Prints all valid data types")
        print("'exit' - Exits from the program")
        print()
        user_input = input().split()
        command = user_input[0]
        work_load = len(user_input)
        if command == SUBQUERY:
            squery = user_input[1:]
            print(squery)
            
        elif command == QUERY:
            print("querying player...")
            for i in range(2):
                print()
            for i in range(1,work_load):
                query_player(user_input[i], squery)
            for i in range(2):
                print()
        elif command == DATATYPES:
            print("printing data types...")
            for i in range(2):
                print()
            datatype()
            for i in range(2):
                print()
        elif command == COLLECT:
            print("collecting data...")
            for i in range(2):
                print()
            collect(user_input[1:])
            for i in range(2):
                print()
        elif command == EXIT:
            print("program terminating...")
            for i in range(2):
                print()
            exit()
        else:
            for i in range(2):
                print()
            print("command not recognized, try again")

def collect(squery):
    # going to need to parse each letter, collect all players and place inside map
    alphabet = list(map(chr, range(97,123)))
    processed = {'foo': -1}
    for letter in alphabet:
        contents = endpoint(letter)
        
        base_data = json.loads(contents)[BASE][RESULT]
        player_count = int(base_data[SIZE])
        if(player_count == 0):
            print("Player Data Empty")
        elif(player_count == 1):
            out = "name"
            q = len(squery)
            if q > 0:
                for sq in squery:
                    out += "," + sq
            else:
                player_data = base_data["row"][0]
                keys = player_data.keys()
                for k in keys:
                    out += "," + k

            player_data = base_data["row"]
            keys = player_data.keys()
            out = player_data["name_display_last_first"]
            if out not in processed.keys():
                processed[out] = 1
            else:
                if q > 0:
                    for sq in squery:
                        if sq in keys:
                            out += "," + player_data[sq]
                else:
                    for k in keys:
                        out += "," + player_data[k]

                print(out)
        else:
            out = "name"
            q = len(squery)
            if q > 0:
                for sq in squery:
                    out += "," + sq
            else:
                player_data = base_data["row"][0]
                keys = player_data.keys()
                for k in keys:
                    out += "," + k

            print(out)
            for i in range(player_count):
                player_data = base_data["row"][i]
                keys = player_data.keys()
                
                out = player_data["name_display_last_first"]
                if out not in processed.keys():
                    processed[out] = 1
                else:
                    if q > 0:
                        for sq in squery:
                            if sq in keys:
                                out += "," + player_data[sq]
                    else:
                        for k in keys:
                            out += "," + player_data[k]

                    print(out)

    



def datatype():
    contents = endpoint("cespedes")

    base_data = json.loads(contents)[BASE][RESULT]
    player_count = int(base_data[SIZE])

    if(player_count == 0):
        print("Player Data Empty")

    for i in range(player_count):
        player_data = base_data["row"]
        keys = player_data.keys()

        for key in keys:
            print(key)

def query_player(player, squery):
    contents =  endpoint(player)

    base_data = json.loads(contents)[BASE][RESULT]
    player_count = int(base_data[SIZE])

    if(player_count == 0):
        print("Player Data Empty")
    elif(player_count == 1):
        out = "name"
        q = len(squery)
        if q > 0:
            for sq in squery:
                out += "," + sq
        else:
            player_data = base_data["row"][0]
            keys = player_data.keys()
            for k in keys:
                out += "," + k

        player_data = base_data["row"]
        keys = player_data.keys()
        out = player_data["name_display_last_first"]
        if q > 0:
            for sq in squery:
                if sq in keys:
                    out += "," + player_data[sq]
        else:
            for k in keys:
                out += "," + player_data[k]

        print(out)
    else:
        out = "name"
        q = len(squery)
        if q > 0:
            for sq in squery:
                out += "," + sq
        else:
            player_data = base_data["row"][0]
            keys = player_data.keys()
            for k in keys:
                out += "," + k


        print(out)
        for i in range(player_count):
            player_data = base_data["row"][i]
            keys = player_data.keys()
            
            out = player_data["name_display_last_first"]
            if q > 0:
                for sq in squery:
                    if sq in keys:
                        out += "," + player_data[sq]
            else:
                for k in keys:
                    out += "," + player_data[k]

            print(out)

def main():
    menu()





if __name__ == "__main__":
    main()