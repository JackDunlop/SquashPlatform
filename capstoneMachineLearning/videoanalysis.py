
''' *************************************************************************** IMPORTS **********************************************************************************************
    ********************************************************************************************************************************************************************************** '''


import sys
import os
import cv2


''' *************************************************************************** CUSTOM ERRORS ***************************************************************************************
    ********************************************************************************************************************************************************************************** '''

class ApplicationError(Exception):
    """Parent class for custom errors."""
    pass

class PathDoesNotExistError(ApplicationError):
    """Exception raised when the specified file does not exist."""
    def __init__(self, file, message="Files path does not exist, DO NOT PASS IN RELATIVE PATH, MUST PASS IN FULL PATH."):
        self.file = file
        self.message = message
        super().__init__(f"{message}: {file}")

class OutputFolderDoesNotExistError(ApplicationError):
    """Exception raised when the output folder does not exist."""
    def __init__(self, file, message="Output folder does not exist, you need a folder to store the output videos names outputVideos."):
        self.file = file
        self.message = message
        super().__init__(f"{message}: {file}")

class UniqueIdentifierIsntUnique(ApplicationError):
    """Exception raised when the passed unique identifier already existis."""
    def __init__(self, uniqueIdentifier, message="Unique identifier already existis. "):
        self.file = uniqueIdentifier
        self.message = message
        super().__init__(f"{message}: {uniqueIdentifier}")

class InvalidRequiredArgumentsError(ApplicationError):
    """Exception raised when two arguments have not been passed in."""
    def __init__(self, arguments, message="Must have two passed in arguments."):
        self.arguments = arguments[1:]  # skip the script name
        self.message = message
        super().__init__(f"{message}: Arguments Passed in {self.arguments}")



''' *************************************************************************** HANDLING ARUGMENTS  **********************************************************************************
    ********************************************************************************************************************************************************************************** '''

class Arguments:
    def __init__(self, videoPath, uniqueIdentifier):
        self.videoPath = videoPath
        self.uniqueIdentifier = uniqueIdentifier

    def print_arguments(self):
        print(f"Video Path: {self.videoPath}")
        print(f"Unique Identifier: {self.uniqueIdentifier}")

    def checkArgumentLength(argv):
        if len(argv) == 3:
            args = Arguments(argv[1], argv[2])
           # args.print_arguments()
            return args
        else:
            raise InvalidRequiredArgumentsError(argv)
    
    def checkPathExists(self):
        if not os.path.isfile(self.videoPath):
            raise PathDoesNotExistError(self.videoPath)
    
    def checkOutputFolderExists(self):
        currentScriptDirectory = os.path.dirname(os.path.abspath(__file__))
        outputFolderPath = os.path.join(currentScriptDirectory, "outputVideos")
        if not os.path.exists(outputFolderPath):
            raise OutputFolderDoesNotExistError(outputFolderPath)
        return outputFolderPath

    def checkFileIdentifierIsUnique(self, outputFolderPath):
        fileNames = [f for f in os.listdir(outputFolderPath) if os.path.isfile(os.path.join(outputFolderPath, f))]
        parsedFilenames = [filename.split('_')[0] for filename in fileNames]
        if self.uniqueIdentifier in parsedFilenames:
            raise UniqueIdentifierIsntUnique(self.uniqueIdentifier)
    
''' *************************************************************************** VIDEO FILE  ******************************************************************************************
    ********************************************************************************************************************************************************************************** '''

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames

def save_video(ouput_video_frames,output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (ouput_video_frames[0].shape[1], ouput_video_frames[0].shape[0]))
    for frame in ouput_video_frames:
        out.write(frame)
    out.release()




def main():


    # Handling Arguments
    args = Arguments.checkArgumentLength(sys.argv)
    args.checkPathExists()
    outputFolderPath = args.checkOutputFolderExists()
    args.checkFileIdentifierIsUnique(outputFolderPath)
    
    # Handling Video
    videoFrames = read_video(args.videoPath)
    print(f"Number of frames read: {len(videoFrames)}")

if __name__ == "__main__":
    main()
