from ryan_tools import *

def get_year(datetime):
    return str(datetime.year)

def find_washes(data_in, account, month_str = False):

    account = read_cash(account)
    data = data_in[data_in['Account'] == account]
    if month_str != False:
        data = data[data['Month'].str.contains(month_str, case = False)]
    i = 0
    for index in data.index:
        print(i, '/',len(data.index))
        
        i = i + 1
        if data.loc[index, 'Done'] == False:
            year = str(data.loc[index, 'Date'].year)
            
            account = data.loc[index, 'Account']
            month = data.loc[index, 'Month']
            amount = data.loc[index, 'Amount']
            temp = data[- data['Done']]
            temp = temp[temp['Amount'] == (-1 * amount)]
            temp = temp[temp['Account'] == account]
            temp = temp[temp['Month'] == month]
            temp = temp[temp['year'] == year]
            
            x = 0
            
            for index2 in temp.index:
                if x == 0:
                    data.loc[index, 'Done'] = True
                    data.loc[index2, 'Done'] = True
                x = x + 1
    data['Debits'] = data.loc[data['Amount'] >= 0, 'Amount']
    data['Credits'] = data.loc[data['Amount'] <= 0, 'Amount']
    choice = input('To clipboard?')
    if 'y' in str(choice).lower():
        data.to_clipboard()
        
    return data

filename = input('FileName?\n')
print('Reading Data')
data = pd.read_csv(filename)
data.columns = ['Number', 'Date', 'Type', 'ID', 'Description', 'Account', 'Amount']
print('Reading Date')
data['Date'] = data['Date'].apply(read_date)
print('Getting Month')
data['Month'] = data['Date'].apply(get_month)
data['year'] = data['Date'].apply(get_year)


data['Done'] = False

data['Account'] = data['Account'].apply(read_cash)
print('Reading Cash')
data['Amount'] = data['Amount'].apply(read_cash)
data.to_csv('Analyzed _ ' + str(filename))
