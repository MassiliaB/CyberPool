#include "request.h"

int main(int ac, char **av)
{
	if (ac < 2)
	{
		write(1, "Err: you need to provide at least the URL of the webpage\n", 56);
		return 0;
	}
    struct CURLResp resp;
    if (!request(&resp, av[1]))
        return 0;
//	printf("%s\n", resp.html);
    struct Images imgUrls = { NULL, 0, NULL};
    scrapeImages(resp.html, &imgUrls);
    for (size_t i = 0; i < imgUrls.count; ++i) {
        printf("Image URL %lu: %s, Extension: %s\n", i + 1, imgUrls.urls[i], imgUrls.ext[i]);
    }
    const char* path = "data/";
    for (size_t i = 0; i < imgUrls.count; ++i) {
        if (downloadImage(imgUrls.urls[i], imgUrls.ext[i], path)) {
        }
    }
    freeImg(&imgUrls);
	free(resp.html);
    return 0;	
}
