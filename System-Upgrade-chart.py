from xmlrpc.client import ServerProxy
import ssl
import streamlit as st
import pandas as pd
import altair as alt

MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"

# You might need to set to other options depending on your
# server SSL configuartion and your local SSL configuration
context = ssl._create_unverified_context()
client = ServerProxy(MANAGER_URL, context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

activesystems = client.system.listActiveSystems(key)

system_names = []
package_counts = []

for i in range(len(activesystems)):
    system_names.append(activesystems[i]['name'])
    package_counts.append(len(client.system.listLatestUpgradablePackages(key, activesystems[i]['id'])))
data = pd.DataFrame({
    'System Name': system_names,
    'Package Counts': package_counts
})

st.write(f"Number of active systems: {len(activesystems)}")

st.write('Packages Count by System')
chart = alt.Chart(data).mark_bar().encode(
    x='System Name',
    y='Package Counts'
)
st.altair_chart(chart, use_container_width=True)

client.auth.logout(key)