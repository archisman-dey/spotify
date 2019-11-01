#include <VirtualWire.h>

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
	// put your setup code here, to run once:

}

void loop() 
{
	// put your main code here, to run repeatedly:

}