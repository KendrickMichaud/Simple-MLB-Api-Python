# MLB-Python-Wrapper
Wrapper for MLB Data API

# How to use
To run, you need to install the latest version of Python (currently 3.9). It is recommended to use the Microsoft Store's download as it seems to cause the least trouble for Windows users.

To install, simply download the main.py file. Then open command prompt and call "python main.py". At that point the program will start and will show a menu.

Everything in the program is delimited by white spaces so keep that in mind.

Supported Commands (Data is outputted for csv but parameters for commands should always be separated by white space)

- Subquery: Filters player data by data types you want; 
  Usage: "subquery player_id college team_id"
- Query: Grabs player data related to the names as parameters;  
  Usage: "query cespedes"
- Datatypes: Shows all valid data types that you can look for; 
  Usage: "datatypes"
- Collect: Collects all player data for datatypes passed; 
  Usage: "collect player_id team_id college weight"
- Exit: Exits the program; 
  Usage: "exit"
