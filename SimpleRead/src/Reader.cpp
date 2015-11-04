/* 
 * File:   Reader.cpp
 * Author: Nils
 * 
 * Created on 3. November 2015, 16:18
 */

#include "Reader.h"

Reader::Reader() {
    setup();
}

Reader::~Reader() {
}

int Reader::getAverage(int x, int y, int dist, DepthPixel* pDepth, int width) {
    int value = 0;
    for (int i = y - dist; i <= y + dist; i++)
        value += pDepth[i * width + x];
    return value / (dist * 2 + 1);
}

void Reader::setup() {
    Status rc = OpenNI::initialize();
    if (rc != STATUS_OK) {
        printf("Initialize failed\n%s\n", OpenNI::getExtendedError());
        return;
    }


    rc = device.open(ANY_DEVICE);
    if (rc != STATUS_OK) {
        printf("Couldn't open device\n%s\n", OpenNI::getExtendedError());
        return;
    }



    if (device.getSensorInfo(SENSOR_DEPTH) != NULL) {
        rc = depth.create(device, SENSOR_DEPTH);
        if (rc != STATUS_OK) {
            printf("Couldn't create depth stream\n%s\n", OpenNI::getExtendedError());
            return;
        }
    }

    rc = depth.start();
    if (rc != STATUS_OK) {
        printf("Couldn't start the depth stream\n%s\n", OpenNI::getExtendedError());
        return;
    }


}

int Reader::getRow(int row[]) {
    VideoFrameRef frame;
    
    int changedStreamDummy;
    VideoStream* pStream = &depth;
    Status rc = OpenNI::waitForAnyStream(&pStream, 1, &changedStreamDummy, SAMPLE_READ_WAIT_TIMEOUT);
    if (rc != STATUS_OK) {
        printf("Wait failed! (timeout is %d ms)\n%s\n", SAMPLE_READ_WAIT_TIMEOUT, OpenNI::getExtendedError());
        return 0;
    }

    rc = depth.readFrame(&frame);
    if (rc != STATUS_OK) {
        printf("Read failed!\n%s\n", OpenNI::getExtendedError());
        return 0;
    }

    if (frame.getVideoMode().getPixelFormat() != PIXEL_FORMAT_DEPTH_1_MM && frame.getVideoMode().getPixelFormat() != PIXEL_FORMAT_DEPTH_100_UM) {
        printf("Unexpected frame format\n");
        return 0;
    }

    DepthPixel* pDepth = (DepthPixel*) frame.getData();
    //int middleIndex = (frame.getHeight()+1)*frame.getWidth()/2;

    int y = frame.getHeight() / 2;
    int dist = 2;

    for (int x = 0; x < frame.getWidth(); x++){
        row[x] = getAverage(x, y, dist, pDepth, frame.getWidth());       
    }
    return 1;
}


void Reader::shutdown() {
    depth.stop();
    depth.destroy();
    device.close();
    OpenNI::shutdown();
}

