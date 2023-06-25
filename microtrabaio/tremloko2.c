#include <stdio.h>
#include <stdlib.h>
#include <avr/io.h>

#define FOSC 16000000U // Clock Speed
#define BAUD 9600
#define MYUBRR FOSC / 16 / BAUD - 1

#define SENSOR (1 << PD2)
#define ULTRASONIC 1
#define BUZZER PD4

#define ROTATIVO PB1


unsigned int Leitura_AD; // ADC
float tensao; // Tensao Ultrassonico
float dist;

//variaveis dos calculos
int gotas = 0;
unsigned int segundos = 0;
unsigned int cont = 0;
bool contar;
unsigned int infusao_volume;
unsigned int infusao_tempo;
double fluxo_definido = 0;
double fluxo_real = 0;
double erro = 0;
double potencia;
int estado = 0;


//variaveis de uart
char msg_tx[20];
char msg_rx[32];

int pos_msg_rx = 0;
int tamanho_msg_rx = 3;
unsigned int x = 0, valor = 0;

void rotativo_init() {
    // Configura o pino rotativo como saída
    DDRB |= (1 << ROTATIVO);
    
    // Configura o Timer/Counter1 para operar em modo rotativo rápida (8 bits)
    TCCR1A |= (1 << COM1A1) | (1 << WGM10);
    TCCR1B |= (1 << CS10) | (1 << WGM12);

    // Configura o valor máximo do contador para 255
    OCR1A = 255;
}

void rotativo_set_potencia(uint8_t potencia) {
    OCR1B = potencia;
}

// contar gotas
ISR(INT0_vect)
{
	if (gotas == 0)
	{
		TCCR0B = (1 << CS01);
	}
	gotas ++;
}

// timer
ISR(TIMER0_COMPA_vect)
{
	cont++;
	if (cont == 10000)
	{
		cont = 0;
		segundos++;
	}
}

ISR(ADC_vect)
{
	// Detecção de bolhas
	Leitura_AD = ADC;  // Armazenamento da leitura

	tensao = (Leitura_AD * 5) / 1023.0;  // Cálculo da Tensão
	dist = (tensao * 20) / 5.0;  // Cálculo da distância
	itoa(dist, msg_tx, 10);

	// Se detectado algo a menos de 5cm
	if (dist < 5)
	{
		estado = 4;
	}
	UART_Transmit("Dist: ");
	UART_Transmit(msg_tx);
	UART_Transmit("\n");
}


void UART_Init(unsigned int ubrr)
{
	//Configura a baud rate
	UBRR0H = (unsigned char)(ubrr >> 8);
	UBRR0L = (unsigned char)ubrr;
	//Habilita a recepcao, tranmissao e interrupcao na recepcao
	UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
	//Configura o formato da mensagem: 8 bits de dados e 1 bits de stop
	UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void UART_Transmit(char *dados)
{
	//Envia todos os caracteres do buffer dados ate chegar um final de linha
	while (*dados != 0)
	{
		while (!(UCSR0A & (1 << UDRE0))); // Aguarda a transmissão acabar
		//Escreve o caractere no registro de tranmissão
		UDR0 = *dados;
		//Passa para o próximo caractere do buffer dados
		dados++;
	}
}

ISR(USART_RX_vect)
{
	//Escreve o valor recebido pela UART na posição pos_msg_rx do buffer msg_rx
	msg_rx[pos_msg_rx++] = UDR0;
	if (pos_msg_rx == tamanho_msg_rx)
		pos_msg_rx = 0;
}

int main(void)
{
	UART_Init(MYUBRR);
	//ativa entradas e saidas
	
	DDRD |= (ROTATIVO + BUZZER);
	PORTD &= ~(ROTATIVO + BUZZER);
	PORTD |= SENSOR;
	
	EICRA = (1 << ISC01);
	EIMSK = (1 << INT0);

	//ctc
	TCCR0A = (1 << WGM01);
	TCCR0B = 0;
	OCR0A = 199;
	TIMSK0 = (1 << OCIE0A);
	
	rotativo_init();

	//adc
	ADMUX = (0 << REFS1) + (1 << REFS0); //Utiliza 5V como referência (1023)
	ADCSRA = (1 << ADEN) + (1 << ADPS2) + (1 << ADPS1) + (1 << ADPS0); //Habilita ADC e PS 128 (10 bits)
	ADCSRA |= (1 << ADIE);  // Habilita interrupção do ADC
	ADCSRA |= (1 << ADSC);  // Inicia a conversão do ADC
	ADCSRB = 0; //Conversão Única

	sei();

	while(1)
	{
	switch (estado)
		{
		case 0:
			UART_Transmit("Entre com o Volume, 3 digitos e em ml:\n");
			x = 0;
			valor = 0;
			msg_rx[0] = 0;
			msg_rx[1] = 0;
			msg_rx[2] = 0;
			while (x == 0)
			{
				valor = (msg_rx[0] - 48) * 100 + (msg_rx[1] - 48) * 10 + (msg_rx[2]) * 1;
				if ((valor > 0) && (valor < 999))
				{
					infusao_volume = valor;
					x = 1;
				}
			}

			UART_Transmit("foi\n");
			_delay_ms(500);

			UART_Transmit("Entre com o Tempo de indusao, 3 digitos em minutos:\n");

			msg_rx[0] = 0;
			msg_rx[1] = 0;
			msg_rx[2] = 0;
			valor = 0;
			x = 0;

			while (x == 0)
			{
				valor = (msg_rx[0] - 48) * 100 + (msg_rx[1] - 48) * 10 + (msg_rx[2]) * 1;
				if ((valor > 0) && (valor < 10000))
				{
					infusao_tempo = valor;
					x = 1;
				}
			}

			UART_Transmit("foi\n");
			_delay_ms(500);

			fluxo_definido = (infusao_volume * 1.0) / ((infusao_tempo * 1.0) / 60);
			itoa(fluxo_definido, msg_tx, 10);
			UART_Transmit(msg_tx);
			UART_Transmit("ml/h\n");
			_delay_ms(500);

			potencia = (fluxo_definido / 450) * 100.0;
			OCR2A = int(potencia);
			// Faz o motor girar no sentido horário
        	rotativo_set_potencia(200); // Ajuste o valor do ciclo de trabalho conforme necessário
        	_delay_ms(2000);

        	// Faz o motor girar no sentido anti-horário
        	rotativo_set_potencia(75); // Ajuste o valor do ciclo de trabalho conforme necessário
        	_delay_ms(2000);

			UART_Transmit("Potencia: ");
			itoa(potencia, msg_tx, 10);
			UART_Transmit(msg_tx);
			UART_Transmit("%\n");
			_delay_ms(500);

			UART_Transmit("Fluxo e potencia definidos!\n");
			_delay_ms(500);

			estado = 1;
			break;

		case 1:
			UART_Transmit("Alterar parametros? (sim | nao) \n");
			msg_rx[0] = 0;
			msg_rx[1] = 0;
			msg_rx[2] = 0;
			x = 0;

			while (x == 0)
			{
				if ((msg_rx[0] == 's') && (msg_rx[1] == 'i') && (msg_rx[2] == 'm'))
				{
					estado = 0;
					x = 1;
					break;
				}
				else if ((msg_rx[0] == 'n') && (msg_rx[1] == 'a') && (msg_rx[2] == 'o'))
				{
					estado = 2;
					x = 1;
					break;
				}
			}

		case 2:
			UART_Transmit("Detectando gotas...\n");
			gotas = 0;

			_delay_ms(1000);
			UART_Transmit("\nFluxo Real: ");
			fluxo_real = (gotas * 3600) * 0.05;
			itoa(fluxo_real, msg_tx, 10);
			UART_Transmit(msg_tx);
			UART_Transmit("ml/h\n");

			itoa(gotas, msg_tx, 10);
			UART_Transmit(msg_tx);
			UART_Transmit(" gotas");
			UART_Transmit(" em 1 segundo");

			TCCR0B = 0;
			gotas = 0;
			UART_Transmit("\n");
			UART_Transmit("\n");
			estado = 3;
			break;

		case 3:
			itoa(dist, msg_tx, 10);
			erro = ((fluxo_real - fluxo_definido) / fluxo_definido) * 100;
			itoa(erro, msg_tx, 10);

			UART_Transmit("Erro: ");
			UART_Transmit(msg_tx);
			UART_Transmit("% \n");
			estado = 1;
			break;

		case 4:
			PORTD |= BUZZER;
			OCR0A = 0;
			UART_Transmit("Bolhas detectadas! \n");
			_delay_ms(2000);
			PORTD &= ~BUZZER;
			estado = 1;
			
			break;
		default:
			estado = 1;
			break;
		}
		ADMUX = (ADMUX & 0xF8) | ULTRASONIC; // Determinar o pino de leitura
	}
}

