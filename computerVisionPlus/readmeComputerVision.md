### Autors | Autores | Authors:
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
## 1. COMPUTER VISION ANALITICS

To choose the caracteristic points or `keypoints` we considered 3 algorithms: Harris, ORB and SIFT. All of them are already implemented in the library openCV We decided to choose SIFT because it is more capable of detect caracteristic points and it is scale invariant. Here we have the caracteristic points for each algorithm with the same image:

- Harris:

  ![img](https://lh3.googleusercontent.com/ravi3roIZ7aLTwf3P2vsZva8BeNnI1RHElBRdgIHtZQRBznhGILvu8mHO_F0fXsC2d3BNNnJ_97WXdd18aSAGbcin-oYyGuHdPIO19dfhhzDpRhoCZ3nzmeLhvIf1KZQeIVPHTJIAt0aRqSidugUw1AP1w=nw)

- ORB:

  ![img](https://lh6.googleusercontent.com/6KdwpTvLMS6RkGyFPHIWYtyzdstVRQn1GmTqOavmmZAcMon-nvrZQQTGCanBO38auYhabZPmAZjfcQXCw9rwi6G4AbPo_5K2cCdHTG0M4-GzzuxuAaL3zaDZPDIfEpJJ2FkIcWIUL47h_iPeVcT5bQyCAw=nw)

- SIFT:

![img](https://lh5.googleusercontent.com/xF2jlF30FSXITav2iSe8U7JzsVzF2BtWVT9t5eWqaGbFaCWCUNlGOFFqDbPKd-LJ_8DyPN-J0Cwkjfrz4-iVexKQSZjo30jeynIQbl3KvdC7aaSjZRceMSG5X9sGYh4GEFJSFcjpG0d35Dg9pxVEba1d4w=nw)

 

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
Desprès de decidir que ens agradaria utilitzar l'algorisme SIFT vam decidir implementar-lo com a repte ja que considerem que d'aquesta manera aprendriem i el comprendriem més encara que al projecte utilitzem el SIFT de OpenCV per temes d'optimització i temps.

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

  ![img](/Users/gerard/Desktop/A_LHm_I8-IBZRWyQJHa_mgYzCqK3TlEtlep9kyw3gk7RUtI182HPk4CWiBG9En95kKXhhBPWwUSfg1zLea8nv10DdeleepKGBTS4UOVwOzMFbCy9XxwKgpo7szICQnsgTKcgsPxIqo3lLpTmhnswaa6h4w=nw.png)

## Procés de reconstrucció - Modelatge 2D a partir de dues imatges utilitzant SIFT.

Tal i com s'explica al títol, en aquest apartat explicarem quin procés hem realitzat per tal d'acomplir el repte proposat de generar un mapa de punts 3D donades dues imatges. Agafarem l'imatge utilitzada al video del README.md per l'explicació.

### Passos per a la reconstrucció:

1. **Dades proporcionades:** Primerament, rebrem dues imatges, en el nostre projecte del robot, les imatges proporcionades seràn les dues que realitza la càmera de la Raspberry Pi.
  El robot prendra les imatges del següent rostre com es veu en el video:

  ![rostro-humano-atado-con-alambre-ROTADO](/Users/gerard/Desktop/rostro-humano-atado-con-alambre-ROTADO.jpg)
2. **Calcular SIFT:** A continuació es realitza l'algorisme SIFT, el qual ja sabem com funciona degut a l'explicació anterior. Aplicarem l'algorisme SIFT per a cada imatge per tal d'obtenir els `keypoints` i `descriptors` de cada una.
3. **Matching:** Una vegada amb els `keypoints` i `descriptors` de cada imatge, realitzarem el matching, on busquem identificar ` keypoints` que apareguin en les dues imatges. Per fer aixó, nosaltres hem utilitzat `knnMatch`from `FlannBasedMatcher` de OpenCV per comparar els `descriptors ` del keypoints d'una imatge amb els de l'altre imatge. Si els `descriptors `de 2 `keypoints` fan match signfica que són el mateix.
4. **Good Matches:** Del pas anterior, hem trobat molts matches, és a dir, molts punts característics que es trobaven alhora en les dues imatges, però el més segur és que molts d'aquests siguin càlculs erronis degut a la similaritud de diversos sectors de la imatge. És per això per el que realtizarem un filtratge dels matches per tal de quedar-nos amb els "Good Matches" o matches confiables. Per calcular-los, apliquem el test de Lowe's (Lowe's Ratio Test) o "prova de ràtio de pendent". 
5. **First Reconstruction**: NO ES NECESSARI per la version actual 2D. Aquesta funcio es de cara a l'ampliació on volem veure en 3D el rostre i interactuar amb ell. De cara al futur el que fa una triangulació amb dades de la camara que treu de l'imatge per pasar els punts de 2D a 3D. 

Es visualitza el resultat:![WhatsApp Image 2023-06-05 at 15.31.14](/Users/gerard/Downloads/WhatsApp Image 2023-06-05 at 15.31.14.jpeg)
