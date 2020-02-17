from __future__ import annotations
from subprocess import Popen, PIPE

def download_page(
                url: str,
                log_file_name: str = None,
                own_wget_options: str = None
                ) -> None:
    return download_pages([url], log_file_name, own_wget_options)

def download_pages(
                urls: list[str],
                log_file_name: str = None,
                own_wget_options: str = None
                ) -> None:
    if log_file_name:
        f_desc = open(log_file_name, 'w')
    try:
        for url in urls:
            if own_wget_options: request = 'wget ' + own_wget_options + ' ' + url
            else: request = 'wget -p -k -r -N -l inf --no-remove-listing ' + url

            if f_desc:
                f_desc.write('DOWNLOADING ' + url + '\n')
                f_desc.write('Request: ' + request)

            process = Popen(request, shell=True, stdout=PIPE)
            process.wait()

            if f_desc:
                try:
                    out = process.communicate()[0].decode('utf-8').strip()
                    f_desc.write(out)
                    f_desc.write('\n')
                    f_desc.write('-'*50)
                    f_desc.write('\n')
                except Exception as e:
                    f_desc.write(e)
                    f_desc.write('\n')
                    f_desc.write('='*50)
                    f_desc.write('\n')
                f_desc.write('\tDONE\n')
    finally:
        if f_desc: f_desc.close()
