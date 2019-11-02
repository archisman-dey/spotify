#include <VirtualWire.h>

byte input[2];

void qsend (byte *message, byte len)
{
	Serial.print("Sending : ");

	for (int i = 0; i < len; i++)
	{
		Serial.print(message[i]);
		Serial.print(" ");
	}

	Serial.println();
	vw_send((byte *)message, len);
	vw_wait_tx(); // Wait until the whole message is gone
}

void setup()
{ 
	Serial.begin(9600);
	// Initialize the IO and ISR
	vw_set_ptt_inverted(true);
	vw_set_tx_pin(12);
	vw_setup(4000); // Bits per sec
}

void loop()
{
	if (Serial.available())
	{
		int in = Serial.readStringUntil('\n').toInt();
		Serial.println(in);
		input[0] = in/1000 ;
		input[1] = in%1000;

		Serial.print("Received : ");
		Serial.println(input[0]);

		qsend(input, 2);
		Serial.println("Done sending");
	}
}