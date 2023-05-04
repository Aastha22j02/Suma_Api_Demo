import streamlit as st

from xmlrpc.client import ServerProxy

import ssl

MANAGER_URL = "https://10.0.0.20/rpc/api"

MANAGER_LOGIN = "sumaadmin"

MANAGER_PASSWORD = "exadmin"


def main():
    context = ssl._create_unverified_context()

    client = ServerProxy(MANAGER_URL, context=context)

    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

    # Get list of active systems

    activesystems = client.system.listActiveSystems(key)

    # Display table of upgradeable packages for each system

    st.title('Upgradeable Packages')

    for system in activesystems:
        system_name = system['name']

        upgradeable_packages = client.system.listLatestUpgradablePackages(key, system['id'])

        package_names = [package['name'] for package in upgradeable_packages]

        st.write(f"{system_name}:")

        st.table(package_names)

    client.auth.logout(key)


if __name__ == '__main__':
    main()
