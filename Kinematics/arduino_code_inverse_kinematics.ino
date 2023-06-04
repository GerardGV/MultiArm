#include <AccelStepper.h>
#include <math.h>
#include <Stepper.h>

#define stepsPerRevolution 2048
#define IN1  10
#define IN2  11
#define IN3  12
#define IN4  13

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
double largo1 = 1.2;
double largo2 = 0.8;
double angulo1, angulo2;
double Pi = 3.14159;

AccelStepper stepper2(AccelStepper::FULL4WIRE, 2, 3, 4, 5);
AccelStepper stepper1(AccelStepper::FULL4WIRE, 6, 7, 8, 9);
Stepper stepper3(2048, 10, 11, 12, 13);


double distancia(double x, double y) {
  return sqrt(x * x + y * y);
}

double radianesAGrados(double radianes) {
  return radianes * 180.0 / Pi;
}

double leyDelCoseno(double A, double B, double C) {

  double div = (A * A + B * B - C * C) / (2 * A * B);
  if (div < -1.0)
    div = -1.0;
  if (div > 1.0)
    div = 1.0;

  return acos(div);
}

int angleToStep(float angle) {
  float degreesPerStep = 360.0 / stepsPerRevolution;
  return round(angle / degreesPerStep);
}

void calculate(int x, int y, int z)
{
  double dist = distancia(x, y);
  double D1 = atan2(y, x);
  int D2 = leyDelCoseno(dist, largo1, largo2);
  double a1Radianes = D1 + D2;
  double a2Radianes = leyDelCoseno(largo1, largo2, dist);

  angulo1 = radianesAGrados(a1Radianes);
  angulo2 = radianesAGrados(a2Radianes);

  int angulo1_1 = angleToStep(angulo1);
  int angulo2_2 = angleToStep(angulo2);

  stepper1.moveTo(angulo1_1);
  stepper2.moveTo(angulo2_2);

  while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
  }

  int pasos1 = 10;

  for (int j = 0; j < pasos1; j++)
  {
    for (int i = 0; i < z; i++)
    {
      digitalWrite(IN1, paso[i][0]);
      digitalWrite(IN2, paso[i][1]);
      digitalWrite(IN3, paso[i][2]);
      digitalWrite(IN4, paso[i][3]);
      delay(10);
    }
  }
  delay(1000);
}

void setup() {
  Serial.begin(9600);
  stepper1.setMaxSpeed(1000);
  stepper1.setAcceleration(500);
  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(500);
  stepper1.setCurrentPosition(0);
  stepper2.setCurrentPosition(0);
  stepper3.setSpeed(100);
  delay(2000);
}

void loop() {
  serial.print("Introdueix coord X: ");
  while (Serial.available() == 0) {
    // Espera hasta que haya datos disponibles en el búfer de entrada serial
  }
  float X = Serial.parseFloat();

  serial.print("Introdueix coord Y: ");
  while (Serial.available() == 0) {
    // Espera hasta que haya datos disponibles en el búfer de entrada serial
  }
  float Y = Serial.parseFloat();

  serial.print("Introdueix coord Z: ");
  while (Serial.available() == 0) {
    // Espera hasta que haya datos disponibles en el búfer de entrada serial
  }
  float Z = Serial.parseFloat();

  while(Serial.available() == 0){
    char caracter = Serial.read();

    if (isdigit(caracter)) {
      numero = numero * 10 + (caracter - '0');
  }

  calculate(X, Y, Z);
  delay(1000);
}
