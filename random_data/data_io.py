

class Data:

    def __init__(self, in_path: str, out_path: str):

        self.in_path = in_path
        self.out_path = out_path
        self.all_data = []

    @staticmethod
    def treat_data(data):

        unwanted_chars = 'áãâêéíóõôú'
        wanted_chars = 'aaaeiooou'
        for i, char in enumerate(unwanted_chars):
            data = data.replace(char, wanted_chars[i]).lower()
            data = data.replace('\n', ' ')

        return data

    def read_data(self):

        with open(self.in_path, 'r') as infile:
            lines = infile.readlines()
            for line in lines:
                # print(line)
                line = self.treat_data(line)

                self.all_data.append(line) 
        print(self.all_data)
        return set(self.all_data)

    def save_data(self):
        with open(self.out_path, 'w') as outfile:
            for data in self.all_data:
                outfile.write(data)
                outfile.write('\n')


if __name__ == '__main__':

    path = 'data/last_names.txt'
    data = Data(path, path)
    data.read_data()
    data.save_data()

# print(all_data)
