
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

  int pasos2 = 50; 
  int pasos3 = 50; 
  int pasosp = 50;

  for (int j = 0; j < max(pasos2, pasos3); j++)
  {
    if (j < pasos2)
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

    if (j < pasos3)
    {
      for (int i = 3; i >= 0; i--)
      {
        digitalWrite(IN5, paso[i][0]);
        digitalWrite(IN6, paso[i][1]);
        digitalWrite(IN7, paso[i][2]);
        digitalWrite(IN8, paso[i][3]);
        delay(10);
      }
    }

    if (j < pasosp)
    {
      for (int i = 3; i >= 0; i--)
      {
        digitalWrite(IN9, paso[i][0]);
        digitalWrite(IN10, paso[i][1]);
        digitalWrite(IN11, paso[i][2]);
        digitalWrite(IN12, paso[i][3]);
        delay(10);
      }
    }
  }

  delay(1000);

  int pasos0 = 20;
  int pasos01 = 20; 

  for (int j = 0; j < max(pasos0, pasos01); j++)
  {
    if (j < pasos0)
    {
      for (int i = 3; i >= 0; i--)
      {
        digitalWrite(IN5, paso[i][0]);
        digitalWrite(IN6, paso[i][1]);
        digitalWrite(IN7, paso[i][2]);
        digitalWrite(IN8, paso[i][3]);
        delay(10);
      }
    }

  }
  delay(1000);

  int pasos4 = 30; 
  int pasos5 = 30;
  int pasosp2 = 30; 

  for (int j = 0; j < max(pasos4, pasos5); j++)
  {
    if (j < pasos4)
    {
      for (int i = 3; i >= 0; i--)
      {
        digitalWrite(IN1, paso[i][0]);
        digitalWrite(IN2, paso[i][1]);
        digitalWrite(IN3, paso[i][2]);
        digitalWrite(IN4, paso[i][3]);
        delay(10);
      }
    }

    if (j < pasos5)
    {
      for (int i = 3; i >= 0; i--)
      {
        digitalWrite(IN5, paso[i][0]);
        digitalWrite(IN6, paso[i][1]);
        digitalWrite(IN7, paso[i][2]);
        digitalWrite(IN8, paso[i][3]);
        delay(10);
      }
    }

  }

  delay(1000);

  exit(0);
}
