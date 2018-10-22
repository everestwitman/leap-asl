import pickle

database = pickle.load(open('userData/database.p', 'rb'))

userName = raw_input('Please enter your name: ')
if (userName in database): 
    database[userName]['logins'] = database[userName]['logins'] + 1
    print 'Welcome back, ' + userName + '.'
else: 
    database[userName] = {'logins': 1}
    print 'Welcome, ' + userName + ''

print database
pickle.dump(database, open('userData/database.p', 'wb'))
