import socket
import random
import pandas as pd
from sklearn.linear_model import LinearRegression


s = socket.socket()
print('socket create')
s.bind(('localhost', 10000))

s.listen(1)
print('waiting for connections')

while True:
    c, addr = s.accept()
    print("connected with ", addr)

    manpower = random.randint(8000,10000)

    data = c.recv(1024).decode()
    print(data)

    a = data.split("/")

    new_disaster_group = a[0]
    new_disaster_type = a[1]
    new_disaster_subgroup = a[2]


    df = pd.read_csv('final_data_set.csv')

    x = df[['Disaster_Type', 'Disaster_Subgroup', 'Disaster_Group']]
    y = df['Manpower']

    X_encoded = pd.get_dummies(x)

    model = LinearRegression()
    model.fit(X_encoded, y)

    new_data = pd.DataFrame({
        'Disaster_Type': [new_disaster_type],
        'Disaster_Subgroup': [new_disaster_subgroup],
        'Disaster_Group': [new_disaster_group]
    })

    new_data_encoded = pd.get_dummies(new_data)

    new_data_encoded = new_data_encoded.reindex(columns=X_encoded.columns, fill_value=0)

    req_manpower = int(model.predict(new_data_encoded))
    
    if((manpower<req_manpower)):
        remain = str(manpower)
        req_manpower1=str(req_manpower)+" required manpower exceeds the available manpower"

    elif(manpower>=req_manpower):
        req_manpower1=req_manpower
        remain = str(manpower-req_manpower)
    print(manpower)
    print(req_manpower1)
    print(remain)

    send_data = str(manpower)+"/"+str(req_manpower1)+"/"+str(remain)
    c.send(send_data.encode())

    c.close()
