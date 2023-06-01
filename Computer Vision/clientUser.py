import socket
import json
import sys

PORT=3389
IP='34.172.166.240'

def jsonSetUp(instruction:str, message):
    """
    :param instruction: It could NAN, TOOLCHG, MOVE, PHOTO
    :param message: any type of data to transmit
    :return: json file with configured parameters
    """

    #dictonary to create json file
    data = {
        "instruction": instruction,
        "message": message
    }

    # dictionary becomes json file
    json_data = json.dumps(data)

    return json_data


def connectionSocket(ip, port:int):
    """"
    Socket creation and connection
    """
    s = socket.socket()  # socket creation
    s.connect((ip, port))
    return s

def communicationClient(socketUser, instruccions="NAN", message="NAN"):
    """
    :param socketUser:
    :param instruccions: It could NAN, TOOLCHG, MOVE, PHOTO, TURN_OFF
    :param message: any type of data to be sent
    :return:
    """
    # data set to json
    json_data = jsonSetUp(instruccions, message)


    if instruccions == "MOVE" or instruccions == "TOOLCHG":
        # sending data through TCP socket connection
        print("Json data: ", json_data)
        socketUser.send(json_data.encode())  # encode transform data to binary

    elif instruccions == "PHOTO":
        # sending data through TCP socket connection
        socketUser.send(json_data.encode())  # encode transform data to binary

        # Tamaño máximo de los datos a recibir en un solo bloque
        buffer_size = 1024
        # Variable para almacenar los datos recibidos
        received_data = ""

        # Recibir los datos en un bucle hasta que se complete la cadena JSON
        while True:
            # Recibir datos del socket
            data = socketUser.recv(buffer_size).decode()

            # Si no se reciben más datos, salir del bucle
            if not data:
                break

            # Concatenar los datos recibidos
            received_data += data

        # Imprimir los datos recibidos
        print("Server data:", received_data)

        try:
            # Decodificar la cadena JSON
            jsonData = json.loads(received_data)

            # Acceder al valor "message"
            print("jsonData['message']:", jsonData["message"])

            return jsonData["message"]

        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
            return None



if __name__ == '__main__':

    socketClient=connectionSocket(IP, PORT)
    pointsList=[[1,2,3], [2,3,4],[2,2,2]]
    jsonDataMessage = communicationClient(socketClient, instruccions="PHOTO")
    print("MAIN: JsonData['message']: ", jsonDataMessage)
    print("MAIN: type(JsonData['message']): ", type(jsonDataMessage))

