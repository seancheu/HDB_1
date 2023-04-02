import PySimpleGUI as sg
import pandas as pd
import re, pyi_splash

# Update the text on the splash screen
pyi_splash.update_text("PyInstaller is a great software!")
pyi_splash.update_text("Second time's a charm!")

# Close the splash screen. It does not matter when the call
# to this function is made, the splash screen remains open until
# this function is called or the Python program is terminated.
pyi_splash.close()

# natural sorter function
def natural_sort_key(s):
    return [int(x) if x.isdigit() else x.lower() for x in re.split('(\d+)', s)]

# function to get the recommendation for the most expensive unit
def get_most_expensive():
    most_expensive = data.loc[data['resale_price'].idxmax()]
    age = 2021 - int(most_expensive['lease_start'])
    return f"{most_expensive['flat_type']} HDB in BLK {most_expensive['block']} {most_expensive['street_name']} \n" \
           f"Floor level: {most_expensive['storey_range']}\n" \
           f"Age of flat: {age} years old\n"\
           f"Area(per sqm): {most_expensive['area_sqm']}\n"\
           f"Latest Resale Price: ${most_expensive['resale_price']:,}\n\n"

file_layout = [
    [sg.Text('Select CSV file to read:'), sg.Input(key='file_path'), sg.FileBrowse()],
    [sg.Button('Open'), sg.Button('Exit')]
]

file_window = sg.Window('Open File', file_layout)

while True:
    event, values = file_window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Open':
        try:
            data = pd.read_csv(values['file_path'])
            break
        except:
            sg.popup_error('Invalid file format. Please select a CSV/Excel file.')
    
file_window.close()

# Convert the date column to a datetime format
data['month'] = pd.to_datetime(data['month'])

# Filter the data to only include rows with dates between 2020 and 2021
start_date = pd.to_datetime('2020-01')
end_date = pd.to_datetime('2022-01')
data = data[(data['month'] >= start_date) & (data['month'] < end_date)]

# print(data.head())

# get a list of unique town names from the DataFrame
town_names = data['town'].unique().tolist()

# get a list of unique town names from the DataFrame
flat_type = data['flat_type'].unique().tolist() 
flat_types_sorted = sorted(flat_type, key=natural_sort_key)

# create a new data field for age of flat
flat_age = 99 - data['lease_rem']

# create the layout for the GUI
layout = [
    [sg.Text('Select Preferred Town:'), sg.DropDown(town_names, key='town')],
    [sg.Text('Select Flat Type:'), sg.DropDown(flat_types_sorted, key='flat_type')],
    [sg.Text('Enter Your Budget ($):'), sg.InputText(key='budget')],
    [sg.Button('Recommend'), sg.Button('Most Expensive Flat'), sg.Button('Clear'), sg.Button('Exit')],
    [sg.Text('Recommended Properties (based on latest resale price in 2021):')],
    [sg.Multiline(key='recommendation', size=(200,100),pad=(0, (10, 0)))]
]

# create the window
window = sg.Window('HDB Flat Recommender', layout, resizable=True, size=(400,400))

# event loop to process user inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Clear':
        window['town'].update('')
        window['flat_type'].update('')
        window['budget'].update('')
        window['recommendation'].update('')
        recommendation_count = 0

    elif event == 'Most Expensive Flat':
        recommendation_text = get_most_expensive()
        window['recommendation'].update(recommendation_text)
            
    elif event == 'Recommend':
        if not values['town'] and not values['flat_type'] and not values['budget']:
            sg.popup('Please fill in the fields.')
        
        else:
            # filter the data based on the user inputs
            filtered_data = data[
                (data['town'] == values['town']) &
                (data['flat_type'] == values['flat_type']) &
                (data['resale_price'] <= int(values['budget']))
            ]
            
            if filtered_data.empty:
                sg.popup(f"Cannot find any matching flats with your criteria of: \n{values['town']} - {values['flat_type']} unit - SGD${values['budget']}", title="GG liao")
            else:
                # sort the filtered data by the absolute difference between the resale price and the budget
                filtered_data['diff'] = abs(filtered_data['resale_price'] - int(values['budget']))
                filtered_data = filtered_data.sort_values('diff')
                
                # get all properties that meet the criteria
                recommendations = filtered_data.to_dict('records')

                # display the recommendations in the GUI
                recommendation_text = ""
                for recommendation in recommendations:
                    age = 2021 - int(recommendation['lease_start'])
                    recommendation_text += f"{recommendation['flat_type']} HDB in BLK {recommendation['block']} {recommendation['street_name']} \n" \
                                        f"Floor level: {recommendation['storey_range']}\n" \
                                        f"Flat Age: {age} years old\n"\
                                        f"Area(per sqm): {recommendation['area_sqm']}\n"\
                                        f"Latest Resale Price: ${recommendation['resale_price']:,}\n\n"

                window['recommendation'].update(recommendation_text)

# close the window
window.close()

