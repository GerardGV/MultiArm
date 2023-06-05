import socket
import json
from google.cloud import storage
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import time
import picamera
import serial

puerto = '/dev/ttyACM0'
velocity = 9600

PORT = 3400
IP = '12.345.678.901' # Here your IP server

def capture_image(file_name):
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)
        camera.capture(file_name)
        camera.stop_preview()
        capture_image('image1.jpg')
        time.sleep(5)
        capture_image('image2.jpg')

def upload_image(bucket_name, file_path, destination_blob_name, credentials_file):
    # instance of google cloud client with token access
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    client = storage.Client(credentials=credentials)

    # Bucket get
    bucket = client.bucket(bucket_name)

    # Blob file creacion in bucket
    blob = bucket.blob(destination_blob_name)

    #upload blob file
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

    # Inicialize arduino raspberry comunication
    arduino = serial.Serial(puerto, velocity)
    time.sleep(1)

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

                # iteration of different draw points
                for point in json_data["message"]:
                    for axis in point:
                        arduino.write(axis.encode()) # sending coordates from axis x, y and z

            elif instruction == "TOOLCHG":

                json_data = jsonSetUp("NAN", "NAN")
                print(json_data)

                # sending data through TCP socket connection
                socketUser.send(json_data.encode())  # encode transform data to binary

                arduino.write(instruction.encode())# sending signal to change tool

            elif instruction == "PHOTO":

                bucket_name = "imagenes-modeling"   # DECLARAMOS EN QUE BUCKET SE SUBEN LAS IMÁGENES
                credentials_file = "credentials.json"   # USAMOS LAS CREDENCIALES QUE TIENEN PERMISO

                # PARÁMETROS PARA LA PRIMERA IMÁGEN
                #file_path = "imgFaces/VC part/img08_V2_1_face_Pol_sense_sostre.jpeg"  # to test image from local, not raspberry
                file_path = "image1.jpg"  # path to image1
                destination_blob_name = "image1.jpeg"   # image name in bucket

                # PARÁMETROS PARA LA SEGUNDA IMÁGEN
                #file_path2 = "imgFaces/VC part/img08_V2_2_face_Pol_sense_sostre.jpeg"  # to test image from local, not raspberry
                file_path2 = "image2.jpg" # path to image 2
                destination_blob_name2 = "image2.jpeg"  # image name in bucket

                # Getting images
                upload_image(bucket_name, file_path, destination_blob_name, credentials_file)# sending image 1
                upload_image(bucket_name, file_path2, destination_blob_name2, credentials_file)# sending image2

                images = ['image1.jpeg', 'image2.jpeg']

                # data set to json
                json_data = jsonSetUp("NAN", images)
                print(json_data)

                # sending data through TCP socket connection
                socketUser.send(json_data.encode())  # encode transform data to binary

            elif instruction == "TURN_OFF":
                # robot turn off
                socketUser.close()
                arduino.write(instruction.encode())  # sending signal to change turn off the robot
                break


if __name__ == '__main__':
    # In case you want to test some new feature, use this main function
    socketClient = connectionSocket(IP, PORT)
    communicationRobot(socketClient)
