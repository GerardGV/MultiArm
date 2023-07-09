### Selecciona un idioma | Select a language:
* <a href="#catalan">Català</a>
* <a href="#castellano">Castellano</a>
* <a href="#ingles">English</a>


<h1 id= "catalan"> Procés de reconstrucció - Modelatge 2D a partir de dues imatges utilitzant SIFT </h1>

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

<h1 id= "castellano">Proceso de reconstrucción - Modelado 2D a partir de dos imágenes usando SIFT </h1>

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

<h1 id= "ingles"> Reconstruction process - 2D Modeling from two images using SIFT</h1>

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