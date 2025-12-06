from models.user import User

class UserMapper:

    @staticmethod
    def from_event(event: dict) -> User:
        return User(
            user_id=event["user_id"],
            gender=event["gender"],
            first_name=event["first_name"],
            last_name=event["last_name"],
            email=event["email"],
            password=event["password"],
            dob=event["dob"],
            phone=event["phone"],
            cell=event["cell"],
            picture_large=event["picture_large"],
            picture_medium=event["picture_medium"],
            picture_thumbnail=event["picture_thumbnail"],
            city=event["city"],
            state=event["state"],
            state_id=event["state_id"],
            postcode=event["postcode"],
            latitude=float(event["latitude"]),
            longitude=float(event["longitude"]),
            created_at=event["created_at"],
        )
