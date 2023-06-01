import socket
import json

from google.cloud import storage
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

PORT_USER = 3389
PORT_ROBOT = 3400

# Cloud function URL
URL = "https://europe-west1-sistemas-multimedia.cloudfunctions.net/tratarImagenes"

# User's socket creation
sockListenUser = socket.socket()
print("USER Socket successfully created")
sockListenUser.bind(('', PORT_USER))
print("socket binded to %s" % (PORT_USER))

# Robot's socket creation
sockListenRobot = socket.socket()
print("ROBOT Socket successfully created")
sockListenRobot.bind(('', PORT_ROBOT))
print("socket binded to %s" % (PORT_ROBOT))

sockListenUser.listen(5)
print("socket USER is listening")
socketConnListenUser, addr = sockListenUser.accept()
print('Got connection from', addr)

sockListenRobot.listen(5)
print("socket ROBOT is listening")
socketConnListenRobot, addr2 = sockListenRobot.accept()
print('Got connection from', addr2)

while True:

    data = socketConnListenUser.recv(1024)
    print(data.decode())
    # If there is data from robot, it will be sent to ROBOT
    if data:
        dataUser = json.loads(data.decode())

        #Shut dawn the server
        if dataUser["instruction"] == "TURN_OFF":
            break

        socketConnListenRobot.send(data)
        print("SENT TO ROBOT")
        dataRobot = socketConnListenRobot.recv(1024)
        print("DATA RECIBIDA DE ROBOT")

        if dataRobot:
            dictDataRobot = json.loads(dataRobot.decode())
            if dictDataRobot["message"] != "NAN":
                # HERE CALL TO CLOUD FUNCIONS
                params = {
                    'filename1': "image1.jpeg",
                    'filename2': "image2.jpeg"
                }
                credentials = service_account.IDTokenCredentials.from_service_account_file('credentials.json',
                                                                                           target_audience=URL)

                authed_session = AuthorizedSession(credentials)

                resp = authed_session.post(URL, params=params)  # , headers=headers (PARA LA PRIMERA FUNCIÓN)
                print(resp.status_code)

                points3d = resp.json()
                #print(type(points3d))

                dictDataRobot["message"] = points3d["pts3D"]
                #print(type(dictDataRobot["message"]))

                jsonDataRobot = json.dumps(dictDataRobot)
                #print(type(jsonDataRobot))
                #print(jsonDataRobot)
                socketConnListenUser.send(jsonDataRobot.encode())
                socketConnListenUser.shutdown(socket.SHUT_WR)
                #socketConnListenUser.send(dictDataRobot)
                print("SENT TO USER")


    #time.sleep(0.5)
