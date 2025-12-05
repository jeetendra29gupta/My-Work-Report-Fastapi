from config import client


def user_signup(payload: dict):
    response = client.post("/auth/signup", json=payload)
    try:
        response.raise_for_status()
        return response.json()

    except Exception:
        return response.text


def main():
    signup_jeetendra_29_gupta = user_signup({
        "full_name": "Jeetendra Gupta",
        "email_id": "jeetendra29gupta@example.com",
        "phone_no": "+91 000000000 10",
        "password": "jeetendra29gupta",
    })
    print(signup_jeetendra_29_gupta)

    signup_sameer_14_gupta = user_signup({
        "full_name": "Sameer Gupta",
        "email_id": "sameer14gupta@example.com",
        "phone_no": "+91 111111111 10",
        "password": "sameer14gupta",
    })
    print(signup_sameer_14_gupta)

    signup_prince_18_gupta = user_signup({
        "full_name": "Prince Gupta",
        "email_id": "prince18gupta@example.com",
        "phone_no": "+91 222222222 10",
        "password": "prince18gupta",
    })
    print(signup_prince_18_gupta)

    signup_black_02_rose = user_signup({
        "full_name": "Black Rose",
        "email_id": "black02rose@example.com",
        "phone_no": "+91 333333333 10",
        "password": "black02rose",
    })
    print(signup_black_02_rose)

    signup_blue_11_bird = user_signup({
        "full_name": "Blue Bird",
        "email_id": "blue11bird@example.com",
        "phone_no": "+91 444444444 10",
        "password": "blue11bird",
    })
    print(signup_blue_11_bird)

    signup_juju_08_raven = user_signup({
        "full_name": "Juju Raven",
        "email_id": "juju08raven@example.com",
        "phone_no": "+91 555555555 10",
        "password": "juju08raven",
    })
    print(signup_juju_08_raven)


if __name__ == '__main__':
    main()
