CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=-std=c++11
LDFLAGS=
LDLIBS=

SRCS=day16.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: run

run: day16
	@./day16

day16: $(OBJS)
	@$(CXX) $(LDFLAGS) -o day16 $(OBJS) $(LDLIBS) 

day16.o: day16.cpp

clean:
	@$(RM) $(OBJS)

distclean: clean
	@$(RM) day16
