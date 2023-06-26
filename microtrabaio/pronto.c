#include <stdio.h>
#include <stdlib.h>
#include <avr/io.h>

#define FOSC 16000000U
#define BAUD 9600
#define MYUBRR FOSC / 16 / BAUD - 1

//sensor, buzzer e motor
#define SENSOR (1 << PD2)
#define BUZZER PD4
#define ROTATIVO (1 << PD6)

// ADC
unsigned int Leitura_AD; 
float distancia;

//variaveis dos calculos
int gotas = 0;
unsigned int segundos = 0;
unsigned int infusao_volume;
unsigned int infusao_tempo;
double fluxo_definido = 0;
double fluxo_real = 0;
double erro = 0;
double potencia;

//flags e auxiliares
int estado, x, cont = 0;
unsigned int leitura;
bool funcionando = true;

//variaveis do uart
char msg_tx[20];
char msg_rx[32];
int pos_msg_rx = 0;
int tamanho_msg_rx = 3;
unsigned int valor = 0;

//funcoes adc
void ADC_init(void)
{
	ADMUX = (1 << REFS0);
	ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
}

int ADC_read(int ch)
{
	char i;
	int ADC_temp = 0;
	int ADC_read = 0;
	ch &= 0x07;
	ADMUX = (ADMUX & 0xF8) | ch;
	ADCSRA |= (1 << ADSC);
	while (!(ADCSRA & (1 << ADIF)));
	for (i = 0; i < 8; i++)
	{
		ADCSRA |= (1 << ADSC);
		while (!(ADCSRA & (1 << ADIF)));
		ADC_temp = ADCL;
		ADC_temp += (ADCH << 8);
		ADC_read += ADC_temp;
	}
	ADC_read = (ADC_read / 8);
	return ADC_read;
}

//inits
void sensor_init()
{
	PORTD |= SENSOR;
	EICRA = (1 << ISC01);
	EIMSK = (1 << INT0);
}

void timer_init()
{
	TCCR2A = (1 << WGM21);
	TCCR2B = (1 << CS22) | (1 << CS21) | (1 << CS20);
	OCR2A = 199;
	TIMSK2 = (1 << OCIE2A);
}

void rotativo_init()
{
	DDRD |= ROTATIVO;
	PORTD &= ~ROTATIVO;
	TCCR0A |= (1 << WGM01) | (1 << WGM00) | (1 << COM0A1);
	TCCR0B = 1;
	OCR0A = 0;
}

void UART_Init(unsigned int ubrr)
{
	// Configura uma taxa de transmissao
	UBRR0H = (unsigned char)(ubrr >> 8);
	UBRR0L = (unsigned char)ubrr;

	// Habilita a recepcao, transmissao e interrupcao na recepcao
	UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);

	// Configura o formato da mensagem: 8 bits de dados e 1 bit de stop
	UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

//uart
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

int main(void)
{
	//inits
	UART_Init(MYUBRR);
	sensor_init();
	timer_init();
	ADC_init();
	rotativo_init();
	sei();

	
	while(funcionando == true)
	{
		switch (estado)
		{
		case 0:
			//entrada de dados
			UART_Transmit("Entre com o Volume, 3 digitos e em ml:\n");
			x = 0;
			valor = 0;
			msg_rx[0] = 0;
			msg_rx[1] = 0;
			msg_rx[2] = 0;
			while (x == 0)
			{
				valor = (msg_rx[0] - 48) * 100 + (msg_rx[1] - 48) * 10 + (msg_rx[2] - 48) * 1;
				if ((valor > 0) && (valor < 999))
				{
					infusao_volume = valor;
					x = 1;
				}
			}
			UART_Transmit("Entre com o Tempo de indusao, 3 digitos em minutos:\n");
			
			msg_rx[0] = 0;
			msg_rx[1] = 0;
			msg_rx[2] = 0;
			valor = 0;
			x = 0;

			while (x == 0)
			{
				valor = (msg_rx[0] - 48) * 100 + (msg_rx[1] - 48) * 10 + (msg_rx[2] - 48) * 1;
				if ((valor > 0) && (valor < 10000))
				{
					infusao_tempo = valor;
					x = 1;
				}
			}
			
			//definicao de fluxo
			fluxo_definido = (infusao_volume * 1.0) / ((infusao_tempo * 1.0) / 60);

			//altera o motor
			potencia = (fluxo_definido / 450);
			OCR0A = (int)(potencia * 255);

			//
			UART_Transmit("Potencia: ");
			itoa(potencia * 100.0, msg_tx, 10);
			UART_Transmit(msg_tx);
			UART_Transmit("%\n");

			UART_Transmit("Fluxo e potencia definidos!\n");

			if(funcionando == true)
				estado = 1;
			break;

		case 1:
			//fazer mudancas nos parametros
			UART_Transmit("Alterar parametros? (sim | nao) \n");
			msg_rx[0] = 0;
			msg_rx[1] = 0;
			msg_rx[2] = 0;
			x = 0;
			if(funcionando == true)
			{
				while (x == 0)
				{
					if ((msg_rx[0] == 's') && (msg_rx[1] == 'i') && (msg_rx[2] == 'm'))
					{
						UART_Transmit("sim\n");
						estado = 0;
						x = 1;
						break;
					}
					if ((msg_rx[0] == 'n') && (msg_rx[1] == 'a') && (msg_rx[2] == 'o'))
					{
						UART_Transmit("nao\n");
						estado = 2;
						x = 1;
						break;
					}

				}
			}

			break;

		case 2:
			//detecta as gotas e mostra os calculos
			UART_Transmit("Detectando gotas...\n");
			gotas = 0;
			_delay_ms(1000);
			UART_Transmit("\nFluxo Real: ");
			fluxo_real = (gotas * 3600) * 0.05;
			itoa(gotas, msg_tx, 10);
			UART_Transmit(msg_tx);
			UART_Transmit(" gotas");
			UART_Transmit(" em 1 segundo");
			TCCR0B = 0;
			gotas = 0;
			UART_Transmit("\n");
			UART_Transmit("\n");
			if(funcionando == true)
				estado = 3;

			break;

		case 3:
			//mostra o erro
			erro = ((fluxo_real - fluxo_definido) / fluxo_definido) * 100;
			itoa(erro, msg_tx, 10);
			UART_Transmit("Erro: ");
			UART_Transmit(msg_tx);
			UART_Transmit("% \n");
			if(funcionando == true)
				estado = 1;
			break;
		case 4:
			UART_Transmit("\nBOLHAS DETECTADAS!!!\n");
			break;
		
		default:
			estado = 0;
			break;
		}
	}
}

//ISRs

//conta gotas
ISR(INT0_vect)
{
	if (gotas == 0)
	{
		TCCR0B = (1 << CS01);
	}
	gotas++;

}

//usart
ISR(USART_RX_vect)
{
	msg_rx[pos_msg_rx++] = UDR0;
	if (pos_msg_rx == tamanho_msg_rx)
		pos_msg_rx = 0;
}

//timer de tempo
ISR(TIMER2_COMPA_vect)
{
	if(funcionando == true)
	{
		//contagem de segundos
		cont++;
		if (cont == 1000)
		{
			cont = 0;
			segundos ++;
			int X = segundos;
		}
		//detecta bolhas pelo potenciometro
		leitura = ADC_read(ADC4D);
		distancia = leitura * 20.0 / 1023;
		if(distancia <= 5)
		{
			PORTD |= BUZZER; //liga buzzer
			estado = 4;
			UART_Transmit("\nBOLHAS DETECTADAS!!!\n");
			OCR0A = 0; //para motor
			funcionando = false;
		}
	}
}
