from fastapp.routers.auth import fake_hash_password

def test_fake_hash_password():
    print(fake_hash_password("password"))

if __name__ == '__main__':
    test_fake_hash_password()