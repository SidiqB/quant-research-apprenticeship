// Test transport only: preserve all stdin bytes, including whitespace and NUL.
#include "years.hpp"

#include <iostream>
#include <iterator>
#include <limits>
#include <stdexcept>
#include <string>

int main(int argc, char* argv[]) {
    if (argc == 2 && std::string(argv[1]) == "--int-max") {
        std::cout << std::numeric_limits<int>::max() << '\n';
        return 0;
    }
    if (argc != 1) {
        return 2;
    }
    const std::string text{std::istreambuf_iterator<char>(std::cin),
                           std::istreambuf_iterator<char>()};
    if (std::cin.bad()) {
        return 2;
    }
    try {
        const int years = parse_whole_years(text);
        std::cout << "ok " << years << '\n';
    } catch (const std::invalid_argument&) {
        std::cout << "invalid\n";
    } catch (const std::out_of_range&) {
        std::cout << "range\n";
    }
}
