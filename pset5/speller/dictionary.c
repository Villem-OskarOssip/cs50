// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "dictionary.h"

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    printf("%s", word);
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    FILE *di = fopen(dictionary, "rb"); //r for text files, rb for non-text file
    if (di == NULL) {
        return false;

    }

    // https://stackoverflow.com/questions/238603/how-can-i-get-a-files-size-in-c
    fseek(di, 0L, SEEK_END); //seek end of the file
    long fsize = ftell(di);
    fseek(di, 0L, SEEK_SET); //seek back

    char *buf[LENGTH + 1];
    //char *buf = malloc(fsize + 1); //allocates the requested memory and returns a pointer to it.
    
    if (buf == NULL) {
        fclose(di);
        return false;
    }
    
    fread(buf, fsize, 1, di); //read the file
    fclose(di); //close the file

    //buffer[fsize] = '\0';


    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    return false;
}
