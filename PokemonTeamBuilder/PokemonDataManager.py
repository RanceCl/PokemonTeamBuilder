
'''
The following is for the purpose of building and editing a team of Pokemon using Pandas dataframes.
Dataframes will be manipulated by a user using a GUI in a different file.
'''
import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


# Parent class to hold the dataframe for different data type (e.g., Pokemon, Moves, Items) and filter methods.
class Data:
    def __init__(self, data):
        self.data = data
        self.data = self.data.fillna("-")
        self.filtered = self.data
        self.filters = {}
        self.nameFilter = ""

    # Returns the data for the requested element if it is in the database
    def elementInfo(self,name):
        return self.data[self.data.index == name]

    # Filters the data based on specified filter data.
    def filterData(self):
        # Filtered data is reset so that updated filters won't rely on the old data.
        self.filtered = self.data.copy()

        # Filters the data based on what filters have been added. This is performed on the original dataset. 
        for filter_name, filter_value in self.filters.items():
            # Before each filter, the filtered dataframe is checked to make sure it isn't entirely empty as filtering an empty dataframe will remove columns.
            if filter_value != "" and not self.filtered.empty:
                self.filtered = self.filtered[(self.filtered[filter_name] == filter_value)]
        return None
    
    # Filters data based on name. This is separate since the filter conditions are different.
    def filterName(self):
        # Filters the data based on if the names contain the string that they are being filtered against.
        if (self.nameFilter != "") & (not self.filtered.empty):
            self.filtered = self.filtered[self.filtered.index.str.contains(self.nameFilter, case=False)]
        return None

    # Places an empty filter value into the filter name if no filter value was given.
    def isEmptyFilterValue(self, filter_value):
        if filter_value == None:
            return ""
        return filter_value

    # Adds a new filter to be applied to the data. Each filter value and its corresponding column are stored in a dictionary.
    def addFilter(self, filter_name, filter_value):
        # Name filter is separate from other filters and is thus not to be placed in the dictionary.
        if filter_name == "Name":
            self.nameFilter = self.isEmptyFilterValue(filter_value)
        # Any other filter value will be placed into the filters dictionary
        else:
            self.filters[filter_name] = self.isEmptyFilterValue(filter_value)
        return None

    # Performs all the necessary filter methods.
    def quickFilter(self, filter_name, filter_value):
        self.addFilter(filter_name, filter_value)
        self.filterData()
        self.filterName()
        return self.filtered

    def filterReset(self):
        self.filters = {}
        self.filtered = self.data.copy()
        return self.filtered

# Class to hold the dataframe for every Pokemon species as well as the filter methods.
class PokemonData(Data):
    def __init__(self, data):
        super().__init__(data)
        self.data['Abilities'] =  data['Abilities'].str.split(',') #Make abilities into an array
        self.filtered = self.data.copy()

        #Ability filters start as empty. "" indicates that the filter shouldn't be implemented
        self.typeFilter = ""
        self.abilityFilter = ""
    
    # Finds the Pokemon with with the Pokemon matching index number
    def index(self, pokedexNumber):
        return self.data[self.data['National Pokedex No'] == pokedexNumber]

    # Filters the Pokemon based on the desired type. Both Type 1 and Type 2 are checked.
    def filterType(self):
        if (self.typeFilter != "") & (not self.filtered.empty):
            # Searches type 1 and type 2 slot.
            self.filtered = self.filtered[
                (self.filtered['Type 1'] == self.typeFilter) | 
                (self.filtered['Type 2'] == self.typeFilter)]
        return None

    # Filters the Pokemon based on the desired ability. 
    def filterAbility(self):
        if (self.abilityFilter != "") & (not self.filtered.empty):
            # Checks the entire array of abilities available to a Pokemon.
            self.filtered = self.filtered[
                [(self.abilityFilter in x) for x in self.filtered['Abilities']]]
        return None

    # Adds the filters to be applied to the data.
    def addFilter(self, filter_name, filter_value):
        if filter_name == "Name":
            self.nameFilter = self.isEmptyFilterValue(filter_value)
        elif filter_name == "Type":
            self.typeFilter = self.isEmptyFilterValue(filter_value)
        elif filter_name == "Ability":
            self.abilityFilter = self.isEmptyFilterValue(filter_value)
        return None

    # Filters the datarame based on all of the specified filters.
    # Due to how unique the filters for this dataset is, specifically, a separate method was created from the standard data.
    # Performs all the necessary filter methods
    def quickFilter(self, filter_name, filter_value):
        self.filtered = self.data.copy()
        self.addFilter(filter_name, filter_value)
        self.filterType()
        self.filterAbility()
        self.filterName()
        return self.filtered

    def sortData(self, sortBy):
        self.data = self.data.sort_values(by = [sortBy, "Pokemon"])
        self.filtered = self.filtered.sort_values(by = [sortBy, "Pokemon"])
        return self.filtered
    
    def filterReset(self):
        self.typeFilter = ""
        self.abilityFilter = ""
        self.nameFilter = ""
        self.sortData("National Pokedex No")
        self.filtered = self.data
        return self.filtered

# Class to hold every Pokemon dataframe in a single database.
class PokemonDatabase:
    def __init__(self, excelName):
        # Reads in each sheet to store as data for each Pokemon species and lists of every move, ability, and item
        self.pokemonData = PokemonData(pd.read_excel(excelName, sheet_name=0, index_col=1))
        self.abilityList = pd.read_excel(excelName, sheet_name=1, index_col=0)
        self.moveData = Data(pd.read_excel(excelName, sheet_name=2, index_col=0))
        self.natureList = pd.read_excel(excelName, sheet_name=3, index_col=0)
        self.itemData = Data(pd.read_excel(excelName, sheet_name=4, index_col=0))
        
        self.abilityList = self.abilityList.fillna("-")
        self.natureList = self.natureList.fillna("-")

    # Returns the data for the requested ability if it is in the database
    def abilityDescription(self,name):
        return self.abilityList[self.abilityList.index == name]
    
    # Returns the data for the requested nature if it is in the database
    def natureDescription(self,name):
        return self.natureList[self.natureList.index == name]


# Class to handle individual Pokemon methods
# This class holds a Pokemon's name, index number, types, stats, nature, gender, ability, and moves.
class Pokemon:
    def __init__(self, name, database):
        self.database = database
        
        # Initialize the elements of the Pokemon
        columns=['National Pokedex No','Type 1','Type 2','Nature',
                 'Health','Attack','Defense','Special Attack','Special Defense','Speed',
                 'Ability','Item','Move 1','Move 2','Move 3','Move 4','Form']
        
        self.pokemon = pd.DataFrame(columns=columns, index = [0])
        
        # Copy the stats from the pokemon into a dataframe for calculating stats altered by nature
        self.baseStats = self.pokemon[["Health","Attack","Defense","Special Attack","Special Defense","Speed"]].copy()
        
        # Initialize variables
        self.pokemon['Nature'] = 'Hardy'
        self.abilities = self.pokemon['Ability'] = self.pokemon['Item'] = None
        self.pokemon['Move 1'] = self.pokemon['Move 2'] = self.pokemon['Move 3'] = self.pokemon['Move 4'] = None
        
        # Check to see if the Pokemon currently has data
        self.exist = "Fail"
        self.changeSpecies(name)
        
    # Changes the specie of the Pokemon without fundamentally altering other aspects.
    def changeSpecies(self, name):
        pokemonStats = self.database.pokemonData.elementInfo(name)
        # Indicate that the Pokemon wasn't in the database
        if pokemonStats.empty:
            print(f"A Pokemon with the name {name} could not be found.")
            return "Fail"
        
        # Rename the indexes to the Pokemon names to easily update the values
        self.pokemon.rename(index = {self.pokemon.index[0]: name}, inplace = True)
        self.baseStats.rename(index = {self.baseStats.index[0]: name}, inplace = True)
        
        # Update variables
        self.pokemon.update(pokemonStats)
        self.baseStats.update(self.pokemon)
        
        # Change the ability to the first available one for the new species.
        self.abilities = pokemonStats["Abilities"][0]
        self.changeAbility(0)
        
        # Call to change nature to change the stats to reflect the new specie.
        self.changeNature(self.pokemon['Nature'][0])
        
        # Indicate if there are any specific requirements for the current Pokemon's form.
        self.formNeeds(self.pokemon['Form'][0])
        
        self.exist = "Success"

        # Change the index names for the each dataframe for aesthetic purposes
        self.pokemon.index.names = ['Pokemon']
        return "Success"

    # Determine if the Pokemon already has the move in its moveset
    def isMoveInMoveset(self, name):
        return ((self.pokemon['Move 1'][0] == name) |
                (self.pokemon['Move 2'][0] == name) |
                (self.pokemon['Move 3'][0] == name) | 
                (self.pokemon['Move 4'][0] == name))

    
    # Takes in the name of the attack to be added and the index of the move to be changed
    # If the move already exists in the Pokemon's moveset or the index is beyond the possible range, nothing changes
    def changeMove(self, name, a):
        # Only perform if the move isn't already in the Pokemon's moveset and the move index is valid.
        if((not self.isMoveInMoveset(name)) & (a <= 4)):
            move = self.database.moveData.elementInfo(name)
            
            # Make sure the move is in the database
            if not move.empty:
                self.formMaintain(self.pokemon['Move '+str(a)][0])
                self.pokemon['Move '+str(a)] = name
                return "Success"
        return "Fail"
    
    # Make sure ability index isn't out of range.
    def getValidAbilityIndex(self, a):
        if (a < 0) or (a >= len(self.abilities)):
            return 0
        else:
            return a

    # Changes the ability of the Pokemon to another ability in the list. 
    # If the desired index is out of range, the first available ability will be selected
    def changeAbility(self, a):
        ability = self.database.abilityDescription(self.abilities[self.getValidAbilityIndex(a)])
        if not ability.empty:
            self.pokemon['Ability'] = ability.index[0]
            return "Success"
        self.pokemon['Ability'] = None
        return "Fail"
    
    # Changes the Pokemon's held item to be the new name, if it exists in the database.
    def changeItem(self, name):
        if not self.database.itemData.elementInfo(name).empty:
            self.formMaintain(self.pokemon['Item'][0])
            self.pokemon['Item'] = name
            return "Success"
        self.pokemon['Item'] = None
        return "Fail"
    
    def applyStatChanges(self, increasedStat, decreasedStat):
        self.pokemon[increasedStat] = self.pokemon[increasedStat] + 0.1 * self.pokemon[increasedStat]
        self.pokemon[decreasedStat] = self.pokemon[decreasedStat] - 0.1 * self.pokemon[decreasedStat]

    # Changes the Pokemon's nature to the requested name, if it exists in the database.
    # A Pokemon's nature will alter its stats based on what effect the nature will have.
    # Calling this will change the name and the effected stats to reflect the impact of the Pokemon's new nature.
    def changeNature(self, name):
        # Remove modifications from previous nature
        self.pokemon.update(self.baseStats)
        
        # Update stats based on nature
        nature = self.database.natureDescription(name)
        if not nature.empty:
            self.pokemon["Nature"] = name
            increasedStat = nature["Increased stat"][0]
            decreasedStat = nature["Decreased stat"][0]

            # Apply stat modifiers based on new nature
            if increasedStat != decreasedStat:
                self.applyStatChanges(increasedStat, decreasedStat)
                
            return "Success"
        self.pokemon["Nature"] = "Hardy"
        return "Fail"

    # This method will take in the form specifier of a Pokemon and perform necessary changes to their held item or attacks to match it.
    # Some Pokemon forms require it to be holding a specific item, abiliity, or move to trigger. The name of the indicated object is held in the "form" cell of a Pokemon's row.
    # This method will be called if the form isn't 0, changeing the required variable to match what it needs to on the Pokemon.
    def formNeeds(self, name):
        # If the form is 0, that means no changes need to be made.
        if name != 0:
            self.changeItem(name)
            self.changeMove(name,1)
        return None

    # This method is called to change a Pokemon to its base form if an item or move that maintained its current form has been removed.
    # The name sent is the name of the value that is going to be removed. If this value is equal to the form value, then the Pokemon will be made into its base form.
    def formMaintain(self, name):
        if (name == self.pokemon['Form'][0]):
            baseForm = self.pokemon.index[0]
            # Remove the suffix of a Pokemon's name that indicates it is in a different form to find the name of the base form. 
            if (" - Mega" in baseForm):
                # Removes all possible mega possiblities. Since nothing will occur if the substring isn't in the name, an if-else statement isn't required.
                baseForm = baseForm.replace(" - Mega X","")
                baseForm = baseForm.replace(" - Mega Y","")
                baseForm = baseForm.replace(" - Mega","")
            else:
                baseForm = baseForm.replace(" - Primal","")
                baseForm = baseForm.replace(" - Origin","")
                baseForm = baseForm.replace(" - Crowned","")
                baseForm = baseForm.replace(" - Pirouette","")

            # Change the Pokemon's specie to its base form.
            self.changeSpecies(baseForm)
        return None


# This is the class to hold a team of Pokemon. Each Pokemon is its own class.
# A team can have no more than 6 Pokemon at any given time.
class PokemonTeam:
    def __init__(self, database):
        self.database = database
        self.team = []
        
        columns=['Type 1','Type 2','Nature','Health','Attack','Defense','Special Attack',
                 'Special Defense','Speed','Ability','Item','Move 1','Move 2','Move 3','Move 4']
        self.teamBasic = pd.DataFrame(columns=columns)
        
    # Adds a Pokemon to the team based on an operation given from other methods
    # Assumes that the position provided will be valid since it has already been checked.
    # When inserting, the requested position must be in range.
    def addPokemon(self, name):
        # Team size can't exceed 6 if adding a Pokemon to the team
        if len(self.team) >= 6:
            return "Fail"
        pokemon = Pokemon(name, self.database)
        # Make sure the Pokemon is in the database
        if pokemon.exist == 'Fail':
            return "Fail"
        else:
            self.team.append(pokemon)
            self.updateBasic()
        return pokemon
    
    # Remove the Pokemon at position 'a' if it in range.
    def removePokemon(self, a):
        try:
            del self.team[a]
            self.updateBasic()
        except IndexError:
            pass
        return None
        
    # Change the species of the Pokemon at position 'a'
    def changeSpecies(self, name, a):
        # Make sure that a is in the possible range. 
        try:
            self.team[a].changeSpecies(name)
            self.updateBasic()
        except IndexError:
            pass
        return None
    
    # Swap the positions of the Pokemon at position 'a' and position 'b'
    def swapPokemon(self, a, b):
        try:
            self.team[b], self.team[a] = self.team[a], self.team[b]
            self.updateBasic()
        except IndexError:
            pass
        return None
    
    # Updates the basic dataset. This is done so that repeated Pokemon can be included in the dataframe without complications.
    def updateBasic(self):
        # Empty the old basic summary information
        self.teamBasic = self.teamBasic.iloc[0:0]
        
        # Place all of the Pokemon into an empty DataFrame 
        for pokemon in self.team:
            self.teamBasic = pd.concat([self.teamBasic, pokemon.pokemon])
        return None
    
    # Imports a team from an excel document.
    def teamImport(self, name):
        # Ensure that a valid name has been given.
        if (not name):
            return False

        # If the file name doesn't include the file extension, append it to the name.
        if (len(name) <= 5) | (name[-5:] != ".xlsx"):
            name = name + ".xlsx"

        # Ensure that the file exists before attempting to read.
        if (not os.path.isfile("Saved Teams/"+name)):
            return False

        teamBasic = pd.read_excel("Saved Teams/"+name, index_col=0)
        teamBasic = teamBasic.fillna(np.nan).replace([np.nan], [None])
        
        # Clean out the previous team.
        self.team.clear()

        # Add every Pokemon in the imported team to the team list.
        for i in range(len(teamBasic)):
            self.addPokemon(teamBasic.index[i])
            self.team[i].pokemon["Ability"] = teamBasic.iloc[i]["Ability"]
            self.team[i].pokemon["Item"] = teamBasic.iloc[i]["Item"]
            self.team[i].changeNature(teamBasic.iloc[i]["Nature"])
            self.team[i].pokemon["Move 1"] = teamBasic.iloc[i]["Move 1"]
            self.team[i].pokemon["Move 2"] = teamBasic.iloc[i]["Move 2"]
            self.team[i].pokemon["Move 3"] = teamBasic.iloc[i]["Move 3"]
            self.team[i].pokemon["Move 4"] = teamBasic.iloc[i]["Move 4"]

        return True

    # Exports the current team to an excel document.
    def teamExport(self, name):
        # Ensure that the name is valid. Ensure that the team isn't empty.
        if (not name) | (name == "Pokemon Data.xlsx") | (name == "Pokemon Data.xlsx") | (self.teamBasic.empty):
            return False

        # If the file name doesn't include the file extension, append it to the name.
        if (len(name) <= 5) | (name[-5:] != ".xlsx"):
            name = name + ".xlsx"

        # Export the team to an excel document in the "Saved Teams" folder.
        self.teamBasic.to_excel("Saved Teams/"+name)
        return True
