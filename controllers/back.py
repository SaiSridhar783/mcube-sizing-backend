def get_max_user_id(self) -> int:
        return max(user["user_id"] for user in self.users)

def create_user(self, user_data: dict) -> dict:
    new_user_id = self.get_max_user_id() + 1
    user_data['user_id'] = new_user_id
    self.users.append(user_data)
    return user_data
