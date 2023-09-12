import logging

import pandas as pd
import pysftp

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    ftp_url = 'sftp.regrid.com'
    uname = 'grist'
    pword = 'sweeping-clamour-beheld-mesmeric'

    geojson_path = '/download/geoJSON'
    with pysftp.Connection(ftp_url, username=uname, password=pword) as sftp:
        with sftp.cd(geojson_path):
            df = pd.DataFrame({'zip_remote_path': list(sftp.listdir())})
            df.to_csv('zip_remote_paths.csv', index=False)


if __name__ == '__main__':
    main()
