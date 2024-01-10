#include "request.h"

void freeImg(struct Images* imgUrls)
{
    for (size_t i = 0; i < imgUrls->count; ++i) {
        free(imgUrls->urls[i]);
        free(imgUrls->ext[i]);
    }
    free(imgUrls->urls);
    free(imgUrls->ext);
}

int isWhitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

void scrapeImages(const char* htmlContent, struct Images* imgUrls) {
    const char  *extensions[] = { ".jpg", ".jpeg", ".png", ".gif", ".bmp" };
    const char  *htmlPtr = htmlContent;

    while (*htmlPtr != '\0') {
        for (size_t i = 0; i < 5; ++i) {
            size_t extLength = strlen(extensions[i]);
            if (strncmp(htmlPtr, extensions[i], extLength) == 0) {
                const char  *startPos = htmlPtr;
                while (startPos > htmlContent && !isWhitespace(*startPos) && *startPos != '"' && *startPos != '\'' && *startPos != ';' && *startPos != '(' && *startPos != ')' && *startPos != '=' && *startPos != ',' && *startPos != '[' && *startPos != ']' && *startPos != '{' && *startPos != '}') {
                    --startPos;
                }
                ++startPos;

                if (strncmp(startPos, "http://", 7) == 0 || strncmp(startPos, "https://", 8) == 0) {
                    const char  *endPos = htmlPtr + extLength;
                    while (!isWhitespace(*endPos) && *endPos != '"' && *endPos != '\'' && *endPos != ';' && *endPos != '(' && *endPos != ')' && *endPos != ',' && *endPos != '[' && *endPos != ']' && *endPos != '{' && *endPos != '}' && *endPos != '\0') {
                        ++endPos;
                    }
                    size_t urlLength = endPos - startPos;
                    char* imgUrl = malloc(urlLength + 1);
                    strncpy(imgUrl, startPos, urlLength);
                    imgUrl[urlLength] = '\0';
                    imgUrls->urls = realloc(imgUrls->urls, (imgUrls->count + 1) * sizeof(char*));
                    imgUrls->urls[imgUrls->count] = imgUrl;
                    imgUrls->ext = realloc(imgUrls->ext, (imgUrls->count + 1) * sizeof(char*));
                    imgUrls->ext[imgUrls->count] = strdup(extensions[i]);
                    ++imgUrls->count;
                    htmlPtr += extLength;
                }
            }
        }
        ++htmlPtr;
    }
}

int downloadImage(const char* url, const char* ext, const char* path)
{
    CURL        *curl;
    FILE        *fp;
    static int  imgNb = 0;
    char        temp[20];
    char        filename[256];

    curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "Curl initialization failed\n");
        return 0;
    }

    strcpy(filename, path);
    strcat(filename, "image_");
    sprintf(temp,"%d", imgNb);
    strcat(filename, temp);
    strcat(filename, ext);
    imgNb++;

    fp = fopen(filename, "wb");
    if (!fp) {
        fprintf(stderr, "Failed to open file for writing\n");
        curl_easy_cleanup(curl);
        return 0;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, NULL);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);

    CURLcode res = curl_easy_perform(curl);
    fclose(fp);
    curl_easy_cleanup(curl);

        printf("image = %s and %s\n", filename, url);
    if (res != CURLE_OK) {
        fprintf(stderr, "Failed to download image: %s\n", curl_easy_strerror(res));
        remove(filename);
        return 0;
    }

    printf("Downloaded: %s\n", filename);
    return 1;
}