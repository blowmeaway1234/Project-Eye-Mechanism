#include "max_7219.h"
//SPI 1
extern SPI_HandleTypeDef hspi1;

uint8_t buf[2];

//Send data void
void sendData(uint8_t Address,uint8_t Data)
{
	buf[0] = Address;
	buf[1] = Data;
	CS_RESET;
	HAL_SPI_Transmit(&hspi1,buf,2,10);
	CS_SET;
}
//Init Max 7219
void init_max7219()
{
	//Select Decode mode:
	sendData(0x09,0x00);
	//Set intensity: 
	sendData(0x0A,9);
	//Scan limit: get all number
	sendData(0x0B,7);
	//No shutdown, turn off display test:
	sendData(0x0C,1);
	sendData(0x0F,0);
}	
void display_dot(uint8_t x,uint8_t y)
{
    sendData(y+1, (3<<x));
    sendData(y+2, (3<<x));
}
// Remove 0
void display_number(uint32_t num){
    // count the number of digits
    uint8_t count=1;
    uint32_t n = num;
    while(n/10){
        count++;
        n = n/10;
    }
    // set scanlimit
    sendData(0x0B, count-1);
    // dislay number
    for(int i=0; i<count;i++){
        sendData(i+1,num%10);
        num = num/10;
    }
}
void display_float(float num, uint8_t dec)
	{
    int32_t integerPart = num;
    int32_t fractionalPart = (num - integerPart) * pow(10,dec);
    int32_t number = integerPart*pow(10,dec) + fractionalPart;
    // count the number of digits
    uint8_t count=1;
    int32_t n = number;
    while(n/10){
        count++;
        n = n/10;
    }
    // set scanlimit
    sendData(0x0B, count-1);
    // dislay number
    for(int i=0; i<count;i++)
		{
        if(i==dec)
            sendData(i+1,(number%10)|0x80); // turn on dot segment 
        else
            sendData(i+1,number%10);
        number = number/10;
    }
	}
void clean_led(void)
{
	sendData(0x08,0);
	sendData(0x07,0);
	sendData(0x06,0);
	sendData(0x05,0);
	sendData(0x04,0);
	sendData(0x03,0);
	sendData(0x02,0);
	sendData(0x01,0);
	sendData(0x00,0);
}
void toggle_intensitive(uint8_t a)
{
	for (int i = 0;i<a;i++)
	{
	sendData(0x0A,9);
	HAL_Delay(50);
	sendData(0x0A,4);
	HAL_Delay(50);
	}
}
void display_column_y(uint8_t column_no)
{
	for (uint8_t i = 1; i <= 8; i++)
	{
    sendData(i, 1 << column_no); // dich chuyen den vi tri y = i voi x = 7

	}
}