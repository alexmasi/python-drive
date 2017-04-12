from drive import Drive
import datetime
import os


def main():
    """Uploads files in a directory to Google Drive.

    """
    source_drive_path = input("Input path to source directory: ")
    my_drive = Drive()
    folder = my_drive.query("name = 'Drone Club Videos'")
    folder_id = folder['files'][0]['id']
    new_folder_id = my_drive.create_folder(str(datetime.date.today()),
                                           folder_id)
    for f in os.scandir(source_drive_path):
        my_drive.upload_file(f.name, f.path, new_folder_id)


if __name__ == '__main__':
    main()
