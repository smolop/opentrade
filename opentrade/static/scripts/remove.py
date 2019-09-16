""" This script is recommended to use with shell_plus"""

class Remove(object):

    def __init__(self):
        username = input('username: ')
        self.user = self.get_user(username)
        print(self.user)

    def get_user(self, username):
        return User.objects.get(username=username)

    def get_profile(self):
        return Profile.objects.get(user=self.user)

    def delete_all(self):
        profile = self.get_profile()
        ScheduledSharesOperations.objects.filter(user=self.user).delete()
        Favorite.objects.filter(user=self.user).delete()
        Share.objects.filter(portfolio=profile.portfolio).delete()
        profile.wallet.delete()
        profile.portfolio.delete()
        profile.delete()
        self.user.delete()
