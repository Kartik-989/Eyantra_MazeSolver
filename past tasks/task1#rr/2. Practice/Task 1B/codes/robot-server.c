/*
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1B of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
*/

/*
* Team ID:			[ 4695 ]
* Author List:		[ Kartik,Kapil ]
* Filename:			robot-server.c
* Functions:		socket_create, receive_from_send_to_client
* 					[ Comma separated list of functions in this file ]
* Global variables:	SERVER_PORT, RX_BUFFER_SIZE, TX_BUFFER_SIZE, MAXCHAR,
* 					dest_addr, source_addr, rx_buffer, tx_buffer,
* 					ipv4_addr_str, ipv4_addr_str_client, listen_sock, line_data, input_fp, output_fp,
*					ptr

* 					[ List of global variables defined in this file ]
*/


// Include necessary header files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>


// Constants defined
#define SERVER_PORT 3333
#define RX_BUFFER_SIZE 1024
#define TX_BUFFER_SIZE 1024

#define MAXCHAR 1000				// max characters to read from txt file

// Global variables
struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;

char rx_buffer[RX_BUFFER_SIZE];		// buffer to store data from client
char tx_buffer[RX_BUFFER_SIZE];		// buffer to store data to be sent to client

char ipv4_addr_str[128];			// buffer to store IPv4 addresses as string
char ipv4_addr_str_client[128];		// buffer to store IPv4 addresses as string

int listen_sock;

char line_data[MAXCHAR];

FILE *input_fp, *output_fp;
int ptr=2;


/*
* Function Name:	socket_create
* Inputs:			dest_addr [ structure type for destination address ]
* 					source_addr [ structure type for source address ]
* Outputs: 			my_sock [ socket value, if connection is properly created ]
* Purpose: 			the function creates the socket connection with the server
* Example call: 	int sock = socket_create(dest_addr, source_addr);
*/
int socket_create(struct sockaddr_in dest_addr, struct sockaddr_in source_addr){
	int my_sock;
	int sock;
	int addr_family;
	int ip_protocol;
	int len;

	dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(SERVER_PORT);
	addr_family = AF_INET;
	ip_protocol = IPPROTO_IP;

	sock=socket(addr_family,SOCK_STREAM,ip_protocol);  //creating a socket 
	
	if(sock==-1){
		printf("socket error\n");
	}
	else{
		printf("socket created\n");
	}
	/*******  binding socket to an adderress   *********/
	if((bind(sock,(struct sockaddr*)&dest_addr,sizeof(dest_addr)))==-1){
		printf("socket binded error \n");
	}
	else {
		printf("socket binded\n");
	}
	/********* listning for client ********/
	if(listen(sock,5)==-1){
		printf("lisning error\n");
	}
	else {
		printf("listning for client\n");	
	}
	/**********  Accept request from client ************/
    len=sizeof(source_addr);
	my_sock=accept(sock,(struct sockaddr*)&source_addr,&len);
	if(my_sock!=-1){
		printf("  accepted\n" );
		
	}
	
	return my_sock;
}


/*
* Function Name:	receive_from_send_to_client
* Inputs:			sock [ socket value, if connection is properly created ]
* Outputs: 			None
* Purpose: 			the function receives the data from server and updates the 'rx_buffer'
*					variable with it, sends the obstacle position based on obstacle_pos.txt
*					file and sends this information to the client in the provided format.
* Example call: 	receive_from_send_to_client(sock);
*/
int receive_from_send_to_client(int sock){
	int x,y,length,flag=0,flagx=1,flagy=1;
	/****** read recived data from client and put it into an buffer**********/
	x=read(sock,rx_buffer,sizeof(rx_buffer));
	if(x>0){
    	printf("data recived %s\n",rx_buffer);
		}
		rewind(input_fp);

/******** to check the obstacle for a maze in file  and make required formet an send data to client********/
	while(fgets(line_data, MAXCHAR, input_fp)!=NULL){
		if(rx_buffer[0]==line_data[0]){
			flag=1;
			printf("%s\n%d\n",line_data,ptr);
			length=strlen(line_data);
			printf("%d",length);
			if((line_data[ptr]=='\r')||(line_data[ptr]=='\n')){
			
				ptr=2;
				char tx_buffer[]= "@$@";
				y=write(sock,tx_buffer,sizeof(tx_buffer));
					if(y>0){
						printf("data sent1 %s\n",tx_buffer);
						
					}
			}
			else{
				
				while(line_data[ptr]!=')'){
					ptr=ptr+1;
					}
				if(line_data[ptr-2]==','){
					flagy=0;
					}
				if(flagy==0&&line_data[ptr-4]=='('){
					flagx=0;
					}
				if(flagy==1&&line_data[ptr-5]=='('){
					flagx==0;
					}
				
				if(flagx==0&&flagy==0){
					char tx_buffer[]="@( , )@";
					tx_buffer[2]=line_data[ptr-3];
					tx_buffer[4]=line_data[ptr-1];
					y=write(sock,tx_buffer,sizeof(tx_buffer));
					if(y>0){
						printf("data sent2 %s\n",tx_buffer);
					}
				}

				else if(flagx==1&&flagy==0){
					char tx_buffer[]="@(  , )@";
					tx_buffer[2]=line_data[ptr-4];
					tx_buffer[3]=line_data[ptr-3];
					tx_buffer[5]=line_data[ptr-1];
					y=write(sock,tx_buffer,sizeof(tx_buffer));
					if(y>0){
						printf("data sent2 %s\n",tx_buffer);
					}
				}

				else if (flagx==0&&flagy==1){
					char tx_buffer[]="@( ,  )@";
					tx_buffer[2]=line_data[ptr-4];
					tx_buffer[4]=line_data[ptr-2];
					tx_buffer[5]=line_data[ptr-1];
					y=write(sock,tx_buffer,sizeof(tx_buffer));
					if(y>0){
						printf("data sent2 %s\n",tx_buffer);
					}
				}

				else if(flagx==1&&flagy==1){
					 char tx_buffer[]="@(  ,  )@";
					tx_buffer[2]=line_data[ptr-5];
					tx_buffer[3]=line_data[ptr-4];
					tx_buffer[5]=line_data[ptr-2];
					tx_buffer[6]=line_data[ptr-1];
					y=write(sock,tx_buffer,sizeof(tx_buffer));
					if(y>0){
						printf("data sent2 %s\n",tx_buffer);
					}
				}
					
				
				ptr=ptr+1;
				
			}
			break;

		}
	}
	if(flag==0){	
	char tx_buffer[]="@$@";
    y=write(sock,tx_buffer,sizeof(tx_buffer));
	if(y>0){
		printf("data sent3 %s\n",tx_buffer);
	}

	}
	
	
	return 0;

}


/*
* Function Name:	main()
* Inputs:			None
* Outputs: 			None
* Purpose: 			the function solves Task 1B problem statement by making call to
* 					functions socket_create() and receive_from_send_to_client()
*/
int main() {
    char *input_file_name = "obstacle_pos.txt";
	char *output_file_name = "data_from_client.txt";

	// Create socket and accept connection from client
	int sock = socket_create(dest_addr, source_addr);
	
	input_fp = fopen(input_file_name, "r");

	if (input_fp == NULL){
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}
    
	fgets(line_data, MAXCHAR, input_fp);

	output_fp = fopen(output_file_name, "w");

	if (output_fp == NULL){
		printf("Could not open file %s\n",output_file_name);
		return 1;
	}

	while (1) {
       
		// Receive and send data from client and get the new shortest path
		receive_from_send_to_client(sock);

		// NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANGE HERE
		fputs(rx_buffer, output_fp);
		fputs("\n", output_fp);

	}

	return 0;
}

