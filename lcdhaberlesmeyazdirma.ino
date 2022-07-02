
// include the library code:
#include <LiquidCrystal_I2C.h>
#include <stdio.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin();
  // initialize the serial communications:
  Serial.begin(9600);
}

void loop() {
  // when characters arrive over the serial port...
  if (Serial.available()) {
    // read all the available characters
    while (Serial.available() > 0) {
      // display each character to the LCD

      Serial.setTimeout(50);
      int x = Serial.parseInt();
      int y = Serial.parseInt();
      int flag = Serial.parseInt();
      char str[10];
      char str2[10]; 
      char str3[20];

      if(flag ==1)  
      { 
        lcd.setCursor(0,0);
        lcd.print("x = ");
        lcd.setCursor(0,1);
        lcd.print("y = ");
        
        if(x >= 0)
        {
          sprintf(str,"%d          ",x);
        }
        else{
          sprintf(str,"%d          ",x);
        }
       
        if(y >= 0)
        {
          sprintf(str2,"%d         ",y);
        }
        else{
          sprintf(str2,"%d         ",y);
        }
        
        lcd.setCursor(4,0);
        lcd.print(str);
        lcd.setCursor(4,1);
        lcd.print(str2);
      }
      else if (flag == 0)
      {
        lcd.clear();
        lcd.setCursor(0,0);
        sprintf(str3,"Top bulunamadi. ");
        lcd.print(str3);
      }
   
     
      
    }
  }
}
