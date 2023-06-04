
 
// Definimos los pines donde tenemos conectadas las bobinas
#define IN1  6
#define IN2  7
#define IN3  8
#define IN4  9
#define IN5  2
#define IN6  3
#define IN7  4
#define IN8  5
#define IN9  10
#define IN10  11
#define IN11  12
#define IN12  13
#define IN13 0
#define IN14 1
 
// Secuencia de pasos (par máximo)
int paso[4][4] =
{
  {1, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 1},
  {1, 0, 0, 1}
};

int paso2[4][4] =
{
  {0, 0, 1, 1},
  {1, 0, 0, 1},
  {1, 1, 0, 0},
  {0, 1, 1, 0}
};
 
void setup()
{
  // Todos los pines en modo salida
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  pinMode(IN7, OUTPUT);
  pinMode(IN8, OUTPUT);

  pinMode(IN9, OUTPUT);
  pinMode(IN10, OUTPUT);
  pinMode(IN11, OUTPUT);
  pinMode(IN12, OUTPUT);

  pinMode(IN13, OUTPUT);
  pinMode(IN14, OUTPUT);
}
  
void loop()
{ 

  digitalWrite(IN13, LOW);
  digitalWrite(IN14, LOW);
  //subir
  int pasos1 = 50; // Cantidad de pasos a mover

  for (int j = 0; j < pasos1; j++)
  {
    for (int i = 0; i < 4; i++)
    {
      digitalWrite(IN9, paso[i][0]);
      digitalWrite(IN10, paso[i][1]);
      digitalWrite(IN11, paso[i][2]);
      digitalWrite(IN12, paso[i][3]);
      delay(10);
    }
  }
  delay(1000); // Espera 1 segundo antes de reiniciar el movimiento

  //deracha
  int pasos2 = 280; // Cantidad de pasos a mover
  
  for (int j = 0; j < pasos2; j++)
  {
    for (int i = 0; i < 4; i++)
    {
      digitalWrite(IN1, paso[i][0]);
      digitalWrite(IN2, paso[i][1]);
      digitalWrite(IN3, paso[i][2]);
      digitalWrite(IN4, paso[i][3]);
      delay(10);
    }
  }
  delay(1000); // Espera 1 segundo antes de reiniciar el movimiento

  //bajar
  int pasos4 = 60; // Cantidad de pasos a mover

  for (int j = 0; j < pasos4; j++)
  {
    for (int i = 3; i >= 0; i--)
    {
      digitalWrite(IN9, paso2[i][0]);
      digitalWrite(IN10, paso2[i][1]);
      digitalWrite(IN11, paso2[i][2]);
      digitalWrite(IN12, paso2[i][3]);
      delay(10);
    }
  }
  delay(1000);


  //coger cabezal
  digitalWrite(IN13, HIGH);
  digitalWrite(IN14, LOW);
  delay(2000);
  digitalWrite(IN13, LOW);
  digitalWrite(IN14, LOW);

  //subir
  int pasos5 = 60; // Cantidad de pasos a mover

  for (int j = 0; j < pasos5; j++)
  {
    for (int i = 0; i < 4; i++)
    {
      digitalWrite(IN9, paso[i][0]);
      digitalWrite(IN10, paso[i][1]);
      digitalWrite(IN11, paso[i][2]);
      digitalWrite(IN12, paso[i][3]);
      delay(10);
    }
  }
  delay(4000); // Espera 1 segundo antes de reiniciar el movimiento

  //bajar
  int pasos6 = 50; // Cantidad de pasos a mover

  for (int j = 0; j < pasos6; j++)
  {
    for (int i = 3; i >= 0; i--)
    {
      digitalWrite(IN9, paso2[i][0]);
      digitalWrite(IN10, paso2[i][1]);
      digitalWrite(IN11, paso2[i][2]);
      digitalWrite(IN12, paso2[i][3]);
      delay(10);
    }
  }
  delay(1000);

  //dejar cabezal
  digitalWrite(IN13, HIGH);
  digitalWrite(IN14, HIGH);
  delay(2000);
  digitalWrite(IN13, LOW);
  digitalWrite(IN14, LOW);

  int pasos8 = 60; // Cantidad de pasos a mover

  for (int j = 0; j < pasos8; j++)
  {
    for (int i = 0; i < 4; i++)
    {
      digitalWrite(IN9, paso[i][0]);
      digitalWrite(IN10, paso[i][1]);
      digitalWrite(IN11, paso[i][2]);
      digitalWrite(IN12, paso[i][3]);
      delay(10);
    }
  }
  delay(4000);

  exit(0);
}
