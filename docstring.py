import streamlit as st
from xmlrpc.client import ServerProxy
import ssl
import datetime

#Set up connection parameters for the SUMA server
MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"


def main():
    """
    Main function to run the application.
    """
    # Create an SSL context to allow communication with the SUMA server
    context = ssl._create_unverified_context()

    # Create a connection to the SUMA server with the provided login credentials
    client = ServerProxy(MANAGER_URL, context=context)
    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

    # Get a list of all active systems from the SUMA server
    activesystems = client.system.listActiveSystems(key)

    # Display a table of the latest upgradable packages for each active system
    data = []
    for i in range(len(activesystems)):
        count = len(client.system.listLatestUpgradablePackages(key, activesystems[i]['id']))
        data.append((activesystems[i]['name'], count))
    st.title('Latest Upgradable Packages')
    st.table(data)

    # Create a form to upgrade a package to a target system
    st.subheader('Upgrade a Package')
    package_list = []
    for system in activesystems:
        system_name = system['id']
        upgradeable_packages = client.system.listLatestUpgradablePackages(key, system['id'])
        package_names = [package['name'] for package in upgradeable_packages]
        if package_names:
            package_list.append((system_name, package_names))
    if package_list:
        selected_system = st.selectbox('Select the target system:', [system[0] for system in package_list])
        selected_package = st.selectbox('Select the package name:',
                                        package_list[[system[0] for system in package_list].index(selected_system)][1])
        if st.button('Upgrade'):
            # Upgrade the specified package to the target system
            client.system.schedulePackageUpdate(key, selected_system, datetime.datetime.now().isoformat())
            st.success(f'Package {selected_package} has been successfully upgraded to {selected_system}!')
    else:
        st.warning('There are no upgradable packages available in any of the active systems.')

    # Log out from the SUMA server
    client.auth.logout(key)


if __name__ == '__main__':

    main()

# import streamlit as st
# from xmlrpc.client import ServerProxy
# import ssl
#
# MANAGER_URL = "https://10.0.0.20/rpc/api"
# MANAGER_LOGIN = "sumaadmin"
# MANAGER_PASSWORD = "exadmin"
#
#
# def main():
#     context = ssl._create_unverified_context()
#     client = ServerProxy(MANAGER_URL, context=context)
#     key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)
#
#     # Get a list of all active systems
#     activesystems = client.system.listActiveSystems(key)
#
#     # Display a table of the latest upgradable packages for each active system
#     data = []
#     for i in range(len(activesystems)):
#         count = len(client.system.listLatestUpgradablePackages(key, activesystems[i]['id']))
#         data.append((activesystems[i]['name'], count))
#     st.title('Latest Upgradable Packages')
#     st.table(data)
#
#     # Create a form to upgrade a package to a target system
#     st.subheader('Upgrade a Package')
#     package_list = []
#     for system in activesystems:
#         system_name = system['name']
#         upgradeable_packages = client.system.listLatestUpgradablePackages(key, system['id'])
#         package_names = [package['name'] for package in upgradeable_packages]
#         if package_names:
#             package_list.append((system_name, package_names))
#     if package_list:
#         selected_system = st.selectbox('Select the target system:', [system[0] for system in package_list])
#         selected_package = st.selectbox('Select the package name:',
#                                         package_list[[system[0] for system in package_list].index(selected_system)][1])
#         if st.button('Upgrade'):
#             # Upgrade the specified package to the target system
#             client.packages.upgrade(key, selected_system, selected_package)
#             st.success(f'Package {selected_package} has been successfully upgraded to {selected_system}!')
#     else:
#         st.warning('There are no upgradable packages available in any of the active systems.')
#
#     client.auth.logout(key)
#
#
# if __name__ == '__main__':
#     main()