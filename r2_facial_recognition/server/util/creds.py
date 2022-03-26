# for user auth
from google_auth_oauthlib.flow import Flow, InstalledAppFlow

# for service auth
from google.oauth2 import service_account
import google.auth

# the permissions that should be granted to the app
SCOPE = 'https://www.googleapis.com/auth/spreadsheets'

# A flow object has functionality to help gain user credentials


def get_user_credentials(user_secret_file):
    """
    Obtain credentials using a user account
    """
    # useful:
    # https://developers.google.com/api-client-library/python/guide/aaa_oauth

    """
    There are two methods used to obtain the user
    credentials. The InstalledAppFlow method is preferred.

    Make sure only one of the methods is used. Comment
    out the one that isn't being used.
    """

    # the following code uses a generalized flow, which allows manual handling
    # of the authorization code
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #create a new flow object from a client secrets file, which stores 
    parameters for oauth2
    flow = Flow.from_client_secrets_file(
            user_secret_file,
            scopes=[SCOPE],
            redirect_uri="urn:ietf:wg:oauth:2.0:oob")

    #now, user must navigate to a url to provide consent
    auth_url, state = flow.authorization_url()
    print("Go here: {}".format(auth_url))

    #user will get an authorization code, which is used to get access token
    code = input("Enter code: ")

    #final step, get the access token
    flow.fetch_token(code=code)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    # the following code uses an InstalledAppFlow, making authorization
    # easier on an installed app

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    flow = InstalledAppFlow.from_client_secrets_file(
            user_secret_file,
            scopes=[SCOPE])

    """
    This will create a temporary local server that
    attempts to redirect the browser to the auth url.
    It listens for the authorization code in the response.
    Once it gets it, it will shut down. It will also
    acquire the access token.
    """
    flow.run_local_server()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # get the credentials
    credentials = flow.credentials
    
    return credentials


def get_service_credentials(service_secret_file):
    """
    Obtain credentials using a service account
    """
    
    try:
        # get application default credentials if they exist
        scoped_credentials, project = google.auth.default(
            scopes=[SCOPE])
    except google.auth.exceptions.DefaultCredentialsError:
        print("default credentials not found, obtaining from json file")

        # create a new Credentials from file
        credentials = service_account.Credentials.from_service_account_file(
            service_secret_file)

        # get a new copy of Credentials, but with proper scope
        scoped_credentials = credentials.with_scopes([SCOPE])

    return scoped_credentials

