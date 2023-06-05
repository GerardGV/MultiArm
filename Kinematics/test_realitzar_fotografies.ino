
#define IN1  6
#define IN2  7
#define IN3  8
#define IN4  9

#define IN5  10
#define IN6  11
#define IN7  12
#define IN8  13

#define IN13 0
#define IN14 1
 
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
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  pinMode(IN7, OUTPUT);
  pinMode(IN8, OUTPUT);

  pinMode(IN13, OUTPUT);
  pinMode(IN14, OUTPUT);
}
  
void loop()
{ 

  digitalWrite(IN13, LOW);
  digitalWrite(IN14, LOW);

  //subir
  int p = 300;
  for (int j = 0; j < p; j++)
  {
    for (int i = 0; i < 4; i++)
    {
      digitalWrite(IN5, paso[i][0]);
      digitalWrite(IN6, paso[i][1]);
      digitalWrite(IN7, paso[i][2]);
      digitalWrite(IN8, paso[i][3]);
      delay(10);
    }
  }
  delay(1000);

  //base izquierda
  int p2 = 100;
  for (int j = 0; j < p2; j++)
  {
    for (int i = 3; i >= 0; i--)
    {
      digitalWrite(IN1, paso2[i][0]);
      digitalWrite(IN2, paso2[i][1]);
      digitalWrite(IN3, paso2[i][2]);
      digitalWrite(IN4, paso2[i][3]);
      delay(10);
    }
  }
  delay(3000);

  //base derecha
  int p3 = 150;
  for (int j = 0; j < p3; j++)
  {
    for (int i = 0; i < 4; i++)
    {
      digitalWrite(IN1, paso2[i][0]);
      digitalWrite(IN2, paso2[i][1]);
      digitalWrite(IN3, paso2[i][2]);
      digitalWrite(IN4, paso2[i][3]);
      delay(10);
    }
  }
  delay(1000);


  exit(0);
}
