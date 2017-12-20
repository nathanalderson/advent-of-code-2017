#include <iostream>
#include <string>
#include <sstream>
#include <list>
#include <iterator>
#include <cstring>

using namespace std;

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

void spin(int a, char * progs) {
    /* cout << "spin " << a << endl; */
    char end[16] = {};
    memcpy(end, &progs[16-a], a);
    char begin[16] = {};
    memcpy(begin, progs, 16-a);
    memcpy(progs, end, a);
    memcpy(&progs[a], begin, 16-a);
    /* cout << progs << endl; */
}

void exchange(int a, int b, char * progs) {
    /* cout << "exchange " << a << ", " << b << endl; */
    int tmp = progs[a];
    progs[a] = progs[b];
    progs[b] = tmp;
    /* cout << progs << endl; */
}

void partner(char a, char b, char * progs) {
    /* cout << "partner " << a << ", " << b << endl; */
    int a_index;
    int b_index;
    find2(a, b, progs, a_index, b_index);
    int tmp = progs[a_index];
    progs[a_index] = progs[b_index];
    progs[b_index] = tmp;
    /* cout << progs << endl; */
}

void dance(char * progs, list<string> moves) {
    for(string move : moves) {
        if (move[0] == 's') {
            spin(stoi(move.substr(1)), progs);
        } else if (move[0] == 'x') {
            size_t slash = move.find('/');
            int a = stoi(move.substr(1,slash-1));
            int b = stoi(move.substr(slash+1));
            exchange(a, b, progs);
        } else if (move[0] == 'p') {
            partner(move[1], move[3], progs);
        }
    }
}

int main() {
    // TODO: read moves from input file
    list<string> test_moves = split("s1,x3/4,pe/b", ',');
    // TODO: use partial function application to build moves
    // so we don't reparse the moves every time
    char progs[17] = "abcdefghijklmnop";
    dance(progs, test_moves);
    cout << progs << endl;
}
