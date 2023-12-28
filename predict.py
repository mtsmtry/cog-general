# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import requests
import tarfile

def download_and_extract_tar(url, target_path):
    """
    Download a tar file from the given URL and extract it to the target path.

    :param url: URL of the tar file to download.
    :param target_path: Path where the tar file will be extracted.
    """
    # Download the tar file
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")

    # Save the tar file
    tar_file_path = url.split('/')[-1]
    with open(tar_file_path, 'wb') as file:
        file.write(response.content)

    # Extract the tar file
    with tarfile.open(tar_file_path, "r:*") as tar:
        tar.extractall(path=target_path)

    print(f"Tar file downloaded and extracted to {target_path}")

class Predictor(BasePredictor):
    def setup(self) -> None:
        self.predictor = None

    def predict(
        self,
        src_url: str = Input(),
        input: str = Input()
    ) -> Path:
        if not self.predictor:
            download_and_extract_tar(src_url, '.')
            from src.main import Predictor
            self.predictor = Predictor()
        self.predictor.predict(input)
