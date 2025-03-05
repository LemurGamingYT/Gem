/*******************************************************************************************
*
*   raylib [text] example - Unicode
*
*   Example complexity rating: [★★★★] 4/4
*
*   Example originally created with raylib 2.5, last time updated with raylib 4.0
*
*   Example contributed by Vlad Adrian (@demizdor) and reviewed by Ramon Santamaria (@raysan5)
*
*   Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
*   BSD-like license that allows static linking with closed source software
*
*   Copyright (c) 2019-2025 Vlad Adrian (@demizdor) and Ramon Santamaria (@raysan5)
*
********************************************************************************************/

#include "raylib.h"

#include <stdio.h>
#include <string.h>

#define SIZEOF(A) (sizeof(A)/sizeof(A[0]))
#define EMOJI_PER_WIDTH 8
#define EMOJI_PER_HEIGHT 4

// String containing 180 emoji codepoints separated by a '\0' char
const char *const emojiCodepoints = "\xF0\x9F\x8C\x80\x00\xF0\x9F\x98\x80\x00\xF0\x9F\x98\x82\x00\xF0\x9F\xA4\xA3\x00\xF0\x9F\x98\x83\x00\xF0\x9F\x98\x86\x00\xF0\x9F\x98\x89\x00"
    "\xF0\x9F\x98\x8B\x00\xF0\x9F\x98\x8E\x00\xF0\x9F\x98\x8D\x00\xF0\x9F\x98\x98\x00\xF0\x9F\x98\x97\x00\xF0\x9F\x98\x99\x00\xF0\x9F\x98\x9A\x00\xF0\x9F\x99\x82\x00"
    "\xF0\x9F\xA4\x97\x00\xF0\x9F\xA4\xA9\x00\xF0\x9F\xA4\x94\x00\xF0\x9F\xA4\xA8\x00\xF0\x9F\x98\x90\x00\xF0\x9F\x98\x91\x00\xF0\x9F\x98\xB6\x00\xF0\x9F\x99\x84\x00"
    "\xF0\x9F\x98\x8F\x00\xF0\x9F\x98\xA3\x00\xF0\x9F\x98\xA5\x00\xF0\x9F\x98\xAE\x00\xF0\x9F\xA4\x90\x00\xF0\x9F\x98\xAF\x00\xF0\x9F\x98\xAA\x00\xF0\x9F\x98\xAB\x00"
    "\xF0\x9F\x98\xB4\x00\xF0\x9F\x98\x8C\x00\xF0\x9F\x98\x9B\x00\xF0\x9F\x98\x9D\x00\xF0\x9F\xA4\xA4\x00\xF0\x9F\x98\x92\x00\xF0\x9F\x98\x95\x00\xF0\x9F\x99\x83\x00"
    "\xF0\x9F\xA4\x91\x00\xF0\x9F\x98\xB2\x00\xF0\x9F\x99\x81\x00\xF0\x9F\x98\x96\x00\xF0\x9F\x98\x9E\x00\xF0\x9F\x98\x9F\x00\xF0\x9F\x98\xA4\x00\xF0\x9F\x98\xA2\x00"
    "\xF0\x9F\x98\xAD\x00\xF0\x9F\x98\xA6\x00\xF0\x9F\x98\xA9\x00\xF0\x9F\xA4\xAF\x00\xF0\x9F\x98\xAC\x00\xF0\x9F\x98\xB0\x00\xF0\x9F\x98\xB1\x00\xF0\x9F\x98\xB3\x00"
    "\xF0\x9F\xA4\xAA\x00\xF0\x9F\x98\xB5\x00\xF0\x9F\x98\xA1\x00\xF0\x9F\x98\xA0\x00\xF0\x9F\xA4\xAC\x00\xF0\x9F\x98\xB7\x00\xF0\x9F\xA4\x92\x00\xF0\x9F\xA4\x95\x00"
    "\xF0\x9F\xA4\xA2\x00\xF0\x9F\xA4\xAE\x00\xF0\x9F\xA4\xA7\x00\xF0\x9F\x98\x87\x00\xF0\x9F\xA4\xA0\x00\xF0\x9F\xA4\xAB\x00\xF0\x9F\xA4\xAD\x00\xF0\x9F\xA7\x90\x00"
    "\xF0\x9F\xA4\x93\x00\xF0\x9F\x98\x88\x00\xF0\x9F\x91\xBF\x00\xF0\x9F\x91\xB9\x00\xF0\x9F\x91\xBA\x00\xF0\x9F\x92\x80\x00\xF0\x9F\x91\xBB\x00\xF0\x9F\x91\xBD\x00"
    "\xF0\x9F\x91\xBE\x00\xF0\x9F\xA4\x96\x00\xF0\x9F\x92\xA9\x00\xF0\x9F\x98\xBA\x00\xF0\x9F\x98\xB8\x00\xF0\x9F\x98\xB9\x00\xF0\x9F\x98\xBB\x00\xF0\x9F\x98\xBD\x00"
    "\xF0\x9F\x99\x80\x00\xF0\x9F\x98\xBF\x00\xF0\x9F\x8C\xBE\x00\xF0\x9F\x8C\xBF\x00\xF0\x9F\x8D\x80\x00\xF0\x9F\x8D\x83\x00\xF0\x9F\x8D\x87\x00\xF0\x9F\x8D\x93\x00"
    "\xF0\x9F\xA5\x9D\x00\xF0\x9F\x8D\x85\x00\xF0\x9F\xA5\xA5\x00\xF0\x9F\xA5\x91\x00\xF0\x9F\x8D\x86\x00\xF0\x9F\xA5\x94\x00\xF0\x9F\xA5\x95\x00\xF0\x9F\x8C\xBD\x00"
    "\xF0\x9F\x8C\xB6\x00\xF0\x9F\xA5\x92\x00\xF0\x9F\xA5\xA6\x00\xF0\x9F\x8D\x84\x00\xF0\x9F\xA5\x9C\x00\xF0\x9F\x8C\xB0\x00\xF0\x9F\x8D\x9E\x00\xF0\x9F\xA5\x90\x00"
    "\xF0\x9F\xA5\x96\x00\xF0\x9F\xA5\xA8\x00\xF0\x9F\xA5\x9E\x00\xF0\x9F\xA7\x80\x00\xF0\x9F\x8D\x96\x00\xF0\x9F\x8D\x97\x00\xF0\x9F\xA5\xA9\x00\xF0\x9F\xA5\x93\x00"
    "\xF0\x9F\x8D\x94\x00\xF0\x9F\x8D\x9F\x00\xF0\x9F\x8D\x95\x00\xF0\x9F\x8C\xAD\x00\xF0\x9F\xA5\xAA\x00\xF0\x9F\x8C\xAE\x00\xF0\x9F\x8C\xAF\x00\xF0\x9F\xA5\x99\x00"
    "\xF0\x9F\xA5\x9A\x00\xF0\x9F\x8D\xB3\x00\xF0\x9F\xA5\x98\x00\xF0\x9F\x8D\xB2\x00\xF0\x9F\xA5\xA3\x00\xF0\x9F\xA5\x97\x00\xF0\x9F\x8D\xBF\x00\xF0\x9F\xA5\xAB\x00"
    "\xF0\x9F\x8D\xB1\x00\xF0\x9F\x8D\x98\x00\xF0\x9F\x8D\x9D\x00\xF0\x9F\x8D\xA0\x00\xF0\x9F\x8D\xA2\x00\xF0\x9F\x8D\xA5\x00\xF0\x9F\x8D\xA1\x00\xF0\x9F\xA5\x9F\x00"
    "\xF0\x9F\xA5\xA1\x00\xF0\x9F\x8D\xA6\x00\xF0\x9F\x8D\xAA\x00\xF0\x9F\x8E\x82\x00\xF0\x9F\x8D\xB0\x00\xF0\x9F\xA5\xA7\x00\xF0\x9F\x8D\xAB\x00\xF0\x9F\x8D\xAF\x00"
    "\xF0\x9F\x8D\xBC\x00\xF0\x9F\xA5\x9B\x00\xF0\x9F\x8D\xB5\x00\xF0\x9F\x8D\xB6\x00\xF0\x9F\x8D\xBE\x00\xF0\x9F\x8D\xB7\x00\xF0\x9F\x8D\xBB\x00\xF0\x9F\xA5\x82\x00"
    "\xF0\x9F\xA5\x83\x00\xF0\x9F\xA5\xA4\x00\xF0\x9F\xA5\xA2\x00\xF0\x9F\x91\x81\x00\xF0\x9F\x91\x85\x00\xF0\x9F\x91\x84\x00\xF0\x9F\x92\x8B\x00\xF0\x9F\x92\x98\x00"
    "\xF0\x9F\x92\x93\x00\xF0\x9F\x92\x97\x00\xF0\x9F\x92\x99\x00\xF0\x9F\x92\x9B\x00\xF0\x9F\xA7\xA1\x00\xF0\x9F\x92\x9C\x00\xF0\x9F\x96\xA4\x00\xF0\x9F\x92\x9D\x00"
    "\xF0\x9F\x92\x9F\x00\xF0\x9F\x92\x8C\x00\xF0\x9F\x92\xA4\x00\xF0\x9F\x92\xA2\x00\xF0\x9F\x92\xA3\x00";

struct {
    char *text;
    char *language;
} const messages[] = { // Array containing all of the emojis messages
    {"\x46\x61\x6C\x73\x63\x68\x65\x73\x20\xC3\x9C\x62\x65\x6E\x20\x76\x6F\x6E\x20\x58\x79\x6C\x6F\x70\x68\x6F\x6E\x6D\x75\x73\x69\x6B\x20\x71\x75\xC3\xA4\x6C"
    "\x74\x20\x6A\x65\x64\x65\x6E\x20\x67\x72\xC3\xB6\xC3\x9F\x65\x72\x65\x6E\x20\x5A\x77\x65\x72\x67", "German"},
    {"\x42\x65\x69\xC3\x9F\x20\x6E\x69\x63\x68\x74\x20\x69\x6E\x20\x64\x69\x65\x20\x48\x61\x6E\x64\x2C\x20\x64\x69\x65\x20\x64\x69\x63\x68\x20\x66\xC3\xBC\x74"
    "\x74\x65\x72\x74\x2E", "German"},
    {"\x41\x75\xC3\x9F\x65\x72\x6F\x72\x64\x65\x6E\x74\x6C\x69\x63\x68\x65\x20\xC3\x9C\x62\x65\x6C\x20\x65\x72\x66\x6F\x72\x64\x65\x72\x6E\x20\x61\x75\xC3\x9F"
    "\x65\x72\x6F\x72\x64\x65\x6E\x74\x6C\x69\x63\x68\x65\x20\x4D\x69\x74\x74\x65\x6C\x2E", "German"},
    {"\xD4\xBF\xD6\x80\xD5\xB6\xD5\xA1\xD5\xB4\x20\xD5\xA1\xD5\xBA\xD5\xA1\xD5\xAF\xD5\xAB\x20\xD5\xB8\xD6\x82\xD5\xBF\xD5\xA5\xD5\xAC\x20\xD6\x87\x20\xD5\xAB"
    "\xD5\xB6\xD5\xAE\xD5\xAB\x20\xD5\xA1\xD5\xB6\xD5\xB0\xD5\xA1\xD5\xB6\xD5\xA3\xD5\xAB\xD5\xBD\xD5\xBF\x20\xD5\xB9\xD5\xA8\xD5\xB6\xD5\xA5\xD6\x80", "Armenian"},
    {"\xD4\xB5\xD6\x80\xD5\xA2\x20\xD5\xB8\xD6\x80\x20\xD5\xAF\xD5\xA1\xD6\x81\xD5\xAB\xD5\xB6\xD5\xA8\x20\xD5\xA5\xD5\xAF\xD5\xA1\xD6\x82\x20\xD5\xA1\xD5\xB6\xD5"
    "\xBF\xD5\xA1\xD5\xBC\x2C\x20\xD5\xAE\xD5\xA1\xD5\xBC\xD5\xA5\xD6\x80\xD5\xA8\x20\xD5\xA1\xD5\xBD\xD5\xA1\xD6\x81\xD5\xAB\xD5\xB6\x2E\x2E\x2E\x20\xC2\xAB\xD4\xBF"
    "\xD5\xB8\xD5\xBF\xD5\xA8\x20\xD5\xB4\xD5\xA5\xD6\x80\xD5\xB8\xD5\xB6\xD6\x81\xD5\xAB\xD6\x81\x20\xD5\xA7\x3A\xC2\xBB", "Armenian"},
    {"\xD4\xB3\xD5\xA1\xD5\xBC\xD5\xA8\xD5\x9D\x20\xD5\xA3\xD5\xA1\xD6\x80\xD5\xB6\xD5\xA1\xD5\xB6\x2C\x20\xD5\xB1\xD5\xAB\xD6\x82\xD5\xB6\xD5\xA8\xD5\x9D\x20\xD5"
    "\xB1\xD5\xB4\xD5\xBC\xD5\xA1\xD5\xB6", "Armenian"},
    {"\x4A\x65\xC5\xBC\x75\x20\x6B\x6C\xC4\x85\x74\x77\x2C\x20\x73\x70\xC5\x82\xC3\xB3\x64\xC5\xBA\x20\x46\x69\x6E\x6F\x6D\x20\x63\x7A\xC4\x99\xC5\x9B\xC4\x87"
    "\x20\x67\x72\x79\x20\x68\x61\xC5\x84\x62\x21", "Polish"},
    {"\x44\x6F\x62\x72\x79\x6D\x69\x20\x63\x68\xC4\x99\x63\x69\x61\x6D\x69\x20\x6A\x65\x73\x74\x20\x70\x69\x65\x6B\xC5\x82\x6F\x20\x77\x79\x62\x72\x75\x6B\x6F"
    "\x77\x61\x6E\x65\x2E", "Polish"},
    {"\xC3\x8E\xC8\x9B\x69\x20\x6D\x75\x6C\xC8\x9B\x75\x6D\x65\x73\x63\x20\x63\xC4\x83\x20\x61\x69\x20\x61\x6C\x65\x73\x20\x72\x61\x79\x6C\x69\x62\x2E\x0A\xC8\x98"
    "\x69\x20\x73\x70\x65\x72\x20\x73\xC4\x83\x20\x61\x69\x20\x6F\x20\x7A\x69\x20\x62\x75\x6E\xC4\x83\x21", "Romanian"},
    {"\xD0\xAD\xD1\x85\x2C\x20\xD1\x87\xD1\x83\xD0\xB6\xD0\xB0\xD0\xBA\x2C\x20\xD0\xBE\xD0\xB1\xD1\x89\xD0\xB8\xD0\xB9\x20\xD1\x81\xD1\x8A\xD1\x91\xD0\xBC\x20"
    "\xD1\x86\xD0\xB5\xD0\xBD\x20\xD1\x88\xD0\xBB\xD1\x8F\xD0\xBF\x20\x28\xD1\x8E\xD1\x84\xD1\x82\xD1\x8C\x29\x20\xD0\xB2\xD0\xB4\xD1\x80\xD1\x8B\xD0\xB7\xD0\xB3\x21", "Russian"},
    {"\xD0\xAF\x20\xD0\xBB\xD1\x8E\xD0\xB1\xD0\xBB\xD1\x8E\x20\x72\x61\x79\x6C\x69\x62\x21", "Russian"},
    {"\xD0\x9C\xD0\xBE\xD0\xBB\xD1\x87\xD0\xB8\x2C\x20\xD1\x81\xD0\xBA\xD1\x80\xD1\x8B\xD0\xB2\xD0\xB0\xD0\xB9\xD1\x81\xD1\x8F\x20\xD0\xB8\x20\xD1\x82\xD0\xB0\xD0\xB8"
    "\x0A\xD0\x98\x20\xD1\x87\xD1\x83\xD0\xB2\xD1\x81\xD1\x82\xD0\xB2\xD0\xB0\x20\xD0\xB8\x20\xD0\xBC\xD0\xB5\xD1\x87\xD1\x82\xD1\x8B\x20\xD1\x81\xD0\xB2\xD0\xBE\xD0\xB8\x20"
    "\xE2\x80\x93\x0A\xD0\x9F\xD1\x83\xD1\x81\xD0\xBA\xD0\xB0\xD0\xB9\x20\xD0\xB2\x20\xD0\xB4\xD1\x83\xD1\x88\xD0\xB5\xD0\xB2\xD0\xBD\xD0\xBE\xD0\xB9\x20\xD0\xB3\xD0\xBB\xD1"
    "\x83\xD0\xB1\xD0\xB8\xD0\xBD\xD0\xB5\x0A\xD0\x98\x20\xD0\xB2\xD1\x81\xD1\x85\xD0\xBE\xD0\xB4\xD1\x8F\xD1\x82\x20\xD0\xB8\x20\xD0\xB7\xD0\xB0\xD0\xB9\xD0\xB4\xD1\x83\xD1"
    "\x82\x20\xD0\xBE\xD0\xBD\xD0\xB5\x0A\xD0\x9A\xD0\xB0\xD0\xBA\x20\xD0\xB7\xD0\xB2\xD0\xB5\xD0\xB7\xD0\xB4\xD1\x8B\x20\xD1\x8F\xD1\x81\xD0\xBD\xD1\x8B\xD0\xB5\x20\xD0\xB2"
    "\x20\xD0\xBD\xD0\xBE\xD1\x87\xD0\xB8\x2D\x0A\xD0\x9B\xD1\x8E\xD0\xB1\xD1\x83\xD0\xB9\xD1\x81\xD1\x8F\x20\xD0\xB8\xD0\xBC\xD0\xB8\x20\xE2\x80\x93\x20\xD0\xB8\x20\xD0\xBC"
    "\xD0\xBE\xD0\xBB\xD1\x87\xD0\xB8\x2E", "Russian"},
    {"\x56\x6F\x69\x78\x20\x61\x6D\x62\x69\x67\x75\xC3\xAB\x20\x64\xE2\x80\x99\x75\x6E\x20\x63\xC5\x93\x75\x72\x20\x71\x75\x69\x20\x61\x75\x20\x7A\xC3\xA9\x70"
    "\x68\x79\x72\x20\x70\x72\xC3\xA9\x66\xC3\xA8\x72\x65\x20\x6C\x65\x73\x20\x6A\x61\x74\x74\x65\x73\x20\x64\x65\x20\x6B\x69\x77\x69", "French"},
    {"\x42\x65\x6E\x6A\x61\x6D\xC3\xAD\x6E\x20\x70\x69\x64\x69\xC3\xB3\x20\x75\x6E\x61\x20\x62\x65\x62\x69\x64\x61\x20\x64\x65\x20\x6B\x69\x77\x69\x20\x79\x20"
    "\x66\x72\x65\x73\x61\x3B\x20\x4E\x6F\xC3\xA9\x2C\x20\x73\x69\x6E\x20\x76\x65\x72\x67\xC3\xBC\x65\x6E\x7A\x61\x2C\x20\x6C\x61\x20\x6D\xC3\xA1\x73\x20\x65\x78"
    "\x71\x75\x69\x73\x69\x74\x61\x20\x63\x68\x61\x6D\x70\x61\xC3\xB1\x61\x20\x64\x65\x6C\x20\x6D\x65\x6E\xC3\xBA\x2E", "Spanish"},
    {"\xCE\xA4\xCE\xB1\xCF\x87\xCE\xAF\xCF\x83\xCF\x84\xCE\xB7\x20\xCE\xB1\xCE\xBB\xCF\x8E\xCF\x80\xCE\xB7\xCE\xBE\x20\xCE\xB2\xCE\xB1\xCF\x86\xCE\xAE\xCF\x82\x20"
    "\xCF\x88\xCE\xB7\xCE\xBC\xCE\xAD\xCE\xBD\xCE\xB7\x20\xCE\xB3\xCE\xB7\x2C\x20\xCE\xB4\xCF\x81\xCE\xB1\xCF\x83\xCE\xBA\xCE\xB5\xCE\xBB\xCE\xAF\xCE\xB6\xCE\xB5\xCE"
    "\xB9\x20\xCF\x85\xCF\x80\xCE\xAD\xCF\x81\x20\xCE\xBD\xCF\x89\xCE\xB8\xCF\x81\xCE\xBF\xCF\x8D\x20\xCE\xBA\xCF\x85\xCE\xBD\xCF\x8C\xCF\x82", "Greek"},
    {"\xCE\x97\x20\xCE\xBA\xCE\xB1\xCE\xBB\xCF\x8D\xCF\x84\xCE\xB5\xCF\x81\xCE\xB7\x20\xCE\xAC\xCE\xBC\xCF\x85\xCE\xBD\xCE\xB1\x20\xCE\xB5\xCE\xAF\xCE\xBD"
    "\xCE\xB1\xCE\xB9\x20\xCE\xB7\x20\xCE\xB5\xCF\x80\xCE\xAF\xCE\xB8\xCE\xB5\xCF\x83\xCE\xB7\x2E", "Greek"},
    {"\xCE\xA7\xCF\x81\xCF\x8C\xCE\xBD\xCE\xB9\xCE\xB1\x20\xCE\xBA\xCE\xB1\xCE\xB9\x20\xCE\xB6\xCE\xB1\xCE\xBC\xCE\xAC\xCE\xBD\xCE\xB9\xCE\xB1\x21", "Greek"},
    {"\xCE\xA0\xCF\x8E\xCF\x82\x20\xCF\x84\xCE\xB1\x20\xCF\x80\xCE\xB1\xCF\x82\x20\xCF\x83\xCE\xAE\xCE\xBC\xCE\xB5\xCF\x81\xCE\xB1\x3B", "Greek"},

    {"\xE6\x88\x91\xE8\x83\xBD\xE5\x90\x9E\xE4\xB8\x8B\xE7\x8E\xBB\xE7\x92\x83\xE8\x80\x8C\xE4\xB8\x8D\xE4\xBC\xA4\xE8\xBA\xAB\xE4\xBD\x93\xE3\x80\x82", "Chinese"},
    {"\xE4\xBD\xA0\xE5\x90\x83\xE4\xBA\x86\xE5\x90\x97\xEF\xBC\x9F", "Chinese"},
    {"\xE4\xB8\x8D\xE4\xBD\x9C\xE4\xB8\x8D\xE6\xAD\xBB\xE3\x80\x82", "Chinese"},
    {"\xE6\x9C\x80\xE8\xBF\x91\xE5\xA5\xBD\xE5\x90\x97\xEF\xBC\x9F", "Chinese"},
    {"\xE5\xA1\x9E\xE7\xBF\x81\xE5\xA4\xB1\xE9\xA9\xAC\xEF\xBC\x8C\xE7\x84\x89\xE7\x9F\xA5\xE9\x9D\x9E\xE7\xA6\x8F\xE3\x80\x82", "Chinese"},
    {"\xE5\x8D\x83\xE5\x86\x9B\xE6\x98\x93\xE5\xBE\x97\x2C\x20\xE4\xB8\x80\xE5\xB0\x86\xE9\x9A\xBE\xE6\xB1\x82", "Chinese"},
    {"\xE4\xB8\x87\xE4\xBA\x8B\xE5\xBC\x80\xE5\xA4\xB4\xE9\x9A\xBE\xE3\x80\x82", "Chinese"},
    {"\xE9\xA3\x8E\xE6\x97\xA0\xE5\xB8\xB8\xE9\xA1\xBA\xEF\xBC\x8C\xE5\x85\xB5\xE6\x97\xA0\xE5\xB8\xB8\xE8\x83\x9C\xE3\x80\x82", "Chinese"},
    {"\xE6\xB4\xBB\xE5\x88\xB0\xE8\x80\x81\xEF\xBC\x8C\xE5\xAD\xA6\xE5\x88\xB0\xE8\x80\x81\xE3\x80\x82", "Chinese"},
    {"\xE4\xB8\x80\xE8\xA8\x80\xE6\x97\xA2\xE5\x87\xBA\xEF\xBC\x8C\xE9\xA9\xB7\xE9\xA9\xAC\xE9\x9A\xBE\xE8\xBF\xBD\xE3\x80\x82", "Chinese"},
    {"\xE8\xB7\xAF\xE9\x81\xA5\xE7\x9F\xA5\xE9\xA9\xAC\xE5\x8A\x9B\xEF\xBC\x8C\xE6\x97\xA5\xE4\xB9\x85\xE8\xA7\x81\xE4\xBA\xBA\xE5\xBF\x83", "Chinese"},
    {"\xE6\x9C\x89\xE7\x90\x86\xE8\xB5\xB0\xE9\x81\x8D\xE5\xA4\xA9\xE4\xB8\x8B\xEF\xBC\x8C\xE6\x97\xA0\xE7\x90\x86\xE5\xAF\xB8\xE6\xAD\xA5\xE9\x9A\xBE\xE8\xA1\x8C\xE3\x80\x82", "Chinese"},

    {"\xE7\x8C\xBF\xE3\x82\x82\xE6\x9C\xA8\xE3\x81\x8B\xE3\x82\x89\xE8\x90\xBD\xE3\x81\xA1\xE3\x82\x8B", "Japanese"},
    {"\xE4\xBA\x80\xE3\x81\xAE\xE7\x94\xB2\xE3\x82\x88\xE3\x82\x8A\xE5\xB9\xB4\xE3\x81\xAE\xE5\x8A\x9F", "Japanese"},
    {"\xE3\x81\x86\xE3\x82\x89\xE3\x82\x84\xE3\x81\xBE\xE3\x81\x97\x20\x20\xE6\x80\x9D\xE3\x81\xB2\xE5\x88\x87\xE3\x82\x8B\xE6\x99\x82\x20\x20\xE7\x8C\xAB\xE3\x81\xAE\xE6\x81\x8B", "Japanese"},
    {"\xE8\x99\x8E\xE7\xA9\xB4\xE3\x81\xAB\xE5\x85\xA5\xE3\x82\x89\xE3\x81\x9A\xE3\x82\x93\xE3\x81\xB0\xE8\x99\x8E\xE5\xAD\x90\xE3\x82\x92\xE5\xBE\x97\xE3\x81\x9A\xE3\x80\x82", "Japanese"},
    {"\xE4\xBA\x8C\xE5\x85\x8E\xE3\x82\x92\xE8\xBF\xBD\xE3\x81\x86\xE8\x80\x85\xE3\x81\xAF\xE4\xB8\x80\xE5\x85\x8E\xE3\x82\x92\xE3\x82\x82\xE5\xBE\x97\xE3\x81\x9A\xE3\x80\x82", "Japanese"},
    {"\xE9\xA6\xAC\xE9\xB9\xBF\xE3\x81\xAF\xE6\xAD\xBB\xE3\x81\xAA\xE3\x81\xAA\xE3\x81\x8D\xE3\x82\x83\xE6\xB2\xBB\xE3\x82\x89\xE3\x81\xAA\xE3\x81\x84\xE3\x80\x82", "Japanese"},
    {"\xE6\x9E\xAF\xE9\x87\x8E\xE8\xB7\xAF\xE3\x81\xAB\xE3\x80\x80\xE5\xBD\xB1\xE3\x81\x8B\xE3\x81\x95\xE3\x81\xAA\xE3\x82\x8A\xE3\x81\xA6\xE3\x80\x80\xE3\x82\x8F\xE3\x81\x8B\xE3\x82\x8C\xE3\x81\x91\xE3\x82\x8A", "Japanese"},
    {"\xE7\xB9\xB0\xE3\x82\x8A\xE8\xBF\x94\xE3\x81\x97\xE9\xBA\xA6\xE3\x81\xAE\xE7\x95\x9D\xE7\xB8\xAB\xE3\x81\xB5\xE8\x83\xA1\xE8\x9D\xB6\xE5\x93\x89", "Japanese"},

    {"\xEC\x95\x84\xEB\x93\x9D\xED\x95\x9C\x20\xEB\xB0\x94\xEB\x8B\xA4\x20\xEC\x9C\x84\xEC\x97\x90\x20\xEA\xB0\x88\xEB\xA7\xA4\xEA\xB8\xB0\x20\xEB\x91\x90\xEC\x97\x87\x20"
    "\xEB\x82\xA0\xEC\x95\x84\x20\xEB\x8F\x88\xEB\x8B\xA4\x2E\x0A\xEB\x84\x88\xED\x9B\x8C\xEB\x84\x88\xED\x9B\x8C\x20\xEC\x8B\x9C\xEB\xA5\xBC\x20\xEC\x93\xB4\xEB\x8B\xA4\x2E"
    "\x20\xEB\xAA\xA8\xEB\xA5\xB4\xEB\x8A\x94\x20\xEB\x82\x98\xEB\x9D\xBC\x20\xEA\xB8\x80\xEC\x9E\x90\xEB\x8B\xA4\x2E\x0A\xEB\x84\x90\xEB\x94\xB0\xEB\x9E\x80\x20\xED\x95\x98"
    "\xEB\x8A\x98\x20\xEB\xB3\xB5\xED\x8C\x90\xEC\x97\x90\x20\xEB\x82\x98\xEB\x8F\x84\x20\xEA\xB0\x99\xEC\x9D\xB4\x20\xEC\x8B\x9C\xEB\xA5\xBC\x20\xEC\x93\xB4\xEB\x8B\xA4\x2E", "Korean"},
    {"\xEC\xA0\x9C\x20\xEB\x88\x88\xEC\x97\x90\x20\xEC\x95\x88\xEA\xB2\xBD\xEC\x9D\xB4\xEB\x8B\xA4", "Korean"},
    {"\xEA\xBF\xA9\x20\xEB\xA8\xB9\xEA\xB3\xA0\x20\xEC\x95\x8C\x20\xEB\xA8\xB9\xEB\x8A\x94\xEB\x8B\xA4", "Korean"},
    {"\xEB\xA1\x9C\xEB\xA7\x88\xEB\x8A\x94\x20\xED\x95\x98\xEB\xA3\xA8\xEC\x95\x84\xEC\xB9\xA8\xEC\x97\x90\x20\xEC\x9D\xB4\xEB\xA3\xA8\xEC\x96\xB4\xEC\xA7\x84\x20\xEA\xB2\x83\xEC\x9D\xB4"
    "\x20\xEC\x95\x84\xEB\x8B\x88\xEB\x8B\xA4", "Korean"},
    {"\xEA\xB3\xA0\xEC\x83\x9D\x20\xEB\x81\x9D\xEC\x97\x90\x20\xEB\x82\x99\xEC\x9D\xB4\x20\xEC\x98\xA8\xEB\x8B\xA4", "Korean"},
    {"\xEA\xB0\x9C\xEC\xB2\x9C\xEC\x97\x90\xEC\x84\x9C\x20\xEC\x9A\xA9\x20\xEB\x82\x9C\xEB\x8B\xA4", "Korean"},
    {"\xEC\x95\x88\xEB\x85\x95\xED\x95\x98\xEC\x84\xB8\xEC\x9A\x94\x3F", "Korean"},
    {"\xEB\xA7\x8C\xEB\x82\x98\xEC\x84\x9C\x20\xEB\xB0\x98\xEA\xB0\x91\xEC\x8A\xB5\xEB\x8B\x88\xEB\x8B\xA4", "Korean"},
    {"\xED\x95\x9C\xEA\xB5\xAD\xEB\xA7\x90\x20\xED\x95\x98\xEC\x8B\xA4\x20\xEC\xA4\x84\x20\xEC\x95\x84\xEC\x84\xB8\xEC\x9A\x94\x3F", "Korean"},
};

//--------------------------------------------------------------------------------------
// Module functions declaration
//--------------------------------------------------------------------------------------
static void RandomizeEmoji(void);    // Fills the emoji array with random emojis

static void DrawTextBoxed(Font font, const char *text, Rectangle rec, float fontSize, float spacing, bool wordWrap, Color tint);   // Draw text using font inside rectangle limits
static void DrawTextBoxedSelectable(Font font, const char *text, Rectangle rec, float fontSize, float spacing, bool wordWrap, Color tint, int selectStart, int selectLength, Color selectTint, Color selectBackTint);    // Draw text using font inside rectangle limits with support for text selection

//--------------------------------------------------------------------------------------
// Global variables
//--------------------------------------------------------------------------------------
// Arrays that holds the random emojis
struct {
    int index;      // Index inside `emojiCodepoints`
    int message;    // Message index
    Color color;    // Emoji color
} emoji[EMOJI_PER_WIDTH*EMOJI_PER_HEIGHT] = { 0 };

static int hovered = -1, selected = -1;

//------------------------------------------------------------------------------------
// Program main entry point
//------------------------------------------------------------------------------------
int main(void)
{
    // Initialization
    //--------------------------------------------------------------------------------------
    const int screenWidth = 800;
    const int screenHeight = 450;

    SetConfigFlags(FLAG_MSAA_4X_HINT | FLAG_VSYNC_HINT);
    InitWindow(screenWidth, screenHeight, "raylib [text] example - unicode");

    // Load the font resources
    // NOTE: fontAsian is for asian languages,
    // fontEmoji is the emojis and fontDefault is used for everything else
    Font fontDefault = LoadFont("resources/dejavu.fnt");
    Font fontAsian = LoadFont("resources/noto_cjk.fnt");
    Font fontEmoji = LoadFont("resources/symbola.fnt");

    Vector2 hoveredPos = { 0.0f, 0.0f };
    Vector2 selectedPos = { 0.0f, 0.0f };

    // Set a random set of emojis when starting up
    RandomizeEmoji();

    SetTargetFPS(60);               // Set our game to run at 60 frames-per-second
    //--------------------------------------------------------------------------------------

    // Main loop
    while (!WindowShouldClose())    // Detect window close button or ESC key
    {
        // Update
        //----------------------------------------------------------------------------------
        // Add a new set of emojis when SPACE is pressed
        if (IsKeyPressed(KEY_SPACE)) RandomizeEmoji();

        // Set the selected emoji
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && (hovered != -1) && (hovered != selected))
        {
            selected = hovered;
            selectedPos = hoveredPos;
        }

        Vector2 mouse = GetMousePosition();
        Vector2 position = { 28.8f, 10.0f };
        hovered = -1;
        //----------------------------------------------------------------------------------

        // Draw
        //----------------------------------------------------------------------------------
        BeginDrawing();

            ClearBackground(RAYWHITE);

            // Draw random emojis in the background
            //------------------------------------------------------------------------------
            for (int i = 0; i < SIZEOF(emoji); ++i)
            {
                const char *txt = &emojiCodepoints[emoji[i].index];
                Rectangle emojiRect = { position.x, position.y, (float)fontEmoji.baseSize, (float)fontEmoji.baseSize };

                if (!CheckCollisionPointRec(mouse, emojiRect))
                {
                    DrawTextEx(fontEmoji, txt, position, (float)fontEmoji.baseSize, 1.0f, selected == i ? emoji[i].color : Fade(LIGHTGRAY, 0.4f));
                }
                else
                {
                    DrawTextEx(fontEmoji, txt, position, (float)fontEmoji.baseSize, 1.0f, emoji[i].color );
                    hovered = i;
                    hoveredPos = position;
                }

                if ((i != 0) && (i%EMOJI_PER_WIDTH == 0)) { position.y += fontEmoji.baseSize + 24.25f; position.x = 28.8f; }
                else position.x += fontEmoji.baseSize + 28.8f;
            }
            //------------------------------------------------------------------------------

            // Draw the message when a emoji is selected
            //------------------------------------------------------------------------------
            if (selected != -1)
            {
                const int message = emoji[selected].message;
                const int horizontalPadding = 20, verticalPadding = 30;
                Font *font = &fontDefault;

                // Set correct font for asian languages
                if (TextIsEqual(messages[message].language, "Chinese") ||
                    TextIsEqual(messages[message].language, "Korean") ||
                    TextIsEqual(messages[message].language, "Japanese")) font = &fontAsian;

                // Calculate size for the message box (approximate the height and width)
                Vector2 sz = MeasureTextEx(*font, messages[message].text, (float)font->baseSize, 1.0f);
                if (sz.x > 300) { sz.y *= sz.x/300; sz.x = 300; }
                else if (sz.x < 160) sz.x = 160;

                Rectangle msgRect = { selectedPos.x - 38.8f, selectedPos.y, 2 * horizontalPadding + sz.x, 2 * verticalPadding + sz.y };
                msgRect.y -= msgRect.height;

                // Coordinates for the chat bubble triangle
                Vector2 a = { selectedPos.x, msgRect.y + msgRect.height }, b = {a.x + 8, a.y + 10}, c= { a.x + 10, a.y };

                // Don't go outside the screen
                if (msgRect.x < 10) msgRect.x += 28;
                if (msgRect.y < 10)
                {
                    msgRect.y = selectedPos.y + 84;
                    a.y = msgRect.y;
                    c.y = a.y;
                    b.y = a.y - 10;

                    // Swap values so we can actually render the triangle :(
                    Vector2 tmp = a;
                    a = b;
                    b = tmp;
                }

                if (msgRect.x + msgRect.width > screenWidth) msgRect.x -= (msgRect.x + msgRect.width) - screenWidth + 10;

                // Draw chat bubble
                DrawRectangleRec(msgRect, emoji[selected].color);
                DrawTriangle(a, b, c, emoji[selected].color);

                // Draw the main text message
                Rectangle textRect = { msgRect.x + horizontalPadding/2, msgRect.y + verticalPadding/2, msgRect.width - horizontalPadding, msgRect.height };
                DrawTextBoxed(*font, messages[message].text, textRect, (float)font->baseSize, 1.0f, true, WHITE);

                // Draw the info text below the main message
                int size = (int)strlen(messages[message].text);
                int length = GetCodepointCount(messages[message].text);
                const char *info = TextFormat("%s %u characters %i bytes", messages[message].language, length, size);
                sz = MeasureTextEx(GetFontDefault(), info, 10, 1.0f);
                
                DrawText(info, (int)(textRect.x + textRect.width - sz.x), (int)(msgRect.y + msgRect.height - sz.y - 2), 10, RAYWHITE);
            }
            //------------------------------------------------------------------------------

            // Draw the info text
            DrawText("These emojis have something to tell you, click each to find out!", (screenWidth - 650)/2, screenHeight - 40, 20, GRAY);
            DrawText("Each emoji is a unicode character from a font, not a texture... Press [SPACEBAR] to refresh", (screenWidth - 484)/2, screenHeight - 16, 10, GRAY);

        EndDrawing();
        //----------------------------------------------------------------------------------
    }

    // De-Initialization
    //--------------------------------------------------------------------------------------
    UnloadFont(fontDefault);    // Unload font resource
    UnloadFont(fontAsian);      // Unload font resource
    UnloadFont(fontEmoji);      // Unload font resource

    CloseWindow();              // Close window and OpenGL context
    //--------------------------------------------------------------------------------------

    return 0;
}

// Fills the emoji array with random emoji (only those emojis present in fontEmoji)
static void RandomizeEmoji(void)
{
    hovered = selected = -1;
    int start = GetRandomValue(45, 360);

    for (int i = 0; i < SIZEOF(emoji); ++i)
    {
        // 0-179 emoji codepoints (from emoji char array) each 4bytes + null char
        emoji[i].index = GetRandomValue(0, 179)*5;

        // Generate a random color for this emoji
        emoji[i].color = Fade(ColorFromHSV((float)((start*(i + 1))%360), 0.6f, 0.85f), 0.8f);

        // Set a random message for this emoji
        emoji[i].message = GetRandomValue(0, SIZEOF(messages) - 1);
    }
}

//--------------------------------------------------------------------------------------
// Module functions definition
//--------------------------------------------------------------------------------------

// Draw text using font inside rectangle limits
static void DrawTextBoxed(Font font, const char *text, Rectangle rec, float fontSize, float spacing, bool wordWrap, Color tint)
{
    DrawTextBoxedSelectable(font, text, rec, fontSize, spacing, wordWrap, tint, 0, 0, WHITE, WHITE);
}

// Draw text using font inside rectangle limits with support for text selection
static void DrawTextBoxedSelectable(Font font, const char *text, Rectangle rec, float fontSize, float spacing, bool wordWrap, Color tint, int selectStart, int selectLength, Color selectTint, Color selectBackTint)
{
    int length = TextLength(text);  // Total length in bytes of the text, scanned by codepoints in loop

    float textOffsetY = 0.0f;       // Offset between lines (on line break '\n')
    float textOffsetX = 0.0f;       // Offset X to next character to draw

    float scaleFactor = fontSize/(float)font.baseSize;     // Character rectangle scaling factor

    // Word/character wrapping mechanism variables
    enum { MEASURE_STATE = 0, DRAW_STATE = 1 };
    int state = wordWrap? MEASURE_STATE : DRAW_STATE;

    int startLine = -1;         // Index where to begin drawing (where a line begins)
    int endLine = -1;           // Index where to stop drawing (where a line ends)
    int lastk = -1;             // Holds last value of the character position

    for (int i = 0, k = 0; i < length; i++, k++)
    {
        // Get next codepoint from byte string and glyph index in font
        int codepointByteCount = 0;
        int codepoint = GetCodepoint(&text[i], &codepointByteCount);
        int index = GetGlyphIndex(font, codepoint);

        // NOTE: Normally we exit the decoding sequence as soon as a bad byte is found (and return 0x3f)
        // but we need to draw all of the bad bytes using the '?' symbol moving one byte
        if (codepoint == 0x3f) codepointByteCount = 1;
        i += (codepointByteCount - 1);

        float glyphWidth = 0;
        if (codepoint != '\n')
        {
            glyphWidth = (font.glyphs[index].advanceX == 0) ? font.recs[index].width*scaleFactor : font.glyphs[index].advanceX*scaleFactor;

            if (i + 1 < length) glyphWidth = glyphWidth + spacing;
        }

        // NOTE: When wordWrap is ON we first measure how much of the text we can draw before going outside of the rec container
        // We store this info in startLine and endLine, then we change states, draw the text between those two variables
        // and change states again and again recursively until the end of the text (or until we get outside of the container).
        // When wordWrap is OFF we don't need the measure state so we go to the drawing state immediately
        // and begin drawing on the next line before we can get outside the container.
        if (state == MEASURE_STATE)
        {
            // TODO: There are multiple types of spaces in UNICODE, maybe it's a good idea to add support for more
            // Ref: http://jkorpela.fi/chars/spaces.html
            if ((codepoint == ' ') || (codepoint == '\t') || (codepoint == '\n')) endLine = i;

            if ((textOffsetX + glyphWidth) > rec.width)
            {
                endLine = (endLine < 1)? i : endLine;
                if (i == endLine) endLine -= codepointByteCount;
                if ((startLine + codepointByteCount) == endLine) endLine = (i - codepointByteCount);

                state = !state;
            }
            else if ((i + 1) == length)
            {
                endLine = i;
                state = !state;
            }
            else if (codepoint == '\n') state = !state;

            if (state == DRAW_STATE)
            {
                textOffsetX = 0;
                i = startLine;
                glyphWidth = 0;

                // Save character position when we switch states
                int tmp = lastk;
                lastk = k - 1;
                k = tmp;
            }
        }
        else
        {
            if (codepoint == '\n')
            {
                if (!wordWrap)
                {
                    textOffsetY += (font.baseSize + font.baseSize/2)*scaleFactor;
                    textOffsetX = 0;
                }
            }
            else
            {
                if (!wordWrap && ((textOffsetX + glyphWidth) > rec.width))
                {
                    textOffsetY += (font.baseSize + font.baseSize/2)*scaleFactor;
                    textOffsetX = 0;
                }

                // When text overflows rectangle height limit, just stop drawing
                if ((textOffsetY + font.baseSize*scaleFactor) > rec.height) break;

                // Draw selection background
                bool isGlyphSelected = false;
                if ((selectStart >= 0) && (k >= selectStart) && (k < (selectStart + selectLength)))
                {
                    DrawRectangleRec((Rectangle){ rec.x + textOffsetX - 1, rec.y + textOffsetY, glyphWidth, (float)font.baseSize*scaleFactor }, selectBackTint);
                    isGlyphSelected = true;
                }

                // Draw current character glyph
                if ((codepoint != ' ') && (codepoint != '\t'))
                {
                    DrawTextCodepoint(font, codepoint, (Vector2){ rec.x + textOffsetX, rec.y + textOffsetY }, fontSize, isGlyphSelected? selectTint : tint);
                }
            }

            if (wordWrap && (i == endLine))
            {
                textOffsetY += (font.baseSize + font.baseSize/2)*scaleFactor;
                textOffsetX = 0;
                startLine = endLine;
                endLine = -1;
                glyphWidth = 0;
                selectStart += lastk - k;
                k = lastk;

                state = !state;
            }
        }

        textOffsetX += glyphWidth;
    }
}
