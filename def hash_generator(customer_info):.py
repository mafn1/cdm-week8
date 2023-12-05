def hash_generator(customer_info):
    import pandas as pd
    import hashlib as hl
    import os

    customer_info = pd.read_csv('/Users/Michael/Documents/HDA and ML/Modules/Clinical Data Management/Coursework 2/CDM_Coursework2/Data/customer_information.csv')

    customer_info['national_insurance_nospace'] = customer_info['national_insurance_number'].str.replace(' ', '')

    def halved_ni(first_name, surname, national_insurance_number):
        halved_ni = ""
        for index, char in enumerate(national_insurance_number):
            if index % 2 == 1:
                halved_ni += char
        return first_name + surname + halved_ni
    customer_info['new_hashdata'] = customer_info.apply(lambda row: halved_ni(row['given_name'], row['surname'], row['national_insurance_nospace']), axis=1)

    def encode_data(data):
        encoded_data = data.encode('utf-8')
        return encoded_data
    customer_info['encoded_data'] = customer_info.apply(lambda row: encode_data(row['new_hashdata']), axis = 1)

    def generate_salt():
        salt = os.urandom(96)
        return salt
    customer_info['salt'] = customer_info.apply(lambda row: generate_salt(), axis=1)

    def combine_data_with_salt(data, salt):
        hash_data_with_salt = data + salt
        return hash_data_with_salt
    customer_info['data_and_salt_ready'] = customer_info.apply(lambda row: combine_data_with_salt(row['encoded_data'], row['salt']), axis = 1)

    hash_object = hl.sha256()
    def hash_my_data(x):
        hash_object.update(x)
        return hash_object.hexdigest()
    customer_info['hash_result'] = customer_info.apply(lambda row: hash_my_data(row['data_and_salt_ready']), axis = 1)

    return customer_info