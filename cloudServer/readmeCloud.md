### Selecciona un idioma | Select a language:
* <a href="#catala">Català</a>
* <a href="#castellano">Castellano</a>
* <a href="#english">English</a>

<h1 id="catala"> Sistemes Multimèdia - Projecte al Cloud </h1>
Per a la realització del nostre projecte de Sistemes Multimèdia, hem volgut realitzar una integració amb els nostres 
projectes de Robòtica (RLP) i Visió per Computador (VC).
Per al que correspon a aquesta assignatura, hem fet les connexions necessàries per a controlar remotament el 
robot, des d'una aplicació, que també hem implementat.

## Arquitectura:

Per a tal de poder controlar remotament el robot, hem desenvolupat una aplicació, la qual permet interactuar amb el 
robot. En comptes de permetre una connexió remota des d'una xarxa local, hem estructurat l'arquitectura de connexions
de tal manera que es pugui controlar des de qualsevol part del món amb una connexió a Internet.

A continuació es pot veure l'esquema d'aquesta arquitectura.
<p align="center">
<img src="../imgReadMe/imgREADME_SM/sm_connection_architecture.png?raw=true" alt="SM Connection Architecture"/>
</p>
Tal com es pot observar, podem trobar un usuari (User -> `clientUser.py`), el robot (`clientRobot.py`) i al centre de 
tot, el Cloud, en el nostre cas, **Google Cloud**.

### Estructura del Google Cloud:

Primerament, tenim una instància de màquina virtual (VM) mitjançant l'API Compute Engine de 
Google Cloud (A partir d'ara, GC), en aquesta VM té una IP externa estàtica i es troba dins d'una VPC Network de GC, a
la qual li hem afegit les regles de Firewall necessàries per a permetre connexions als ports que realitzarem per a les 
connexions. 

Addicionalment, hi tenim una Cloud Function on tenim tot el codi desenvolupat en el projecte de Visió per Computador 
(hem posat el codi que es troba en la Cloud Function en el fitxer `tractament_imatges.py` per tal que es pugui 
visualitzar), per tal que es realitzin tots els càlculs al Cloud.  
Per a fer els càlculs necessaris, es necessiten dues 
imatges, fetes pel robot. És per això que mitjançant l'API Cloud Storage de GC hem utilitzat el Bucket per guardar-hi 
les imatges que després la Cloud Function utilitza per als càlculs.


<h1> Procés de reconstrucció - Modelatge 2D a partir de dues imatges utilitzant SIFT </h1>

En aquest readme explicarem pas a pas como funciona i que fa cada funció del python script que es troba a la cloud function de Google Cloud Platform. El funcionament de localCloudFunction.py de la carpeta User es el mateix ja que es una versió per fer modificar i fer proves en local. 

Agafarem l'imatge utilitzada al video del README.md per l'explicació.

### Passos per a la reconstrucció:

1. **Dades proporcionades:** Primerament, rebrem dues imatges, en el nostre projecte del robot, les imatges proporcionades seràn les dues que realitza la càmera de la Raspberry Pi.
   El robot prendra les imatges del següent rostre com es veu en el video:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/rostro-humano-atado-con-alambre-ROTADO.jpg?raw=true">  

2. **Calcular SIFT:** A continuació es realitza l'algorisme SIFT, el qual ja sabem com funciona degut a l'explicació anterior. Aplicarem l'algorisme SIFT per a cada imatge per tal d'obtenir els `keypoints` i `descriptors` de cada una.
3. **Matching:** Una vegada amb els `keypoints` i `descriptors` de cada imatge, realitzarem el matching, on busquem identificar ` keypoints` que apareguin en les dues imatges. Per fer aixó, nosaltres hem utilitzat `knnMatch`from `FlannBasedMatcher` de OpenCV per comparar els `descriptors ` del keypoints d'una imatge amb els de l'altre imatge. Si els `descriptors `de 2 `keypoints` fan match signfica que són el mateix.
4. **Good Matches:** Del pas anterior, hem trobat molts matches, és a dir, molts punts característics que es trobaven alhora en les dues imatges, però el més segur és que molts d'aquests siguin càlculs erronis degut a la similaritud de diversos sectors de la imatge. És per això per el que realtizarem un filtratge dels matches per tal de quedar-nos amb els "Good Matches" o matches confiables. Per calcular-los, apliquem el test de Lowe's (Lowe's Ratio Test) o "prova de ràtio de pendent". 
5. **First Reconstruction**: NO ES NECESSARI per la version actual 2D. Aquesta funcio es de cara a l'ampliació on volem veure en 3D el rostre i interactuar amb ell. De cara al futur el que fa una triangulació amb dades de la camara que treu de l'imatge per pasar els punts de 2D a 3D. 

Es visualitza el resultat:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultsVideo.jpeg?raw=true"> 

<h1 id="castellano">Sistemas Multimedia - Proyecto en el Cloud</h1> 

Para la realización de nuestro proyecto de Sistemas Multimedia, hemos querido realizar una integración con los nuestros
proyectos de Robótica (RLP) y Visión por Computador (VC).
Para lo que corresponde a esta asignatura, hemos hecho las conexiones necesarias para controlar remotamente el
robot, desde una aplicación, que también hemos implementado.

## Arquitectura:

Para poder controlar remotamente el robot, hemos desarrollado una aplicación, la cual permite interactuar con el
robot. En lugar de permitir una conexión remota desde una red local, hemos estructurado la arquitectura de conexiones
de modo que se pueda controlar desde cualquier parte del mundo con una conexión a Internet.

A continuación se puede ver el esquema de esa arquitectura.
<p align="center">
<img src="../imgReadMe/imgREADME_SM/sm_connection_architecture.png" alt= "SM Connection Architecture"/>
</p>
Tal como se puede observar, podemos encontrar un usuario (User -> `clientUser.py`), el robot (`clientRobot.py`) y en el centro de
todo, el Cloud, en nuestro caso, **Google Cloud**.

### Estructura de Google Cloud:

En primer lugar, tenemos una instancia de máquina virtual (VM) mediante la API Compute Engine de
Google Cloud (A partir de ahora, GC), en esta VM tiene una IP externa estática y se encuentra dentro de una VPC Network de GC, en
la cual le hemos añadido las reglas de Firewall necesarias para permitir conexiones a los puertos que realizaremos para las
conexiones.

Adicionalmente, tenemos una Cloud Function donde tenemos todo el código desarrollado en el proyecto de Visión por Computador
(hemos puesto el código que se encuentra en la Cloud Function en el archivo `tractament_imatges.py` para que se pueda
visualizar), para que se realicen todos los cálculos en Cloud.
Para realizar los cálculos necesarios, se necesitan dos
imágenes, hechas por el robot. Es por eso que mediante la API Cloud Storage de GC hemos utilizado el Bucket para guardarlo
las imágenes que después la Cloud Function utiliza para los cálculos.


<h1>Proceso de reconstrucción - Modelado 2D a partir de dos imágenes usando SIFT </h1>

En este readme explicaremos paso a paso cómo funciona y que realiza cada función del python script que hay en la  cloud function de Google Cloud Platform. El funcionamiento de localCloudFunction.py de la carpeta User es el mismo ya que es una versión para modificar y hacer pruebas en local.

Cogeremos la imagen utilizada en el vídeo del README.md para la explicación.

### Pasos para la reconstrucción:

1. **Datos proporcionados:** Primeramente, recibiremos dos imágenes, en nuestro proyecto del robot, las imágenes proporcionadas serán las dos que realiza la cámara de la Raspberry Pi.
    El robot tomará las imágenes del siguiente rostro como se ve en el vídeo:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/rostro-humano-atado-con-alambre-ROTADO.jpg?raw=true">

2. **Calcular SIFT:** A continuación se realiza el algoritmo SIFT, el cual ya sabemos cómo funciona debido a la explicación anterior. Aplicaremos el algoritmo SIFT para cada imagen para obtener los `keypoints` y `descriptors` de cada una.
3. **Matching:** Una vez con los `keypoints` y `descriptores` de cada imagen, realizaremos el matching, donde buscamos identificar `keypoints` que aparezcan en las dos imágenes. Para ello, nosotros hemos utilizado `knnMatch` from `FlannBasedMatcher` de OpenCV para comparar los `descriptores` del keypoints de una imagen con los de la otra imagen. Si los `descriptores` de 2 `keypoints` hacen match signfica que son lo mismo.
4. **Good Matches:** Del paso anterior, hemos encontrado muchos matches, es decir, muchos puntos característicos que se encontraban a la vez en las dos imágenes, pero lo más seguro es que muchos de éstos sean cálculos erróneos debido a la similaridad de varios sectores de la imagen. Es por eso por lo que realizaremos un filtrado de los matches para quedarnos con los "Good Matches" o matches confiables. Para calcularlos, aplicamos el test de Lowe's (Lowe's Ratio Test) o "prueba de ratio de pendiente".
5. **First Reconstruction**: NO SE NECESARIO por la version actual 2D. Esta funcion es de cara a la ampliación donde queremos ver en 3D el rostro e interactuar con él. De cara al futuro, lo que hace una triangulación con datos de la camara que saca de la imagen para pasar los puntos de 2D a 3D.

Se visualiza el resultado:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultsVideo.jpeg?raw=true">

<h1 id="english">Multimedia Systems - Cloud Project</h1> 

For the realization of our Multimedia Systems project, we wanted to carry out an integration with ours Robotics (RLP) and Computer Vision (VC) projects.
For what corresponds to this subject, we have made the necessary connections to remotely control the
robot, from an application, which we have also implemented.

## Architecture:

In order to be able to remotely control the robot, we have developed an application, which allows you to interact with it
robot Instead of allowing a remote connection from a local network, we structured the connection architecture
so that it can be controlled from anywhere in the world with an Internet connection.

Below you can see the outline of this architecture.
<p align="center">
<img src="../imgReadMe/imgREADME_SM/sm_connection_architecture.png" alt= "SM Connection Architecture"/>
</p>
As you can see, we can find a user (User -> `clientUser.py`), the robot (`clientRobot.py`) and in the center of
everything, the Cloud, in our case, **Google Cloud**.

### Structure of Google Cloud:

First, we instantiate a virtual machine (VM) using the Compute Engine API
Google Cloud (Henceforth GC), in this VM has a static external IP and is inside a GC VPC Network, in
to which we have added the necessary Firewall rules to allow connections to the ports we will make for them
connections

Additionally, we have a Cloud Function where we have all the code developed in the Computer Vision project
(we have put the code found in the Cloud Function in the `tractament_imatges.py` file so that it can
visualize), so that all calculations are performed in the Cloud.
To make the necessary calculations, two are needed
images, made by the robot. That's why using the GC Cloud Storage API we used the Bucket to save to it
the images that the Cloud Function then uses for calculations.


<h1> Reconstruction process - 2D Modeling from two images using SIFT</h1>

In this readme we will explain step by step how each function from the python script of the cloud function in Google Cloud Platform works and what it does. The operation of localCloudFunction.py from the User folder is the same since it is a version to modify and test locally.

We will take the image used in the README.md video for the explanation.

### Steps for rebuilding:

1. **Data provided:** First, we will receive two images. In our robot project, the images provided will be the two images taken by the Raspberry Pi camera.
    The robot will take the images of the following face as seen in the video:
    
    <img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/rostro-humano-atado-con-alambre-ROTADO.jpg?raw=true">

2. **Calculate SIFT:** The SIFT algorithm is then performed, which we already know how it works due to the previous explanation. We will apply the SIFT algorithm to each image in order to obtain the `keypoints` and `descriptors` of each one.
3. **Matching:** Once with the `keypoints` and `descriptors` of each image, we will perform the matching, where we seek to identify `keypoints` that appear in the two images. To do so, we used `knnMatch`from `FlannBasedMatcher` of OpenCV to compare the `descriptors` of the keypoints of one image with those of the other image. If the `descriptors' of 2 `keypoints' match, it means they are the same.
4. **Good Matches:** From the previous step, we found many matches, that is, many characteristic points that were found at the same time in the two images, but the most certain thing is that many of these are erroneous calculations due to the similarity of various sectors of the image. This is why we will perform a filtering of the matches in order to stay with the "Good Matches" or reliable matches. To calculate them, we apply Lowe's test (Lowe's Ratio Test) or "slope ratio test".
5. **First Reconstruction**: NOT NECESSARY for the current 2D version. This function is for enlargement where we want to see the face in 3D and interact with it. Looking to the future what makes a triangulation with camera data that it takes from the image to pass the points from 2D to 3D.

The result is displayed:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultsVideo.jpeg?raw=true">