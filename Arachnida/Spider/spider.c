#include "request.h"

void init_data (t_data *data)
{
    data->opt_r = 0;
    data->opt_l = 0;
    data->opt_p = NULL;
    data->url = NULL;
}

void freedata(t_data *data)
{
    if (data->opt_p != NULL)
        free(data->opt_p);
    if (data->url != NULL)
        free(data->url);
}

int parse_l (t_data *data, int i, char **av)
{
    if (av[i + 1] != NULL && av[i + 1][0] == '-')
    {
        data->opt_l = D_VALUE;
        return i;
    }
    else if (av[i + 1] != NULL && isdigit(av[i + 1][0]))
    {
        char *endptr;
        long int result = strtol(av[i + 1], &endptr, 10);
        if (*endptr == '\0' && result > 0)
        {
            data->opt_l = (int)result;
            return i + 1;
        }
    }
    return (-1);
}

int parse_p (t_data *data, int i, char **av)
{
    if (av[(i + 1)] == NULL)
        return -1;
    else if (av[(i + 1)][0] == '.')
    {
        i++;
        int j = 0;
        if (av[i][j] == '.' && av[i][j + 1] == '/')
        {
            data->opt_p = strdup(av[i]);
            if (data->opt_p == NULL)
                return -1;
            return i;
        }
    }
    else
    {
        data->opt_p = strdup(D_PATH);
        if (data->opt_p == NULL)
            return -1;
        return i;
    }
    return i;
}

int parse_url (t_data *data, char *av)
{
    if (data->opt_p == NULL)
    {
        data->opt_p = strdup(D_PATH);
        if (data->opt_p == NULL)
            return 0;
    }
    data->url = strdup(av);
    if (data->url == NULL)
        return 0;
    return 1;
}

int    parseArgs(int ac, char **av, t_data *data)
{
    int i = 1;
    while (i < ac && ac > 2)
    {
        if (strcmp(av[i], "-r") == 0)
        {
            if (data->opt_r == 1)
                return 1;
            data->opt_r = 1;
        }
        else if (strcmp(av[i], "-l") == 0)
        {
            if (data->opt_r == 0 || data->opt_l != 0)
                return 1 ;
            i = parse_l(data, i, av);
            if (i == -1)
                return 1;
        }
        else if (strcmp(av[i], "-p") == 0)
        {
            if (data->opt_p != NULL)
                return 1;
            i = parse_p(data, i , av);
            if (i == -1)
                return 1;
        }
        else
            break;
        i++;
    }
    if (!parse_url(data, av[i]))
       return 1;
    return 0;
}

int main(int ac, char **av)
{
    t_data  data;
	if (ac < 2)
	{
        fprintf(stderr, "Err: you need to provide at least the URL of a webpage\n");
		return 0;
	}
    init_data(&data);
    if (parseArgs(ac, av, &data))
    {
        fprintf(stderr, "Err: invalid arguments\n");
        freedata(&data);
        return 0;
    }
    struct CURLResp resp;
    if (!request(&resp, data.url))
        return 0;
    struct Images imgUrls = { NULL, 0, NULL};
    scrapeImages(resp.html, &imgUrls, 0, data.opt_l);
    for (size_t i = 0; i < imgUrls.count; ++i) {
        printf("Image URL %lu: %s, Extension: %s\n", i + 1, imgUrls.urls[i], imgUrls.ext[i]);
    }
    const char* path = "data/";
    for (size_t i = 0; i < imgUrls.count; ++i) {
        if (downloadImage(imgUrls.urls[i], imgUrls.ext[i], path)) {
        }
    }
    freedata(&data);
    freeImg(&imgUrls);
	free(resp.html);
    return 0;	
}
