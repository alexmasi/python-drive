import httplib2
import apiclient
import mimetypes
import datetime
import os
from quickstart import get_credentials

class Drive:
    def __init__(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build("drive", "v3", http=http)

    def query(self, q):
        """Execute a query on drive files.

        Args:
            q: Query type and keyword (ex. "name contains 'drone'").
        Returns:
            List of File resources.
        """
        return self.service.files().list(q=q).execute()

    def create_folder(self, folder_name, parent_id=None):
        """Create a new folder.

        Args:
            folder_name: Name for new folder.
            parent_id: Parent folder ID if not in root.
        Returns:
            New folder ID.
        """
        folder_metadata = {
            'name' : folder_name,
            'mimeType' : 'application/vnd.google-apps.folder',
            'parents' : [parent_id]
        }
        folder = self.service.files().create(body=folder_metadata,
                                             fields='id').execute()
        return folder.get('id')

    def upload_file(self, file_name, file_path, parent_id=None):
        """Upload a file.

        Args:
            file_name: Name of file.
            file_path: Path to file.
            parent_id: Parent folder ID if not in root.
        """
        file_metadata = {
            'name' : file_name,
            'mimeType' : mimetypes.guess_type(file_path),
            'parents' : [parent_id]
        }
        media = apiclient.http.MediaFileUpload \
                (file_path, mimetype=file_metadata['mimeType'],
                 chunksize=4*10**7, resumable=True)
        request = self.service.files().create \
                  (body=file_metadata, media_body=media, fields='id')
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploading", file_name,
                      ": %d%%..." % int(status.progress() * 100))
        print("Upload of", file_name, "is complete!")
