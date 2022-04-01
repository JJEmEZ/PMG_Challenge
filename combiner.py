import sys
import os
import pandas as pd


class CSVCombiner:

    @staticmethod
    def validate_file_paths(argv):
        """
        This function ensures that the arguments entered by the users and the file-paths with them are valid.
        :param argv: a set of stdin arguments
        :return: if all arguments entered are valid
        """

        if len(argv) <= 1:
            print("Error: No file-paths input. Please run the code as follows: \n" +
                  "python ./csv_combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv")
            return False

        filelst = argv[1:]

        for file_path in filelst:
            if not os.path.exists(file_path):
                print("Error: File or directory not found: " + file_path)
                return False
            if os.stat(file_path).st_size == 0:
                print("Warning: The following file is empty: " + file_path)
                return False
        return True

    def combine_files(self, argv: list):
        """
        This function combines all rows in the given file list by printing them to stdout
        :param argv: list, must contain valid csv file paths
        """
        chunksize = 10 ** 5
        chunk_list = []

        if self.validate_file_paths(argv):
            filelst = argv[1:]

            for file_path in filelst:

                # read as chunks to prevent memory issues
                for chunk in pd.read_csv(file_path, chunksize=chunksize):

                    # get the file name from the path
                    filename = os.path.basename(file_path)

                    # add the 'filename' column to the chunk
                    chunk['filename'] = filename
                    chunk_list.append(chunk)

            # flag to indicate if a header should be added
            header = True

            # combine all chunks
            for chunk in chunk_list:
                print(chunk.to_csv(index=False, header=header, line_terminator='\n', chunksize=chunksize), end='')
                header = False
        else:
            return


def main():
    combiner = CSVCombiner()
    combiner.combine_files(sys.argv)

if __name__ == '__main__':
    main()
