#include "years.hpp"

#include <charconv>
#include <stdexcept>
#include <system_error>

int parse_whole_years(const std::string& text) {
    if (text.empty()) {
        throw std::invalid_argument("years must contain at least one digit");
    }
    for (const char character : text) {
        if (character < '0' || character > '9') {
            throw std::invalid_argument("years must contain only ASCII decimal digits");
        }
    }
    int years = 0;
    const char* end = text.data() + text.size();
    const auto result = std::from_chars(text.data(), end, years, 10);
    if (result.ec == std::errc::result_out_of_range) {
        throw std::out_of_range("years exceed the int range");
    }
    if (result.ec != std::errc{} || result.ptr != end) {
        throw std::invalid_argument("years must be a complete decimal integer");
    }
    return years;
}
