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

def communicationClient(socketUser, instructions="NAN", message="NAN"):
    """
    :param socketUser:
    :param instructions: Puede ser NAN, TOOLCHG, MOVE, PHOTO, TURN_OFF
    :param message: Cualquier tipo de dato para ser enviado
    :return:
    """
    # Configurar los datos en formato JSON
    json_data = jsonSetUp(instructions, message)

    if instructions == "MOVE" or instructions == "TOOLCHG":
        # Enviar datos a través de la conexión TCP del socket
        print("Json data: ", json_data)
        socketUser.send(json_data.encode())  # Codificar para convertir los datos a binario

    elif instructions == "PHOTO":
        # Enviar datos a través de la conexión TCP del socket
        socketUser.send(json_data.encode())  # Codificar para convertir los datos a binario

        # Tamaño máximo de los datos a recibir en un solo bloque
        buffer_size = 1024
        # Variable para almacenar los datos recibidos
        received_data = b""  # Usar bytes en lugar de cadena para concatenar datos
        it = 0
        while True:
            # Recibir datos del socket
            data = socketUser.recv(buffer_size)
            print("Num de recv: ", it)
            it += 1
            if not data:
                break

            # Concatenar los datos recibidos
            received_data += data

        # Decodificar la cadena completa de datos recibidos
        received_data = received_data.decode()

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

