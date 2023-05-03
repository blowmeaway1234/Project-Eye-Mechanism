#ifndef MAX7219_H_
#define MAX7219_H_

#include "stm32f1xx_hal.h"
#include <stdint.h>
#include <stdio.h>
#include <math.h>

// define GPIO port and pin for CS
#define CS_PORT GPIOA
#define CS_PIN 4

// define macros for CS control
#define CS_RESET CS_PORT->ODR &= ~(1 << CS_PIN)
#define CS_SET CS_PORT->ODR |= (1 << CS_PIN)

// function 
void init_max7219(void);
void clean_led(void);
void sendData(uint8_t Address, uint8_t Data);
void display_number(uint32_t num);
void display_dot(uint8_t x,uint8_t y);
void display_float(float num, uint8_t dec);
void toggle_intensitive(uint8_t a);
// For matrix led
void display_column_y(uint8_t column_no);
#endif /* MAX7219_H_ */