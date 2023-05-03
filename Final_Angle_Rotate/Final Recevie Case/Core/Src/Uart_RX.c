#include "Uart_RX.h"

#define MAX_DATA_UART 100
static uint8_t uart_buff[MAX_DATA_UART];
static uint8_t uart_len;
uint8_t uart_flag =0;
void receive_data(uint8_t data_rx)
{
	//Check data receive done
	if(data_rx == '\n')
	{
		uart_flag=1;
	}
	else //Check not don't continue
	{
		uart_buff[uart_len++]=data_rx;
	}
}
//Handel
void uart_handle()
{
	if(uart_flag)
	{
		uart_flag=0;
	}
}
// Init uart command line
void uart_init()
{
	
}
