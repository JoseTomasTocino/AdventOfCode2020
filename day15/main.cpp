#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>

struct NumberNode {
    unsigned long last;
    unsigned long nextToLast;
};

int main()
{
    std::vector<unsigned long> numbers = {1,2,16,19,18,0};
//        std::vector<unsigned long> numbers = {0, 3, 6};
    auto numberCount = numbers.size();

    std::unordered_map<unsigned long, NumberNode> numberMap;

    unsigned long turn = 1;
    unsigned long lastNumber = 0;

    while (turn <= 30000000)
    {
        std::cout << "Turn: " << turn << ". ";

        if (turn - 1 < numberCount)
        {
            lastNumber = numbers[turn - 1];
            std::cout << "Starting number: " << lastNumber << ". ";
            numberMap[lastNumber] = { turn, 0 };
        }

        else
        {
            NumberNode node = numberMap[lastNumber];

            if (node.nextToLast == 0)
            {
                std::cout << "Last number (" << lastNumber << ") first appeareance, current: 0";
                lastNumber = 0;
            }

            else
            {
                auto diff = node.last - node.nextToLast;

                std::cout << "Last number (" << lastNumber << ") already appeared on turns " << node.last << " and " << node.nextToLast << ", diff: " << diff;
                lastNumber = diff;
            }

            if (numberMap.find(lastNumber) == numberMap.end())
            {
                numberMap[lastNumber] = { turn, 0 };
            }

            else
            {
                numberMap[lastNumber].nextToLast = numberMap[lastNumber].last;
                numberMap[lastNumber].last = turn;
            }
        }

        std::cout << std::endl;
        turn += 1;

        if (turn % 10000 == 0)
            std::cerr << turn << std::endl;

    }

    std::cerr << lastNumber << std::endl;
}