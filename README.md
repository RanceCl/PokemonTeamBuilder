# PokemonTeamBuilder
The program is a program to allow a user to create and customize a team of 6 Pokemon. For each, the user can specify the specie, the moves it will know, the item it will be holding, and the nature it will have.

The program reads in the Excel Document "Pokemon Data.xlsx". This document holds the data for every single Pokemon, ability, move, nature, and item available in any game up to generation 9, stored on separate sheets. The first sheet holds every Pokemon species available to pick from, listing their type(s), stats, and potential abilites; each Pokemon also has a "Form" variable, which indicates if the Pokemon is a transformation and what induces it. The second sheet lists and describes every ability that exists in the Pokemon database. The third sheet holds the data for every move that exists for Pokemon, including their power, their category (whether it is physical, special, or a status move), its accuracy, its power points, as well as a description of the attack. The fourth sheet holds every nature available to a Pokemon as well as what stats it will effect; a Pokemon's nature will increase one of its stat values and decrease another. The fifth sheet holds a list of every item available for a Pokemon to hold. 

## Data Manager
PokemonDataManager was the file that would handle the majority of the data manipulation and storing for the project. 

### Database
The entire database would be read into a class for each of them, with each class having methods to filter the data based on the criteria available to it. For items, the only filter option was by name. The most in depth of these were for the moves and the Pokemon Species. Moves, along with their name, could be filtered by their type and their category. Pokemon species could be filtered by their name, one of their types, and if they had a specified ability. The class for the Pokemon data also allowed the user to sort the data based on stat values. Each class includes a method to return the stats of a requested name for them. 

### Pokemon Instance
In PokemonDataManager is the class for individual Pokemon. Each instance holds the Pokemon's specie, its stats, its ability, its nature, and its moveset. A Pokemon has a name, up to two types, up to four moves, a single ability out of a few available to that specie, and a nature. 

Upon initialization, the name of the Pokemon would be called by the database to determine if it indeed exists in the database. If it doesn't, nothing happens and the Pokemon is left empty, though can still be manipulated. 

The option to change a Pokemon's specie will change their name, their stats, their typings, and their available abilities to match that of the requested Pokemon specie. If the specie picked is in a form that requires a specific item or move to maintain that form, then they will automatically be added to the Pokemon instance. No changes to the Pokemon's item, nature, or moves will be performed unless they are incompatible with the Pokemon's form. 

The call to change the Pokemon's move takes in the name of the requested move as well as the position that the user wishes to place it. If the move is in the database and the requested position is viable, then the move will be inserted into that position. 

The request to change the ability would only take in an index value, indicating which ability out of those avilable to the Pokemon would be chosen. If the index value exceeded the list of available abilities, then the first ability will be chosen. 

The option to change the nature of the Pokemon not only changes the name of the nature, but also performs the necessary stat calculations during the process, displaying the altered stats instead of the base stats in the database. 

The option to change the item is the most straightforward, taking in the requested name and storing the name if it exists in the database. 

When changing the species and changing the item/move of a Pokemon, the program will check to make sure that changing this will not change the form of the Pokemon. If an item or move is necessary for the Pokemon to be in its current form and it has been changed, then the Pokemon will be changed to its base form. 

### Pokemon Team
In PokemonDataManager is the class for the Pokemon team as a whole. The class allows the user to add and remove Pokemon from the team as well as change the specie of a Pokemon at a given position. 

Adding a Pokemon would append the requested Pokemon specie to the end of the team; the amount of Pokemon in the team can't exceed six, however, and the call will add another Pokemon if doing so would result in a team that exceeded this limit. The call to change the Pokemon specie would take in the new specie and the position of the Pokemon to be changed; nothing will occur if the position is out of bounds. The call to remove a Pokemon from the team will delete the whatever Pokemon is at the position requested; nothing will occur if the position is out of bounds. 

Due to the possibility of repeated species and that Pokemon instances were already stored in their own class, storing the whole team solely in a dataframe and performing a majority of the manipulations on this dataframe was deemed as impractical. Rather, the team was stored in a list of Pokemon instances, with a dataframe of the basic information of the team being updated after every manipulation to be stored to visualize the data for a user. 

## Team Builder GUI
A user interface was constructed for the purpose of allowing a user to create a Pokemon team with ease. 

The main team window would display the current Pokemon team the user has constructed, including the Pokemon's stats, moves, nature, item, and ability. On this window, the user may either add another Pokemon or choose a Pokemon in their team to alter. 

The options to add and change the Pokemon function similarly, giving the user a list of Pokemon to pick from. The user may then filter the list of Pokemon by their types, abilities, or by their name. They may then pick the Pokemon they wish to include in the team. The option to change the Pokemon's move gives the user a list of moves to choose form, which they may filter by type, category, or by name. The option to change the Pokemon's ability will give them the small list of abilities available to that specific Pokemon species, which they may choose from. The option to pick an item gives the user a list of items to pick from which can only be filtered by name. The final option is to change the Pokemon's nature, which will give them a small list of natures, with the impact on their Pokemon's stats being listed. 

