import os

class FileHandler:

    def __init__(self):
        pass

    def read_file(self, filePath):
        lines = []
        if(os.path.isfile(filePath)):
            try:
                with open(filePath) as file:
                    lines=""
                    for line in file:
                        lines+=line
                    #lines = [line for line in file]
            except IOError as e:
                print("No se pudo abrir el archivo.")
                exit(0)
        else:
            print('{} :Archivo no encontrado en la ruta especificada.'.format(filePath))
            exit(0)
        return lines

