### Selecciona un idioma | Select a language:
* <a href="#catala">Català</a>
* <a href="#castellano">Castellano</a>
* <a href="#english">English</a>
---

<img src="imgREADMEs/imgREADME_RLP/imgMultiArmHeader.jpeg?raw=true" align="right" width="300" alt="MultiArm Header Image"/>  
<h1 id="catala"> MultiArm </h1>
Projecte conjunt de les assignatures de Robòtica (RLP), Visió per Computador (VC) i Sistemes Multimèdia (SM) en el qual hem desenvolupat un braç robotic amb visió per computador per a realitzar operacions quirúrgiques remotament via Internet.

# Table of Contents
   * [What is this?](#what-is-this)
   * [Requirements](#requirements)
     * [Hardware](#hardware)
     * [Software](#software)
   * [Documentation](#documentation)
   * [How to use](#how-to-use)

# What is this?

# Requirements:

## Hardware:
- 3 motors pas a pas (28BYJ-48)
- Arduino UNO Rev.3
- Controladora de motors de pas a pas (28BYJ-48) (7 IN pins i de 5-12V)
- Micro Metal Gearmotor HP (Gir Capçal)
- Controladora de motor (micromotor de gir)
 -Fuente de alimentación TACENS anima APII 500
- Placa de prototipo 16,5x5,5cm
- Raspberry pi Zero
- Mòdul de càmera Raspberry Pi Camera v2


## Software:
- [Python 3.10.x](https://www.python.org/)
- [NumPy](https://numpy.org/)
- [PyGame](https://www.pygame.org/news)
- [cv2 (openCV)](https://pypi.org/project/opencv-python/)

# Documentation:
Aquest README conté informació del nostre robot, i un context general de les parts de visió per computador i del Cloud, desenvolupat a Sistemes Multimèdia.
Si estàs interessat en conèixer més detalls dels respectius projectes, pots mirar:
* [Visió per Computador: Implementació de l'algorisme SIFT i modelat 3D](https://github.com/GerardGV/MultiArm/tree/main/Computer%20Vision) on aprofundim més sobre l'algorisme implementat per detectar punts característics de dues imatges i després visualitzar-los en l'aplicació.
* [Sistemes Multimèdia: Projecte al Cloud](https://github.com/GerardGV/MultiArm/tree/main/cloud) on aprofundim més sobre l'arquitectura de comunicacions desenvolupada en el Cloud allotjat a Google Cloud, l'aplicació, el seu funcionament i peticions amb el servidor realitzades.

# How to use:
1. Clone this repository.
    ```terminal
    git clone https://github.com/GerardGV/MultiArm.git
    ```
2. Install Python and the required libraries. 
    ```terminal
    pip install -r requirements.txt
    ```
3. Open the server (execute the cloud/server.py) file
    ```terminal
    python3 cloud/server.py
    ```
4. Open the App (execute the cloud/app.py)
    ```terminal
    python3 cloud/app.py
    ```
5. Open the clientRobot.py and turn on the Robot
    ```terminal
    python3 cloud/clientRobot.py
    ```
6. Enjoy!! 😄 TIP: You can check the Cloud folder README.md to understand the WorkFlow of our app. 

# Authors:
* Pol Colomer Campoy (1605612) | PolKinsa
* Gerard Josep Guarin Velez (1605947) | GerardGV
* Jan Rubio Rico (1603753) | TheRospetit
* Rubén Simó Marin (1569391)
