from models.models import CustomUser


def Usersstatictokens():
    users = CustomUser.objects.all()
    data = []
    for user in users:
        if user.static_token != None:
            data.append(user.static_token)
    return data

