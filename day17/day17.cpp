#include <algorithm>
#include <iostream>
#include <string>
#include <sstream>
#include <list>
#include <iterator>
#include <cstring>
#include <fstream>
#include <functional>
#include <cassert>

using namespace std;

struct Result {
    int value_after_last_insert;
    int value_after_zero;
};

Result play(int stepsize, int rounds) {
    list<int> buff = { 0 };
    auto pos = buff.begin();
    for (int i = 1; i <= rounds; ++i) {
        if (i % 100000 == 0) {
            cout << "round " << i << endl;
        }
        for(int i = 0; i < stepsize; ++i) {
            ++pos;
            if(pos == buff.end()) {
                pos = buff.begin();
            }
        }
        pos = buff.insert(++pos, i);
        /* cout << "insert " << i << endl; */
        /* for (auto v : buff) { */
        /*     cout << v << ", "; */
        /* } */
        /* cout << endl; */
    }
    ++pos;
    if(pos == buff.end()) {
        pos = buff.begin();
    }
    Result result;
    result.value_after_last_insert = *pos;
    result.value_after_zero = *(++find(buff.begin(), buff.end(), 0));
    return result;
}

int main() {
    assert(play(3, 2017).value_after_last_insert == 638);
    Result result1 = play(316, 2017);
    cout << "part 1 = " << result1.value_after_last_insert << endl;
    Result result2 = play(316, 50000000);
    cout << "part 2 = " << result2.value_after_zero << endl;
}

