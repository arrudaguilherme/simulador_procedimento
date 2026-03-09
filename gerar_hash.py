import streamlit_authenticator as stauth

# Senhas em texto puro
senhas = ["admin02182604", "admin02182604"]

# Gerar hashes
hashed = stauth.Hasher(senhas).generate()
print(hashed)