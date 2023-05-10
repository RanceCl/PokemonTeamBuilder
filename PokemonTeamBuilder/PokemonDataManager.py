
'''
The following is for the purpose of building and editing a team of Pokemon using Pandas dataframes
'''
import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


# Class to hold the dataframe for every Pokemon species as well as the filter methods.
class PokemonData:
    def __init__(self, data):
        self.data = data
        self.data['Abilities'] =  data['Abilities'].str.split(',') #Make abilities into an array
        self.data = self.data.fillna("-")
        self.filtered = self.data

        #Ability filters start as empty. "" indicates that the filter shouldn't be implemented
        self.typeFilter = ""
        self.abilityFilter = ""
        self.nameFilter = ""

    # Returns the stats of the requested Pokemon if the Pokemon is in the database
    def stats(self, name):
        return self.data[self.data.index == name]
    
    # Finds the Pokemon with with the Pokemon matching index number
    def index(self, pokedexNumber):
        return self.data[self.data['National Pokedex No'] == pokedexNumber]
        
    # Filters the datarame based on all of the specified filters.
    def filterData(self):
        # Resets the filtered data. This is so that updated filters won't rely on the old data.
        self.filtered = self.data
        
        # The following three filters are applied to the original dataset. 
        # Before each filter, the filtered dataframe is checked to make sure it isn't entirely empty as filtering an empty dataframe will remove columns.
        # Filters the data based on the desired type. Searches type 1 and type 2 slot.
        if (self.typeFilter != "") & (not self.filtered.empty):
            self.filtered = self.filtered[
                (self.filtered['Type 1'] == self.typeFilter) | 
                (self.filtered['Type 2'] == self.typeFilter)]
        
        # Filters the data based on the desired ability
        if (self.abilityFilter != "") & (not self.filtered.empty):
            self.filtered = self.filtered[
                [(self.abilityFilter in x) for x in self.filtered['Abilities']]]

        # Filters the data based on if the names contain the string that they are being filtered against.
        if (self.nameFilter != "") & (not self.filtered.empty):
            self.filtered = self.filtered[self.filtered.index.str.contains(self.nameFilter, case=False)]
        
        return self.filtered

    # This method will filter the dataset to only include Pokemon with names including the desired string.
    def filterName(self, name):
        if name == None:
            self.nameFilter = ""
        else:
            self.nameFilter = name
        return self.filterData()
    
    # This method will filter the dataset to only include Pokemon of the desired type.
    def filterType(self, name):
        if name == None:
            self.typeFilter = ""
        else:
            self.typeFilter = name
        return self.filterData()

    # This method will filter the dataset to only include Pokemon of the desired ability.
    def filterAbility(self, name):
        if name == None:
            self.abilityFilter = ""
        else:
            self.abilityFilter = name
        return self.filterData()
    
    # This method sorts the dataframe by the specified column. Pokemon name is a secondary sorting specifier to ensure that order is consistent.
    def sortData(self, sortBy):
        self.data = self.data.sort_values(by = [sortBy, "Pokemon"])
        self.filtered = self.filtered.sort_values(by = [sortBy, "Pokemon"])
        return self.filtered
    
    # This method resets the filters on the data and the view
    def filterReset(self):
        self.typeFilter = ""
        self.abilityFilter = ""
        self.nameFilter = ""
        self.sortData("National Pokedex No")
        self.filtered = self.data
        return self.filtered

# Class to hold the dataframe for every Pokemon move as well as the filter methods.
class MoveData:
    def __init__(self, data):
        self.data = data
        self.data = self.data.fillna("-")
        self.filtered = self.data

        #Ability filters start as empty. "" indicates that the filter shouldn't be implemented
        self.typeFilter = ""
        self.categoryFilter = ""
        self.nameFilter = ""

    # Returns the data for the requested move if it is in the database
    def description(self,name):
        return self.data[self.data.index == name]

    # Filters the datarame based on all of the specified filters.
    def filterData(self):
        # Resets the filtered data. This is so that updated filters won't rely on the old data.
        self.filtered = self.data
        
        # The following three filters are applied to the original dataset. 
        # Before each filter, the filtered dataframe is checked to make sure it isn't entirely empty as filtering an empty dataframe will remove columns.
        # Filters the data based on the desired type. 
        if (self.typeFilter != "") & (not self.filtered.empty):
            self.filtered = self.filtered[(self.filtered['Type'] == self.typeFilter)]
        
        # Filters the data based on the desired ability
        if (self.categoryFilter != "") & (not self.filtered.empty):
            self.filtered = self.filtered[(self.filtered['Category'] == self.categoryFilter)]

        # Filters the data based on if the names contain the string that they are being filtered against.
        if (self.nameFilter != "") & (not self.filtered.empty):
            self.filtered = self.filtered[self.filtered.index.str.contains(self.nameFilter, case=False)]
        
        return self.filtered

        # This method will filter the dataset to only include moves with names including the desired string.
    def filterName(self, name):
        if name == None:
            self.nameFilter = ""
        else:
            self.nameFilter = name
        return self.filterData()
    
    # This method will filter the dataset to only include moves of the desired type.
    def filterType(self, name):
        if name == None:
            self.typeFilter = ""
        else:
            self.typeFilter = name
        return self.filterData()

    # This method will filter the dataset to only include moves based on if they're physical or special.
    def filterCategory(self, name):
        if name == None:
            self.categoryFilter = ""
        else:
            self.categoryFilter = name
        return self.filterData()

    # This method resets the filters on the data and the view
    def filterReset(self):
        self.typeFilter = ""
        self.categoryFilter = ""
        self.nameFilter = ""
        self.filtered = self.data
        return self.filtered

# Class to hold the dataframe for every Pokemon item as well as the filter methods.
class ItemData:
    def __init__(self, data):
        self.data = data
        self.data = self.data.fillna("-")
        self.filtered = self.data

    # Returns the data for the requested item if it is in the database
    def description(self,name):
        return self.data[self.data.index == name]

    # Filters the datarame based on all of the specified filters.
    def filterData(self, name):
        # Resets the filtered data. This is so that updated filters won't rely on the old data.
        self.filtered = self.data
        
        # Filters the data based on if the names contain the string that they are being filtered against.
        if (name != "") & (name != None) & (not self.filtered.empty):
            self.filtered = self.filtered[self.filtered.index.str.contains(name, case=False)]
        return self.filtered

    # This method resets the filters on the data and the view
    def filterReset(self):
        self.filtered = self.data
        return self.filtered


# Class to hold every Pokemon dataframe in a single database.
class PokemonDatabase:
    def __init__(self, excelName):
        # Reads in each sheet to store as data for each Pokemon species and lists of every move, ability, and item
        self.pokemonData = PokemonData(pd.read_excel(excelName, sheet_name=0, index_col=1))
        self.abilityList = pd.read_excel(excelName, sheet_name=1, index_col=0)
        self.moveData = MoveData(pd.read_excel(excelName, sheet_name=2, index_col=0))
        self.natureList = pd.read_excel(excelName, sheet_name=3, index_col=0)
        self.itemData = ItemData(pd.read_excel(excelName, sheet_name=4, index_col=0))
        
        self.abilityList = self.abilityList.fillna("-")
        self.natureList = self.natureList.fillna("-")
        
        
        #Ability filters start as empty. "" indicates that the filter shouldn't be implemented
        self.typeFilter = ""
        self.abilityFilter = ""
        self.nameFilter = ""
    
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
        columns=['National Pokedex No','Lv','M/F','Type 1','Type 2','Nature',
                 'Health','Attack','Defense','Special Attack','Special Defense','Speed',
                 'Ability','Item','Move 1','Move 2','Move 3','Move 4','Form']
        
        self.pokemon = pd.DataFrame(columns=columns, index = [0])
        
        self.moves = pd.DataFrame(columns=['Type','Category','Power','Accuracy','PP','Effect'], 
                                  index = ['Move 1','Move 2','Move 3','Move 4'])
        
        # Copy the stats from the pokemon into a dataframe for calculating stats altered by nature
        self.baseStats = self.pokemon[["Health","Attack","Defense","Special Attack","Special Defense","Speed"]].copy()
        
        # Initialize variables to first available options or to None to prevent complications later
        self.nature = self.database.natureDescription('Hardy')
        self.pokemon['Lv'],self.pokemon['M/F'],self.pokemon['Nature'] = 100,"F",'Hardy'
        self.abilities = self.pokemon['Ability'] = self.pokemon['Item'] = None
        self.pokemon['Move 1'] = self.pokemon['Move 2'] = self.pokemon['Move 3'] = self.pokemon['Move 4'] = None
        
        # Check to see if the Pokemon currently has data
        self.exist = "Fail"
        self.changeSpecies(name)
        
    # Changes the specie of the Pokemon without fundamentally altering other aspects.
    def changeSpecies(self, name):
        pokemonStats = self.database.pokemonData.stats(name)
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
        # This call uses the name of the currently held nature as the nature itself isn't being changed.
        self.changeNature(self.pokemon['Nature'][0])
        
        # Indicate if there are any specific 
        # Some 
        self.formNeeds(self.pokemon['Form'][0])
        
        self.exist = "Success"

        # Change the index names for the each dataframe for aesthetic purposes
        self.pokemon.index.names = ['Pokemon']
        return "Success"
    
    # Takes in the name of the attack to be added and the index of the move to be changed
    # If the move already exists in the Pokemon's moveset or the index is beyond the possible range, nothing changes
    def changeMove(self, name, a):
        # Only perform if the move isn't already in the Pokemon's moveset
        if((self.pokemon['Move 1'][0] != name) & (self.pokemon['Move 2'][0] != name) &
           (self.pokemon['Move 3'][0] != name) & (self.pokemon['Move 4'][0] != name) & (a < 4)):
            move = self.database.moveData.description(name)
            
            # Make sure the move is in the database
            if not move.empty:
                self.formMaintain(self.pokemon['Move '+str(a)][0])
                self.pokemon['Move '+str(a)] = name
                self.moves.rename(index = {self.moves.index[a-1]: name}, inplace = True)
                self.moves.update(move)
                self.moves.iloc[a-1]["PP"] = str(math.trunc(self.moves.iloc[a-1]["PP"])) + "pp"
                
                # Display the accuracy as a percentage value. Only do this if the accuracy is a number value.
                accuracy = self.moves.iloc[a-1]["Accuracy"]
                if isinstance(accuracy, int) or isinstance(accuracy, float):
                    self.moves.iloc[a-1]["Accuracy"] = str(math.trunc(accuracy)) + "%"
                return "Success"
        return "Fail"
    
    # Changes the ability of the Pokemon to another ability in the list. 
    # If the desired index is out of range, the first available ability will be selected
    def changeAbility(self, a):
        # Make sure ability index isn't out of range.
        if (a < 0) or (a >= len(self.abilities)):
            ability = self.database.abilityDescription(self.abilities[0])
        else:
            ability = self.database.abilityDescription(self.abilities[a])
        if not ability.empty:
            self.pokemon['Ability'] = ability.index[0]
            return "Success"
        return "Fail"
    
    # Changes the Pokemon's held item to be the new name, if it exists in the database.
    def changeItem(self, name):
        if not self.database.itemData.description(name).empty:
            self.formMaintain(self.pokemon['Item'][0])
            self.pokemon['Item'] = name
            return "Success"
        return "Fail"
    
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
                self.pokemon[increasedStat] = self.pokemon[increasedStat] + 0.1 * self.pokemon[increasedStat]
                self.pokemon[decreasedStat] = self.pokemon[decreasedStat] - 0.1 * self.pokemon[decreasedStat]
            return "Success"
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
        
        columns=['Lv','M/F','Type 1','Type 2','Nature',
                 'Health','Attack','Defense','Special Attack','Special Defense','Speed',
                 'Ability','Item','Move 1','Move 2','Move 3','Move 4']
        #self.pokemon = pd.DataFrame(columns=columns, index = [0])
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
        if (a < len(self.team)) and (a >= 0):
            del self.team[a]
            self.updateBasic()
        return None
        
    # Change the species of the Pokemon at position 'a'
    def changeSpecies(self, name, a):
        # Make sure that a is in the possible range. 
        if (a < len(self.team)) and (a >= 0):
            self.team[a].changeSpecies(name)
            self.updateBasic()
        return None
    
    # Swap the positions of the Pokemon at position 'a' and position 'b'
    def swapPokemon(self, a, b):
        if (a < len(self.team)) and (a >= 0) and (b < len(self.team)) and (b >= 0):
            self.team[b], self.team[a] = self.team[a], self.team[b]
            self.updateBasic()
        return None
    
    # Updates the basic dataset. This is done so that repeated Pokemon can be included in the dataframe without complications.
    def updateBasic(self):
        # Empty the old basic summary information
        self.teamBasic = self.teamBasic.iloc[0:0]
        
        # Place all of the Pokemon into an empty DataFrame 
        for pokemon in self.team:
            self.teamBasic = pd.concat([self.teamBasic, pokemon.pokemon])
        return None
    
    # Prints a basic summary of all the Pokemon in the team
    def printTeamBasic(self):
        print('-'*80)
        print(self.teamBasic)
        print("-"*80)
        return None
        
    # Prints in detail every Pokemon in the team
    def printTeamVerbose(self):
        print("-"*80)
        print("-"*80)
        for index, pokemon in enumerate(self.team):
            print(f"Team Member {index+1}:")
            pokemon.printPokemon()
            print("-"*80)
        print("-"*80)
        return None