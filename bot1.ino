#include <VirtualWire.h>

#define leftmotor1 3
#define leftmotor2 6
#define rightmotor1 9
#define rightmotor2	10

#define MOVE_DELAY 100
#define ANGLE_DELAY 200
#define LED_BLINK_TIME 200
#define CHECKSUM 12
#define BOT_NUMBER 1

bool debug = true;

byte message[VW_MAX_MESSAGE_LEN]; // a buffer to store the incoming messages
byte messageLength = VW_MAX_MESSAGE_LEN; // the size of the message

//returns an array of bytes whose last element matches with code
//byte is a one byte int
byte* receive ()
{
	if (debug)
	{
		Serial.println("Called receive.");
	}
	byte* temp = new byte[1];
	do
	{
		if(vw_get_message(message, &messageLength)) // Non-blocking
		{
			if (debug)
				Serial.print("Received : ");

			for (int i = 0 ; i < messageLength ; i++)
			{
				if (debug)
					Serial.print(message[i]);
			}

			temp[0] = message[BOT_NUMBER - 1];
			byte checksum = message[messageLength - 1];

			if (debug)
			{
				Serial.print("Extracted : ");
				Serial.println(temp[0]);
				Serial.print("Checksum is : ");
				Serial.println(checksum);
			}
			if (checksum == CHECKSUM)
				break;
		}
	}while(true);

	return temp;
}

void setup() 
{
	if (debug)
	{
		Serial.begin(9600);
	}
	// Initialize the IO and ISR
	vw_set_rx_pin(12);
	vw_setup(4000); // Bits per sec
	vw_rx_start(); // Start the receiver
	// put your setup code here, to run once:
	pinMode(leftmotor1, OUTPUT);
	pinMode(leftmotor2, OUTPUT);
	pinMode(rightmotor1, OUTPUT);
	pinMode(rightmotor2, OUTPUT);
	pinMode(13, OUTPUT); //for LED
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

void back()
{
	digitalWrite(leftmotor1, HIGH);
	digitalWrite(leftmotor2, LOW);
	digitalWrite(rightmotor1, HIGH);
	digitalWrite(rightmotor2, LOW);
}

void forward()
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
	byte* input = receive();
	if (debug)
	{
		Serial.print("Received : ");
		Serial.println(input[0]);
	}
	digitalWrite(13, HIGH);
	delay(LED_BLINK_TIME);
	digitalWrite(13, LOW);
	
	if (input[0] == 1)
	{
		leftturn();
		delay(ANGLE_DELAY);
		stop();
	}
	else if (input[0] == 2)
	{
		rightturn();
		delay(ANGLE_DELAY);
		stop();
	}
	else if (input[0] == 3)
	{
		forward();
		delay(MOVE_DELAY);
		stop();
	}
	else if (input[0] == 4)
	{
		back();
		delay(MOVE_DELAY);
		stop();
	}
	else if (input[0] == 5)
	{
		stop();
	}
	else if (input[0] == 6)
	{
		digitalWrite(13, HIGH);
	}
}