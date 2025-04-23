


@staticmethod
def create(username: str, account: str, password: str, phone_number: str, social_preference: str, role):
        return User(
            username=username,
            account=account,
            password=password,
            phone_number=phone_number,
            social_preference=social_preference,
            role=role
        )