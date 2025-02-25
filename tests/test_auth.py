from app.auth.auth import hash_password, verify_password

def test_hash_password():
    senha = "minha_senha_secreta"
    senha_hash = hash_password(senha)
    assert senha != senha_hash
    assert verify_password(senha, senha_hash) == True

def test_invalid_password():
    senha_hash = hash_password("senha_correta")
    assert verify_password("senha_errada", senha_hash) == False
    assert verify_password("senha_correta", senha_hash) == True