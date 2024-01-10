#include "request.h"

static size_t	WriteHTML(void *contents, size_t size, size_t nmemb, void *userp)
{
	size_t realsize = size * nmemb;
    struct CURLResp *resp = (struct CURLResp *)userp;
    char *ptr = realloc(resp->html, resp->size + realsize + 1);

    if (!ptr)
    {
        fprintf(stderr, "Err: Not enough memory available (realloc returned NULL)\n");
     	return 0;
     }
     resp->html = ptr;
     memcpy(&(resp->html[resp->size]), contents, realsize);
     resp->size += realsize;
     resp->html[resp->size] = 0;

     return realsize;
}

struct CURLResp GetRequest(const char *url)
{
    CURL *curl_request = curl_easy_init();
    if (!curl_request) {
        fprintf(stderr, "Err: Curl initialization failed\n");
        exit(EXIT_FAILURE);
    }
    struct CURLResp resp;
    resp.html = malloc(1);
    resp.size = 0;

    curl_easy_setopt(curl_request, CURLOPT_URL, url);
    curl_easy_setopt(curl_request, CURLOPT_WRITEFUNCTION, WriteHTML);
    curl_easy_setopt(curl_request, CURLOPT_WRITEDATA, (void *)&resp);
    curl_easy_setopt(curl_request, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36");

    CURLcode res = curl_easy_perform(curl_request);

    if (res != CURLE_OK) {
        fprintf(stderr, "Err: GET request failed: %s\n", curl_easy_strerror(res));
    }

    curl_easy_cleanup(curl_request);
    return resp;
}

int request(struct CURLResp *resp, const char *url)
{
	curl_global_init(CURL_GLOBAL_ALL);
    CURL *curl_request = curl_easy_init();
    if (!curl_request){
        fprintf(stderr, "Err: Curl initialization failed\n");
        return 0;
    }
    *resp = GetRequest(url);
    curl_easy_cleanup(curl_request);
    curl_global_cleanup();
    return 1;
}