//include modules

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "driver/uart.h"
#include "string.h"
#include "driver/gpio.h"

#include <unistd.h>
#include <socket.h>
#include <stdio.h>
#include <arpa/inet.h>

//main program
int main(){

    //UART SETUP

    const int uart_buffer_size = (1024*2);
    QueueHandle_t uart_queue;

    const uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    };

    uart_driver_install(UART_NUM_1, uart_buffer_size, uart_buffer_size, 10, &uart_queue, 0)

    uart_param_config(UART_NUM_1, &uart_config);

    uart_set_pin(UART_NUM_1, 1, 0, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);

    //TCP SETUP

    int clientSocket;
    struct sockaddr_in server_addr;
    char server_message[100], client_message[100];

    memset(server_message,'\0',sizeof(server_message));
    memset(client_message,'\0',sizeof(client_message));


    clientSocket = socket(AF_INET, SOCK_STREAM, 0);

    if(clientSocket < 0){
        printf("Unable to create socket\n");
        return -1;
    }

    printf("Socket created successfully\n");

    // Set port and IP:
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons("PORT OF SERVER");
    server_addr.sin_addr.s_addr = inet_addr("IPADDRESS OF SERVER");

    // Bind to the set port and IP:
    if(connect(clientSocket, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
        printf("Unable to connect\n");
        return -1;
    }
    printf("Connected with server successfully\n");
    

    //MAIN RECIEVE AND FORWARD LOOP

    while(1){
        
            uint8_t data[128];
            int length = 0;
            ESP_ERROR_CHECK(uart_get_buffered_data_len(uart_num, (size_t*)&length));
            length = uart_read_bytes(uart_num, data, length, 100);

            if (length > 0) {
                send(clientSocket, data, length, 0);
                uart_flush(UART_NUM_1);
            }

            else{
                return -1;
            }

            
            while(1){
                ssize_t bytes_read = recv(clientSocket, server_message, sizeof(server_message), MSG_DONTWAIT);
                if (bytes_read == -1) {
                continue;
                }
                else {
                break;
                }
            }

            uart_write_bytes(UART_NUM_1, (const char*)server_message, strlen(server_message));

            sleep(60); 


    }


}


