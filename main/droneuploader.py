from drive import Drive
import datetime
import os
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("upload_dir", action="store", type=str,
                    help="specify folder to upload")

arguments = parser.parse_args()


def main():
    """Uploads files in a directory to Google Drive.

    """
    upload_dir_path = os.path.abspath(arguments.upload_dir) + "/"
    my_drive = Drive()
    folder = my_drive.query("name = 'Drone Club Videos'")
    folder_id = folder['files'][0]['id']
    new_folder_id = my_drive.create_folder(str(datetime.date.today()),
                                           folder_id)
    for f in os.scandir(upload_dir_path):
        my_drive.upload_file(f.name, f.path, new_folder_id)


if __name__ == '__main__':
    main()
