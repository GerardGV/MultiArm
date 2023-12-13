#### Autors | Autores | Authors:
* Pol Colomer Campoy (1605612)
* Gerard Josep Guarin Velez (1605947)
* Jan Rubio Rico (1603753)

### Selecciona un idioma | Select a language:
* <a href="#catala">Català</a>
* <a href="#castellano">Castellano</a>
* <a href="#english">English</a>
---
<h1 id="english"> COMPUTER VISION</h1>

Computer vision is used in this project to get caracteristic points from the robot images. These caracteristic points are visualized in the user application. They are going to be used to a multiview estereo proces in future versions.

In this directory you will find the computer vision part of the project:

<ol>
	<li>computerVisionAnalitics.py: We analized 3 different algorithms to choose which we were going to use in our project.</li>
  <li>sift.py: We implemented SIFT algorithm straight from David G. Lowe paper from 2004 and other sources as a challange and to understand SIFT better.</li>
</ol>
<h2> 1. COMPUTER VISION ANALITICS </h2>

To choose the caracteristic points or `keypoints` we considered 3 algorithms: Harris, ORB and SIFT. All of them are already implemented in the library openCV We decided to choose SIFT because it is more capable of detect caracteristic points and it is scale invariant. Here we have the caracteristic points for each algorithm with the same image:

- Harris:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultHarris.jpg?raw=true">  

- ORB:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultORB.jpg?raw=true">  

- SIFT:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultSIFT.jpg?raw=true">

## SIFT (Scale Invariant Feature Transform)

The SIFT algorithm is particularly useful for detecting feature points invariant to changes in scale, rotation, and illumination in an image. The detection process is carried out through several stages. First, one is applied
scale pyramid to identify potential points at different levels of resolution.
A keypoint detection algorithm is then used to identify regions with distinctive features,
such as corners and regions with sudden intensity changes.
Once the key points are detected, the SIFT algorithm calculates a descriptor for each point. These descriptors are
numerical vectors that capture the local features of the region around each keypoint, such as the direction of the
gradient and magnitude. This makes it possible to compare and match characteristic points between different images, since the
descriptors are robust to geometric and photometric changes.

The SIFT algorithm has been widely used in various computer vision applications, such as the
image matching, object recognition and three-dimensional reconstruction. Its robustness and
invariance to different transformations have contributed to its popularity and its applicability in different areas.

### SIFT Manual Implementation:
After deciding that we would like to use the SIFT algorithm we decided to implement it as a challenge since we consider that in this way we would learn and understand it more even though in the project we use OpenCV's SIFT for optimization and time issues.

The implementation consists of 4 steps:

1. **Obtaining key points:** To obtain key points, or characteristic points, the image must be convoluted with
     a Gaussian mask, resulting in a smoothed or `scaled` image. We have to generate `n` scales to then obtain a space of Gaussian differences. Each new smoothed image is generated with a mask with the `sigma` used in the creation of the previous smoothed image by a `k^n` hyperparameter. Smoothed images are grouped into `octaves`. The 'octaves' differ in that the resolution is reduced. In each octave the pixels have a resolution of `2^n of the Octave`. When we obtain the Differences of Gaussian spaces, we subtract each new smoothed image from the previous one, iterate through each pixel of the resulting image and if the pixel is a maximum or a minimum in the `3x3x3` space around it, it consider a keypoint.

2. **Refining keypoint location:** In this section the positions of the keypoints are briefly refined, because the
     'exact' position, adding more decimals to the feature point coordinates.
     To achieve this approximation, Taylor's second-order function and the Hessian matrix must be implemented. Because of the small difference in results applying this step or not applying it and the time it would involve to implement
     this section has not been implemented.

3. **Orientation of the keypoints:** Once we have the keypoints, we calculate their orientation. That's why we have to
     a window around the keypoint of size `3*1.5*scale where the pixel is located`. In this window we calculate the gradients of each pixel to then obtain their magnitudes and orientations. In a histogram of 36 `bins`, 1 for every 10
     degrees, we are adding the value of the weights of each pixel. To assign the weights, we calculated the average between `1.5*scale`
     and pixel magnitude. Once all the pixels of the window have been iterated around the keypoint, the angle of the is chosen
     `bin` with maximum value as the orientation of the key point. For each of the `bins` that has a value equal to or greater than
     `0.8 of the maximum bin', new key points are created at the same position but with a different orientation.

4. **Construction of the descriptors:** For the construction of the descriptors, an area of `16x16 pixels` must be observed in the
     around the key point. In this area `4x4 descriptors` are created. Within each descriptor a histogram is calculated
     of orientations of `8 bins`. In order to fill the histogram, do the same as in the previous step, the gradients are calculated
     to then calculate the orientations and magnitudes of each pixel. From each orientation of the new histogram of orientations the dominant orientation of the pixel in step **3.** is subtracted so that they are relative to this dominant orientation. Once all the
     histograms of each `4x4` descriptor the `bins` are concatenated resulting in the key point descriptor which
     it is used when you want to match key points from another image.

   Characteristic points of our SIFT:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/manualSIFTResults.png?raw=true"> 

<h1 id="catala"> COMPUTER VISION </h1>

La Visió per Computador es fa servir en aquest projecte per obtenir característiques de les imatges de robot. Aquests punts de caràcter són visualitzats en l'aplicació d'usuari. Aquests s'utilitzaran per a un procés estèreo multivista en futures versions.

En aquest directori de visió per computador trobaràs:

<ol>
<li>computerVisionAnalitics.py: Hem analitzat 3 algorismes diferents per triar quins utilitzaríem en el nostre projecte.</li>
<li>sift.py: Vam implementar l'algorisme SIFT directament del document de David G. Lowe de 2004 i altres fonts com a repte i per a entendre millor el SIFT.</li>
</ol>
<h2> 1. ANÀLISI DE VISIÓ PER COMPUTADOR </h2>

Per escollir els punts característics o `keypoints` hem considerat 3 algorismes: Harris, ORB i SIFT. Tots ells ja estan implantats a la biblioteca openCV Vam decidir triar SIFT perquè és més capaç de detectar punts característics i és invariant a escala. Aquí tenim els punts característics de cada algorisme amb la mateixa imatge:

- Harris:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultHarris.jpg?raw=true">  

- ORB:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultORB.jpg?raw=true">  

- SIFT:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultSIFT.jpg?raw=true">

## SIFT (Scale Invariant Feature Transform)

L'algoritme SIFT és especialment útil per detectar punts característics invariants a canvis d'escala, rotació i il·luminació en una imatge. El procés de detecció es realitza mitjançant diverses etapes. Primerament, s'aplica una 
piràmide d'escala per identificar punts potencials en diferents nivells de resolució. 
Després, s'utilitza un algoritme de detecció de punts clau per identificar les regions amb característiques distintives,
com ara cantonades i regions amb canvis bruscs d'intensitat.
Un cop es detecten els punts clau, l'algoritme SIFT calcula un descriptor per a cada punt. Aquests descriptors són 
vectors numèrics que capturen les característiques locals de la regió entorn de cada punt clau, com ara la direcció del 
gradient i la magnitud. Això permet comparar i emparellar punts característics entre diferents imatges, ja que els 
descriptors són robustos davant de canvis geomètrics i fotomètrics.

L'algoritme SIFT ha estat àmpliament utilitzat en diverses aplicacions de visió per ordinador, com ara la 
correspondència d'imatges, el reconeixement d'objectes i la reconstrucció tridimensional. La seva robustesa i 
invariància a diferents transformacions han contribuït a la seva popularitat i la seva aplicabilitat en diferents àrees.

### SIFT Implementació Manual:
Després de decidir que ens agradaria utilitzar l'algorisme SIFT vam decidir implementar-lo com a repte ja que considerem que d'aquesta manera aprendriem i el comprendriem més encara que al projecte utilitzem el SIFT de OpenCV per temes d'optimització i temps.

L'implementació consta de 4 passos:

1. **Obtenció de key points:** Per l'obtenció de key points, o punts característics, s'ha de convolucionar la imatge amb
    una màscara Gaussiana, donant com a resultat una imatge suavitzada o `escala`. Hem de generar `n` escales per després aconseguir un espai de diferències Gaussianes. Cada imatge suavitzada nova es genera amb una màscara amb la qual té la `sigma` utilitzada en la creació de la imatge suavitzada anterior per un hiperparàmetre `k^n`. Les imatges suavitzades estan agrupades en `octaves`. Les `octaves` es diferencien en el fet que es redueix la resolució. En cada octava els pixeles tenen una resolució de `2^n de l'Octava`. Quan obtenim els espais de Diferències de Gaussianes, restem a cada imatge suavitzada nova a l'anterior, iterem per cada píxel de la imatge resultant i si el píxel és un màxim o un mínim en l'espai `3x3x3` al seu voltant, es considera un keypoint.

2. **Refining keypoint location:** En aquest apartat es refinen breument les posicions dels keypoints, perquè s'obté la 
    posició 'exacta', afegint més desimals a les coordenades del punts característics.
    Per a aconseguir aquesta aproximació, s'han d'implementar la funció de segon ordre de Taylor i la matriu Hessiana. A causa de la poca diferència dels resultats aplicant aquest pas o no aplicant-lo i al temps que implicaria implementar 
    aquest apartat, no s’ha implementat.

3. **Orientació dels keypoints:** Una vegada tenim els key points, calculem quina orientació tenen. Per això, hem de fer
    una finestra al voltant del keypoint de mida `3*1.5*escala on es troba el píxel`. En aquesta finestra calculem els gradients de cada píxel per a continuació aconseguir les seves magnituds i orientacions. En un histograma de 36 `bins`, 1 per cada 10 
    graus, anem afegint el valor dels pesos de cada píxel. Per assignar els pesos, hem calculat la mitja entre `1.5*escala` 
    i la magnitud del píxel. Una vegada iterat tots els píxels de la finestra al voltant del keypoint, es tria l'angle del 
    `bin` amb valor màxim com l’orientació del key point. Per cadascun dels `bins` que tingui un valor igual o major al 
    `0.8 del bin màxim`, es creen nous key points a la mateixa posició però amb l’orientació diferent.

4. **Construcció dels descriptors:** Per la construcció dels descriptors s’ha d'observar una àrea de `16x16 píxels` al 
    voltant del key point. En aquesta àrea es creen `descriptors de 4x4`. Dins de cada descriptor es calcula un histograma
    d'orientacions de `8 bins`. Per tal d’omplir l’histograma es fa el mateix que al pas anterior, es calcula els gradients
    per després calcular les orientacions i magnituds de cada píxel. A cada orientació del nou histograma d'orientacions es resta l'orientació dominant del píxel del pas **3.** perquè siguin relatives a aquesta orientació dominant. Una vegada calculats tots els 
    histogrames de cada descriptor `4x4` es concatenen els `bins` donant com a resultat el descriptor del key point el qual 
    s’utilitza quan es vol fer match amb key points d’una altra imatge.

  Punts característics del nostre SIFT:

  <img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/manualSIFTResults.png?raw=true"> 

<h1 id="castellano"> COMPUTER VISION </h1>

La Visión por Computadora se utiliza en este proyecto para obtener características de las imágenes del robot. Estas características se visualizan en la aplicación de usuario y se utilizarán para un proceso estéreo multivista en futuras versiones.

En este directorio de visión por computadora encontrarás:

<ol>
  <li>computerVisionAnalitics.py: Se han analizado 3 algoritmos diferentes para mejorar la calidad en nuestro proyecto.</li>
  <li>sift.py: Implementamos el algoritmo SIFT directamente del artículo de David G. Lowe de 2004 y otras fuentes, como un desafío y para comprender mejor SIFT.</li>
</ol>
<h2> 1. ANÁLISIS DE VISIÓN POR COMPUTADORA </h2>

Para las características de los puntos o `keypoints`, consideramos 3 algoritmos: Harris, ORB y SIFT. Todos ellos ya están implementados en la biblioteca openCV. Se decide elegir SIFT porque es más capaz de detectar puntos característicos y es invariante a escala. Aquí están los puntos característicos de cada algoritmo con la misma imagen:

- Harris:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultHarris.jpg?raw=true">  

- ORB:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultORB.jpg?raw=true">  

- SIFT:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/resultSIFT.jpg?raw=true">

## SIFT (Scale Invariant Feature Transform)

El algoritmo SIFT es especialmente útil para detectar puntos característicos invariantes a cambios de escalera, rotación e iluminación en una imagen. El proceso de detección se realiza mediante distintas etapas. En primer lugar, se aplica una
pirámide de escalera para identificar puntos potenciales en diferentes niveles de resolución.
Después, se utiliza un algoritmo de detección de puntos clave para identificar a las regiones con características distintivas,
tales como esquinas y regiones con cambios bruscos de intensidad.
Una vez detectados los puntos clave, el algoritmo SIFT calcula un descriptor para cada punto. Estos descriptores son
vectores numéricos que capturan las características locales de la región en torno a cada punto clave, como la dirección del
gradiente y la magnitud. Esto permite comparar y emparejar puntos característicos entre diferentes imágenes, ya que los
descriptores son robustos frente a cambios geométricos y fotométricos.

El algoritmo SIFT ha sido ampliamente utilizado en diversas aplicaciones de visión por ordenador, como la
correspondencia de imágenes, reconocimiento de objetos y reconstrucción tridimensional. Su robustez y
invariancia a distintas transformaciones han contribuido a su popularidad y su aplicabilidad en diferentes áreas.

### SIFT Implementación Manual:
Después de decidir que nos gustaría utilizar el algoritmo SIFT decidimos implementarlo como reto ya que consideramos que de esta forma aprenderíamos y lo comprenderíamos más aunque en el proyecto utilizamos el SIFT de OpenCV para temas de optimización y tiempo.

La implementación consta de 4 pasos:

1. **Obtención de key points:** Para la obtención de key points, o puntos característicos, debe convolucionarse la imagen con
     una máscara Gaussiana, dando como resultado una imagen suavizada o `escala`. Debemos generar `n` escalas para después conseguir un espacio de diferencias Gaussianas. Cada imagen suavizada nueva se genera con una máscara con la que tiene la `sigma` utilizada en la creación de la imagen suavizada anterior por un hiperparámetro `k^n`. Las imágenes suavizadas están agrupadas en octavas. Las octavas se diferencian en que se reduce la resolución. En cada octava los pixeles tienen una resolución de `2^n de la Octava`. Cuando obtenemos los espacios de Diferencias de Gaussianas, restamos a cada imagen suavizada nueva a la anterior, iteramos por cada píxel de la imagen resultante y si el píxel es un máximo o un mínimo en el espacio `3x3x3` a su alrededor, considera un keypoint.

2. **Refining keypoint location:** En este apartado se refinan brevemente las posiciones de los keypoints, porque se obtiene la
     posición 'exacta', añadiendo más desimales a las coordenadas de los puntos característicos.
     Para conseguir esta aproximación, deben implementarse la función de segundo orden de Taylor y la matriz Hessiana. Debido a la poca diferencia de los resultados aplicando este paso o no aplicándolo y al tiempo que implicaría implementar
     este apartado no se ha implementado.

3. **Orientación de los keypoints:** Una vez tenemos los key points, calculamos qué orientación tienen. Por eso, debemos hacer
     una ventana alrededor del keypoint de tamaño `3*1.5*escalera donde se encuentra el píxel`. En esta ventana calculamos los gradientes de cada píxel para a continuación conseguir sus magnitudes y orientaciones. En un histograma de 36 bins, 1 por cada 10
     grados, vamos añadiendo el valor de los pesos de cada píxel. Para asignar los pesos, hemos calculado la media entre `1.5*escala`
     y la magnitud del píxel. Una vez iterado todos los píxeles de la ventana alrededor del keypoint, se elige el ángulo del
     `bin` con valor máximo como la orientación del key point. Por cada uno de los `bins` que tenga un valor igual o mayor al
     `0.8 del bin máximo`, se crean nuevos key points en la misma posición pero con la orientación distinta.

4. **Construcción de los descriptores:** Para la construcción de los descriptores debe observarse un área de `16x16 píxeles` en
     alrededor del key point. En esta área se crean `descriptores de 4x4`. Dentro de cada descriptor se calcula un histograma
     de orientaciones de `8 bins`. Para llenar el histograma se hace lo mismo que en el paso anterior, se calcula los gradientes
     para después calcular las orientaciones y magnitudes de cada píxel. En cada orientación del nuevo histograma de orientaciones se resta la orientación dominante del píxel del paso **3.** para que sean relativas a esa orientación dominante. Una vez calculados todos los
     histogramas de cada descriptor `4x4` se concatienen los `bins` dando como resultado el descriptor del key point el cual
     se utiliza cuando se desea hacer match con key points de otra imagen.

   Puntos característicos de nuestro SIFT:

<img src="https://github.com/GerardGV/MultiArm/blob/43c2da3dd5e04115009f267e393c5cc74e6b2c27/imgReadMe/imgREADME_VC/manualSIFTResults.png?raw=true"> 
