from random import choice, randint
import csv

def return_data(path):
    with open(path, 'r') as infile:
        lines = infile.readlines()
        data = [line.replace('\n', '').strip() for line in lines]

    return data


def generate_emails(n_emails):

    names = return_data(path='files/names.txt')
    last_names = return_data(path='files/last_names.txt')
    servers = return_data(path='files/servers.txt')

    emails = []
    for _ in range(n_emails):
        email = f'{choice(names)}{choice(last_names)}@{choice(servers)}'
        emails.append(email)

    return emails

def format_rg(rg):

    rg_length = len(rg)
    
    if rg_length == 6:
        rg = f'{rg[:2]}.{rg[2:5]}-{rg[-1]}'
    elif rg_length == 9 or rg_length == 8 :
        rg = f'{rg[:2]}.{rg[2:5]}.{rg[5:7]}-{rg[-1]}'
    else:
        rg = f'{rg[:2]}.{rg[2:]}'

    return rg


def generate_rgs(n_rgs):
    # xx.xxx.xxx-x

    rgs = []
    for _ in range(n_rgs):
        rg = str(randint(100000, 100000000))
        rg = format_rg(rg)
        rgs.append(rg)

    return rgs

def generate_data(n_data):
    emails = generate_emails(n_data)
    rgs = generate_rgs(n_data)

    data = []
    for email, rg in zip(emails, rgs):
        data.append([email, rg])
        
    return data


def save_data(filename, all_data):

    with open(f'../data/{filename}' + '.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        for data in all_data:
            writer.writerow(data)


if __name__=='__main__':
        
    data = generate_data(600)
    save_data('emails_rgs', data)