from urllib import quote


def url_encode(base_url, params):
    url_args = "&".join(["{}={}".format(k, quote(v)) for k, v in params.items()])

    auth_url = "{}/?{}".format(base_url, url_args)
    return auth_url


def parse_form_data(form_data):
    stripped = [x.strip() for x in form_data.split(',')]
    return stripped
