import os
import subprocess

def Archive_model(dirModel, archiveName, mode):
    """This function archives the model.

    Args:
        dirModel (str): the full folder path of the model.
        archiveName (str): The full path of the target archive file.
        mode (str): "all" = all files; noDat = no *.dat files
    """

    if not os.path.isfile(archiveName):
        try:
            os.chdir(dirModel)
            if mode == "all":
                args = 'a ',archiveName,' * -r'
            elif mode == "noDat":
                args = 'a ',archiveName,' -xr!*.dat'

            exe7z = r"C:\Program Files\7-Zip\7z.exe"
            subprocess.call([exe7z, args], shell=True)
            isSuccessful = True
            message = "Archiving successful!"
        except Exception as e:
            isSuccessful = False
            message = e
    else:
        isSuccessful = False
        message = "Archived file already exists!"
    return (isSuccessful,message)    

if __name__=='__main__':

    dirModel = r"C:\isis\data\examples\ISIS 2D\Coastal"
    archiveName = r"C:\temp\Model_v2.zip"
    mode = "noDat"
    output = Archive_model(dirModel, archiveName, mode)
    print(output)

