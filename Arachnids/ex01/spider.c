#include "request.h"

void init_data (t_data *data)
{
    data->opt_r = 0;
    data->opt_l = 0;
    data->opt_p = NULL;
}

void feedata(t_data *data)
{
    if (!(data->opt_p == NULL))
        free(data->opt_p);
}

int parse_l (t_data *data, int i, char **av)
{
    if (av[i + 1] != NULL && av[i + 1][0] == '-')
    {
        data->opt_l = D_VALUE;
        return (i);
    }
    else if (av[i + 1] != NULL && isdigit(av[i + 1][0]))
    {
        int j = 0;
        i++;
        while (av[i] != NULL && j < (strlen(av[i])))
        {
            if (!(isdigit(av[i][j])))
                return (-1);
            j++;
        }
        data->opt_l = atoi(av[i]);
        return (i);
    }
    else
        return (-1);
    return (i);
}

int parse_p (t_data *data, int i, char **av, int ac)
{
    if (av[(i + 1)] == NULL)
        return (-1);
    else if (av[(i + 1)][0] == '.')
    {
        i++;
        int j = 0;
        if (av[i][j] == '.' && av[i][j + 1] == '/')
        {
            data->opt_p = (char*)malloc(strlen(av[i]) + 1);
            strcpy(data->opt_p, av[i]);
            if (data->opt_p == NULL)
                return (-1);
            return (i);
        }
    }
    else
    {
        data->opt_p = (char *)malloc(strlen(D_PATH) + 1);
        strcpy(data->opt_p, D_PATH);
        if (data->opt_p == NULL)
            return (-1);
        return (i);
    }
    return (i);
}

int    parsArgs(int ac, char **av, t_data *data)
{
    int i = 1;
    init_data(&data);

    while (i < ac)
    {
        if (strcmp(av[i], "-r") == 0)
            data->opt_r = 1;
        else if (strcmp(av[i], "-l") == 0)
        {
            if (data->opt_r == 0)
                return -1 ;
            i = parse_l(&data, i, av);
            if (i == -1)
                return 1;
        }
        else if (strcmp(av[i], "-p") == 0)
        {
            i = parse_p(&data, i , av, ac);
            if (i == -1)
            {
                freedata(&data);
                return 1;
            }
        }
        else
            break;
        i++;
    }
    printf("\n r= %d\n", data->opt_r);
    printf("\n l= %d\n", data->opt_l);
    printf("\n p= %s\n", data->opt_p);
}

int main(int ac, char **av)
{
    t_data  data;
	if (ac < 2)
	{
		write(1, "Err: you need to provide at least the URL of the webpage\n", 56);
		return 0;
	}
    if (parseArgs(ac, av, &data) == -1)
    {
		write(1, "Err: invalid arguments\n", 23);
        freedata(&data);
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
    freedata(&data);
    freeImg(&imgUrls);
	free(resp.html);
    return 0;	
}
