#include <VirtualWire.h>

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
	vw_setup(2000); // Bits per sec
}

void loop()
{
	if (Serial.available())
	{
		byte input[2] = {Serial.read() - 48, 123};

		Serial.print("Received : ");
		Serial.println(input[0]);

		qsend(input, 2);
		Serial.println("Done sending");
	}
}