#ifndef UART_RX_H
#define UART_RX_H

#include "stdint.h"
#include "stm32f1xx_hal.h"
void receive_data(uint8_t data_rx);
void uart_handle(void);
void uart_init(void);

#endif 
