'''
The following code handles the graphical user interface to build and edit a team of Pokemon.
Relies on "PokemonDataManager.py" for data management. 

Users can select from lists or type in values to change their team as well as import and export their team
to and from excel files.
'''

from pickletools import read_unicodestring1
import PokemonDataManager as pdm
import PySimpleGUI as sg

# This method takes in a dataframe and returns the headings and the data in list form.
# Doing this ordinarily requires calling tolist twice with the same dataframe, so this will save space.
def quickToList(df):
    return df.columns.tolist(), df.values.tolist()

# Method to quickly and repeatedly construct PySimpleGUI tables using headings and data from tables
def initialTable(headings, data):
    return sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)

def quickLayout(headings, data, buttons):
    # [[initialTable(headings, data)],buttons,]
    if buttons:
        return [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],buttons,]
    return [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],]


# This method will return the window of the filtered Pokemon list when called.
def pokemonSelect(pdb):
    headings, data = quickToList(pdb.pokemonData.filtered[['Type 1','Type 2','Health','Attack','Defense','Special Attack',
                                                    'Special Defense','Speed','Abilities']].reset_index())

    layout = [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],
                [sg.Button('Select Pokemon', key='_pokemonselected_'),
                sg.Button('Filter by name', key='_filtername_'),
                sg.Button('Filter by type', key='_filtertype_'),
                sg.Button('Filter by ability', key='_filterability_'),
                sg.Button('Reset Filters', key='_filterreset_')],]
    return data, sg.Window("Pokemon List (Name: "+pdb.pokemonData.nameFilter + ", Type: "+pdb.pokemonData.typeFilter + ", Ability: "+pdb.pokemonData.abilityFilter + ")", layout)
    
# This method will take in a filter and a specification on what type of filter it is.
# Since filtering will always result in the window needing to be updated, this function will close the old pokemon list and return the new window
def pokemonFilter(pdb, name, clarifier, window):
    if clarifier == "Reset":
        pdb.pokemonData.filterReset()
    else:
        pdb.pokemonData.quickFilter(clarifier, name)

    # Update the window with the newly filtered list.
    window.close()
    return pokemonSelect(pdb)

# The method is called whenever the user wishes to add a Pokemon to the party. If nothing is selected, no changes will be made to the team.
def addPokemon(pdb, team, operation, a):

    # Initial creation of the list of Pokemon
    data, window = pokemonSelect(pdb)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '_pokemonselected_':
            # Make sure that a row has been selected
            if values['-TABLE-']:
                # Add a Pokemon with the selected name into the party. "data[values['-TABLE-'][0]][0]" is the name corresponding with the selected row.
                if operation == "Change":
                    team.changeSpecies(data[values['-TABLE-'][0]][0], a)
                else:
                    team.addPokemon(data[values['-TABLE-'][0]][0])
                break
        # This event will give the user the option to enter a type to filter the list of Pokemon by. 
        elif event == '_filtername_':
            text = sg.popup_get_text('Enter part of the name of the Pokemon you want ', title="Name Filter")
            data, window = pokemonFilter(pdb, text, "Name", window)
        # This event will give the user the option to enter a type to filter the list of Pokemon by. 
        elif event == '_filtertype_':
            text = sg.popup_get_text('Enter type to filter by', title="Type Filter")
            data, window = pokemonFilter(pdb, text, "Type", window)
        # This event will give the user the option to enter an ability to filter the list of Pokemon by. 
        elif event == '_filterability_':
            text = sg.popup_get_text('Enter ability to filter by', title="Ability Filter")
            data, window = pokemonFilter(pdb, text, "Ability", window)

        # This event will reset any filters applied
        elif event == '_filterreset_':
            data, window = pokemonFilter(pdb, "Reset", "Reset", window)

    # Reset filtered list for future use.
    pdb.pokemonData.filterReset()

    # Return to the previous window
    window.close()
    return None





# The method is called whenever the user wishes to change the nature of the Pokemon.
def changeNature(dataList, teamMember):

    # Initial creation of the list of Pokemon
    headings, data = quickToList(dataList.reset_index())
    layout = [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],
              [sg.Button('Select Nature', key='_selected_')],]

    window = sg.Window("Nature List", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '_selected_':
            # Make sure that a row has been selected
            if values['-TABLE-']:
                teamMember.changeNature(data[values['-TABLE-'][0]][0])
                break

    # Return to the previous window
    window.close()
    #team.printTeamBasic()
    return None


# This method will return the window of the filtered Pokemon list when called.
def moveSelect(pdb):
    headings, data = quickToList(pdb.moveData.filtered.reset_index())

    layout = [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],
              [sg.Button('Select Move', key='_selected_'),
               sg.Button('Filter by name', key='_filtername_'),
               sg.Button('Filter by type', key='_filtertype_'),
               sg.Button('Filter by category', key='_filtercategory_'),
               sg.Button('Reset Filters', key='_filterreset_')],]
    return data, sg.Window("Move List (Name: " + pdb.moveData.nameFilter + ", " + ', '.join(f'{k}: {v}' for k,v in pdb.moveData.filters.items()) + ")", layout)
    
# This method will take in a filter and a specification on what type of filter it is.
# Since filtering will always result in the window needing to be updated, this function will close the old pokemon list and return the new window
def moveFilter(pdb, name, clarifier, window):
    if clarifier == "Reset":
        pdb.moveData.filterReset()
    else:
        pdb.moveData.quickFilter(clarifier, name)

    # Update the window with the newly filtered list.
    window.close()
    return moveSelect(pdb)

# The method is called whenever the user wishes to add a Pokemon to the party. If nothing is selected, no changes will be made to the team.
def changeMove(pdb, teamMember, a):
    # Initial creation of the list of Pokemon
    data, window = moveSelect(pdb)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '_selected_':
            # Make sure that a row has been selected
            if values['-TABLE-']:
                # Determine what is being changed
                teamMember.changeMove(data[values['-TABLE-'][0]][0],a)
                break
        # This event will give the user the option to enter a type to filter the list of Pokemon by. 
        elif event == '_filtername_':
            text = sg.popup_get_text('Enter part of the name of the move you want ', title="Name Filter")
            data, window = moveFilter(pdb, text, "Name", window)
        # This event will give the user the option to enter a type to filter the list of Pokemon by. 
        elif event == '_filtertype_':
            text = sg.popup_get_text('Enter type to filter by', title="Type Filter")
            data, window = moveFilter(pdb, text, "Type", window)
        # This event will give the user the option to enter an ability to filter the list of Pokemon by. 
        elif event == '_filtercategory_':
            text = sg.popup_get_text('Is the move you want Physical, Special, or Status?', title="Category Filter")
            data, window = moveFilter(pdb, text, "Category", window)
        # This event will reset any filters applied
        elif event == '_filterreset_':
            data, window = moveFilter(pdb, "Reset", "Reset", window)

    # Reset filtered list for future use.
    pdb.moveData.filterReset()

    # Return to the previous window
    window.close()
    return None


# This method will return the window of the filtered item list when called.
def itemSelect(pdb):
    headings, data = quickToList(pdb.itemData.filtered.reset_index())

    layout = [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],
              [sg.Button('Select Item', key='_selected_'),
               sg.Button('Filter by name', key='_filtername_'),
               sg.Button('Reset Filters', key='_filterreset_')],]
    return data, sg.Window("Item List", layout)
    
# This method will take in a filter and a specification on what type of filter it is.
# Since filtering will always result in the window needing to be updated, this function will close the old pokemon list and return the new window
def itemFilter(pdb, name, clarifier, window):
    if clarifier == "Reset":
        pdb.itemData.filterReset()
    else:
        pdb.itemData.quickFilter(clarifier, name)
    
    # Update the window with the newly filtered list.
    window.close()
    return itemSelect(pdb)

# The method is called whenever the user wishes to add a Pokemon to the party. If nothing is selected, no changes will be made to the team.
def changeItem(pdb, teamMember):
    # Initial creation of the list of Pokemon
    data, window = itemSelect(pdb)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '_selected_':
            # Make sure that a row has been selected
            if values['-TABLE-']:
                # Determine what is being changed
                teamMember.changeItem(data[values['-TABLE-'][0]][0])
                break
        # This event will give the user the option to enter a type to filter the list of Pokemon by. 
        elif event == '_filtername_':
            text = sg.popup_get_text('Enter part of the name of the item you want ', title="Name Filter")
            data, window = itemFilter(pdb, text, "Name", window)
        elif event == '_filterreset_':
            data, window = itemFilter(pdb, "Reset", "Reset", window)

    # Reset filtered list for future use.
    pdb.itemData.filterReset()

    # Return to the previous window
    window.close()
    return None


# Takes in an array of ability names and outputs two lists. 
# The first holds the headers while the second holds all of the information about each ability
def abilityList(pdb, abilities):
    headings = ['Ability', 'Effect']
    data = []
    for ability in abilities:
        data.append(pdb.abilityDescription(ability)['Effect'].reset_index().values.tolist()[0])
    return headings, data

# This event will allow the user to choose one of the options a Pokemon has for its ability.
def changeAbility(pdb, teamMember):
    headings, data = abilityList(pdb, teamMember.abilities)
    layout = [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],
              [sg.Button('Select Ability', key='_abilityselected_')],]
    
    window = sg.Window("Ability List", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '_abilityselected_':
            # Make sure that a row has been selected
            if values['-TABLE-']:
                teamMember.changeAbility(values['-TABLE-'][0])
                break

    # Return to the previous window
    window.close()
    return None


# This method will return the window of the current team composition when called.
def teamSelect(team):
    #headings, data = quickToList(team.teamBasic.reset_index())
    headings = ['Name','Type 1','Type 2','Nature','Hp','Atk','Def','SpA','SpD','Spd',
                 'Ability','Item','Move 1','Move 2','Move 3','Move 4']
    data = team.teamBasic.reset_index().values.tolist()

    layout = [[sg.Table(values=data, headings=headings, justification='center', key='-TABLE-', enable_events=True, enable_click_events=True)],
              [sg.Button('Add Pokemon',key='_addpokemon_'), sg.Button('Change Pokemon',key='_changepokemon_'), sg.Button('Change Item',key='_changeitem_'),
               sg.Button('Change Move 1',key='_changem1_'), sg.Button('Change Move 2',key='_changem2_'), sg.Button('Import',key='_import_')],
              [sg.Button('Remove Pokemon',key='_removepokemon_'), sg.Button('Change Nature',key='_changenature_'), sg.Button('Change Ability',key='_changeability_'),
               sg.Button('Change Move 3',key='_changem3_'), sg.Button('Change Move 4',key='_changem4_'), sg.Button('Export',key='_export_')],
              ]
    return sg.Window("Pokemon Team", layout)


def main():
    pdb = pdm.PokemonDatabase('Pokemon Data.xlsx')
    team = pdm.PokemonTeam(pdb)
    window = teamSelect(team)


    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # Begin the method to add a new Pokemon to the team
        elif event == '_addpokemon_':
            window.close()
            addPokemon(pdb, team, "Add", 0)
            window = teamSelect(team)

        # Remove the selected Pokemon
        elif event == '_removepokemon_':
            # Make sure that a row has been selected
            if values['-TABLE-']:
                window.close()
                team.removePokemon(values['-TABLE-'][0])
                window = teamSelect(team)

        # This event will allow the user to change the species of the currently selected Pokemon. 
        elif event == '_changepokemon_':
            if values['-TABLE-']:
                window.close()
                addPokemon(pdb, team, "Change", values['-TABLE-'][0])
                window = teamSelect(team)

        # This event will allow the user to choose one of the options a Pokemon has for its ability
        elif event == '_changeability_':
            if values['-TABLE-']:
                window.close()
                changeAbility(pdb, team.team[values['-TABLE-'][0]])
                team.updateBasic()
                window = teamSelect(team)
        
        # This event will allow the user to change the Pokemon's nature
        elif event == '_changenature_':
            if values['-TABLE-']:
                window.close()
                changeNature(pdb.natureList, team.team[values['-TABLE-'][0]])
                team.updateBasic()
                window = teamSelect(team)
        
        # This event will allow the user to change the Pokemon's item
        elif event == '_changeitem_':
            if values['-TABLE-']:
                window.close()
                changeItem(pdb, team.team[values['-TABLE-'][0]])
                team.updateBasic()
                window = teamSelect(team)
        
        # This event will allow the user to change the Pokemon's 1st move
        elif event == '_changem1_':
            if values['-TABLE-']:
                window.close()
                changeMove(pdb, team.team[values['-TABLE-'][0]], 1)
                team.updateBasic()
                window = teamSelect(team)

        # This event will allow the user to change the Pokemon's 2nd move
        elif event == '_changem2_':
            if values['-TABLE-']:
                window.close()
                changeMove(pdb, team.team[values['-TABLE-'][0]], 2)
                team.updateBasic()
                window = teamSelect(team)

        # This event will allow the user to change the Pokemon's 3rd move
        elif event == '_changem3_':
            if values['-TABLE-']:
                window.close()
                changeMove(pdb, team.team[values['-TABLE-'][0]], 3)
                team.updateBasic()
                window = teamSelect(team)

        # This event will allow the user to change the Pokemon's 4th move
        elif event == '_changem4_':
            if values['-TABLE-']:
                window.close()
                changeMove(pdb, team.team[values['-TABLE-'][0]], 4)
                team.updateBasic()
                window = teamSelect(team)
                
        # This event will allow the user to import their team from an excel document.
        elif event == '_import_':
            window.close()
            text = sg.popup_get_text('Enter the name of your team ', title="Import team")
            team.teamImport(text)
            team.updateBasic()
            window = teamSelect(team)

        # This event will allow the user to export their team to an excel document.
        elif event == '_export_':
            window.close()
            text = sg.popup_get_text('Enter a name for your team ', title="Export team")
            team.teamExport(text)
            team.updateBasic()
            window = teamSelect(team)
    

main()
