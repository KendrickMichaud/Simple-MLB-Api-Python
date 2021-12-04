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
output_file = ""

def endpoint(player):
    return urllib.request.urlopen("http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='" + player + "%25'").read()

def header(squery, base_data, f):
    out = "last,first"
    q = len(squery)
    if q > 0:
        for sq in squery:
            out += "," + sq
    else:
        player_data = base_data["row"][0]
        keys = player_data.keys()
        for k in keys:
            out += "," + k
    
    if f is not None:
        f.write(out + "\n")
    else:
        print(out)

def process_player(player, squery, f):
    q = len(squery)
    out = player["name_display_last_first"]

    if q > 0:
        for sq in squery:
            out += "," + player[sq]
    else:
        for k in player.keys():
            out += "," + player[k]
    
    if f is not None:
        f.write(out + "\n")
    else:
        print(out)
    



def menu():
    
    print("Welcome, when querying and collecting, space each parameter after the command and it will process each sequentially")
    squery = []
    output_file = ""
    while True: 
        print("'out' - sets output file for query/collect; leave blank for printout on console")
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
        elif command == 'out':
            print("setting output...")
            if work_load == 1:
                output_file = ""
            else:
                output_file = user_input[1]
            print(output_file)
        elif command == QUERY:
            print("querying player...")
            for i in range(2):
                print()
            for i in range(1,work_load):
                query_player(user_input[i], squery, output_file)
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
            collect(user_input[1:], output_file)
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


def collect(squery, output_file):
    # going to need to parse each letter, collect all players and place inside map
    alphabet = list(map(chr, range(97,123)))
    processed = {'foo': -1}
    x = len(output_file)
    if x > 0:
        f = open(output_file, "w", encoding="utf-8")
    else:
        f = None


    header(squery, json.loads(endpoint("cespedes"))[BASE][RESULT], f)

    for letter in alphabet:
        contents = endpoint(letter)
        
        base_data = json.loads(contents)[BASE][RESULT]
        player_count = int(base_data[SIZE])
        if(player_count == 0):
            continue
        elif(player_count == 1):
            player_data = base_data["row"]
            name = player_data["name_display_last_first"]
            if name not in processed.keys():
                processed[name] = 1
            else:
                process_player(player_data, squery, f)
        else:
            for i in range(player_count):
                player_data = base_data["row"][i]
                name = player_data["name_display_last_first"]
                if name not in processed.keys():
                    processed[name] = 1
                else:
                    process_player(player_data, squery, f)
    
    if f is not None:
        f.close()
    
    print("finished task")


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

def query_player(player, squery, output_file):
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

        if(output_file != ""):
            f = open(output_file, "w", encoding="utf-8")
            f.write(out + "\n")
        else:
            print(out)

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

        if(output_file != ""):
            f.write(out + "\n")
            f.close()
        else:
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

        if(output_file != ""):
            f = open(output_file, "w", encoding="utf-8")
            f.write(out + "\n")
        else:
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

            if(output_file != ""):
                f.write(out + "\n")
            else:
                print(out)

        if(output_file != ""):
            f.close()

def main():
    menu()

if __name__ == "__main__":
    main()