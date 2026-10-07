#include <charconv>
#include <iostream>
#include <string>
#include <system_error>

// Fixed library observations, not a whole-year parser or external-input interface.
int main() {
    const std::string suffix_text = "2x";
    int suffix_value = 0;
    const auto suffix_result = std::from_chars(
        suffix_text.data(), suffix_text.data() + suffix_text.size(), suffix_value);
    std::cout << std::boolalpha;
    std::cout << "2x: conversion success = " << (suffix_result.ec == std::errc{})
              << ", complete input = "
              << (suffix_result.ptr == suffix_text.data() + suffix_text.size())
              << ", value = " << suffix_value << '\n';

    const std::string negative_text = "-1";
    int negative_value = 0;
    const auto negative_result = std::from_chars(
        negative_text.data(), negative_text.data() + negative_text.size(), negative_value);
    std::cout << "-1: conversion success = " << (negative_result.ec == std::errc{})
              << ", complete input = "
              << (negative_result.ptr == negative_text.data() + negative_text.size())
              << ", value = " << negative_value << '\n';
    std::cout << "Neither input satisfies the whole-year text contract.\n";
}
