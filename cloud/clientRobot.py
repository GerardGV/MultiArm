import socket
import json
from google.cloud import storage
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

PORT = 3400
IP = '34.172.166.240'


def upload_image(bucket_name, file_path, destination_blob_name, credentials_file):
    # Crea una instancia del cliente de Google Cloud Storage con las credenciales de la identidad de servicio
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    client = storage.Client(credentials=credentials)

    # Obtiene el bucket
    bucket = client.bucket(bucket_name)

    # Crea un nuevo blob (archivo) en el bucket
    blob = bucket.blob(destination_blob_name)

    # Carga el archivo en el blob
    blob.upload_from_filename(file_path)

    print('Imagen cargada exitosamente en el bucket.')


def jsonSetUp(instruction: str, message):
    """
    :param instruction: It could NAN, TOOLCHG, MOVE, PHOTO
    :param message: any type of data to transmit
    :return: json file with configured parameters
    """

    # dictonary to create json file
    data = {
        "instruction": instruction,
        "message": message
    }

    # dictionary becomes json file
    json_data = json.dumps(data)

    return json_data


def connectionSocket(ip, port: int):
    """"
    Socket creation and connection
    """
    s = socket.socket()  # socket creation
    s.connect((ip, port))
    return s


def communicationRobot(socketUser):
    """
     instruction: It could NAN, TOOLCHG, MOVE, PHOTO, TURN_OFF
    """
    # It's listening until recive data from server
    while True:
        serverData = socketUser.recv(1024)
        if serverData:
            print("DATA RECIBIDA")
            jsonData = json.loads(serverData.decode())
            instruction = jsonData["instruction"]
            print(jsonData)

            if instruction == "MOVE":
                print(jsonData["message"])
                # Sending coordenates to arduino
                json_data = jsonSetUp("NAN", "NAN")
                print(json_data)

                # sending data through TCP socket connection
                socketUser.send(json_data.encode())  # encode transform data to binary

            elif instruction == "TOOLCHG":

                json_data = jsonSetUp("NAN", "NAN")
                print(json_data)

                # sending data through TCP socket connection
                socketUser.send(json_data.encode())  # encode transform data to binary

            elif instruction == "PHOTO":
                bucket_name = "imagenes-modeling"   # DECLARAMOS EN QUE BUCKET SE SUBEN LAS IMÁGENES
                credentials_file = "credentials.json"   # USAMOS LAS CREDENCIALES QUE TIENEN PERMISO

                # PARÁMETROS PARA LA PRIMERA IMÁGEN
                file_path = "./img/img08_V2_1_face_Pol_sense_sostre.jpeg"    # NOMBRE IMAGEN 1
                destination_blob_name = "image1.jpeg"   # NOMBRE QUE LA IMAGEN QUE TENDRÁ EN EL BUCKET

                # PARÁMETROS PARA LA SEGUNDA IMÁGEN
                file_path2 = "./img/img08_V2_2_face_Pol_sense_sostre.jpeg"  # NOMBRE IMAGEN 2
                destination_blob_name2 = "image2.jpeg"  # NOMBRE QUE LA IMAGEN QUE TENDRÁ EN EL BUCKET
                # Getting images

                upload_image(bucket_name, file_path, destination_blob_name, credentials_file)       # IMAGEN 1
                upload_image(bucket_name, file_path2, destination_blob_name2, credentials_file)     # IMAGEN 2

                images = ['image1.jpeg', 'image2.jpeg']

                # data set to json
                json_data = jsonSetUp("NAN", images)
                print(json_data)

                # sending data through TCP socket connection
                socketUser.send(json_data.encode())  # encode transform data to binary

            elif instruction == "TURN_OFF":
                # robot turn off
                socketUser.close()
                break


if __name__ == '__main__':
    # In case you want to test some new feature, use this main function
    socketClient = connectionSocket(IP, PORT)
    communicationRobot(socketClient)
