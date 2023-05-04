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

    activesystems = client.system.listActiveSystems(key)

    data = []
    for i in range(len(activesystems)):
        count = len(client.system.listLatestUpgradablePackages(key, activesystems[i]['id']))
        data.append((activesystems[i]['name'], count))

    client.auth.logout(key)

    st.title('Latest Upgradable Packages')
    st.table(data)

    # Create a column chart with x-axis as active system names and y-axis as count of upgradable packages
    st.subheader('Column Chart')
    chart_data = dict(data)
    st.bar_chart(chart_data)

    # Create a line chart with x-axis as active system names and y-axis as count of upgradable packages
    st.subheader('Line Chart')
    st.line_chart(chart_data)


if __name__ == '__main__':
    main()