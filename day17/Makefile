CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=-std=c++11
LDFLAGS=
LDLIBS=

SRCS=day17.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: run

run: day17
	@./day17

day17: $(OBJS)
	@$(CXX) $(LDFLAGS) -o day17 $(OBJS) $(LDLIBS) 

day17.o: day17.cpp

clean:
	@$(RM) $(OBJS)

distclean: clean
	@$(RM) day17
