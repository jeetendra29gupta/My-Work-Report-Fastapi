from config import client


def user_login(payload: dict):
    response = client.post("/auth/login", json=payload)
    response.raise_for_status()
    return response.json()


def main():
    login_jeetendra_29_gupta = user_login({
        "email_id": "jeetendra29gupta@example.com",
        "password": "jeetendra29gupta",
    })
    print("Login Jeetendra 29 Gupta", login_jeetendra_29_gupta)

    login_sameer_14_gupta = user_login({
        "email_id": "sameer14gupta@example.com",
        "password": "sameer14gupta",
    })
    print("Login Sameer 14 Gupta", login_sameer_14_gupta)

    login_prince_18_gupta = user_login({
        "email_id": "prince18gupta@example.com",
        "password": "prince18gupta",
    })
    print("Login Prince 18 Gupta", login_prince_18_gupta)


if __name__ == '__main__':
    main()

"""
Login Jeetendra 29 Gupta {
    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY1NzI2NjA5fQ.LfBbE1-_qS_Sixe2cHTDLwEG5ct8KcX_UYKyO5PhGts', 
    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxODUxMjI2NjA5fQ.ro9rqJLKuUIei0J_fUm21bOvGcEVt4Hp9LGLNOnGb40', 
    'token_type': 'bearer'
}

Login Sameer 14 Gupta {
    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzY1NzI2NjEwfQ.N1y_Fj2Wh-wqwpEpakAlV8cQLPku4LMYli4Za8iBeRI', 
    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxODUxMjI2NjEwfQ.Y43yunj6_4pBzUUYoINTQnna50aiStfkrUtu_IkIZqU', 
    'token_type': 'bearer'
}

Login Prince 18 Gupta {
    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzY1NzI2NjEwfQ.6yNlN5CRWzC1uNoTOwdqHW_ZclFlpR50HLyg-2Mj9Ps', 
    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxODUxMjI2NjEwfQ.RSElkP35BHkFS1sFRTnDwWESg0FA5zRNsCW55YtaL7o', 
    'token_type': 'bearer'
}
"""