#include <FastLED.h>

#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_LEDS    300
#define DATA_PIN    3
#define BRIGHTNESS  255

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() { 
    FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.clear();  // clear all pixel data
    FastLED.show();
}

void loop() {
}
