#include <wiringPi.h>

#include <string>
#include <fstream>
#include <iostream>
#include <valarray>
#include <ctime>
#include <unistd.h>
#include <sys/signal.h>
#include <cstdlib>

#include "../cpp/driver/everloop_image.h"
#include "../cpp/driver/everloop.h"
#include "../cpp/driver/microphone_array.h"
#include "../cpp/driver/wishbone_bus.h"

#define CHAN 0

namespace hal = matrix_hal;

uint16_t numLEDs(uint16_t channels, uint16_t subVal) {
	return channels - subVal;
}

//int main(int argc, const char *argv[]) {
int main(int argc, char *argv[]) {
	//std::string name = argv[1];
	
	//process PID argument of python classification script
	//the python script waits on a SIGUSR1 set below in record state
	char* PID_string;
	int PID_int = 0;
	if (argc < 2) {
		std::cout << "Missing PID argument of Python classification script" << std::endl;
		exit(1);
	} else {
		PID_string = argv[1];
		PID_int = std::atoi(PID_string);
		std::cout << "Classification script PID: ";
		std::cout << PID_int << std::endl;
	}
	
	hal::WishboneBus bus;
	bus.SpiInit();

	hal::MicrophoneArray mics;
	mics.Setup(&bus);

	hal::Everloop everloop;
	everloop.Setup(&bus);

	hal::EverloopImage image1d;

	uint16_t seconds_to_record = 1; //1 second voice segments for testing
	uint64_t instantE = 0;
	uint64_t avgEnergy = 0;
	std::valarray<uint64_t> localAverage (20);
	localAverage = 0;

	//std::time_t result = std::time(nullptr);
	//time_t tStamp = std::asctime(std::localtime(&result));

	//mics.setgain(8); //not sure i need this.  think this is set in driver
	//

	std::cout << "Begin Recording..." << std::endl;

	uint16_t channels = numLEDs(mics.Channels(), CHAN);

	//int16_t buffer[mics.Channels() + 1][seconds_to_record * mics.SamplingRate()];
	int16_t buffer[channels+1][seconds_to_record * mics.SamplingRate()]; //start with 1 mic
	//if we only end up doing 1 mic, we can adjust driver cpp/drivers/microphone_array.cpp to have channels set to 1, not 8.

	mics.CalculateDelays(0,0,1000,320*1000);
	//int j=0;
	//bool flag = true;

	//FIX HERE, NOT GATHERING DATA CORRECTLY, NEED THE FOR LOOK ON LINE 63 TO BE REPLICATED IN CODE
	//BELOW!
	uint32_t stepComp = seconds_to_record * mics.SamplingRate();
	mics.SetGain(8);

	bool standbyFlag = true;
	bool recordFlag = false;
	bool lightFlag = true;
	bool convertFlag = false;
	uint32_t step = 0;

	while (1) {
		mics.Read(); //this reads all the channels, so will have to adjust read() in cpp/drivers/microphone_array.cpp to only read 1 microphone in order to save power
		if(standbyFlag) {
			if(lightFlag) {
				image1d.leds[0].red = 0;
				image1d.leds[0].green = 0;
				image1d.leds[0].blue = 20;
				everloop.Write(&image1d);
				lightFlag = false;
			}
			instantE = 0;
			for(uint32_t s = 0; s < mics.NumberOfSamples(); s++) {
				instantE = instantE + (mics.At(s,0)) * (mics.At(s,0));
			}
			/*localAverage[j%20] = instantE;
			avgEnergy = 0;
			for(auto& data : localAverage) {
				avgEnergy = (avgEnergy + data);
			}
			j++;*/
			//std::cout << "Instant Energy: " << instantE << std::endl;
			if(instantE > 400000000) { //threshold here needs to be adjusted
				standbyFlag = false;
				recordFlag = true;
				lightFlag = true;
				//convertFlag = true; //don't forget to remove this later
			}
		}
		if(recordFlag) {
			if(lightFlag) {
				image1d.leds[0].red = 20;
				image1d.leds[0].green = 0;
				image1d.leds[0].blue = 0;
				everloop.Write(&image1d);
				lightFlag = false;
			}
			//std::cout << "Begin recording..." << std::endl;
			for(uint32_t s = 0; s < mics.NumberOfSamples(); s++) {
				for(uint16_t c = 0; c < channels; c++) {
					buffer[c][step] = mics.At(s,c);
				}
				buffer[channels][step] = mics.Beam(s);
				step++;
			}
			if(step == stepComp) {
				recordFlag = false;
				convertFlag = true;
				image1d.leds[0].red = 0;
				image1d.leds[0].green = 20;
				image1d.leds[0].blue = 0;
				everloop.Write(&image1d);
				lightFlag = true;
			}
		}
		if(convertFlag) {
			for (uint16_t c = 0; c < channels; c++) {
				std::string filename = "mic_" + std::to_string(mics.SamplingRate()) +	"_s16le_channel_" + std::to_string(c) + ".raw";
				std::ofstream os(filename, std::ofstream::binary);
				os.write((const char*)buffer[c], stepComp * sizeof(int16_t));
				os.close();
			}
			system("./convertAudio.sh");
			std::cout << "WAV file created" << std::endl;
			standbyFlag = true;
			convertFlag = false;
			
			std::cout << "send SIGUSR1" << std::endl;
			kill(PID_int, SIGUSR1);
			step = 0;
		}
	}
}



