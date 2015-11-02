include /home/pi/devel/OpenNI2/ThirdParty/PSCommon/BuildSystem/CommonDefs.mak

BIN_DIR = ../Bin

INC_DIRS = \
	/home/pi/devel/OpenNI2/Include \
	/home/pi/devel/OpenNI2/ThirdParty/GL/ \
	/home/pi/devel/OpenNI2/Samples/Common

SRC_FILES = *.cpp

ifeq ("$(OSTYPE)","Darwin")
	CFLAGS += -DMACOS
	LDFLAGS += -framework OpenGL -framework GLUT
else
	CFLAGS += -DUNIX -DGLX_GLXEXT_LEGACY
	USED_LIBS += glut GL
endif

USED_LIBS += OpenNI2

EXE_NAME = SimpleViewer

CFLAGS += -Wall

include /home/pi/devel/OpenNI2/ThirdParty/PSCommon/BuildSystem/CommonCppMakefile
