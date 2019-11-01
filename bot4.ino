#include <VirtualWire.h>

#define leftmotor1 3
#define leftmotor2 6
#define rightmotor1 9
#define rightmotor2	10

byte message[VW_MAX_MESSAGE_LEN]; // a buffer to store the incoming messages
byte messageLength = VW_MAX_MESSAGE_LEN; // the size of the message

//returns an array of bytes whose last element matches with code
//byte is a one byte int
byte* receive (byte code, byte len)
{
	Serial.print("Called receive with code ");
	Serial.println(code);
	byte* temp = new byte[len];
	do 
	{
		if(vw_get_message(message, &messageLength)) // Non-blocking
		{
			Serial.print("Received: ");
			for (int i = 0 ; i < messageLength ; i++)
			{
				Serial.write(message[i]);
				temp[i] = message[i];
			}
			Serial.println();
			Serial.println("The array is : ");

			for(int k = 0 ; k < messageLength ; k++)
			{
				Serial.print(temp[k]);
				Serial.print(" ");
			}
			Serial.println();
			if (temp[len - 1] == code)
				break;
		}
	}while(true);
}

void setup() 
{
	Serial.begin(9600);
	// Initialize the IO and ISR
	vw_setup(2000); // Bits per sec
	vw_rx_start(); // Start the receiver
	// put your setup code here, to run once:
	pinMode(leftmotor1, OUTPUT);
	pinMode(leftmotor2, OUTPUT);
	pinMode(rightmotor1, OUTPUT);
	pinMode(rightmotor2, OUTPUT);
}

void rightturn()
{
	digitalWrite(leftmotor1, HIGH);
	digitalWrite(leftmotor2, LOW);
	digitalWrite(rightmotor1, LOW);
	digitalWrite(rightmotor2, HIGH);
}

void leftturn()
{
	digitalWrite(leftmotor1, LOW);
	digitalWrite(leftmotor2, HIGH);
	digitalWrite(rightmotor1, HIGH);
	digitalWrite(rightmotor2, LOW);
}

void forward()
{
	digitalWrite(leftmotor1, HIGH);
	digitalWrite(leftmotor2, LOW);
	digitalWrite(rightmotor1, HIGH);
	digitalWrite(rightmotor2, LOW);
}

void back()
{
	digitalWrite(leftmotor1, LOW);
	digitalWrite(leftmotor2, HIGH);
	digitalWrite(rightmotor1, LOW);
	digitalWrite(rightmotor2, HIGH);
}

void stop()
{
	digitalWrite(leftmotor1, LOW);
	digitalWrite(leftmotor2, LOW);
	digitalWrite(rightmotor1, LOW);
	digitalWrite(rightmotor2, LOW);
}

void loop() 
{
	// put your main code here, to run repeatedly:
	byte* input = receive(123, 2);
	Serial.print("Received : ");
	Serial.println(input[0]);
	
	if (input[0] == 1)
	{
		leftturn();
	}
	else if (input[0] == 2)
	{
		rightturn();
	}
	else if (input[0] == 3)
	{
		forward();
	}
	else if (input[0] == 4)
	{
		back();
	}
	else if (input[0] == 5)
	{
		stop();
	}
}