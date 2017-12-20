#include <iostream>
#include <string>
#include <sstream>
#include <list>
#include <iterator>
#include <cstring>
#include <fstream>
#include <functional>

using namespace std;
using namespace std::placeholders;

template<typename Out>
void split(const string &s, char delim, Out result) {
    stringstream ss(s);
    string item;
    while (getline(ss, item, delim)) {
        *(result++) = item;
    }
}

list<string> split(const string &s, char delim) {
    list<string> elems;
    split(s, delim, back_inserter(elems));
    return elems;
}

void find2(char a, char b, char const * progs, int& a_index, int& b_index) {
    a_index = -1;
    b_index = -1;
    for(int i = 0; i < 16; ++i) {
        if (progs[i] == a)
            a_index = i;
        else if (progs[i] == b)
            b_index = i;
        if (a_index != -1 && b_index != -1)
            break;
    }
}

class Move {
public:
    virtual void move(char * progs) = 0;
};

class Spin: public Move {
    int a;
public:
    Spin(int a_): a(a_) {}
    void move(char * progs) {
        /* cout << "spin " << a << endl; */
        char begin[16] = {};
        memcpy(begin, progs, 16-a);
        memcpy(progs, &progs[16-a], a);
        memcpy(&progs[a], begin, 16-a);
        /* cout << progs << endl; */
    }
};

class Exchange: public Move {
    int a,b;
public:
    Exchange(int a_, int b_): a(a_), b(b_) {}
    void move(char * progs) {
        /* cout << "exchange " << a << ", " << b << endl; */
        int tmp = progs[a];
        progs[a] = progs[b];
        progs[b] = tmp;
        /* cout << progs << endl; */
    }
};

class Partner: public Move {
    int a,b;
public:
    Partner(int a_, int b_): a(a_), b(b_) {}
    void move(char * progs) {
        /* cout << "partner " << a << ", " << b << endl; */
        int a_index;
        int b_index;
        find2(a, b, progs, a_index, b_index);
        int tmp = progs[a_index];
        progs[a_index] = progs[b_index];
        progs[b_index] = tmp;
        /* cout << progs << endl; */
    }
};

Move * to_move(string s) {
    if (s[0] == 's') {
        Spin * spin = new Spin(stoi(s.substr(1)));
        return spin;
    } else if (s[0] == 'x') {
        size_t slash = s.find('/');
        int a = stoi(s.substr(1,slash-1));
        int b = stoi(s.substr(slash+1));
        Exchange * exchange = new Exchange(a, b);
        return exchange;
    } else if (s[0] == 'p') {
        Partner * partner = new Partner(s[1], s[3]);
        return partner;
    }
}

void dance(char * progs, list<Move *> moves) {
    for(Move * move : moves) {
        move->move(progs);
    }
}

list<Move *> get_moves() {
    ifstream inFile;
    inFile.open("/home/nalderso/projects/advent-of-code-2017/day16/input");
    string raw;
    if (!inFile) {
        cerr << "Unable to open file";
        exit(-1);
    }
    inFile >> raw;
    inFile.close();
    list<string> raw_moves = split(raw, ',');
    list<Move *> moves;
    for(string s : raw_moves) {
        moves.push_back(to_move(s));
    }
    return moves;
}

int main() {
    list<Move *> moves = get_moves();
    char progs[17] = "abcdefghijklmnop";
    dance(progs, moves);
    cout << "part 1: " << progs << endl;
    for (int i = 0; i < 1000000000 - 1; i++) {
        if (i % 1000 == 0) {
            cout << "round " << i << endl;
        }
        dance(progs, moves);
    }
    cout << "part 2: " << progs << endl;
}

