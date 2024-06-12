import os


def get_documents_folder():
    home = os.path.expanduser("~")
    documents_folder = os.path.join(home, 'Documents')
    return documents_folder


def read_search_text_from_file(directory, filename):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()  # Remove any surrounding whitespace
    except Exception as e:
        print(f"Could not read the search text file: {file_path}. Error: {e}")
        return None


def search_text_in_files(directory, search_text):
    num = 0
    if search_text is None:
        return
    # Loop through all files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Open and read each file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Check if the search text is in the file content
                    if search_text in content:
                        print(f"Text found in: {file_path}")
                        num+=1
            except Exception as e:
                print(f"Could not read file: {file_path}. Error: {e}")
    return num

subfolder = "24-6-11b"
# Example usage
documents_folder = os.path.expanduser("~/Documents/extracted_files")

extracted_files_folder = os.path.join(documents_folder, subfolder)
search_text_file = 'search_text.txt'  # Replace with the name of the file containing the search text

search_text = read_search_text_from_file(documents_folder, search_text_file)
num_found = search_text_in_files(extracted_files_folder, search_text)
print(f"That text was found {num_found} times in {search_text_file}")


{
    "file_prefix": "slitAperture1_loop",
    "init": [
        "_L12 = 20.0",
        "_L2S = 5.0",
        "_LS3 = 5.0",
        "_L34 = 5.0",
        "_spotSize = 0.5",
        "_qsa2_ratio = 0.5",
        "_S3Offset = 0.0",
        "_thetaOffset = 0.0",
        "_pre = 1.0",
        "_mon0 = 1.0",
        "_mon1 = 1.0",
        "_exp = 1.0",
        "live = {}",
        "live.wavelength = {}",
        "live.wavelength.wavelength = 1.0"
    ],
    "loops": [
        {
            "vary": [
                [
                    "_q",
                    {
                        "range": {
                            "start": 0.008,
                            "step": 0.0005,
                            "stop": 0.025
                        }
                    }
                ],
                [
                    "_mon1",
                    1250
                ],
                [
                    "sampleAngle",
                    "Math.asin(_q*live.wavelength.wavelength/(4.0 * Math.PI)) * 180.0 / Math.PI + _thetaOffset"
                ],
                [
                    "detectorAngle",
                    "2.0 * Math.asin(_q*live.wavelength.wavelength/(4.0 * Math.PI)) * 180.0 / Math.PI"
                ],
                [
                    "slitAperture1",
                    "_q*(((_L12*_spotSize*live.wavelength.wavelength)/(_L2S*4.0*Math.PI)) - _qsa2_ratio*((_L12+_L2S)/_L2S))"
                ],
                [
                    "slitAperture2",
                    "_q*_qsa2_ratio"
                ],
                [
                    "slitAperture3",
                    "((_L12+_L2S+_LS3)/_L12) * (slitAperture1+slitAperture2) - slitAperture1+ _S3Offset"
                ],
                [
                    "slitAperture4",
                    "((_L12+_L2S+_LS3+_L34)/_L12) * (slitAperture1+slitAperture2) - slitAperture1+ _S3Offset"
                ],
                [
                    "counter.timePreset",
                    "_pre * ( _mon0 + _mon1* Math.pow(_q, _exp))"
                ]
            ]
        },
        {
            "vary": [
                [
                    "_q",
                    {
                        "range": {
                            "start": 0.025,
                            "step": 0.0024,
                            "stop": 0.2506
                        }
                    }
                ],
                [
                    "_mon1",
                    3000
                ],
                [
                    "sampleAngle",
                    "Math.asin(_q*live.wavelength.wavelength/(4.0 * Math.PI)) * 180.0 / Math.PI + _thetaOffset"
                ],
                [
                    "detectorAngle",
                    "2.0 * Math.asin(_q*live.wavelength.wavelength/(4.0 * Math.PI)) * 180.0 / Math.PI"
                ]
            ]
        }
    ]
}

