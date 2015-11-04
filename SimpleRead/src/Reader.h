/* 
 * File:   Reader.h
 * Author: Nils
 *
 * Created on 3. November 2015, 16:18
 */

#include <stdio.h>
#include <OpenNI.h>





#define SAMPLE_READ_WAIT_TIMEOUT 2000 //2000ms

#ifndef READER_H
#define	READER_H

using namespace openni;
using namespace std;

class Reader {
public:
    Reader();
    virtual ~Reader();
    int getRow(int row[]);
    void shutdown();
private:
    Device device;
    VideoStream depth;
    
    int getAverage(int x, int y, int dist, DepthPixel* pDepth, int width);
    void setup();
};

#endif	/* READER_H */

