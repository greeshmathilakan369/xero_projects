import configparser
import email
import json
import os
import time


message = []
error_msg = ""
initial_start_time = ''


def propertyConnection():
    """Import ini config file"""
    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    settings.read(dir + os.sep + 'Config.ini')
    settings.sections()
    return settings


settings = propertyConnection()
authorize_url = settings.get('urls', 'authorize_url')
token_url = settings.get('urls', 'token_url')
callback_uri = settings.get('urls', 'callback_uri')
test_api_url = settings.get('urls', 'test_api_url')
client_id = settings.get('client', 'client_id')
client_secret = settings.get('client', 'client_secret')
ROOT_DIR = os.path.abspath(os.curdir)


def main():
    # Main method which fetch data from all the api end points and saves as csv files in
    # share point folder

    global message, error_msg

    initial_start_time = datetime.now()
    current_time = initial_start_time.strftime("%H:%M:%S")
    print("Execution started : ", current_time)
    try:
        company_data_df, tokens = get_company()
        if len(message) > 0:
            mail_report(initial_start_time)
            exit()
        start_time = round(datetime.now().timestamp())
        expire = int(tokens['expires_in'])
        access_token = tokens['access_token']
        access_refresh_token = tokens['refresh_token']
        company_data_df = company_data_df[
            company_data_df['Name'] == 'Garrima Pty Ltd t/a Imperial Kitchens']
        company_uri = company_data_df['Uri'].iloc[0]

        company_files_df = get_company_files(access_token, company_uri, access_refresh_token,
                                             expire, start_time)
        company_files_df.index = np.arange(0, len(company_files_df))

        path = settings.get('sharepoint_path', 'path')
        file_path = path + '/CompanyFile.csv'

        if not company_files_df.empty:
            if not os.path.isfile(file_path):
                company_files_df.to_csv(file_path, header='columns')
            else:
                company_files_df.to_csv(file_path, header='columns')

        for url in api_end_points:
            try:
                print(url)
                if (url == '/GeneralLedger/JournalTransaction'):
                    company_df, start_time, access_token, access_refresh_token = get_company_api2(
                        company_uri, url,
                        access_token, access_refresh_token,
                        expire, start_time)
                else:
                    company_df, start_time, access_token, access_refresh_token = get_company_api(
                        access_token, company_uri,
                        url, access_refresh_token,
                        expire, start_time)
                if not company_df.empty:
                    if url == '/Contact/Supplier':
                        df_expected = company_df['Addresses'].apply(pd.Series)
                        address_0 = df_expected[0].apply(pd.Series)
                        company_df = pd.concat([company_df, address_0], axis=1).drop('Addresses',
                                                                                     axis=1)
                        company_df = pd.DataFrame(company_df)

                    if url == '/Contact/Customer':
                        df_expected = company_df['Addresses'].apply(pd.Series)
                        address_0 = df_expected[0].apply(pd.Series)
                        company_df = pd.concat([company_df, address_0], axis=1).drop('Addresses',
                                                                                     axis=1)
                        company_df = pd.DataFrame(company_df)

                    if url == '/Sale/CustomerPayment':
                        df_expected = company_df['Invoices'].apply(pd.Series)
                        address_0 = df_expected[0].apply(pd.Series)
                        company_df = pd.concat([company_df, address_0], axis=1).drop('Invoices',
                                                                                     axis=1)
                        company_df = pd.DataFrame(company_df)

                    if url == '/Contact/Employee':
                        df_expected = company_df['Addresses'].apply(pd.Series)
                        address_0 = df_expected[0].apply(pd.Series)
                        company_df = pd.concat([company_df, address_0], axis=1).drop('Addresses',
                                                                                     axis=1)
                        company_df = pd.DataFrame(company_df)

                    name = url.replace('/', '')
                    name = name + '.csv'
                    company_df.index = np.arange(0, len(company_df))

                    # Saves files to the local machine as csv
                    path = settings.get('sharepoint_path', 'path')
                    file_path = path + '/' + name
                    if not os.path.isfile(file_path):
                        company_df.to_csv(file_path, header='columns')
                    else:
                        company_df.replace(to_replace=[r"\\n|\\r", "\n|\r"], value=["", ""],
                                           regex=True,
                                           inplace=True)
                        company_df.to_csv(file_path, header='columns')
            except:
                continue
    except Exception as inst:
        message.append("Invalid Access Code")
        error_msg = error_msg + str(inst) + str(traceback.format_exc())
        print("Error in connection : ", inst)
        print(traceback.format_exc())

    # Writing status of execution to log.csv
    if len(message) > 0:
        status_dict = {'ExecutionDate': str(datetime.now().date()),
                       'ExecutionStartTime': str(current_time),
                       'ExecutionEndTime': str(datetime.now().strftime("%H:%M:%S")),
                       'Status': 'Error occurred, Execution not completed',
                       'Remarks': str(error_msg)}
        mail_report(initial_start_time)
    else:
        status_dict = {'ExecutionDate': str(datetime.now().date()),
                       'ExecutionStartTime': str(current_time),
                       'ExecutionEndTime': str(datetime.now().strftime("%H:%M:%S")),
                       'Status': 'Execution completed successfully',
                       'Remarks': ''}

    df = pd.DataFrame(columns=['ExecutionDate', 'ExecutionStartTime', 'ExecutionEndTime', 'Status', 'Remarks'])
    df = df.append(status_dict, ignore_index=True)
    df.index = np.arange(0, len(df))

    file_path = str(os.path.dirname(os.path.abspath(__file__))) + '/' + 'log.csv'
    if os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', header=False)
    else:
        df.to_csv(file_path, header='columns')

    print("Execution Ended:", str(datetime.now().strftime("%H:%M:%S")))
    print(f"Total time taken: {datetime.now() - initial_start_time}")
    return


def get_company():
    global message, error_msg
    try:
        authorization_code = get_access_code()
        access_token_response = get_access_token(authorization_code)
        tokens = json.loads(access_token_response.text)
        access_token = tokens['access_token']
        api_call_headers = {'Authorization': 'Bearer ' + access_token,
                            'x-myobapi-cftoken': 'base64_username:base64_password',
                            'x-myobapi-key': client_id,
                            'x-myobapi-version': 'v2'}
        api_call_response = requests.get(test_api_url, headers=api_call_headers)
        company_data = api_call_response.text
        company_data = json.loads(company_data)
        company_data_df = pd.DataFrame(company_data)
        return company_data_df, tokens
    except Exception as e:
        print("Error :", e)
        print(traceback.format_exc())
        if len(message) <= 0:
            message.append("Access Code is not correct")
            error_msg = error_msg + str(e) + "\n" + str(traceback.format_exc())
        return